import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time


def search_arxiv(query: str, max_results: int = 3, retries: int = 3) -> list:
    """Search arXiv for papers matching a query, sorted by relevance."""
    base = "http://export.arxiv.org/api/query?"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = base + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MultiagentSystem/1.0 (educational research agent)"},
    )

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                data = response.read().decode("utf-8")
            papers = _parse_arxiv(data)
            if papers:
                return papers
            time.sleep(3)
        except Exception as e:
            if attempt == retries - 1:
                return [{"error": f"arXiv request failed: {e}"}]
            time.sleep(3)
    return []

def _parse_arxiv(data: str) -> list:
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(data)
    papers = []
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns)
        summary = entry.find("atom:summary", ns)
        link = entry.find("atom:id", ns)
        authors = [a.find("atom:name", ns).text
                   for a in entry.findall("atom:author", ns)]
        papers.append({
            "title": title.text.strip() if title is not None else "Untitled",
            "summary": (summary.text.strip()[:300] + "...") if summary is not None else "",
            "authors": authors[:3],
            "url": link.text.strip() if link is not None else "",
        })
    return papers