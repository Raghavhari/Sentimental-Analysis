import pandas as pd
import requests
import subprocess
from django.template import loader
from django.http import HttpResponse

def analysis(data):
    model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    hf_token = "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"
    API_URL = "https://api-inference.huggingface.co/models/" + model
    headers = {"Authorization": "Bearer %s" % (hf_token)}
    
    payload = dict(inputs=data, options=dict(wait_for_model=True))
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def get_sentiment_data(tweets):
    tweets_analysis = []
    for tweet in tweets:
        try:
            sentiment_result = analysis(tweet)[0]
            top_sentiment = max(sentiment_result, key=lambda x: x['score'])
            sentiment_label = top_sentiment['label']
            tweets_analysis.append({'tweet': tweet, 'sentiment': sentiment_label})
        except Exception as e:
            print(e)
    
    df = pd.DataFrame(tweets_analysis)
    sentiment_counts = df.groupby(['sentiment']).size().to_dict()
    
    return df, sentiment_counts

def render_sentiment_results(tweets, hashtag):
    df, sentiment_counts = get_sentiment_data(tweets)
    #template = loader.get_template('sentiment_results.html')
    context = {
        'tweets': df.to_dict(orient='records'),
        'sentiment_counts': sentiment_counts,
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
    
    # Render sentiment results
    html_output = render_sentiment_results(tweets, hashtag)
    return html_output
    



