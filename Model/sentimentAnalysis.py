# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 12:45:40 2014

@author: svaughan
"""

from pattern.web import *
from pattern.en import *
from urllib2 import Request, urlopen
from symbolToName import *


def twitter_sentiment(company):
    #set up Twitter search engine
    t = Twitter(language='en')
    
    #initalize variables
    output = {}
    k=0
    dates = []
    
    #Check that there is a result, and use that as reference tweet id later
    for tweet in t.search(company, start=None, count=1):
        i = tweet.id
        
    #loop that runs untilyou can't pull more data from Twitter
    running = True
    while running:
        try:
            i = unicode(int(i)-1000000000000000) #look further back in twitter's archive
            if t.search(company, start=i, count=1)==[]:
                raise SystemExit("Sorry, your company doesn't have any recent tweets") #break the try except statement
            for tweet in t.search(company, start=i, count=100):
                date = unicode_tweet_date_reformat(tweet.date)
                dates.append(date)
                totSentimentTemp = sentiment(tweet.text)
                output[date] = totSentimentTemp[0]
        except:
            running = False
    return [output, dates]
    
def twitter_sentiment_average(company):
    #set up Twitter search engine
    t = Twitter(language='en')
    
    #initalize variables
    output = {}
    dates = []
    
    #Check that there is a result, and use that as reference tweet id later
    for tweet in t.search(company, start=None, count=1):
        i = tweet.id
        print i
        
    #loop that runs untilyou can't pull more data from Twitter
    running = True
    while running:
        try:
            count = 0
            totSentiment = 0
            if t.search(company, start=i, count=1)==[]:
                raise SystemExit("Sorry, your company doesn't have any recent tweets") #break the try except statement
            for tweet in t.search(company, start=i, count=100):
                count+=1
                date = unicode_tweet_date_reformat(tweet.date)
                totSentimentTemp = sentiment(tweet.text)
                totSentiment += totSentimentTemp[0]
            dates.append(date)
            output[date] = totSentiment/count
            i = unicode(int(i)-1000000000000000) #look further back in twitter's archive
        except:
            running = False
    return [output, dates]
        
def unicode_tweet_date_reformat(unicodeDate):
    month = unicodeDate[4:7]
    date = unicodeDate[8:10]
    hour = unicodeDate[11:13]
    minute = unicodeDate[14:16]
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
    minute = int(minute)
    return (month, date, hour, minute)
    
def reformatted_date_subtraction(current_date, prev_date):
    hoursAgo = current_date[2] - prev_date[2]
    rollover = 0
    if hoursAgo < 0:
        hoursAgo += 24
        rollover = 1
    daysAgo = current_date[1]-prev_date[1]-rollover
    if daysAgo < 0:
        if prev_date[0] == 1 or prev_date[0] == 3 or prev_date[0] == 5 or prev_date[0] == 7 or prev_date[0] == 8 or prev_date[0] == 10 or prev_date[0] == 12:
            daysAgo+=31
        elif prev_date[0] == 2:
            daysAgo+=28
        else:
            daysAgo+=30
    hoursAgo+=24*daysAgo
    return hoursAgo
    

if __name__ == '__main__':
    print twitter_sentiment('walmart')
    print twitter_sentiment_average('walmart')