"""
Author: Antoine Comets
Date: 12/04/2016

This file contains the source code for relevantExtracts which extracts excerpts from a list of earnings call
transcripts URLs given as input. The relevant excerpts contain keywords also passed as argument in a list.
Source: https://github.com/trinitybest/Web_Scraping_SeekingAlpha

"""

import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
from login import loginSA
import sys
import codecs
from time import sleep

def relevantExtracts(session, urls, keywords):
    #session = loginSA()[1]
    extracts = []

    userHeader = {"Referer": "http://seekingalpha.com/",
                  "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    
    for url in urls:
        displayoptions = {'part': 'single'}
        r = session.get(url, headers = userHeader, params = displayoptions)
        
        soup = BeautifulSoup(r.content, 'lxml')
        sleep(0.1)
        
        headline = soup.find_all("h1", {"itemprop":"headline"})
        title = headline[0].text if headline else 'Title missing'
        ###print("title: ", title)
    
        dateTime = soup.find_all("meta", {"property":"article:published_time"})
        date1 = dateTime[0].get("content") if dateTime else ''
        date2 = date1.split('T') if date1 else ''
        date = date2[0] if date2 else 'Date missing'
        time1 = date2[1:] if date2 else ''
        time2 = time1[0].split('Z') if time1 else ''
        time = time2[0] if time2 else 'Time missing'
        ###print("Date time is: {0} and {1}".format(date, time))
        
        
        bodyAll = soup.find_all("div", {"id":"a-body"})
        if bodyAll:
            bodyAll = bodyAll[0].text
            body = bodyAll.split("\n")
            for p in body:
                if list(set(p.split()) & set(keywords)) != []:
                    extracts.append({"title": title,
                                     "date": date,
                                     "time": time, 
                                     "bodyContent": p})
        else:
            extracts.append({"title": title,
                             "date": date,
                             "time": time, 
                             "bodyContent": "Unable to retrieve content from URL: " + url})
        #print(bodyAll)
        
    
        return extracts


if __name__ == "__main__":
    session = loginSA()[1]

