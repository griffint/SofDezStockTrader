# -*- coding: utf-8 -*-
"""
Created on Sun May  4 16:48:04 2014

@author: griffin
"""

from stocks import *
from ystockquote.griffstockquote import *


def predictionTesting(tickerSym, predPrice):
    """Takes as input a ticker symbol and the predicted price from the algorithm
    and compares it to the next day. Prints the actual price and error"""
    
    tempDict = get_historical_prices_list('AAP','2014-05-02','2014-05-02')
    actualPrice = float((tempDict['Price'])[0])
    error = (predPrice-actualPrice)/actualPrice
    print "actual price = "+ str(actualPrice)
    print "error = " +  str(error*100) + "%"
    
    
if __name__=='__main__':
    predictionTesting('AAP',126)