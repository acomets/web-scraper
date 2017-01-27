"""
This file contains the source code to update our list of S&P 500 companies containing
their name, symbol and sector. It was found on the following git repo

Source: https://github.com/datasets/s-and-p-500-companies

"""

from bs4 import BeautifulSoup
import urllib2
import csv
from os import mkdir
from os.path import exists, join

datadir = join('..', 'data')
if not exists(datadir):
    mkdir(datadir)
source_page = urllib2.urlopen('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies').read()
soup = BeautifulSoup(source_page, 'lxml')
table = soup.find("table", { "class" : "wikitable sortable" })

# Fail now if we haven't found the right table
header = table.findAll('th')
if header[0].string != "Ticker symbol" or header[1].string != "Security":
    raise Exception("Can't parse wikipedia's table!")

# Retreive the values in the table
records = []
rows = table.findAll('tr')
for row in rows:
    fields = row.findAll('td')
    if fields:
        symbol = fields[0].string
        name = fields[1].string
        sector = fields[3].string
        records.append([symbol, name, sector])

header = ['Symbol', 'Name', 'Sector']
writer = csv.writer(open('../data/constituents.csv', 'w'), lineterminator='\n')
writer.writerow(header)
# Sorting ensure easy tracking of modifications
records.sort(key=lambda s: s[1].lower())
writer.writerows(records)    
