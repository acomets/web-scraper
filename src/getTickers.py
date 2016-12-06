"""
Author: Antoine Comets
Date: 12/04/2016

This file contains the source code of getTicker, which returns the tickers of all the S&P 500 companies
belonging to the relevant industry sector given as input.

"""

import pandas as pd
from os.path import join

def getTickers(sector):
    file = join("..", "data/constituents.csv")
    data = pd.read_csv(file)
    companies = data[data["Sector"] == sector]
    return list(companies["Symbol"])

