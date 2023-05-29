from django.shortcuts import render, HttpResponse
import pandas as pd
import matplotlib
import re

# Set the backend to a non-interactive backend
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from .models import Tweet


csv_file_path = "C:/Users/Admin/Desktop/Django/leanman/amerix_tweets.csv"

def home(request):
    tweets = Tweet.objects.all()

    return render(request, "home/home.html", {'tweets': tweets, 'header': 'Latest Tweets'})

def masculinity_saturday(request):
    tweets = Tweet.objects.filter(full_text__contains='#MasculinitySaturday')
    context = {'tweets': tweets, 'header': 'Masculinity Saturday'}
    return render(request, "home/home.html", context)

def hashtag(request, hashtag=None):

    tweets_with_hashtags = Tweet.objects.filter(full_text__icontains='#')
    hashtags_set = set()
    for tweet in tweets_with_hashtags:
        hashtags = re.findall(r"#(\w+)", tweet.full_text)
        hashtags_set.update(hashtags)
    if hashtag == None:
        hashtag = list(hashtags_set)[0]
    tweets = Tweet.objects.filter(full_text__icontains=f'#{hashtag}')
    context = {'tweets': tweets, 'header':f"#{hashtag}", 'hashtags': hashtags_set}
    return render(request, 'home/hashtags.html', context)


def stats(request):
    tweets = Tweet.objects.all()
    return render(request, "home/stats.html", {'tweets': tweets, 'header': 'Tweet Stats'})

def popular(request):
     # Re
     # trieve the most liked tweets (e.g., top 5)
    popular_tweets = Tweet.objects.order_by('-favorite_count')

    context = {'tweets': popular_tweets, 'header': 'Popular Tweets'}
    return render(request, 'home/home.html', context)

def search(request):
    keyword = request.GET.get('keyword', '')  # Get the keyword from the query parameters
    
    # Filter tweets based on the keyword
    tweets = Tweet.objects.filter(full_text__icontains=keyword)
    
    context = {'tweets': tweets, 'keyword': keyword}
    return render(request, 'home/search.html', context)


def word_cloud(request):

    # Retrieve all tweets
    tweets = Tweet.objects.all()
    
    # Extract text from tweets
    text = ' '.join(tweet.full_text for tweet in tweets)
    
    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400).generate(text)

    # Render the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()

    # Save the word cloud to a temporary file
    image_path =  'static/images/wordcloud.png'
    plt.savefig(image_path)
    plt.close()
    context = {'wordcloud_img': image_path, 'header': 'Frequently used words'}
    return render(request, 'home/word_cloud.html', context)


# def remove_links(tweet_text):
#     # Regular expression pattern to match URLs
#     url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

#     # Remove URLs from the tweet text
#     cleaned_text = re.sub(url_pattern, '', tweet_text)

#     return cleaned_text


# def clean_tweets(request):
#     # Retrieve all tweets from the database
#     tweets = Tweet.objects.all()

#     # Clean and update each tweet
#     for tweet in tweets:
#         cleaned_text = remove_links(tweet.full_text)
#         tweet.full_text = cleaned_text
#         tweet.save()
#     return HttpResponse("Tweets Cleaned")

def save_data_from_csv(request, file_path=csv_file_path):
    data = pd.read_csv(file_path)
    for index, row in data.iterrows():
        tweet = Tweet(
            created_at=row['created_at'],
            id=row['id_str'],
            full_text=row['full_text'],
            retweet_count=row['retweet_count'],
            favorite_count=row['favorite_count']
        )
        print("Tweet index:", index)
        tweet.save()
    return HttpResponse("Saved to database")