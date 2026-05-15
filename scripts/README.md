# Scripts

Three automation scripts for the ai-journey project.

## Setup (do this once)

### 1. Install Python dependencies
```bash
pip3 install requests anthropic python-dotenv
```

### 2. Create your .env file
```bash
cp setup.env.example .env
```
Then open `.env` and fill in your credentials (see instructions below).

### 3. Add .env to .gitignore (IMPORTANT — keeps your keys safe)
```bash
echo "scripts/.env" >> ../.gitignore
echo "scripts/last-caption.txt" >> ../.gitignore
echo "scripts/follower-history.csv" >> ../.gitignore
```

---

## Scripts

### follower-tracker.py
Pulls your Instagram follower count and updates `progress.json`.

**Requires:** `IG_ACCOUNT_ID` + `IG_ACCESS_TOKEN` in `.env`
**Run:** `python3 follower-tracker.py` (once a day)

### caption-generator.py
Give it your hook + bullet points → get a ready-to-post caption.

**Requires:** `ANTHROPIC_API_KEY` in `.env`
**Run:** `python3 caption-generator.py`

### weekly-digest.py
Reads your latest `week-N.md` → generates a summary → saves to `digest.json`.

**Requires:** `ANTHROPIC_API_KEY` in `.env`
**Run:** `python3 weekly-digest.py` then `git add ../digest.json && git push`

---

## Getting Your Credentials

### Instagram Graph API (for follower-tracker.py)

Follow these steps in order:

**Step 1 — Switch to Creator account on Instagram**
- Instagram app → Profile → Menu (three lines) → Settings → Account → Switch to Professional Account → Creator

**Step 2 — Create a Facebook Page**
- facebook.com → Create → Page → give it any name (e.g. your Instagram handle)
- This is required by Meta — you don't need to use it for anything else

**Step 3 — Connect Instagram to the Facebook Page**
- Instagram app → Settings → Account → Linked Accounts → Facebook → connect the page you just made

**Step 4 — Create a Meta Developer App**
- Go to: developers.facebook.com/apps
- Click "Create App" → choose "Business" type
- Give it any name (e.g. "ai-journey-tracker")
- Add product: "Instagram Graph API"

**Step 5 — Get your Instagram Business Account ID**
- In your developer app: Tools → Graph API Explorer
- Select your app from the dropdown
- In the query box type: `me/accounts` → click Submit
- Copy the `id` field — that's your Page ID
- Then query: `{PAGE_ID}?fields=instagram_business_account` → copy that ID
- That's your `IG_ACCOUNT_ID`

**Step 6 — Get a long-lived access token**
- In Graph API Explorer: click "Generate Access Token"
- Select your app + your Facebook Page
- Check permissions: `instagram_basic`, `instagram_manage_insights`, `pages_show_list`
- Copy the token
- Exchange for long-lived token (valid 60 days) by running:
```bash
curl "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_TOKEN"
```
- Copy the `access_token` from the response → that's your `IG_ACCESS_TOKEN`

**Step 7 — Fill in .env**
```
IG_ACCOUNT_ID=1234567890
IG_ACCESS_TOKEN=EAABwzLixnjYBO...
```

### Anthropic API (for caption-generator.py and weekly-digest.py)
- Go to: console.anthropic.com
- Settings → API Keys → Create Key
- Copy the key → paste as `ANTHROPIC_API_KEY` in `.env`
- Cost: ~$0.001 per caption, ~$0.001 per digest. Nearly free.

---

## When to run each script

| Script | When | Command |
|--------|------|---------|
| follower-tracker.py | Every morning | `python3 follower-tracker.py` |
| weekly-digest.py | End of each week after filling week-N.md | `python3 weekly-digest.py` |
| caption-generator.py | Before posting a Reel | `python3 caption-generator.py` |
