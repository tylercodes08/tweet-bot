import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tweepy
import random
import os, json
from dotenv import load_dotenv
import time

max_delay_seconds = 3 * 3600
delay = random.randint(0, max_delay_seconds)

print(f"Sleeping for {delay // 60} minutes and {delay % 60} seconds...")
time.sleep(delay)

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

# Flatten and clean all extras from all rows
all_extras_global = [
    tag.strip()
    for row in data
    for tag in row.get("Extra", "").split(",")
    if tag.strip()
]

# Remove duplicates
all_extras_global = list(set(all_extras_global))

# Loop through rows to find the next unposted tweet
for i, row in enumerate(data):
    if str(row["Posted"]).strip().upper() != "TRUE":
        tweet_text = row["Tweet Text"]
        hashtag = row.get("Hashtags", "").strip()

        # Remove the main hashtag from extras to avoid duplication
        filtered_extras = list(set(all_extras_global) - {hashtag})

        # Randomly select exactly 2 extras if possible
        if len(filtered_extras) >= 2:
            selected_extras = random.sample(filtered_extras, k=2)
        else:
            selected_extras = []  # If less than 2 available, use nothing

        # Always include the main hashtag
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
