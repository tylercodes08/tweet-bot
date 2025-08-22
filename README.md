# 🐦 Daily Tweet Bot

This bot automatically posts a tweet every day using content from a **Google Sheet**. It's perfect for scheduling tweets ahead of time without needing to manually log in to Twitter/X.

---

## ✅ What It Does

- Reads tweets from a **Google Sheet** that you control.
- Each row in the sheet includes:
  - **Tweet Text**: The main message.
  - **Hashtags**: Hashtag that the tweet must include.
  - **Extra**: Extra hashtags.
  - **Posted**: Marks whether the tweet has already been sent.
- Combines the text, hashtags, and extras into a full tweet.
- Posts the tweet to **Twitter/X** using the API.
- Marks the tweet as **Posted** in the sheet, so it doesn’t post the same one again.
- Optionally **randomizes** the posting time within a set hour (to look more natural).
- Can run on your computer or automatically every day using **GitHub Actions**.

---

## 🛠 Requirements

You’ll need:

1. **Python 3.8+**
2. A **Google Service Account** with access to your sheet (explained below).
3. **Twitter API credentials** (for posting the tweets).
4. A **GitHub account** to automate the bot with GitHub Actions.

---

## 📊 How to Set Up the Google Sheet

Create a Google Sheet with these columns (first row = headers):

| Tweet Text        | Hashtags        | Extra            | Posted |
|------------------|-----------------|------------------|--------|
| Example tweet... | #Python, #Bot   | 🔥 Don't miss it | FALSE  |

- **Tweet Text**: Your main tweet content.
- **Hashtags**: Any hashtag that the tweet must include.
- **Extra**: Any extra hashtags to append (optional).
- **Posted**: Leave as `FALSE` for new tweets. The bot changes it to `TRUE` after posting.

---

## 🔐 Setup: Google Sheets Access

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable the **Google Sheets API**.
3. Create a **Service Account** and download the JSON key file.
4. Share your Google Sheet with the **email address** of the service account (with Editor access).
5. Copy json file into repository secrets.

---

## 🔑 Setup: Twitter/X API Access

1. Go to [Twitter Developer Portal](https://developer.twitter.com/).
2. Create an App and generate:
   - API Key  
   - API Secret Key  
   - Access Token  
   - Access Token Secret  
3. Store these as repository secrets.

---

# ⚙️ Automating the Daily Tweet Bot with GitHub Actions

You can run your daily tweet bot **automatically every day** using **GitHub Actions**. This lets you schedule tweets without needing to keep your computer on or run Python manually.

---

## 📦 What Is GitHub Actions?

GitHub Actions lets you **run code on a schedule** (like a daily cron job) from your GitHub repository. This is perfect for automating things like tweeting daily from a Google Sheet.

---

## 🧾 Prerequisites

Make sure your bot works **locally** before setting up GitHub Actions. You’ll need:

- Your working `tweet_bot.py` script.
- `requirements.txt` with your dependencies.
- Your `credentials.json` (from your Google Service Account).
- Your Twitter and Google credentials (to be saved as GitHub secrets).

---

## 🪄 Step-by-Step: Set Up GitHub Actions

### 1. Add the Workflow File

Create a file in your project at:

.github/workflows/tweet.yml

### 2. Add Your Secrets

Hopefully you've already stored your credentials as repository secrets. If not, you can do so by going to your repo's settings, naviagating to Secrets and Variables → Actions → New repository secret

## ✅ Test It
You can trigger the workflow manually:
1. Go to the Actions tab in your repo.
2. Click on the "Daily Tweet Bot" workflow.
3. Click "Run workflow" to test it instantly.

## 🧠 Notes
- Cron jobs use UTC time — adjust accordingly for your timezone.
- Logs for each run are available in the Actions tab for debugging.