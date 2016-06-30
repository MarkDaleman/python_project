import sqlite3
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


# Variables that contains the user credentials to access Twitter API
# Consumer keys and access tokens, used for OAuth
consumer_key = 'IeU3EOZjfUDtP9XxqS14OeAw2'
consumer_secret = '5380ntb89KwLqX3uS3clzagstS2NigJji0YVy4HSsXxFUAOynA'
access_token = '737235484200587264-Z7BhnzrZt9cBMhtLwqrNein1ZNZ42nq'
access_token_secret = 'EbnZQvQhs0fedk6R7uhJkPVymyiV6RnvK7vKUub2pogGF'

#Globale variabelen vaststellen
global conn
conn = sqlite3.connect('tweets.db')
global c
c = conn.cursor()


def createTabel():
    conn.execute('''CREATE TABLE TweetOpslag
       (ID INT PRIMARY KEY     NOT NULL,
       Tweet           TEXT    NOT NULL,
       Source            TEXT     NOT NULL,
       Timestamp       TEXT,
       Analyse         FLOAT);''')
    print("Table created successfully")


def getTweets():
    print("Tweets aan het verzamelen...")
    # Geef hier het aantal Tweets op wat je wilt verzamelen
    maxTweets = 2000 # moet naar 10.000
    # Op welke hashtag gaan we zoeken
    searchQuery = "trump"
    auth = OAuthHandler(consumer_key, consumer_secret)
    # Zorgen dat de API kan verbinden
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # Python laten verbinden met de Sqlite database
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=searchQuery, language="en").items(maxTweets)]
    # Tweet resultaten opslaan in de database
    for tweet in searched_tweets:
        ID = (tweet.id)
        Tweet = (tweet.text)
        Source = (tweet.source)
        Hour = (tweet.created_at.hour)
        Analyse = TextBlob(tweet.text)
        Test2 = (Analyse.sentiment.polarity)
        print(Test2)
        params = (ID, Tweet, Source, Hour, Test2)
        conn.execute("INSERT INTO TweetOpslag (ID,Tweet,Source,Timestamp,Analyse) \
      VALUES (?,?,?,?,?)", params);
    # Database wijzigingen opslaan
    conn.commit()
    print("Database is up to date met de laatste tweets")

def tweetAll():
    # Hoeveel tweets zijn er ?
    try:
        tweetAll = conn.execute("SELECT COUNT(Analyse) FROM TweetOpslag")
    except sqlite3.ProgrammingError as error:
        print(error)
    for row in tweetAll:
        tweetAll = row
        return tweetAll

def tweetNegatief():
    # Hoeveel negatieve tweets zijn er ?
    try:
        tweetNegatief = conn.execute("SELECT COUNT(Analyse) FROM TweetOpslag WHERE Analyse < 0.0")
    except sqlite3.ProgrammingError as error:
        print(error)
    for row in tweetNegatief:
        tweetNegatief = row
        return tweetNegatief

def tweetPositief():
    # Hoeveel positieve tweets zijn er ?
    try:
        tweetPositief = conn.execute("SELECT COUNT(Analyse) FROM TweetOpslag WHERE Analyse > 0.0")
    except sqlite3.ProgrammingError as error:
        print(error)
    for row in tweetPositief:
        tweetPositief = row
        return tweetPositief

def tweetNeutraal():
    # Hoeveel neutrale tweets zijn er ?
    tweetNeutraal = conn.execute("SELECT COUNT(Analyse) FROM TweetOpslag WHERE Analyse = 0.0")
    for row in tweetNeutraal:
        tweetNeutraal = row
        return tweetNeutraal

def getTijdInformatie():
    # Hoeveel tweets zijn er per uur ?
    try:
        getTweetUur = conn.execute("SELECT Timestamp, COUNT(Timestamp) FROM TweetOpslag GROUP BY Timestamp ORDER BY Timestamp")

    except sqlite3.ProgrammingError as error:
        print(error)
    getTijdInformatie = getTweetUur.fetchall()
    return getTijdInformatie

