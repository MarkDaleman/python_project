# Bestandsnaam: main.py
# Auteur: Mark Daleman
# Student: 1089446
# Versie: 2.0

import analyse
import matplotlib
matplotlib.use("TkAgg") # Deze gebruiken anders crasht matplotlib icm met Tkinter
import matplotlib.pyplot as plt
from tkinter import *
import tkinter.messagebox as mbox


def PieChart():
    # Figure even als fig neerzetten, dit zodat we hem aan kunnen spreken met fig.xx
    fig = plt.figure()
    # Het venster van een titel voorzien
    fig.canvas.set_window_title('Piechart')
    # Pie chart weergeven met de waardes van de tweets.
    labels = 'Neutraal', 'Positief', 'Negatief'
    sizes = [(int((analyse.tweetNeutraal()[0] * 100) / analyse.tweetAll()[0])),
             (int((analyse.tweetPositief()[0] * 100) / analyse.tweetAll()[0])),
             (int((analyse.tweetNegatief()[0] * 100) / analyse.tweetAll()[0]))]
    # Welke kleuren gaan we gebruiken voor de grafiek
    colors = ['yellow', 'green', 'red']
    # Geef aan of 1 van de 3 vlakken er een beetje moet uitspringen
    # In dit geval gaat de groene, positieve vlak een beetje naar buiten
    explode = (0, 0.1, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=False, startangle=90)
    # Teken de grafiek.
    plt.show();


def TimeLine():
    fig = plt.figure()
    fig.canvas.set_window_title('Tijdlijn')
    x_val = [x[0] for x in analyse.getTijdInformatie()]
    y_val = [x[1] for x in analyse.getTijdInformatie()]
    plt.plot(x_val,y_val)
    plt.plot(x_val,y_val,'or')
    def OnClick(event):
        print(round(event.xdata, 2), round(event.ydata, 2))
        window = Tk()
        window.wm_withdraw()
        mbox.showinfo('Aantal tweets op geselecteerde tijd' ,round(event.ydata, 2))
    cid_up = fig.canvas.mpl_connect('button_press_event', OnClick)
    plt.show()


def DisplayWindow():
    root = Tk()
    root.wm_title("Druk op een knop voor een grafiek")
    root.geometry('{}x{}'.format(400, 200))
    button1 = Button(root, text = 'Plot Mood', command = PieChart)
    button2 = Button(root, text = 'Plot Tijdlijn', command = TimeLine)
    button1.pack(pady=20, padx = 20)
    button2.pack(pady=20, padx = 20)

    root.mainloop()

def testFunctie():

    print(analyse.getTijdInformatie())

if __name__ == '__main__':
    #analyse.createTabel()
    #analyse.getTweets()
    testFunctie()
    #DisplayWindow()