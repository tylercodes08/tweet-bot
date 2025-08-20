# Daily Tweet Bot

This bot posts daily tweets from a Google Sheet. Each tweet can include hashtags and extra phrases, and the bot tracks which tweets have already been posted.

## How It Works

- Reads tweets from a Google Sheet with columns: `Tweet Text`, `Hashtags`, `Extra`, and `Posted`.
- Adds hashtags and optional extra phrases to each tweet.
- Posts the tweet to Twitter using the API.
- Marks the tweet as posted in the sheet to avoid duplicates.
- Can randomize posting time within a fixed hour for variety.
- Works locally or via a scheduled GitHub Actions workflow.

## Notes

- Requires a Google service account for sheet access and Twitter API credentials.
- The workflow can be manually triggered or run on a schedule.
- It is best to use this with GitHub Actions so that you don't have to always log on to your computer
