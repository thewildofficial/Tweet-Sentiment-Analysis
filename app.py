print("Loading Twitter Analysis bot..")
from flask import Flask,render_template,request
import tweepy
import os
from dotenv import load_dotenv
from pyembed.core import PyEmbed
import backend
import collections
import sys

load_dotenv()

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)
 
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

def authenticate():

    return tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret= API_SECRET,
        access_token = ACCESS_TOKEN,
        access_token_secret= ACCESS_TOKEN_SECRET
    )


@app.route('/')
def analysepage():
    return render_template("webpage.html")
@app.route('/result',methods=["GET","POST"])
def result():
    if request.method == "POST":
        embed = None
        tweet_sentiment = None
        author_sentiment = None
        reply_sentiment = None
        link = request.form.to_dict()["linkinput"]
        id = link.split("/status/",1)[1]
        try:
            embed = str(PyEmbed().embed(link))
        except: pass
        tweet = client.get_tweet(id,tweet_fields=["text","conversation_id"],user_fields=["name"])
        text = str(tweet.data["text"])
        conversation_id = str(tweet.data["conversation_id"])
 
        
        tweet_sentiment = backend.tweet_to_sentiment([text])[0]
        replies = client.search_recent_tweets(query= f"conversation_id:{conversation_id}")
        replies_text = []
        for tweet in replies.data: replies_text.append(tweet.data["text"])
        reply_sentiment = backend.tweet_to_sentiment(replies_text)
        reply_frequency = dict(collections.Counter(reply_sentiment))
        print(reply_frequency
) 
        if (max(reply_frequency["POSITIVE"],reply_frequency["NEGATIVE"]) == reply_frequency["POSITIVE"]):
            reply_sentiment = "POSITIVE"
        
        else: reply_sentiment =  "NEGATIVE"
    

    return render_template("webpage.html",embed=embed,tweet_sentiment=tweet_sentiment, reply_sentiment = reply_sentiment)

if __name__ == "__main__":
    client = authenticate()
    app.run(debug=True,port=5000)