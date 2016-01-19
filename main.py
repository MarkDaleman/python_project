import sqlite3
import matplotlib.pyplot as plt
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from math import log
import numpy as np
from onetweet import getOneTweet


#Variables that contains the user credentials to access Twitter API
access_token = "579994863-7kUav4vqVupLe45MQdhCXhu8Y2d7sXq3ut739BvN"
access_token_secret = "akQE3RjdptslhRJw7HZagWhMtoxvkZoUSNNQeO2rBDYQr"
consumer_key = "BXwPemXe8UB9cVEDmymRjawre"
consumer_secret = "7OIv98yOr4Ep3vCJpR3XdSMW3wcDfGURbvWvVmwwuBKg6KIE7C"


def getTweets():
    print("Tweets aan het verzamelen...")
    # Achterlijk groot getal
    maxTweets = 2100
    # Op welke hashtag gaan we zoeken
    searchQuery = 'nederland'
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
        tweets = (tweet.source)
        c.execute('INSERT INTO source VALUES(?)', (tweets,))
        tweets = (tweet.created_at.hour)
        c.execute('INSERT INTO hour VALUES(?)', (tweets,))
    # Database wijzigingen opslaan
    conn.commit()
    print("Database is up to date met de laatste tweets")

def clearTweetTabel():
    # Python laten verbinden met de Sqlite database en leegmaken
    conn = sqlite3.connect('engels.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS tweets")
    c.execute("CREATE TABLE tweets (text TEXT);")
    c.execute("DROP TABLE IF EXISTS source")
    c.execute("CREATE TABLE source (source TEXT);")
    c.execute("DROP TABLE IF EXISTS hour")
    c.execute("CREATE TABLE hour (hour NUMERIC);")

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
    # Zorgen dat de database kan verbinden
    conn = sqlite3.connect('engels.db')
    c = conn.cursor()

    # Alle tweets verzamelen en door de textblob gooien
    tweetDatabase = conn.execute("SELECT * from tweets");
    for row in tweetDatabase:
        alleTweets = TextBlob(row[0])

        ## DEBUG
        # print(alleTweets.sentiment.polarity)

        c.execute("INSERT INTO analyse VALUES(?)", (alleTweets.sentiment.polarity,))
        conn.commit()
    # Alles gelukt ? even de gebruiker laten weten
    print("Database is up to date met analysegegevens")

    # Hoeveel tweets zijn er ?
    tweetAll = conn.execute("SELECT COUNT(*) FROM analyse")
    for row in tweetAll:
        tweetAll = row

    # Hoeveel negatieve tweets zijn er ?
    tweetNegatief = conn.execute("SELECT COUNT(*) FROM analyse WHERE analyse < 0.0")
    for row in tweetNegatief:
        tweetNegatief = row

    # Hoeveel positieve tweets zijn er ?
    tweetPositief = conn.execute("SELECT COUNT(*) FROM analyse WHERE analyse > 0.0")
    for row in tweetPositief:
        tweetPositief = row

    # Hoeveel neutrale tweets zijn er ?
    tweetNeutraal = conn.execute("SELECT COUNT(*) FROM analyse WHERE analyse = 0.0")
    for row in tweetNeutraal:
        tweetNeutraal = row

    tweetAlles = conn.execute("SELECT * FROM analyse")
    for row in tweetAlles:
        tweetAlles = row

    ## DEBUGGEN TIJD EN AANTAL TWEETS
    getTijdAantal = conn.execute("SELECT hour FROM hour GROUP BY hour")
    rowTijd = getTijdAantal.fetchall()
    #print(rowTijd)
    getTijdUur = conn.execute("SELECT COUNT(hour) FROM hour GROUP BY hour")
    rowAantal = getTijdUur.fetchall()
    #print(rowUren)


    getTweetUur = conn.execute("SELECT hour, COUNT(hour) FROM hour GROUP BY hour ORDER BY hour")
    getTijdInformatie = getTweetUur.fetchall()
    #print(BlaBla)

    #print(', '.join(map(str, tweetAlles)))
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
    plt.show();

    x_val = [x[0] for x in getTijdInformatie]
    y_val = [x[1] for x in getTijdInformatie]

    print(x_val)
    plt.plot(x_val,y_val)
    plt.plot(x_val,y_val,'or')
    plt.show()


    #hour=(rowTijd);
    #aantal_tweets=(rowAantal);

    #plt.plot_date(x=hour, y=aantal_tweets)
    #plt.show()



if __name__ == '__main__':
    # handig om te debuggen om te kijken waar de tweet uit bestaat
    #getOneTweet("StarWars")
    #clearAnalyseTabel()
    #clearTweetTabel()
    #getTweets()

    analyseTweets()






