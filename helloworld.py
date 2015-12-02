import sqlite3
import matplotlib.pyplot as plt
import tweepy
from tweepy import OAuthHandler


#Variables that contains the user credentials to access Twitter API
access_token = "579994863-7kUav4vqVupLe45MQdhCXhu8Y2d7sXq3ut739BvN"
access_token_secret = "akQE3RjdptslhRJw7HZagWhMtoxvkZoUSNNQeO2rBDYQr"
consumer_key = "BXwPemXe8UB9cVEDmymRjawre"
consumer_secret = "7OIv98yOr4Ep3vCJpR3XdSMW3wcDfGURbvWvVmwwuBKg6KIE7C"


def getTweets():
    # Achterlijk groot getal
    maxTweets = 10000
    # Op welke hashtag gaan we zoeken
    searchQuery = 'Nederland'
    print("Table is being filled now. With tweets")
    auth = OAuthHandler(consumer_key, consumer_secret)
    # Zorgen dat de API kan verbinden
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # Python laten verbinden met de Sqlite database
    conn = sqlite3.connect('tweets.db')
    c = conn.cursor()
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=searchQuery).items(maxTweets)]
    for tweet in searched_tweets:
        voorbeeld = (tweet.text)
        c.execute('INSERT INTO tweets VALUES(?)', (voorbeeld,))
    # Database wijzigingen opslaan
    conn.commit()
    print("Database is up to date! ^.^")


def clearTabel():
    # Python laten verbinden met de Sqlite database en leegmaken
    conn = sqlite3.connect('tweets.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS tweets")
    c.execute("CREATE TABLE tweets (text TEXT);")
    print("Table tweet is dropped and created a new one")

def countTweets():
    conn = sqlite3.connect('tweets.db')
    print ("Opened database successfully");
    cursor = conn.execute("SELECT COUNT(*) FROM tweets");
    for row in cursor:
        print ("Aantal Tweets = ", row[0])
    print ("Operation done successfully, closing connection");
    conn.close();

def drawSomething():
    plt.plot([1,2,3,4])
    plt.ylabel('some numbers')
    plt.show()

if __name__ == '__main__':
    countTweets();
    drawSomething();






