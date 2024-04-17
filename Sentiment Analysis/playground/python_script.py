import pandas as pd
import requests
import subprocess
from django.template import loader
from django.http import HttpResponse
from collections import Counter
import re

def analysis(data):
    model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    hf_token = "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"
    API_URL = "https://api-inference.huggingface.co/models/" + model
    headers = {"Authorization": "Bearer %s" % (hf_token)}
    
    payload = dict(inputs=data, options=dict(wait_for_model=True))
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def extract_sentiment_words(tweet):
    # Remove mentions, hashtags, and URLs
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet)
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r'http\S+', '', tweet)

    # Tokenize and lowercase the tweet
    words = tweet.lower().split()

    # Remove stopwords or other non-meaningful words
    stopwords = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'from', 'with', 'of', 'about', 'by', 'as', 'i', 'you', 'he', 'she', 'it', 'we', 'they']
    meaningful_words = [word for word in words if word not in stopwords]

    return meaningful_words

def get_sentiment_data(tweets):
    all_words = []
    tweets_analysis = []
    user_view = []
    for tweet in tweets:
        try:
            sentiment_result = analysis(tweet)[0]
            top_sentiment = max(sentiment_result, key=lambda x: x['score'])
            sentiment_label = top_sentiment['label']
            tweets_analysis.append(sentiment_label)
            user_view.append({'tweet': tweet, 'sentiment': top_sentiment['label']})
            all_words.extend(extract_sentiment_words(tweet))
        except Exception as e:
            print(e)
    print(user_view)
    #df = pd.DataFrame(tweets_analysis)
    #sentiment_counts = df.groupby(['sentiment']).size().to_dict()
    #return df, sentiment_counts

    # Calculate overall sentiment
    overall_sentiment = max(set(tweets_analysis), key=tweets_analysis.count)

    # Calculate percentage of each sentiment
    sentiment_counts = {label: tweets_analysis.count(label)/len(tweets_analysis) * 100 for label in set(tweets_analysis)}

    # Find top 3 most used sentiment words
    #top_sentiments = pd.Series(tweets_analysis).value_counts().head(3).to_dict()
    top_sentiments = Counter(all_words).most_common(5)

    return overall_sentiment, sentiment_counts, top_sentiments

def render_sentiment_results(tweets, hashtag):
    #df, sentiment_counts = get_sentiment_data(tweets)
    overall_sentiment, sentiment_counts, top_sentiments = get_sentiment_data(tweets)
    #print(overall_sentiment)
    #print(sentiment_counts)
    #print(top_sentiments)
    #template = loader.get_template('sentiment_results.html')
    context = {
        #'tweets': df.to_dict(orient='records'),
        'overall_sentiment' : overall_sentiment,
        'sentiment_counts': sentiment_counts,
        'top_sentiments' : top_sentiments,
        'hashtag': hashtag,
    }
    #return template.render(context)
    return context
    #return HttpResponse(template.render(context, request))

def main(hashtag, fdate):
    # Example tweets (you can fetch these based on the hashtag and date)
    tweets = ["The more I use @salesforce the more I dislike it. It's slow and full of bugs.",
           "That’s what I love about @salesforce. That it’s about relationships and about caring about people and it’s not only about business and money. Thanks for caring about #TrailblazerCommunity",
          "Coming Home: #Dreamforce Returns to San Francisco for 20th Anniversary. Learn more: http://bit.ly/3AgwO0H via @Salesforce"
          ]
    '''tweets = open("C:\\Users\\jaika\\Downloads\\elon.json", "r")
    file_path = 'data.csv'  # Path to your file
    try:
        with open(file_path, 'r') as file:
            tweets = file.read()
        #return HttpResponse(content)
    except FileNotFoundError:
        return HttpResponse("File not found")
    print(tweets)'''
    # Render sentiment results
    html_output = render_sentiment_results(tweets, hashtag)
    #print(html_output)
    return html_output
#main("jai","jai")
    



