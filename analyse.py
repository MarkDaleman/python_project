import sqlite3 # nodig voor de Database
import tweepy # nodig voor het ophalen van Tweets
from tweepy import OAuthHandler # zorgen voor de verbinding
from textblob import TextBlob # voor het analyseren van de Tweets
import unittest






# Variables that contains the user credentials to access Twitter API
# Consumer keys and access tokens, used for OAuth
consumer_key = 'IeU3EOZjfUDtP9XxqS14OeAw2'
consumer_secret = '5380ntb89KwLqX3uS3clzagstS2NigJji0YVy4HSsXxFUAOynA'
access_token = ''
access_token_secret = 'EbnZQvQhs0fedk6R7uhJkPVymyiV6RnvK7vKUub2pogGF'

#Globale variabelen vaststellen
global conn
global c
# Verbinden met de Database



conn = sqlite3.connect('tweets.db')
c = conn.cursor()


# Functie op de Database aan te maken
# Maak nieuwe database aan met de naam TweetOpslag
# Tabel met de naam Tweet -> TEXT
# Tabel met de naam Source -> TEXT
# Tabel met TimeStamp -> TEXT
# Tabel voor de Analyse -> FLOAT
def createTabel():
    conn.execute('''CREATE TABLE TweetOpslag
       (ID INT PRIMARY KEY     NOT NULL,
       Tweet           TEXT    NOT NULL,
       Source            TEXT     NOT NULL,
       Timestamp       TEXT,
       Analyse         FLOAT);''')
    print("Table created successfully")

# Functie die Tweets verzameld
# Doet alle opgehaalde tweets in een sqlite database
# MaxTweets = Aantal op te halen Tweets
# Searchquery is voor welke hashtag je wilt zoeken
def getTweets():
    print("Tweets aan het verzamelen...")
    maxTweets = 1000
    searchQuery = "python"
    auth = OAuthHandler(consumer_key, consumer_secret)
    # Zorgen dat de API kan verbinden
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=searchQuery, language="en").items(maxTweets)]
    # Tweet resultaten opslaan in de database
    for tweet in searched_tweets:
        ID = (tweet.id) # ID van de Tweet opslaan
        Tweet = (tweet.text) # Text van de Tweet opslaan
        Source = (tweet.source) # Vanaf wat is het verzonden
        Hour = (tweet.created_at.hour) # Welk uur is het getweet ?
        Analyse = TextBlob(tweet.text) #E erst maken we er een textblob van
        Test2 = (Analyse.sentiment.polarity) # Daarna doen we er een sentiment over heen voor de analyse
        params = (ID, Tweet, Source, Hour, Test2) # Parameters voor de Database query voor het invoeren van de gegevens
        conn.execute("INSERT INTO TweetOpslag (ID,Tweet,Source,Timestamp,Analyse) \
      VALUES (?,?,?,?,?)", params);
    # Database wijzigingen opslaan
    conn.commit()


# Functie aantal tweets totaal
# Return aantal opgehaalde tweets
def tweetAll():
    try:
        tweetAll = conn.execute("SELECT COUNT(Analyse) FROM TweetOpslag")
    except sqlite3.ProgrammingError as error:
        print(error)
    for row in tweetAll:
        tweetAll = row
        return tweetAll

# Functie voor het aantal negatieve tweets
# Return het aantal negatieve tweets
def tweetNegatief():
    try:
        tweetNegatief = conn.execute("SELECT COUNT(Analyse) FROM TweetOpslag WHERE Analyse < 0.0")
    except sqlite3.ProgrammingError as error:
        print(error)
    for row in tweetNegatief:
        tweetNegatief = row
        return tweetNegatief

# Functie voor het aantal positieve tweets
# Return het aantal positieve tweets
def tweetPositief():
    try:
        tweetPositief = conn.execute("SELECT COUNT(Analyse) FROM TweetOpslag WHERE Analyse > 0.0")
    except sqlite3.ProgrammingError as error:
        print(error)
    for row in tweetPositief:
        tweetPositief = row
        return tweetPositief

# Functie voor het aantal neutrale tweets
# Return het aantal neutrale tweets
def tweetNeutraal():
    tweetNeutraal = conn.execute("SELECT COUNT(Analyse) FROM TweetOpslag WHERE Analyse = 0.0")
    for row in tweetNeutraal:
        tweetNeutraal = row
        return tweetNeutraal

# Functie voor het ophalen aantal tweets per uur
# Return het uur, per aantal tweets [uur, tweets]
def getTijdInformatie():
    try:
        getTweetUur = conn.execute("SELECT Timestamp, COUNT(Timestamp) FROM TweetOpslag GROUP BY Timestamp ORDER BY Timestamp")
    except sqlite3.ProgrammingError as error:
        print(error)
    getTijdInformatie = getTweetUur.fetchall()
    return getTijdInformatie

# Om te debuggen of vragen ook echt negatief of positief of neutraal zijn
# dit kan je testen met de tests.py file
def text_analyse(sentence):
    # split words to array
    Analyse = TextBlob(sentence)
    Mood = (Analyse.sentiment.polarity)
    return Mood