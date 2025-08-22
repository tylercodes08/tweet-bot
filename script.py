import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tweepy
import random
import os, json
from dotenv import load_dotenv
import time


# Random minute within the hour (0–59)
random_minute = random.randint(0, 59)

# Wait until that minute before posting
current_minute = time.gmtime().tm_min
sleep_seconds = (random_minute - current_minute) * 60
if sleep_seconds > 0:
    time.sleep(sleep_seconds)

# Load Twitter API credentials from environment variables
load_dotenv()
client = tweepy.Client(
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

with open("service_account.json", "r") as f:
    creds = json.load(f)


# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

# Use the JSON key file from GitHub Actions secret or local file
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
gc = gspread.authorize(creds)

# Open your Google Sheet by name
sheet = gc.open("tweet_sheet").sheet1 

# Fetch all rows as dictionaries
data = sheet.get_all_records()

# Loop through rows to find the next unposted tweet
for i, row in enumerate(data):
    if str(row["Posted"]).strip().upper() != "TRUE":
        tweet_text = row["Tweet Text"]
        hashtag = row.get("Hashtags", "")
        extras = [tag.strip() for tag in row.get("Extra", "").split(",") if tag.strip()]

        # Remove the main hashtag from extras to avoid duplication
        filtered_extras = list(set(extras) - {hashtag})

        # Randomly select up to 2 extras (if available)
        selected_extras = random.sample(filtered_extras, k=min(3, len(filtered_extras)))

        # Build the final hashtag string
        all_hashtags = [hashtag] + selected_extras
        tweet_text += "\n\n" + " ".join(all_hashtags)


        try:
            client.create_tweet(text=tweet_text)
            print("Tweet posted:", tweet_text)

            # Mark this tweet as posted in Google Sheet
            sheet.update_cell(i + 2, 2, "TRUE")  # row+2 because header is row 1, Posted is column 2
        except tweepy.TweepyException as e:
            print("Error posting tweet:", e)
        break
else:
    print("No tweets left to post!")
