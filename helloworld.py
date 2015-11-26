import sqlite3
import tweepy
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "579994863-7kUav4vqVupLe45MQdhCXhu8Y2d7sXq3ut739BvN"
access_token_secret = "akQE3RjdptslhRJw7HZagWhMtoxvkZoUSNNQeO2rBDYQr"
consumer_key = "BXwPemXe8UB9cVEDmymRjawre"
consumer_secret = "7OIv98yOr4Ep3vCJpR3XdSMW3wcDfGURbvWvVmwwuBKg6KIE7C"


# This is the listener, resposible for receiving data
class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        #print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    query = 'nederland'
    max_tweets = 3500
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]

    # DB connectie openen
    conn = sqlite3.connect('tweets.db')
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS tweets")
    c.execute("CREATE TABLE tweets (text TEXT);")
    count = 0

    for tweet in searched_tweets:
        print("voor de query")
        ## Zo genereren dat er alleen text in het veld komt
        voorbeeld = (tweet.text)
        print (voorbeeld)
        c.execute('INSERT INTO tweets VALUES(?)', (voorbeeld,))
        print("na de query")
        count +1
        print(count)
        if count > 1000:
            time.sleep(10)
            count = 0
    conn.commit()
    print("na de commit")


    #stream = tweepy.Stream(auth, l)
    #stream.filter(track=['programming'])

