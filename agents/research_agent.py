import json
import time
import re
import os
from datetime import datetime
from agents.base_agent import BaseAgent
from utils.youtube import (get_transcript, extract_concepts, extract_video_id,
                           make_search_queries)
from utils.research import search_arxiv
from utils.visualize import render_mind_map_html


class ResearchAgent(BaseAgent):
    name = "ResearchAgent"

    def handle(self, prompt: str, csv_path: str = None) -> str:
        url = self.find_url(prompt)
        if not url:
            return (f"[{self.name}] I need a YouTube URL to research. "
                    f"Include a link in your request.")

        try:
            segments = get_transcript(url)
        except Exception as e:
            return f"[{self.name}] Couldn't get the transcript: {e}"

        try:
            concepts = extract_concepts(segments)
        except Exception as e:
            return f"[{self.name}] Couldn't extract concepts: {e}"

        mind_map = self.build_mind_map(prompt, url, concepts)

        video_id = extract_video_id(url)
        os.makedirs("outputs", exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join("outputs", f"research_map_{video_id}_{stamp}.json")
        html_path = os.path.join("outputs", f"research_map_{video_id}_{stamp}.html")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(mind_map, f, indent=2)
        render_mind_map_html(mind_map, html_path)

        return (
            f"[{self.name}] Built a research map for: {mind_map['topic']}\n"
            f"  Concepts analyzed: {len(mind_map['concepts'])}\n"
            f"  Papers found: {sum(len(n['papers']) for n in mind_map['mind_map'])}\n"
            f"  JSON saved to: {json_path}\n"
            f"  Visual map saved to: {html_path}\n"
            f"  (Open the .html file in a browser to view the mind map.)"
        )

    def find_url(self, prompt: str) -> str:
        m = re.search(r"https?://[^\s]+", prompt)
        return m.group(0) if m else None

    def build_mind_map(self, goal: str, url: str, concepts: list) -> dict:
        topic = concepts[0] if concepts else "the subject"

        # Only search substantive concepts (skip ultra-granular ones).
        substantive = [c for c in concepts if len(c.split()) <= 3][:5]

        # ONE batched Gemini call for all search queries (was one call per concept).
        query_map = make_search_queries(substantive, topic)

        nodes = []
        seen_urls = set()
        for i, concept in enumerate(substantive):
            if i > 0:
                time.sleep(3)  # arXiv rate courtesy (network, not Gemini)
            query = query_map.get(concept, concept)
            papers = search_arxiv(query, max_results=4)
            paper_refs = []
            for p in papers:
                if "error" in p or p["url"] in seen_urls:
                    continue
                seen_urls.add(p["url"])
                paper_refs.append({"title": p.get("title"), "url": p.get("url")})
                if len(paper_refs) >= 2:
                    break
            nodes.append({"concept": concept, "search_query": query, "papers": paper_refs})

        return {
            "goal": goal,
            "source_video": url,
            "topic": topic,
            "concepts": list(concepts),
            "mind_map": nodes,
        }