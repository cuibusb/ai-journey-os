"""
follower-tracker.py
-------------------
Pulls your Instagram follower count via the Graph API
and writes it to progress.json so your dashboard auto-updates.

Run this once a day:
  python3 follower-tracker.py

Requirements:
  pip3 install requests python-dotenv

Setup:
  1. Copy setup.env.example to .env
  2. Fill in IG_ACCOUNT_ID and IG_ACCESS_TOKEN
"""

import requests
import json
import os
from datetime import date
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
IG_ACCOUNT_ID = os.getenv("IG_ACCOUNT_ID")
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")

def get_follower_count():
    """Fetch current follower count from Instagram Graph API."""
    url = f"https://graph.instagram.com/{IG_ACCOUNT_ID}"
    params = {
        "fields": "followers_count,media_count",
        "access_token": IG_ACCESS_TOKEN
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code} — {response.text}")
        return None

    data = response.json()
    return {
        "followers": data.get("followers_count", 0),
        "posts": data.get("media_count", 0)
    }

def update_progress_json(followers, posts):
    """Write follower count to progress.json for the dashboard."""
    progress_path = "../progress.json"

    # Read existing progress.json
    if os.path.exists(progress_path):
        with open(progress_path, "r") as f:
            progress = json.load(f)
    else:
        progress = {}

    # Update Instagram section
    progress["instagram"] = {
        "followers": followers,
        "posts": posts,
        "last_updated": str(date.today()),
        "target": 10000
    }

    # Save back
    with open(progress_path, "w") as f:
        json.dump(progress, f, indent=2)

    print(f"Updated progress.json — Followers: {followers} | Posts: {posts}")

def log_daily_count(followers):
    """Append today's count to a history CSV for charts."""
    log_path = "follower-history.csv"
    today = str(date.today())

    # Create header if file is new
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write("date,followers\n")

    # Append today's row
    with open(log_path, "a") as f:
        f.write(f"{today},{followers}\n")

    print(f"Logged: {today} — {followers} followers")

if __name__ == "__main__":
    if not IG_ACCOUNT_ID or not IG_ACCESS_TOKEN:
        print("Error: Missing IG_ACCOUNT_ID or IG_ACCESS_TOKEN in .env file.")
        print("Copy setup.env.example to .env and fill in your credentials.")
        exit(1)

    print("Fetching Instagram stats...")
    result = get_follower_count()

    if result:
        update_progress_json(result["followers"], result["posts"])
        log_daily_count(result["followers"])
        print("Done.")
    else:
        print("Failed to fetch data. Check your credentials in .env")
