# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 16:13:27 2014

@author: sawyer
"""

import random
from pattern.web import *
from pattern.en import *
import numpy
import matplotlib
import math
import matplotlib.pylab as pyl
from urllib2 import Request, urlopen
from urllib import urlencode

def twitter_sentiment(company):
    #set up Twitter search engine
    t = Twitter(language='en')
    
    #initalize variables
    string = []
    output = []
    k=0
    
    #Check that there is a result, and use that as reference tweet id later
    for tweet in t.search(company, start=None, count=1):
        i = tweet.id
        current_date = unicode_tweet_date_reformat(tweet.date)
        
    #loop that runs until you can't pull more data from Twitter
    running = True
    while running:
        try:
            string.append('') #initalize variable string that stores all the tweets
            totSentimentTemp = 0 #initialize temporary sentiment variable
            count = 1.0
            i = unicode(int(i)-50000000000000*(k)) #look further back in twitter's archive
            if t.search(company, start=i, count=1)==[]:
                raise SystemExit("Sorry, your company doesn't have any recent tweets") #break the try except statement
            for tweet in t.search(company, start=i, count=100):
                date = tweet.date
                dateNumerical = unicode_tweet_date_reformat(tweet.date)
                hoursAgo = reformatted_date_subtraction(current_date, dateNumerical)
                x = sentiment(tweet.text)
                totSentimentTemp = (totSentimentTemp*(count-1)+x[0])/count
                count+=1
                string[k] += tweet.text
            k+=1 
            output.append([date, hoursAgo, totSentimentTemp])
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
    
def text_to_data(textfile):
    text = open(textfile, 'r')
    x=text.read()
    y = x.split(',')
    for i in range(len(y)):
        y[i]=y[i].translate(None, '[]\n')
        y[i]=float(y[i])
    return y
            
def _request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    req = Request(url)
    resp = urlopen(req)
    content = resp.read().decode().strip()
    return content
    
def get_company_name(symbol):
    return _request(symbol, 'n')

from flask import Flask, render_template, request, redirect
app = Flask(__name__)

email_addresses = []

@app.route('/', methods = ['POST', 'GET'])
def hello_world():
    return render_template('index.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    search = request.form['searchkey']
    timestep = request.form['timestep']
    print("The search is for '" + search + "'")
    print("The timestep is '" + timestep + "'")
    return redirect('/')
    
@app.route('/search', methods = ['POST', 'GET'])
def search():
    try:
        search = request.form['searchkey']
    except:
        return redirect('/')
    timestep = request.form['timestep']
    try:
        results = twitter_sentiment(get_company_name(search))
    except:
        return render_template('error.html')
    if results == []:
        return render_template('noresults.html')
    dates = []
    hours = []
    sentiments = []
    for entry in results:
        temp = entry[0]
        entry[0] = temp[0:16]
        dates.append(entry[0])
        hours.append(entry[1])
        sentiments.append(entry[2])
    pyl.plot(hours, sentiments, 'bo-')
    pyl.axis([-10, numpy.amax(hours)+10, numpy.amin(sentiments)-.2, numpy.amax(sentiments)+.2])
    pyl.xlabel('Hours Ago')
    pyl.ylabel('Sentiment')
    pyl.title('Sentiment Data')
    pyl.savefig('static/sentiment.png')
    pyl.clf()
    x=text_to_data('data.txt')
    y=text_to_data('predicteddata.txt')
    days=[]
    for i in range(len(y)):
        days.append(len(x)+i)
    pyl.plot(x, 'b', label='Past Stock Data')
    pyl.plot(days, y, 'r', label='Predicted Data')
    pyl.xlabel('Day')
    pyl.ylabel('Stock Price')
    pyl.title('Predicted Stock Price')
    pyl.legend(loc=2)
    pyl.savefig('static/data.png')
    pyl.clf()
    return render_template('sentiment.html', dates=dates, hours=hours, sentiments=sentiments, search=search)
    
if __name__ == "__main__":
    print get_company_name('goog')
    app.run()
    
