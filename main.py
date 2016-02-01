import sqlite3
import matplotlib.pyplot as plt
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from onetweet import oneTweet
import tkinter
import tkinter.messagebox as mbox


#Variables that contains the user credentials to access Twitter API
access_token = "579994863-7kUav4vqVupLe45MQdhCXhu8Y2d7sXq3ut739BvN"
access_token_secret = "akQE3RjdptslhRJw7HZagWhMtoxvkZoUSNNQeO2rBDYQr"
consumer_key = "BXwPemXe8UB9cVEDmymRjawre"
consumer_secret = "7OIv98yOr4Ep3vCJpR3XdSMW3wcDfGURbvWvVmwwuBKg6KIE7C"


def getTweets():
    print("Tweets aan het verzamelen...")
    # Geef hier het aantal Tweets op wat je wilt verzamelen
    maxTweets = 5000
    # Op welke hashtag gaan we zoeken
    searchQuery = 'instagram'
    auth = OAuthHandler(consumer_key, consumer_secret)
    # Zorgen dat de API kan verbinden
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # Python laten verbinden met de Sqlite database
    conn = sqlite3.connect('engels.db')
    c = conn.cursor()
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=searchQuery, language="en").items(maxTweets)]
    # Tweet resultaten opslaan in de database
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

def clearTweetDatabase():
    # Python laten verbinden met de Sqlite database en leegmaken
    conn = sqlite3.connect('engelss.db')
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
        c.execute("INSERT INTO analyse VALUES(?)", (alleTweets.sentiment.polarity,))
        conn.commit()

    # Alles gelukt ? even de gebruiker laten weten
    print("Database is up to date met analysegegevens")

    # Hoeveel tweets zijn er ?
    try:
        tweetAll = conn.execute("SELECT COUNT(*) FROM analyse")
    except sqlite3.ProgrammingError as error:
        print(error)
    for row in tweetAll:
        tweetAll = row

    # Hoeveel negatieve tweets zijn er ?
    try:
        tweetNegatief = conn.execute("SELECT COUNT(*) FROM analyse WHERE analyse < 0.0")
    except sqlite3.ProgrammingError as error:
        print(error)
    for row in tweetNegatief:
        tweetNegatief = row

    # Hoeveel positieve tweets zijn er ?
    try:
        tweetPositief = conn.execute("SELECT COUNT(*) FROM analyse WHERE analyse > 0.0")
    except sqlite3.ProgrammingError as error:
        print(error)
    for row in tweetPositief:
        tweetPositief = row

    # Hoeveel neutrale tweets zijn er ?
    tweetNeutraal = conn.execute("SELECT COUNT(*) FROM analyse WHERE analyse = 0.0")
    for row in tweetNeutraal:
        tweetNeutraal = row

    # Laten we alles selecteren
    try:
     tweetAlles = conn.execute("SELECT * FROM analyse")
    except sqlite3.ProgrammingError as error:
        print(error)
    for row in tweetAlles:
        tweetAlles = row

    # Hoeveel tweets zijn er per uur ?
    try:
        getTweetUur = conn.execute("SELECT hour, COUNT(hour) FROM hour GROUP BY hour ORDER BY hour")
    except sqlite3.ProgrammingError as error:
        print(error)
    getTijdInformatie = getTweetUur.fetchall()

    print("Ik ga nu een Pie chart tekenen over de stemming van de mensen")
    # Pie chart weergeven met de waardes van de tweets.
    labels = 'Neutraal', 'Positief', 'Negatief'
    sizes = [(int((tweetNeutraal[0] * 100) / tweetAll[0])), (int((tweetPositief[0] * 100) / tweetAll[0])), (int((tweetNegatief[0] * 100) / tweetAll[0]))]
    colors = ['yellow', 'green', 'red']
    explode = (0, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
					autopct='%1.1f%%', shadow=False, startangle=90)
    plt.show();

    fig = plt.figure()
    print("Ik ga nu een Timeline plotten, hoeveel tweets er per uur zijn getweet")
    # Draw a timeline
    x_val = [x[0] for x in getTijdInformatie]
    y_val = [x[1] for x in getTijdInformatie]
    plt.plot(x_val,y_val)
    plt.plot(x_val,y_val,'or')
    def OnClick(event):
        print(round(event.xdata, 2), round(event.ydata, 2))
        window = tkinter.Tk()
        window.wm_withdraw()
        mbox.showinfo('Aantal tweets op geselecteerde tijd' ,round(event.ydata, 2))
    cid_up = fig.canvas.mpl_connect('button_press_event', OnClick)
    plt.show()


if __name__ == '__main__':
    # handig om te debuggen om te kijken waar de tweet uit bestaat
    oneTweet("instagram")

    clearAnalyseTabel()
    clearTweetDatabase()
    getTweets()

    analyseTweets()






