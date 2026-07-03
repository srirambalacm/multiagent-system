import json
import re
import os
from datetime import datetime
from agents.base_agent import BaseAgent
from utils.youtube import get_transcript, find_concept_segments, extract_video_id, format_timestamp


class WalkthroughAgent(BaseAgent):
    name = "WalkthroughAgent"

    def handle(self, prompt: str, csv_path: str = None) -> str:
        url = self.find_url(prompt)
        if not url:
            return (f"[{self.name}] I need a YouTube URL to build a walkthrough. "
                    f"Include a link in your request.")

        try:
            segments = get_transcript(url)
        except Exception as e:
            return f"[{self.name}] Couldn't get the transcript: {e}"

        try:
            moments = find_concept_segments(segments)
        except Exception as e:
            return f"[{self.name}] Couldn't analyze the transcript: {e}"

        video_id = extract_video_id(url)
        walkthrough = self.build_walkthrough(url, video_id, moments)

        # Save JSON artifact
        os.makedirs("outputs", exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = os.path.join("outputs", f"walkthrough_{video_id}_{stamp}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(walkthrough, f, indent=2)

        # Human-readable summary
        lines = [f"[{self.name}] Concept walkthrough ({len(walkthrough['moments'])} key moments):\n"]
        for m in walkthrough["moments"]:
            lines.append(f"  [{m['timestamp']}] {m['concept']}")
            lines.append(f"      {m['why']}")
            lines.append(f"      Jump: {m['jump_url']}\n")
        lines.append(f"  Saved to: {json_path}")
        return "\n".join(lines)

    def find_url(self, prompt: str) -> str:
        m = re.search(r"https?://[^\s]+", prompt)
        return m.group(0) if m else None

    def build_walkthrough(self, url: str, video_id: str, moments: list) -> dict:
        enriched = []
        for m in moments:
            secs = int(m.get("timestamp_seconds", 0))
            enriched.append({
                "concept": m.get("concept", ""),
                "timestamp": format_timestamp(secs),
                "timestamp_seconds": secs,
                "why": m.get("why", ""),
                "jump_url": f"https://www.youtube.com/watch?v={video_id}&t={secs}s",
            })
        return {
            "source_video": url,
            "moments": enriched,
        }