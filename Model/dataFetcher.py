# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 01:19:46 2014

@author: griffin
"""
from stocks import *
from ystockquote.griffstockquote import *

#stuff from griffstockquote may require libraries--tested an working though

def internetData(tickerSymbol):
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
    
    for i in temp:
        prices.append(i.close)
        volumes.append(i.volume)
    print tickerSymbol
    print "prices length is " + str(len(prices))
    print "volumes length is " + str(len(volumes))
    outputDict = {'Prices':prices,'Volumes':volumes}
    return outputDict

def industryTickers(tickerSym):
    """This function takes as input a industry represented in our database.
       It then returns a list of ticker symbols of all the stocks in that
       industry"""
    temp = Stock.query.filter_by(ticker=tickerSym).first()
    industry1 = temp.industry
    print industry1
    #querys the SQL database for all the tickers with that industry
    subq = Stock.query.filter_by(industry=industry1).distinct(Stock.ticker).all()
    outputlist=[]
    for i in subq:
        outputlist.append(str(i.ticker))
    return outputlist


#this is all the internet pulling cdoe. I'm keeping it here incase we want to
#use it all again

#def industryTickers(tickerSym):
#    """This function takes as input a industry represented in our database.
#        It then returns a list of ticker symbols of all the stocks in that
#        industry"""
#        #uses a csv with all NYSE stocks and their industries
#    with open('NYSEindustries.csv','rb') as f:
#        reader = csv.reader(f)
#        reader.next()
#        tickersList = []
#        industryDict = {}
#        next(reader)
#        for row in reader:
#            #if the industry isn't a key in the dictionary, adds it and the 
#            #corresponding stock
#            if str((row[4].split('/'))[0]) not in industryDict:
#                industryDict[str((row[4].split('/'))[0])] = []
#                industryDict[str((row[4].split('/'))[0])].append(str((row[1].split('/'))[0]))
#            else:
#                #otherwise it adds the ticker to the corresponding industry
#                industryDict[str((row[4].split('/'))[0])].append(str((row[1].split('/'))[0]))
#        
#        for key in industryDict:
#            if tickerSym in industryDict[key]:
#                tickersList = industryDict[key]
#                
#        tickersList.remove(tickerSym)
#        return tickersList
#        
#def internetData(tickerSym):
#    """takes as input a ticker as a string outputs dictionary with sequential
#    lists of prices and volumes"""
#    outputDict = {}
#    tempDict = get_historical_prices_list(tickerSym,'2009-05-01','2014-05-01')
#    #the get_historical function is from griffstockquote
#    outputDict['Volumes']=tempDict['Volume']
#    outputDict['Prices']=tempDict['Price']
#    return outputDict

    


#To get today's data, run get_current_data -- it's from griffstockquote and tested

if (__name__ == "__main__"):
    print internetData('T')
