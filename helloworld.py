import sqlite3

import tweepy
from tweepy import OAuthHandler


#Variables that contains the user credentials to access Twitter API
access_token = "579994863-7kUav4vqVupLe45MQdhCXhu8Y2d7sXq3ut739BvN"
access_token_secret = "akQE3RjdptslhRJw7HZagWhMtoxvkZoUSNNQeO2rBDYQr"
consumer_key = "BXwPemXe8UB9cVEDmymRjawre"
consumer_secret = "7OIv98yOr4Ep3vCJpR3XdSMW3wcDfGURbvWvVmwwuBKg6KIE7C"


def getTweets():
    maxTweets = 10000 # Some arbitrary large number
    searchQuery = 'Nederland'  # this is what we're searching for
    print("Tabel wordt nu gevuld met Twitter berichten")
    auth = OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    conn = sqlite3.connect('tweets.db')
    c = conn.cursor()


    searched_tweets = [status for status in tweepy.Cursor(api.search, q=searchQuery).items(maxTweets)]
    for tweet in searched_tweets:
        voorbeeld = (tweet.text)
        c.execute('INSERT INTO tweets VALUES(?)', (voorbeeld,))
    conn.commit()
    print("Database is geupdatet met alle tweets")


def clearTabel():
    conn = sqlite3.connect('tweets.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS tweets")
    c.execute("CREATE TABLE tweets (text TEXT);")
    print("Tabel tweets is leeg en nieuwe is aangemaakt")

if __name__ == '__main__':

print("I'm working!")







