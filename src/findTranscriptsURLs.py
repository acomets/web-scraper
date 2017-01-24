"""
Author: Antoine Comets
Date: 12/04/2016

This file contains the source code for findTranscriptURLs which finds the URLs of transcripts
from earnings calls of a company, taking as input the company ticker and the number of transcripts to look at.

"""

from bs4 import BeautifulSoup
from urlparse import urljoin
from login import loginSA
from os.path import join

def findTranscriptsURLs(session, ticker, n):
    
    userHeader = {"Referer": "http://seekingalpha.com/",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    
    url = urljoin('http://seekingalpha.com/symbol/', '/'.join([ticker, "earnings", "transcripts"]))
    r = session.get(url, headers = userHeader)
    
    soup = BeautifulSoup(r.content, 'html.parser')
    
    transcripts = []
    transcriptsAll = soup.find_all("a", {"sasource":"qp_analysis"})
    for transcript in transcriptsAll:
        if "Earnings" in transcript.text and "Transcript" in transcript.text:
            transcripts.append(transcript.get("href"))
    #print("Tickers About are: {0}".format(', '.join(tickersAbout)))
    transcriptsStr = ', '.join(transcripts)
    
    return transcripts[:n]


if __name__ == "__main__":
    session = loginSA()[1]
    ticker = "AMZN"
    findTranscriptsURLs(session, ticker, 4)

