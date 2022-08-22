import pandas as pd
positive_tweets = pd.read_json("data/corpora/twitter_samples/positive_tweets.json",lines=True)
print(positive_tweets.head())