"""
caption-generator.py
---------------------
Takes your Reel hook + bullet points and generates a
ready-to-post Instagram caption with hashtags.

Usage:
  python3 caption-generator.py

Requirements:
  pip3 install anthropic python-dotenv

Setup:
  Add ANTHROPIC_API_KEY to your .env file
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Hashtag stacks by month — update the CURRENT_MONTH variable below
HASHTAG_STACKS = {
    1: "#ailearning #codingjourney #learnpython #techjourneybeginners #aiengineering #codingfromzero #pythonlearning #aiforbeginners #techjourney2026 #buildingindaylight",
    2: "#ailearning #codingjourney #learnpython #techjourneybeginners #aiengineering #codingfromzero #pythonlearning #aiforbeginners #techjourney2026 #buildingindaylight",
    3: "#machinelearning #llm #artificialintelligence #aitools #techcareer #mlproject #aiproject #deeplearning #openai #anthropic",
    4: "#machinelearning #llm #artificialintelligence #aitools #techcareer #mlproject #aiproject #deeplearning #openai #anthropic",
    5: "#aijob #techjobs2026 #aiengineerjobs #softwareengineer #techjobsearch #portfolioproject #github #aiportfolio #devcareer",
    6: "#aijob #techjobs2026 #aiengineerjobs #softwareengineer #techjobsearch #portfolioproject #github #aiportfolio #devcareer #hireme",
}

# UPDATE THIS each month
CURRENT_MONTH = 1

def generate_caption(hook: str, bullet_points: list[str], cta: str) -> str:
    """Generate a caption using Claude."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""You are writing an Instagram caption for an AI learning journey account.
The creator is learning AI engineering from zero coding experience and documenting the process.
Tone: honest, relatable, direct. Not corporate. Not inspirational-quote style.

Hook (first line of Reel): {hook}

Key points from the video:
{chr(10).join(f'- {p}' for p in bullet_points)}

Requested CTA: {cta}

Write a caption that:
1. First line restates the hook as a punchy statement (not a question)
2. 2-3 short lines with the key points (no hashtags yet)
3. One blank line
4. The CTA
5. Three dots on their own line: ...
6. Nothing else — no hashtags (those are added separately)

Keep it under 150 words total. Sound like a real person, not a marketer."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text

def main():
    print("=== Caption Generator ===\n")

    hook = input("What's your Reel hook (first 1-3 seconds)?\n> ").strip()

    print("\nEnter your bullet points (press Enter twice when done):")
    bullets = []
    while True:
        line = input(f"Point {len(bullets)+1}: ").strip()
        if not line:
            if bullets:
                break
            continue
        bullets.append(line)

    print("\nWhat's your CTA? (e.g. 'Follow for week 2 update' or 'Comment AI for the full plan')")
    cta = input("> ").strip()

    print("\nGenerating caption...\n")
    caption = generate_caption(hook, bullets, cta)
    hashtags = HASHTAG_STACKS.get(CURRENT_MONTH, HASHTAG_STACKS[1])

    print("=" * 50)
    print("READY TO COPY:\n")
    print(caption)
    print()
    print(hashtags)
    print("=" * 50)

    # Save to file so you can copy it later
    with open("last-caption.txt", "w") as f:
        f.write(caption + "\n\n" + hashtags)
    print("\nAlso saved to: scripts/last-caption.txt")

if __name__ == "__main__":
    if not ANTHROPIC_API_KEY:
        print("Error: Missing ANTHROPIC_API_KEY in .env file.")
        print("Get your key at: https://console.anthropic.com/")
        exit(1)
    main()
