from scrape import ScrapeTweets
# Usage example
input_file = 'amerix_tweets.json'
output_file = 'amerix_tweets.csv'

scrape = ScrapeTweets('amerix')
scrape.json_to_csv()
