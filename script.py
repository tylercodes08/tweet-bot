import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tweepy
import random
import os
from dotenv import load_dotenv

# Load Twitter API credentials from environment variables
load_dotenv()
client = tweepy.Client(
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

with open("service_account.json", "w") as f:
    f.write(os.getenv("JSON"))

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
        hashtags = row.get("Hashtags", "")
        extras = row.get("Extra", "").split(",")  # extra hashtags or phrases

        # Add hashtags and two random extras if available
        random_extras = " ".join(random.sample(extras, min(2, len(extras)))) if extras else ""
        tweet_text += "\n\n" + hashtags + " " + random_extras

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
