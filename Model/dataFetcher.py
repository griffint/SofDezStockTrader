# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 01:19:46 2014

@author: griffin
"""
from stocks import *


def dataFetcher(tickerSymbol):
    temp = Stock.query.filter_by(ticker=tickerSymbol).all()
    #init the lists to store data for output
    prices = []#closing price
    volumes = []
    shortInterests = []
    eps = []
    for i in temp:
        prices.append(i.close)
        volumes.append(i.volume)
        shortInterests.append(i.shortInterest)
        eps.append(i.eps)
    outputDict = {'ClosingPrices':prices,'DailyVolumes':volumes,'ShortInterests':shortInterests,'EarningsPerShare':eps}
    print outputDict
    
if __name__=='__main__':
    dataFetcher('AAPL')