import tweepy
from config import settings


auth = tweepy.OAuthHandler(settings.api_key, settings.api_key_secret)
auth.set_access_token(settings.access_token , settings.access_token_secret)

api = tweepy.API(auth)

username = "gurnelius"

user = api.get_user(screen_name=username)
total_tweets = user.statuses_count

print(f"The user {username} has sent {total_tweets} tweets to Twitter.")
