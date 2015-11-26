import sqlite3
import tweepy
from time import sleep
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

#Variables that contains the user credentials to access Twitter API
access_token = "579994863-7kUav4vqVupLe45MQdhCXhu8Y2d7sXq3ut739BvN"
access_token_secret = "akQE3RjdptslhRJw7HZagWhMtoxvkZoUSNNQeO2rBDYQr"
consumer_key = "BXwPemXe8UB9cVEDmymRjawre"
consumer_secret = "7OIv98yOr4Ep3vCJpR3XdSMW3wcDfGURbvWvVmwwuBKg6KIE7C"


class StdOutListener(StreamListener):
    def on_data(self, data):
        print("Ik krijg data terug!")
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    query = 'Germany'
    max_tweets = 10000
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

    ## DB connectie openen
    conn = sqlite3.connect('tweets.db')
    c = conn.cursor()
    ## Drop table als al bestaat, en maak daarna een nieuwe aan
    c.execute("DROP TABLE IF EXISTS tweets")
    c.execute("CREATE TABLE tweets (text TEXT);")
    ## Counter op 0 zetten zodat ik straks een sleep kan gebruiken
    count = 0

    for tweet in searched_tweets:
        ## Zo genereren dat er alleen text in het veld komt
        voorbeeld = (tweet.text)
        ## Knal de data naar de database
        c.execute('INSERT INTO tweets VALUES(?)', (voorbeeld,))
        #Counter
        count += 1
        if count >= 500:
            print("Sleeping.. Zz")
            sleep(30)
            count = 0
    conn.commit()
    print("Database is geupdatet met alle tweets")


