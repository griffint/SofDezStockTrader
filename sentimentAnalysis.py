# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 12:45:40 2014

@author: svaughan
"""


import random
from pattern.web import *
from pattern.en import *
from urllib2 import Request, urlopen
from urllib import urlencode


def sentiment_to_text(company):
    #set up Twitter search engine
    t = Twitter(language='en')
    
    #initalize variables
    string = []
    output = []
    totSentiment = []
    k=0
    
    #Check that there is a result, and use that as reference tweet id later
    for tweet in t.search(company, start=None, count=1):
        i = tweet.id
        
    #loop that runs untilyou can't pull more data from Twitter
    running = True
    while running:
        try:
            string.append('') #initalize variable string that stores all the tweets
            totSentimentTemp = 0 #initialize temporary sentiment variable
            count = 1.0
            i = unicode(int(i)-250000000000000*(k)) #look further back in twitter's archive
            if t.search(company, start=i, count=1)==[]:
                raise SystemExit("Sorry, your company doesn't have any recent tweets") #break the try except statement
            for tweet in t.search(company, start=i, count=100):
                print tweet.text
                print tweet.date
                date = unicode_tweet_date_reformat(tweet.date)
                x = sentiment(tweet.text)
                print x
                print "\n"
                totSentimentTemp = (totSentimentTemp*(count-1)+x[0])/count
                count+=1
                string[k] += tweet.text
            k+=1 
            output.extend([date, totSentimentTemp])
        except:
            running = False
    return output
        
def unicode_tweet_date_reformat(unicodeDate):
    month = unicodeDate[4:7]
    date = unicodeDate[8:10]
    hour = unicodeDate[11:13]
    date = str(date)
    if month == 'Jan':
        month = 1
    if month == 'Feb':
        month = 2
    if month == 'Mar':
        month = 3
    if month == 'Apr':
        month = 4
    if month == 'May':
        month = 5
    if month == 'Jun':
        month = 6
    if month == 'Jul':
        month = 7
    if month == 'Aug':
        month = 8
    if month == 'Sep':
        month = 9
    if month == 'Oct':
        month = 10
    if month == 'Nov':
        month = 11
    if month == 'Dec':
        month = 12
    date = int(date)
    hour = int(hour)
    return (month, date, hour)
    

def _request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    req = Request(url)
    resp = urlopen(req)
    content = resp.read().decode().strip()
    return content
    
def get_company_name(symbol):
    return _request(symbol, 'n')
    

if __name__ == '__main__':
    print sentiment_to_text("walmart")