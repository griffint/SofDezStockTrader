# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 01:19:46 2014

@author: griffin
"""
from stocks import *
from ystockquote.griffstockquote import *
#stuff from griffstockquote may require libraries--tested an working though

def dataFetcher(tickerSymbol):
    """
    This function takes as input a ticker symbol as a string, for example 'AAPL'
    It returns a dictionary where the keys are the statistic and the values
    are time series lists of that statistic. This function returns all available 
    data for a given ticker symbol.
    """
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
    return outputDict

def getIndustry(tickerSymbol):
    """ This function takes a ticker symbol and outputs the industry"""
    temp =  Stock.query.filter_by(ticker=tickerSymbol).first()
    return temp.industry    

def industryTickers(industryName):
    """This function takes as input a industry represented in our database.
        It then returns a list of ticker symbols of all the stocks in that
        industry"""
        
    temp = Stock.query.filter_by(industry=industryName).all()
    tickerList = []
    for i in temp:
        
        if i.ticker not in tickerList:
            tickerList.append(str(i.ticker))
    return tickerList
    
#To get today's data, run get_current_data -- it's from griffstockquote and tested

if __name__=='__main__':
    print get_current_data('AAPL')
    