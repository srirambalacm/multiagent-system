import json
import html


def render_mind_map_html(mind_map: dict, out_path: str) -> str:
    """Render a mind-map dict into a standalone HTML file. Returns the path written."""
    goal = html.escape(mind_map.get("goal", ""))
    topic = html.escape(mind_map.get("topic", ""))
    video = html.escape(mind_map.get("source_video", ""))

    concept_blocks = []
    for node in mind_map.get("mind_map", []):
        concept = html.escape(node.get("concept", ""))
        query = html.escape(node.get("search_query", ""))
        papers = node.get("papers", [])
        paper_items = ""
        for p in papers:
            title = html.escape(p.get("title", "Untitled"))
            url = html.escape(p.get("url", "#"))
            paper_items += f'<li><a href="{url}" target="_blank">{title}</a></li>'
        if not paper_items:
            paper_items = "<li class='empty'>No papers found</li>"
        concept_blocks.append(f"""
        <div class="concept">
            <div class="concept-title">{concept}</div>
            <div class="query">search: {query}</div>
            <ul>{paper_items}</ul>
        </div>""")

    concepts_html = "\n".join(concept_blocks)

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Research Map — {topic}</title>
<style>
    body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif;
           background: #0f1117; color: #e6e6e6; margin: 0; padding: 40px; }}
    .header {{ margin-bottom: 32px; }}
    h1 {{ font-size: 22px; margin: 0 0 8px; }}
    .meta {{ color: #8b93a7; font-size: 14px; }}
    .meta a {{ color: #6ea8fe; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px; }}
    .concept {{ background: #1a1d29; border: 1px solid #2a2f42;
               border-radius: 12px; padding: 20px; }}
    .concept-title {{ font-size: 16px; font-weight: 600; color: #fff; margin-bottom: 4px; }}
    .query {{ font-size: 12px; color: #6ea8fe; margin-bottom: 12px; font-family: monospace; }}
    ul {{ list-style: none; padding: 0; margin: 0; }}
    li {{ margin-bottom: 8px; font-size: 14px; line-height: 1.4; }}
    li a {{ color: #d0d6e4; text-decoration: none; }}
    li a:hover {{ color: #6ea8fe; text-decoration: underline; }}
    .empty {{ color: #5a6072; font-style: italic; }}
</style>
</head>
<body>
    <div class="header">
        <h1>Research Map: {topic}</h1>
        <div class="meta">Goal: {goal}<br>
        Source: <a href="{video}" target="_blank">{video}</a></div>
    </div>
    <div class="grid">
        {concepts_html}
    </div>
</body>
</html>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    return out_path