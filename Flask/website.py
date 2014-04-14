# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 16:13:27 2014

@author: sawyer
"""

import random
from pattern.web import *
from pattern.en import *

def sentiment_to_text(company):
    #set up Twitter search engine
    t = Twitter(language='en')
    
    #initalize variables
    string = []
    output = []
    k=0
    
    #Check that there is a result, and use that as reference tweet id later
    for tweet in t.search(company, start=None, count=1):
        i = tweet.id
        
    #loop that runs until you can't pull more data from Twitter
    running = True
    while running:
        try:
            string.append('') #initalize variable string that stores all the tweets
            totSentimentTemp = 0 #initialize temporary sentiment variable
            count = 1.0
            i = unicode(int(i)-100000000000000*(k)) #look further back in twitter's archive
            if t.search(company, start=i, count=1)==[]:
                raise SystemExit("Sorry, your company doesn't have any recent tweets") #break the try except statement
            for tweet in t.search(company, start=i, count=100):
                date = tweet.date
                x = sentiment(tweet.text)
                totSentimentTemp = (totSentimentTemp*(count-1)+x[0])/count
                count+=1
                string[k] += tweet.text
            k+=1 
            output.append([date, totSentimentTemp])
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

from flask import Flask, render_template, request, redirect
app = Flask(__name__)

email_addresses = []

@app.route('/', methods = ['POST'])
def hello_world():
    return render_template('index.html')

@app.route('/signup', methods = ['POST'])
def signup():
    search = request.form['searchkey']
    timestep = request.form['timestep']
    print("The search is for '" + search + "'")
    print("The timestep is '" + timestep + "'")
    return redirect('/')
    
@app.route('/search', methods = ['POST'])
def search():
    search = request.form['searchkey']
    timestep = request.form['timestep']
    print("The search is for'" + search + "'")
    print("The timestep is '" + timestep + "'")
    results = sentiment_to_text(search)
    dates = []
    sentiments = []
    for entry in results:
        temp = entry[0]
        entry[0] = temp[0:16]
        dates.append(entry[0])
        sentiments.append(entry[1])
    return render_template('sentiment.html', dates=dates, sentiments=sentiments)
    
if __name__ == "__main__":
    app.run()