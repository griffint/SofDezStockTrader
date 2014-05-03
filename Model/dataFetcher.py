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
    #this qeureys the SQL database for all stock data
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



def industryTickers(tickerSym):
    """This function takes as input a industry represented in our database.
        It then returns a list of ticker symbols of all the stocks in that
        industry"""
    with open('NYSEindustries.csv','rb') as f:
        reader = csv.reader(f)
        reader.next()
        tickersList = []
        industryDict = {}
        next(reader)
        for row in reader:
            
            if str((row[4].split('/'))[0]) not in industryDict:
                industryDict[str((row[4].split('/'))[0])] = []
                industryDict[str((row[4].split('/'))[0])].append(str((row[1].split('/'))[0]))
            else:
                industryDict[str((row[4].split('/'))[0])].append(str((row[1].split('/'))[0]))
        
        for key in industryDict:
            if tickerSym in industryDict[key]:
                tickersList = industryDict[key]
                
        tickersList.remove(tickerSym)
        return tickersList
        
def internetData(tickerSym):
    """takes as input a ticker as a string outputs dictionary with sequential
    lists of prices and volumes"""
    outputDict = {}
    tempDict = get_historical_prices_list(tickerSym,'2009-05-03','2014-05-03')
    outputDict['Volumes']=tempDict['Volume']
    outputDict['Prices']=tempDict['Price']
    return outputDict

    


#To get today's data, run get_current_data -- it's from griffstockquote and tested

if __name__=='__main__':
    print internetData('T')
