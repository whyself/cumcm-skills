"""Search, DOI enrichment, and environment diagnosis with no third-party packages."""

import argparse
import copy
import json
import re
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from xml.etree.ElementTree import ParseError

from providers import SOURCES, doi, resolve, search
from runtime import DEFAULT_CONFIG, FIELDS, Http, SourceError, load_config


def normalized(value):
    return " ".join("".join(c if c.isalnum() else " " for c in unicodedata.normalize("NFKC", value).casefold()).split())


def same_paper(a, b):
    if a.get("doi") and b.get("doi"):
        return a["doi"] == b["doi"]
    for key in ("openalex", "arxiv", "pmid", "semantic"):
        left, right = a["ids"].get(key), b["ids"].get(key)
        if left and right and str(left) == str(right):
            return True
    # Fuzzy title matches stay separate for model review. Conflicting versions also stay separate.
    return bool(a["authors"] and b["authors"] and a["year"] and b["year"] and
                a["year"] == b["year"] and a["type"] == b["type"] and
                normalized(a["title"]) == normalized(b["title"]) and
                [normalized(x) for x in a["authors"]] == [normalized(x) for x in b["authors"]])


def deduplicate(papers):
    groups = []
    for paper in papers:
        group = next((g for g in groups if any(same_paper(paper, p) for p in g) and
                      len({p["doi"] for p in g + [paper] if p.get("doi")}) <= 1), None)
        if group is None:
            groups.append([paper])
        else:
            group.append(paper)
    result = []
    for group in groups:
        ordered = sorted(group, key=lambda p: (p["type"] != "preprint", bool(p["doi"]), bool(p["abstract"]), len(p["authors"])), reverse=True)
        merged = copy.deepcopy(ordered[0])
        merged["source_records"] = copy.deepcopy(group)
        merged["sources"] = list(dict.fromkeys(s for p in group for s in p["sources"]))
        merged["queries"] = list(dict.fromkeys(p["query"] for p in group if p.get("query")))
        merged["fulltext_links"] = []
        for p in group:
            for link in p["fulltext_links"]:
                if link not in merged["fulltext_links"]:
                    merged["fulltext_links"].append(link)
        # Do not silently splice abstracts or authors from a different publication version.
        merged["identity_status"] = "matched_records" if len(group) > 1 else "source_record"
        result.append(merged)
    return result


def task_result(http, task):
    try:
        papers = search(http, **task)
        for paper in papers:
            paper["query"] = task["query"]
        return {**task, "status": "ok" if papers else "empty", "returned": len(papers), "papers": papers}
    except SourceError as exc:
        return {**task, "status": exc.status, "message": str(exc), "returned": 0, "papers": []}
    except Exception as exc:
        return {**task, "status": "invalid_response", "error_type": type(exc).__name__,
                "message": "Provider adapter could not parse the response", "returned": 0, "papers": []}


def validate_tasks(tasks):
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("Plan must be a non-empty JSON array")
    allowed = {"source", "query", "limit", "year_from", "year_to"}
    for task in tasks:
        if not isinstance(task, dict) or set(task) - allowed:
            raise ValueError("Unexpected plan fields")
        if task.get("source") not in SOURCES or not isinstance(task.get("query"), str) or not task["query"].strip():
            raise ValueError("Each plan entry needs a supported source and a non-empty query")
        if type(task.get("limit", 10)) is not int or not 1 <= task.get("limit", 10) <= 100:
            raise ValueError("Per-query limit must be between 1 and 100")
        for key in ("year_from", "year_to"):
            if task.get(key) is not None and (type(task[key]) is not int or not 1000 <= task[key] <= 2999):
                raise ValueError("Year must be a four-digit integer")
        if task.get("year_from") and task.get("year_to") and task["year_from"] > task["year_to"]:
            raise ValueError("year_from exceeds year_to")
    return tasks


def run_search(http, tasks):
    validate_tasks(tasks)
    with ThreadPoolExecutor(max_workers=min(4, len(tasks))) as pool:
        responses = list(pool.map(lambda t: task_result(http, t), tasks))
    papers = deduplicate([p for r in responses for p in r["papers"]])
    logs = [{k: v for k, v in r.items() if k != "papers"} for r in responses]
    successes = sum(r["status"] in ("ok", "empty") for r in responses)
    return {"searched_at": datetime.now(timezone.utc).isoformat(),
            "status": "ok" if successes == len(tasks) else "partial" if successes else "failed",
            "screening_status": "pending_model_review", "unique_count": len(papers),
            "search_log": logs, "papers": papers}


def md_escape(value):
    return re.sub(r"([\\`*_{}\[\]<>])", r"\\\1", str(value or ""))


def report_markdown(result):
    lines = ["# Literature candidates", "", "Status: " + result["status"],
             "Screening: pending model review. Source-reported links have not been downloaded or verified.", ""]
    for i, paper in enumerate(result["papers"], 1):
        lines += [f"## {i}. {md_escape(paper['title'])}", "",
                  "Authors: " + md_escape("; ".join(paper["authors"]) or "not supplied"),
                  "Year: " + str(paper["year"] or "not supplied"),
                  "Venue: " + md_escape(paper["venue"] or "not supplied"),
                  "DOI: " + md_escape(paper["doi"] or "not supplied"),
                  "Article: " + md_escape(paper["url"] or "not supplied"),
                  "Sources: " + ", ".join(paper["sources"]), "",
                  "Abstract (source supplied): " + md_escape(paper["abstract"] or "not supplied"), ""]
        for link in paper["fulltext_links"]:
            lines += ["Full text (source reported): " + md_escape(link["url"])]
        lines.append("")
    lines += ["## Search log", "", "```json", json.dumps(result["search_log"], ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)


def doctor(config, config_path, live=False, sources=None, timeout=20):
    notes = {
        "email": "Needed for PubMed and Unpaywall; shared by Crossref contact identification",
        "openalex_api_key": "Recommended for OpenAlex; basic anonymous access remains available",
        "semantic_scholar_api_key": "Optional; anonymous Semantic Scholar requests may be limited",
        "ncbi_api_key": "Optional NCBI rate allowance",
        "http_proxy": "Only needed when the network requires a proxy",
        "https_proxy": "Only needed when the network requires a proxy",
    }
    result = {"python": sys.version.split()[0], "python_ok": sys.version_info >= (3, 10),
              "third_party_packages": [], "config_path": str(config_path or DEFAULT_CONFIG),
              "config_file_exists": Path(config_path or DEFAULT_CONFIG).exists(),
              "configuration": [{"variable": env, "configured": bool(config[key]), "purpose": notes[key]} for key, env in FIELDS.items()],
              "live_checks": "not_run"}
    if live:
        http = Http(config, timeout=timeout, retries=0)
        tasks = [{"source": source, "query": "graph neural network", "limit": 1} for source in (sources or ["openalex", "crossref", "arxiv"])]
        result["live_checks"] = run_search(http, tasks)["search_log"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, help="Default: ~/.config/literature-search/config.json")
    parser.add_argument("--timeout", type=int, default=20)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("doctor")
    check.add_argument("--live", action="store_true")
    check.add_argument("--sources", nargs="+", choices=SOURCES)
    find = sub.add_parser("search")
    query = find.add_mutually_exclusive_group(required=True)
    query.add_argument("--query", action="append")
    query.add_argument("--plan", type=Path)
    find.add_argument("--sources", nargs="+", choices=SOURCES, default=["openalex", "crossref", "arxiv"])
    find.add_argument("--limit", type=int, default=10, help="Per source/query, 1-100; not a claim of exhaustive retrieval")
    find.add_argument("--year-from", type=int)
    find.add_argument("--year-to", type=int)
    find.add_argument("--out", type=Path, required=True, help="New result directory; existing reports are not overwritten")
    enrich = sub.add_parser("resolve")
    enrich.add_argument("--doi", action="append", required=True)
    enrich.add_argument("--out", type=Path, required=True, help="New JSON result file")
    args = parser.parse_args()
    try:
        if not 1 <= args.timeout <= 60:
            raise ValueError("timeout must be between 1 and 60 seconds")
        config = load_config(args.config)
        if args.command == "doctor":
            result = doctor(config, args.config, args.live, args.sources, args.timeout)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            checks = result["live_checks"]
            return 0 if result["python_ok"] and (checks == "not_run" or all(c["status"] in ("ok", "empty") for c in checks)) else 2
        http = Http(config, timeout=args.timeout)
        if args.command == "search":
            tasks = json.loads(args.plan.read_text(encoding="utf-8-sig")) if args.plan else [
                {"source": s, "query": q, "limit": args.limit, "year_from": args.year_from, "year_to": args.year_to}
                for q in args.query for s in args.sources]
            validate_tasks(tasks)
            if any((args.out / name).exists() for name in ("candidates.json", "candidates.md")):
                raise ValueError("Choose a new output directory; existing reports are not overwritten")
            result = run_search(http, tasks)
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / "candidates.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            (args.out / "candidates.md").write_text(report_markdown(result), encoding="utf-8")
            print(json.dumps({"status": result["status"], "unique_count": result["unique_count"],
                              "output": str(args.out.resolve()), "search_log": result["search_log"]}, ensure_ascii=False, indent=2))
            return 2 if result["status"] == "failed" else 0
        if args.out.exists():
            raise ValueError("Choose a new output file")
        result = []
        for index, identifier in enumerate(args.doi, 1):
            if not doi(identifier):
                result.append({"input_index": index, "status": "invalid_identifier", "message": "Expected a DOI or DOI URL"})
                continue
            try:
                result.append(resolve(http, identifier))
            except (KeyError, TypeError, IndexError, AttributeError, ParseError, SourceError):
                result.append({"input_index": index, "doi": doi(identifier), "status": "invalid_response", "message": "DOI provider response could not be parsed"})
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output": str(args.out.resolve()), "count": len(result)}, ensure_ascii=False))
        return 0 if any(r.get("paper") or r.get("fulltext_links") for r in result) else 2
    except (ValueError, OSError):
        print("Configuration, arguments, or file operation failed. Check documented field names, JSON, paths and output collisions; values are hidden.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    raise SystemExit(main())
