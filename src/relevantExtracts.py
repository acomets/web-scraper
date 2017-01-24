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
    
    for u in urls:
        url = urljoin("http://seekingalpha.com/", u)
        r = session.get(url, headers = userHeader)
        
        soup = BeautifulSoup(r.content, 'html.parser')
        
        try:
            title = soup.find_all("h1", {"itemprop":"headline"})[0].text
        except:
            print("Could not get title: ",url)
            title = ''
        ###print("title: ", title)
    
        dateTime = ''
        date = ''
        time = ''
        try:
            dateTime = soup.find_all("meta", {"property":"article:published_time"})[0]
            #time1 = dateTime.get("content")
            #time2 = dateTime.text
            date = dateTime.get("content").split('T')[0]
            time = dateTime.get("content").split('T')[1].split('Z')[0]
        except Exception as e:
            print("Could not get time: ", e)
        ###print("Date time is: {0} and {1}".format(date, time))
        
        try:
            bodyAll = soup.find_all("div", {"id":"a-body"})[0]
            bodyAll = bodyAll.text
            body = bodyAll.split("\n")
            for p in body:
                if list(set(p.split()) & set(keywords)) != []:
                    extracts.append({"title": title,
                                     "date": date,
                                     "time": time, 
                                     "bodyContent": p})
        except:
            print(url)
        #print(bodyAll)
        
    
        return extracts


if __name__ == "__main__":
    session = loginSA()[1]

