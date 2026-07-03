"""Live integration tests for the video agents.
These consume Gemini API quota and require network — run deliberately:
    python -m tests.test_video
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

VIDEO = "https://www.youtube.com/watch?v=aircAruvnKk"


def test_transcript():
    print("\n[Transcript extraction — live]")
    from utils.youtube import get_transcript
    segments = get_transcript(VIDEO)
    print(f"  Got {len(segments)} segments")
    assert len(segments) > 0, "No transcript segments returned"
    print("  PASS  transcript fetched")


def test_walkthrough():
    print("\n[Walkthrough Agent — live, uses quota]")
    from agents.walkthrough_agent import WalkthroughAgent
    out = WalkthroughAgent().handle(f"walk me through this video: {VIDEO}")
    print(out[:400])
    assert "key moments" in out.lower() or "Jump:" in out
    print("  PASS  walkthrough produced")


if __name__ == "__main__":
    print("Running LIVE video tests (uses API quota)...")
    test_transcript()
    test_walkthrough()
    print("\nDone.")