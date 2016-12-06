"""
Author: Antoine Comets
Date: 12/05/2016

This file contains the source code for the GUI which then calls all other functions.
It uses the tkinter framework.

"""

from Tkinter import *
from os.path import join
import pandas as pd
from login import loginSA
from getTickers import getTickers
from findTranscriptsURLs import findTranscriptsURLs
from relevantExtracts import relevantExtracts
from pdfgen import pdfgen


file = join("..", "data/constituents.csv")
spx = pd.read_csv(file)
sectors = set(spx['Sector'])

class App:

    def __init__(self, master):

        topframe = Frame(master)
        topframe.pack(side=TOP)

        self.sectorLabel = Label(
            topframe, text="Industry sector:"
            )
        self.sectorLabel.grid(row=0, column=0)

        self.sector = StringVar(master)
        self.sectorOptionMenu = apply(OptionMenu, (topframe, self.sector) + tuple(sectors))
        self.sectorOptionMenu.grid(row=0, column=1, sticky='ew')
        
        self.keywordsLabel = Label(
            topframe, text="Enter keywords (separated by ', '):"
            )
        self.keywordsLabel.grid(row=1, column=0)
        
        self.keywords = StringVar(master)
        self.keywordsEntry = Entry(
            topframe, textvariable=self.keywords, width=80
            )
        self.keywordsEntry.grid(row=1, column=1)
        
        bottomframe = Frame(master)
        bottomframe.pack(side=BOTTOM)
        
        self.goButton = Button(
            bottomframe, text="Go", command=self.okbutton
            )
        self.goButton.pack(side=LEFT)
        
        self.closeButton = Button(
            bottomframe, text="Close", command=self.close
            )
        self.closeButton.pack(side=RIGHT)

    def okbutton(self):
        session = loginSA()[1]
        sector = self.sector.get()
        keywords = self.keywords.get()
        tickers = getTickers(sector)
        keywords = keywords.split(', ')
        print ', '.join(keywords)
        n_last_quarters = 4
        
        relevant_extracts = []
        
        for ticker in tickers:
            urls = findTranscriptsURLs(session, ticker, n_last_quarters)
            relevant_extracts += relevantExtracts(session, urls, keywords)
       
        pdfgen(relevant_extracts, sector, keywords)
    
    def close(self):
        root.destroy()

root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below

