import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

import literature_search as cli
from configure import save_config
from providers import crossref_record, doi, oa_record, parse_arxiv, parse_pubmed, record, resolve, search
from runtime import FIELDS, Http, SourceError, load_config


def blank_config():
    return {key: "" for key in FIELDS}


class FakeHttp:
    def __init__(self, responses, config=None):
        self.responses = iter(responses)
        self.config = config or blank_config()
        self.calls = []

    def json(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        value = next(self.responses)
        if isinstance(value, Exception):
            raise value
        return value


class ConfigTests(unittest.TestCase):
    def test_environment_overrides_file_without_legacy_mailboxes(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {"LITERATURE_EMAIL": "env@example.org", "PUBMED_EMAIL": "legacy@example.org"}, clear=True):
            target = Path(tmp) / "config.json"
            save_config(target, {"email": "file@example.org", "openalex_api_key": "key"})
            self.assertEqual(load_config(target)["email"], "env@example.org")
            self.assertEqual(load_config(target)["openalex_api_key"], "key")
            self.assertEqual(json.loads(target.read_text())["email"], "file@example.org")

    def test_doctor_does_not_print_secrets(self):
        config = {key: "private-value" for key in FIELDS}
        output = json.dumps(cli.doctor(config, "missing.json"))
        self.assertNotIn("private-value", output)
        self.assertIn('"configured": true', output)
        self.assertIn('"live_checks": "not_run"', output)

    def test_config_rejects_unknown_or_non_string_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "config.json"
            for value in ({"typo_key": "secret"}, {"email": 12}, []):
                target.write_text(json.dumps(value))
                with self.assertRaises(ValueError):
                    load_config(target)


class ParserTests(unittest.TestCase):
    def test_doi_preserves_valid_punctuation(self):
        self.assertEqual(doi("https://doi.org/10.1234/ABC(DEF)"), "10.1234/abc(def)")
        self.assertIsNone(doi("not a DOI"))

    def test_openalex_abstract_reconstruction_and_missing_location(self):
        paper = oa_record({"display_name": "A paper", "abstract_inverted_index": {"world": [1], "Hello": [0]}, "primary_location": None})
        self.assertEqual(paper["abstract"], "Hello world")
        self.assertIsNone(paper["url"])

    def test_crossref_complete_authors_and_markup(self):
        paper = crossref_record({"title": ["Example"], "author": [{"given": "A", "family": "One"}, {"name": "Research Consortium"}],
                                "published": {"date-parts": [[2022, 3]]}, "abstract": "<jats:p>A <jats:italic>real</jats:italic> abstract.</jats:p>"})
        self.assertEqual(paper["authors"], ["A One", "Research Consortium"])
        self.assertEqual(paper["abstract"], "A real abstract.")
        self.assertEqual(paper["year"], 2022)

    def test_arxiv_keeps_version_and_formal_doi(self):
        raw = b'''<feed xmlns="http://www.w3.org/2005/Atom" xmlns:x="http://arxiv.org/schemas/atom"><entry>
        <id>https://arxiv.org/abs/1234.56789v2</id><title>Example</title><published>2020-01-01</published>
        <author><name>A Person</name></author><summary>Full abstract.</summary><x:doi>10.1234/formal</x:doi>
        <link title="pdf" href="https://arxiv.org/pdf/1234.56789v2"/></entry></feed>'''
        paper = parse_arxiv(raw)[0]
        self.assertEqual(paper["ids"]["arxiv"], "1234.56789")
        self.assertEqual(paper["ids"]["arxiv_version"], "1234.56789v2")
        self.assertEqual(paper["type"], "preprint")
        self.assertEqual(paper["doi"], "10.1234/formal")

    def test_pubmed_preserves_inline_text_labels_and_authors(self):
        raw = b'''<PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>123</PMID><Article>
        <ArticleTitle>Testing <i>in vitro</i> results</ArticleTitle><Abstract><AbstractText Label="RESULTS">A <b>strong</b> result.</AbstractText></Abstract>
        <AuthorList><Author><ForeName>A</ForeName><LastName>One</LastName></Author><Author><CollectiveName>Group</CollectiveName></Author></AuthorList>
        <Journal><Title>Journal</Title><JournalIssue><PubDate><MedlineDate>2021 Jan-Feb</MedlineDate></PubDate></JournalIssue></Journal>
        </Article></MedlineCitation><PubmedData><ArticleIdList><ArticleId IdType="doi">10.1234/example</ArticleId></ArticleIdList></PubmedData>
        </PubmedArticle></PubmedArticleSet>'''
        paper = parse_pubmed(raw)[0]
        self.assertEqual(paper["title"], "Testing in vitro results")
        self.assertEqual(paper["abstract"], "RESULTS: A strong result.")
        self.assertEqual(paper["authors"], ["A One", "Group"])
        self.assertEqual(paper["year"], 2021)


class WorkflowTests(unittest.TestCase):
    def paper(self, source="crossref", identifier="10.1234/paper", kind="article"):
        return record(source, "Example title", ["A One"], 2021, identifier, kind=kind)

    def test_conflicting_dois_not_merged_by_title(self):
        papers = [self.paper(identifier="10.1234/one"), self.paper(identifier="10.1234/two")]
        self.assertEqual(len(cli.deduplicate(papers)), 2)

    def test_group_preserves_preprint_and_does_not_splice_abstract(self):
        formal = self.paper()
        preprint = self.paper("arxiv", kind="preprint")
        preprint.update({"year": 2020, "abstract": "Preprint abstract", "query": "query two"})
        formal["query"] = "query one"
        merged = cli.deduplicate([preprint, formal])[0]
        self.assertEqual(merged["type"], "article")
        self.assertIsNone(merged["abstract"])
        self.assertEqual(len(merged["source_records"]), 2)
        self.assertEqual(set(merged["queries"]), {"query one", "query two"})
        self.assertEqual(merged["identity_status"], "matched_records")

    def test_idless_bridge_does_not_merge_conflicting_dois(self):
        papers = [self.paper(identifier="10.1234/one"), self.paper(identifier=None), self.paper(identifier="10.1234/two")]
        self.assertEqual(len(cli.deduplicate(papers)), 2)

    def test_partial_failure_is_distinct_from_empty_result(self):
        def answer(http, **task):
            if task["source"] == "openalex":
                raise SourceError("rate_limited", "HTTP 429")
            return []
        with patch.object(cli, "search", side_effect=answer):
            result = cli.run_search(None, [{"source": s, "query": "example"} for s in ("openalex", "crossref")])
        self.assertEqual(result["status"], "partial")
        self.assertEqual([r["status"] for r in result["search_log"]], ["rate_limited", "empty"])

    def test_openalex_key_is_sent_as_header(self):
        config = blank_config()
        config["openalex_api_key"] = "private-token"
        http = FakeHttp([{"results": []}], config)
        search(http, "openalex", "example")
        args = http.calls[0][0]
        self.assertEqual(args[3]["Authorization"], "Bearer private-token")
        self.assertNotIn("private-token", args[1])

    def test_shared_email_reaches_unpaywall_and_crossref(self):
        config = blank_config()
        config["email"] = "contact@example.org"
        http = FakeHttp([{"message": {"title": ["Example"], "DOI": "10.1234/x"}}, {"is_oa": True, "oa_locations": [{"url_for_pdf": "https://example.org/paper.pdf", "version": "publishedVersion"}]}], config)
        result = resolve(http, "10.1234/x")
        self.assertEqual(http.calls[0][0][2]["mailto"], config["email"])
        self.assertEqual(http.calls[1][0][2]["email"], config["email"])
        self.assertEqual(result["fulltext_links"][0]["status"], "source_reported")

    def test_crossref_404_falls_back_to_datacite(self):
        http = FakeHttp([SourceError("not_found", "HTTP 404"), {"data": {"attributes": {"titles": [{"title": "Dataset paper"}], "creators": [{"name": "A Person"}], "publicationYear": 2020}}}])
        result = resolve(http, "10.1234/x")
        self.assertEqual(result["paper"]["sources"], ["datacite"])
        self.assertEqual(result["checks"][-1]["status"], "needs_configuration")

    def test_malformed_oa_response_preserves_metadata(self):
        config = blank_config()
        config["email"] = "contact@example.org"
        http = FakeHttp([{"message": {"title": ["Example"], "DOI": "10.1234/x"}}, ["unexpected schema"]], config)
        result = resolve(http, "10.1234/x")
        self.assertEqual(result["paper"]["title"], "Example")
        self.assertEqual(result["checks"][-1]["status"], "invalid_response")

    def test_plan_validates_year_range_and_limit(self):
        for extra in ({"limit": 101}, {"year_from": 2025, "year_to": 2020}, {"unknown": "x"}):
            with self.assertRaises(ValueError):
                cli.validate_tasks([{"source": "crossref", "query": "example", **extra}])

    def test_cli_writes_full_abstract_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {}, clear=True):
            out = Path(tmp) / "results"
            argv = ["literature_search.py", "--config", str(Path(tmp) / "config.json"), "search", "--query", "example", "--sources", "crossref", "--out", str(out)]
            paper = self.paper()
            paper["abstract"] = "Complete abstract. " * 30
            with patch.object(cli, "search", return_value=[paper]), patch.object(cli.sys, "argv", argv), redirect_stdout(io.StringIO()):
                self.assertEqual(cli.main(), 0)
            saved = json.loads((out / "candidates.json").read_text())
            self.assertEqual(saved["papers"][0]["abstract"], paper["abstract"])
            with patch.object(cli.sys, "argv", argv), redirect_stderr(io.StringIO()):
                self.assertEqual(cli.main(), 2)


class HttpTests(unittest.TestCase):
    def test_errors_do_not_expose_request_secrets(self):
        http = Http(blank_config(), retries=0)
        error = HTTPError("https://example.org/?api_key=private-token", 401, "private-token", {}, None)
        with patch.object(http.opener, "open", side_effect=error):
            with self.assertRaises(SourceError) as caught:
                http.get("test", "https://example.org", {"api_key": "private-token"}, interval=0)
        self.assertEqual(caught.exception.status, "unauthorized")
        self.assertNotIn("private-token", str(caught.exception))

    def test_long_retry_after_does_not_block_or_repeat(self):
        http = Http(blank_config())
        error = HTTPError("https://example.org", 429, "limited", {"Retry-After": "90"}, None)
        with patch.object(http.opener, "open", side_effect=error) as request:
            with self.assertRaises(SourceError) as caught:
                http.get("test", "https://example.org", interval=0)
        self.assertEqual(request.call_count, 1)
        self.assertEqual(caught.exception.status, "rate_limited")

    def test_http_date_retry_after_is_respected(self):
        http = Http(blank_config())
        retry_at = format_datetime(datetime.now(timezone.utc) + timedelta(minutes=5), usegmt=True)
        error = HTTPError("https://example.org", 429, "limited", {"Retry-After": retry_at}, None)
        with patch.object(http.opener, "open", side_effect=error) as request:
            with self.assertRaises(SourceError):
                http.get("test", "https://example.org", interval=0)
        self.assertEqual(request.call_count, 1)


if __name__ == "__main__":
    unittest.main()
