import tweepy
import time
import json
from config import settings 
import pandas as pd 

class ScrapeTweets:
    def __init__(self, username):
        self.username = username
        self.output_file = f"{self.username}_tweets.txt"
        self.requests_per_window = 900
        self.window_length_sec = 15 * 60
        self.count = 0

    def authenticate_twitter_api(self):
        auth = tweepy.OAuthHandler(settings.api_key, settings.api_key_secret)
        auth.set_access_token(settings.access_token, settings.access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api
    

    def scrape_tweets(self, api):
        backoff_time = 1  # Initial backoff time in seconds
        with open(self.output_file, "a", encoding="utf-8") as file:
            for tweet in tweepy.Cursor(api.user_timeline, screen_name=self.username, tweet_mode="extended").items():
                try:
                    if hasattr(tweet, "retweeted_status"):  # Skip retweets
                        continue

                    if "extended_tweet" in tweet._json:
                        full_text = tweet._json["extended_tweet"]["full_text"]
                        tweet.full_text = full_text
                    else:
                        full_text = tweet.full_text

                    # Convert tweet object to JSON string
                    tweet_json = json.dumps(tweet._json)

                    # Save tweet JSON string to file
                    file.write(f"{tweet_json}\n")
                    self.count += 1
                    print(f"Tweet {self.count}:")

                    backoff_time = 1  # Reset backoff time after a successful scrape
                except ConnectionResetError as e:
                    print("ConnectionResetError occurred. Retrying in", backoff_time, "seconds...")
                    time.sleep(backoff_time)
                    backoff_time *= 2  # Increase backoff time exponentially for subsequent reconnection attempts
                    continue
                except Exception as e:
                    print("An exception occurred:", e)
                    continue
    import pandas as pd

    def json_to_csv(self):
        # Read JSON file into a Pandas DataFrame
        df = pd.read_json(self.output_file, lines=True)

        csv_file = f"{self.output_file.split('.')[0]}.csv"
        # Save DataFrame to CSV file
        df.to_csv(csv_file, index=False)


    def main(self):
        api = self.authenticate_twitter_api()
        while True:
            try:
                self.scrape_tweets(api)
                break  # Scraping complete, exit the loop
            except tweepy.TweepyException as e:
                print("Error: ", e)
                time.sleep(self.window_length_sec)


if __name__ == "__main__":
    username = "amerix"
    scrape = ScrapeTweets(username)
    scrape.main()