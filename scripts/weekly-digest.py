"""
weekly-digest.py
-----------------
Reads your latest week-N.md file, uses Claude to write
a one-paragraph summary, and saves it to digest.json
so your dashboard shows it automatically.

Usage:
  python3 weekly-digest.py

Then commit and push:
  git add ../digest.json && git commit -m "update: week N digest" && git push

Requirements:
  pip3 install anthropic python-dotenv

Setup:
  Add ANTHROPIC_API_KEY to your .env file
"""

import anthropic
import json
import os
import glob
from datetime import date
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def find_latest_week_file():
    """Find the most recent week-N.md file."""
    # Look in parent directory (ai-journey/)
    files = glob.glob("../week-*.md")
    if not files:
        print("No week-N.md files found in ai-journey/")
        return None, None

    # Sort by week number
    def week_number(f):
        try:
            return int(f.split("week-")[1].split(".")[0])
        except (IndexError, ValueError):
            return 0

    files.sort(key=week_number)
    latest = files[-1]
    week_num = week_number(latest)
    return latest, week_num

def generate_digest(week_content: str, week_num: int) -> dict:
    """Use Claude to summarise the week."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""You are summarising a week of someone's AI learning journey.
They are learning AI engineering from zero coding experience and documenting it on Instagram.

Here is their week {week_num} log:

{week_content}

Write a single paragraph (3-5 sentences) that:
- States what they learned or built this week in plain English
- Notes one thing that was hard or surprising
- Ends with what they're tackling next week
- Sounds honest and human — not marketing language

Keep it under 80 words."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text.strip()

def save_digest(week_num: int, summary: str, week_file: str):
    """Write digest.json to the root of ai-journey/."""
    digest_path = "../digest.json"

    digest = {
        "week": week_num,
        "summary": summary,
        "generated": str(date.today()),
        "source_file": os.path.basename(week_file)
    }

    with open(digest_path, "w") as f:
        json.dump(digest, f, indent=2)

    print(f"Saved digest.json — Week {week_num}")
    print(f"\nSummary:\n{summary}")
    print("\nNext steps:")
    print("  git add ../digest.json")
    print(f"  git commit -m 'update: week {week_num} digest'")
    print("  git push")
    print("\nYour dashboard will auto-update after push.")

if __name__ == "__main__":
    if not ANTHROPIC_API_KEY:
        print("Error: Missing ANTHROPIC_API_KEY in .env file.")
        print("Get your key at: https://console.anthropic.com/")
        exit(1)

    print("=== Weekly Digest Generator ===\n")

    week_file, week_num = find_latest_week_file()
    if not week_file:
        exit(1)

    print(f"Found: {week_file} (Week {week_num})")

    with open(week_file, "r") as f:
        content = f.read()

    if not content.strip():
        print(f"Error: {week_file} is empty. Fill it in first.")
        exit(1)

    print("Generating digest with Claude...\n")
    summary = generate_digest(content, week_num)
    save_digest(week_num, summary, week_file)
