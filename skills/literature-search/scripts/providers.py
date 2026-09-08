"""Provider adapters for academic search and open-access metadata."""

import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import quote, unquote

from runtime import SourceError

SOURCES = ("openalex", "crossref", "arxiv", "semantic", "pubmed")


class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def text(value):
    parser = TextOnly()
    parser.feed(value or "")
    parser.close()
    return " ".join(" ".join(parser.parts).split())


def doi(value):
    value = unquote(value or "").strip()
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value, flags=re.I)
    return value.lower() if re.fullmatch(r"10\.\d{4,9}/\S+", value, flags=re.I) else None


def record(source, title, authors, year, identifier=None, abstract=None, url=None, venue=None, ids=None, fulltext=None, kind=None):
    return {
        "title": text(title), "authors": authors, "year": year, "venue": venue,
        "doi": doi(identifier), "abstract": text(abstract) or None,
        "abstract_source": source if abstract else None,
        "url": url or ("https://doi.org/" + doi(identifier) if doi(identifier) else None),
        "ids": ids or {}, "fulltext_links": fulltext or [], "type": kind,
        "sources": [source], "evidence_level": "abstract" if abstract else "metadata",
        "identity_status": "source_record", "relevance": "not_screened",
    }


def oa_record(w):
    inverted = w.get("abstract_inverted_index") or {}
    words = sorted((position, word) for word, positions in inverted.items() for position in positions)
    locations = [w.get("best_oa_location") or {}, w.get("primary_location") or {}]
    links = [{"url": loc["pdf_url"], "format": "pdf", "status": "source_reported", "source": "openalex"}
             for loc in locations if loc.get("pdf_url")]
    primary = w.get("primary_location") or {}
    return record("openalex", w.get("display_name", ""),
                  [a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author", {}).get("display_name")],
                  w.get("publication_year"), w.get("doi"), " ".join(word for _, word in words),
                  primary.get("landing_page_url"), (primary.get("source") or {}).get("display_name"),
                  {"openalex": w.get("id")}, links, w.get("type"))


def crossref_record(w):
    parts = (w.get("published") or w.get("published-print") or w.get("published-online") or {}).get("date-parts", [[]])
    year = parts[0][0] if parts and parts[0] else None
    authors = [" ".join(filter(None, [a.get("given"), a.get("family")])) or a.get("name", "") for a in w.get("author", [])]
    return record("crossref", (w.get("title") or [""])[0], authors, year, w.get("DOI"),
                  w.get("abstract"), w.get("URL"), (w.get("container-title") or [None])[0], kind=w.get("type"))


def parse_arxiv(raw):
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    result = []
    for entry in ET.fromstring(raw).findall("a:entry", ns):
        url = entry.findtext("a:id", "", ns)
        if "/api/errors" in url:
            raise SourceError("invalid_query", "arXiv rejected the query")
        aid = url.split("/abs/")[-1]
        links = [{"url": link.attrib["href"], "format": "pdf", "status": "source_reported", "source": "arxiv"}
                 for link in entry.findall("a:link", ns) if link.get("title") == "pdf"]
        published = entry.findtext("a:published", "", ns)
        result.append(record("arxiv", entry.findtext("a:title", "", ns),
                             [a.findtext("a:name", "", ns) for a in entry.findall("a:author", ns)],
                             int(published[:4]) if published[:4].isdigit() else None,
                             entry.findtext("x:doi", None, ns), entry.findtext("a:summary", "", ns), url,
                             entry.findtext("x:journal_ref", None, ns),
                             {"arxiv": re.sub(r"v\d+$", "", aid), "arxiv_version": aid}, links, "preprint"))
    return result


def parse_pubmed(raw):
    def content(el):
        return "".join(el.itertext()).strip() if el is not None else ""

    records = []
    for item in ET.fromstring(raw).findall("PubmedArticle"):
        article = item.find("MedlineCitation/Article")
        if article is None:
            continue
        pmid = item.findtext("MedlineCitation/PMID")
        ids = {el.get("IdType"): el.text for el in item.findall("PubmedData/ArticleIdList/ArticleId")}
        authors = [a.findtext("CollectiveName") or " ".join(filter(None, [a.findtext("ForeName"), a.findtext("LastName")]))
                   for a in article.findall("AuthorList/Author")]
        year_text = article.findtext("Journal/JournalIssue/PubDate/Year") or article.findtext("Journal/JournalIssue/PubDate/MedlineDate", "")
        year = re.search(r"\b\d{4}\b", year_text)
        abstract = " ".join(((e.get("Label") + ": ") if e.get("Label") else "") + content(e) for e in article.findall("Abstract/AbstractText"))
        records.append(record("pubmed", content(article.find("ArticleTitle")), authors,
                              int(year.group()) if year else None, ids.get("doi"), abstract,
                              "https://pubmed.ncbi.nlm.nih.gov/" + pmid + "/", article.findtext("Journal/Title"),
                              {"pmid": pmid, "pmcid": ids.get("pmc")}))
    return records


def search(http, source, query, limit=10, year_from=None, year_to=None):
    cfg = http.config
    if source == "openalex":
        params = {"search": query, "per_page": limit}
        filters = []
        if year_from:
            filters.append(f"from_publication_date:{year_from}-01-01")
        if year_to:
            filters.append(f"to_publication_date:{year_to}-12-31")
        if filters:
            params["filter"] = ",".join(filters)
        headers = {"Authorization": "Bearer " + cfg["openalex_api_key"]} if cfg["openalex_api_key"] else {}
        data = http.json(source, "https://api.openalex.org/works", params, headers)
        papers = [oa_record(w) for w in data["results"]]
    elif source == "crossref":
        params = {"query.bibliographic": query, "rows": limit, "mailto": cfg["email"] or None}
        filters = []
        if year_from:
            filters.append(f"from-pub-date:{year_from}-01-01")
        if year_to:
            filters.append(f"until-pub-date:{year_to}-12-31")
        if filters:
            params["filter"] = ",".join(filters)
        data = http.json(source, "https://api.crossref.org/works", params)
        papers = [crossref_record(w) for w in data["message"]["items"]]
    elif source == "arxiv":
        if not re.search(r"\b(?:all|ti|au|abs|cat|id|doi):", query):
            query = " AND ".join("all:" + term for term in re.findall(r'"[^"]+"|\S+', query) if term.upper() != "AND")
        if year_from or year_to:
            query = f"({query}) AND submittedDate:[{year_from or 1900}01010000 TO {year_to or 2099}12312359]"
        papers = parse_arxiv(http.get(source, "https://export.arxiv.org/api/query",
                                      {"search_query": query, "start": 0, "max_results": limit, "sortBy": "relevance"}, interval=3.1))
    elif source == "semantic":
        headers = {"x-api-key": cfg["semantic_scholar_api_key"]} if cfg["semantic_scholar_api_key"] else {}
        params = {"query": query, "limit": limit,
                  "fields": "title,authors,year,abstract,externalIds,url,venue,openAccessPdf,publicationTypes"}
        if year_from or year_to:
            params["year"] = f"{year_from or ''}-{year_to or ''}"
        data = http.json(source, "https://api.semanticscholar.org/graph/v1/paper/search", params, headers, interval=1.1)
        papers = []
        for w in data["data"]:
            external = w.get("externalIds") or {}
            pdf = (w.get("openAccessPdf") or {}).get("url")
            links = [{"url": pdf, "format": "pdf", "status": "source_reported", "source": source}] if pdf else []
            papers.append(record(source, w.get("title", ""), [a["name"] for a in w.get("authors", [])],
                                  w.get("year"), external.get("DOI"), w.get("abstract"), w.get("url"), w.get("venue"),
                                  {"semantic": w.get("paperId"), "arxiv": external.get("ArXiv"), "pmid": external.get("PubMed")}, links))
    elif source == "pubmed":
        if not cfg["email"]:
            raise SourceError("needs_configuration", "PubMed requires LITERATURE_EMAIL (or config email)")
        params = {"db": "pubmed", "term": query, "retmax": limit, "retmode": "json", "email": cfg["email"],
                  "api_key": cfg["ncbi_api_key"] or None, "tool": "literature-search"}
        if year_from or year_to:
            params.update({"datetype": "pdat", "mindate": str(year_from or 1800), "maxdate": str(year_to or 2099)})
        root = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        data = http.json(source, root + "esearch.fcgi", params, interval=0.4)
        if data.get("error") or data.get("esearchresult", {}).get("errorlist"):
            raise SourceError("invalid_query", "PubMed rejected the query")
        ids = data["esearchresult"]["idlist"]
        papers = parse_pubmed(http.get(source, root + "efetch.fcgi", {
            "db": "pubmed", "id": ",".join(ids), "retmode": "xml", "email": cfg["email"],
            "api_key": cfg["ncbi_api_key"] or None, "tool": "literature-search"}, interval=0.4)) if ids else []
    else:
        raise ValueError("Unsupported search source")
    return [p for p in papers if p["title"]]


def resolve(http, identifier):
    identifier = doi(identifier)
    if not identifier:
        raise ValueError("Expected a DOI or DOI URL")
    checks, paper, links = [], None, []
    encoded = quote(identifier, safe="")
    try:
        data = http.json("crossref", "https://api.crossref.org/works/" + encoded,
                         {"mailto": http.config["email"] or None})
        paper = crossref_record(data["message"])
        checks.append({"source": "crossref", "status": "ok"})
    except SourceError as exc:
        checks.append({"source": "crossref", "status": exc.status, "message": str(exc)})
    except (KeyError, TypeError, IndexError, AttributeError, ValueError):
        checks.append({"source": "crossref", "status": "invalid_response"})
    # Crossref is not the registration agency for every DOI.
    if paper is None:
        try:
            data = http.json("datacite", "https://api.datacite.org/dois/" + encoded)["data"]["attributes"]
            abstracts = [d["description"] for d in data.get("descriptions", []) if d.get("descriptionType") == "Abstract"]
            paper = record("datacite", data["titles"][0]["title"], [a.get("name", "") for a in data.get("creators", [])],
                           data.get("publicationYear"), identifier, " ".join(abstracts), data.get("url"))
            checks.append({"source": "datacite", "status": "ok"})
        except SourceError as exc:
            checks.append({"source": "datacite", "status": exc.status, "message": str(exc)})
        except (KeyError, TypeError, IndexError, AttributeError, ValueError):
            checks.append({"source": "datacite", "status": "invalid_response"})
    if http.config["email"]:
        try:
            data = http.json("unpaywall", "https://api.unpaywall.org/v2/" + encoded, {"email": http.config["email"]})
            for location in data.get("oa_locations") or []:
                url = location.get("url_for_pdf") or location.get("url_for_landing_page")
                if url:
                    links.append({"url": url, "format": "pdf" if location.get("url_for_pdf") else "landing_page",
                                  "status": "source_reported", "source": "unpaywall", "version": location.get("version"),
                                  "license": location.get("license")})
            checks.append({"source": "unpaywall", "status": "ok", "is_oa": data.get("is_oa")})
        except SourceError as exc:
            checks.append({"source": "unpaywall", "status": exc.status, "message": str(exc)})
        except (KeyError, TypeError, IndexError, AttributeError, ValueError):
            checks.append({"source": "unpaywall", "status": "invalid_response"})
    else:
        checks.append({"source": "unpaywall", "status": "needs_configuration", "message": "Set LITERATURE_EMAIL"})
    return {"doi": identifier, "url": "https://doi.org/" + identifier, "paper": paper, "fulltext_links": links,
            "checks": checks, "identity_status": "metadata_found" if paper else "unresolved"}
