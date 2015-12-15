import sqlite3
import matplotlib.pyplot as plt
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import numpy as np



#Variables that contains the user credentials to access Twitter API
access_token = "579994863-7kUav4vqVupLe45MQdhCXhu8Y2d7sXq3ut739BvN"
access_token_secret = "akQE3RjdptslhRJw7HZagWhMtoxvkZoUSNNQeO2rBDYQr"
consumer_key = "BXwPemXe8UB9cVEDmymRjawre"
consumer_secret = "7OIv98yOr4Ep3vCJpR3XdSMW3wcDfGURbvWvVmwwuBKg6KIE7C"


def getTweets():
    # Achterlijk groot getal
    maxTweets = 500
    # Op welke hashtag gaan we zoeken
    searchQuery = 'happy'
    auth = OAuthHandler(consumer_key, consumer_secret)
    # Zorgen dat de API kan verbinden
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # Python laten verbinden met de Sqlite database
    conn = sqlite3.connect('engels.db')
    c = conn.cursor()
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=searchQuery, language="en").items(maxTweets)]
    for tweet in searched_tweets:
        tweets = (tweet.text)
        c.execute('INSERT INTO tweets VALUES(?)', (tweets,))
    # Database wijzigingen opslaan
    conn.commit()
    print("Database is up to date met de laatste tweets")

def clearTweetTabel():
    # Python laten verbinden met de Sqlite database en leegmaken
    conn = sqlite3.connect('engels.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS tweets")
    c.execute("CREATE TABLE tweets (text TEXT);")
    print("Tweet tabel is verwijderd en opnieuw aangemaakt")

def clearAnalyseTabel():
    # Python laten verbinden met de Sqlite database en leegmaken
    conn = sqlite3.connect('engels.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS analyse")
    c.execute("CREATE TABLE analyse (analyse NUMERIC);")
    print("analyse tabel is verwijderd en opnieuw aangemaakt")

def analyseTweets():
    print("Ik ga nu analyseren")
    conn = sqlite3.connect('engels.db')
    c = conn.cursor()

    tweetDatabase = conn.execute("SELECT * from tweets");
    for row in tweetDatabase:
        alleTweets = TextBlob(row[0])

        ## DEBUG
        # print(alleTweets.sentiment.polarity)

        c.execute("INSERT INTO analyse VALUES(?)", (alleTweets.sentiment.polarity,))
        conn.commit()
    print("Database is up to date met analysegegevens")
    tweetAll = conn.execute("SELECT COUNT(*) FROM analyse")
    for row in tweetAll:
        tweetAll = row

    tweetNegatief = conn.execute("SELECT COUNT(*) FROM analyse WHERE analyse < 0.0")
    for row in tweetNegatief:
        tweetNegatief = row

    tweetPositief = conn.execute("SELECT COUNT(*) FROM analyse WHERE analyse > 0.0")
    for row in tweetPositief:
        tweetPositief = row

    tweetNeutraal = conn.execute("SELECT COUNT(*) FROM analyse WHERE analyse = 0.0")
    for row in tweetNeutraal:
        tweetNeutraal = row

    # DEBUG PROCENTEN
    #print (int((tweetNeutraal[0] * 100) / tweetAll[0])) #aantal Procent wat Neutraal is
    #print (int((tweetPositief[0] * 100) / tweetAll[0])) #aantal Procent wat Positief is
    #print (int((tweetNegatief[0] * 100) / tweetAll[0])) #aantal Procent wat Negatief is

    # Pie chart weergeven met de waardes van de tweets.
    labels = 'Neutraal', 'Positief', 'Negatief'
    sizes = [(int((tweetNeutraal[0] * 100) / tweetAll[0])), (int((tweetPositief[0] * 100) / tweetAll[0])), (int((tweetNegatief[0] * 100) / tweetAll[0]))]
    colors = ['yellow', 'green', 'red']
    explode = (0, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.show()
if __name__ == '__main__':
    clearAnalyseTabel()
    clearTweetTabel()
    getTweets()
    analyseTweets()






