import pandas as pd
from . import models

def save_data_from_csv(file_path):
    data = pd.read_csv(file_path)
    for index, row in data.iterrows():
        tweet = Tweet(
            created_at=row['created_at'],
            tweet_id=row['id_str'],
            full_text=row['full_text'],
            truncated=row['truncated'],
            display_text_range=row['display_text_range'],
            # Add other fields from the CSV file to the Amerix model
        )
        tweet.save()

if __name__ == "__main__":
    save_data_from_csv("C:/Users/Admin/Desktop/Django/leanman/amerix_tweets.csv")
    