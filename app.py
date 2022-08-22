from flask import Flask,render_template,request
import tweepy
import os
from dotenv import load_dotenv
from pyembed.core import PyEmbed

load_dotenv()

app = Flask(__name__)

BEARER_TOKEN = os.getenv("BEARER_TOKEN")

def authenticate():
    return tweepy.Client(bearer_token=BEARER_TOKEN)


@app.route('/')
def analysepage():
    return render_template("webpage.html")
@app.route('/result',methods=["GET","POST"])
def result():
    if request.method == "POST":
        embed = None
        link = request.form.to_dict()["linkinput"]
        id = link.split("/status/",1)[1]
        try:
            embed = str(PyEmbed().embed(link))
        except: pass
        tweet = client.get_tweet(id)
    return render_template("webpage.html",embed=embed)

if __name__ == "__main__":
    client = authenticate()
    app.run(debug=True,port=5000)