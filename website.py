# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 16:13:27 2014

@author: sawyer
"""

from pattern.web import *
from pattern.en import *
import numpy
import matplotlib.pylab as pyl
from Model import *
from Controller import *
from flask import Flask, render_template, request, redirect

from Model.stocks import db

app = Flask(__name__)
app.config.from_pyfile("config.py")
db.init_app(app)



@app.route('/', methods = ['POST', 'GET'])
def hello_world():
    return render_template('index.html')
    
@app.route('/search', methods = ['POST', 'GET'])
def search():
    search = request.form['searchkey']
    try:
        company_name = symbolToName.get_company_name(search)
        search=search.upper()
    except:
        return redirect('/')
    try:
        company_name = str(company_name)
        results = sentimentAnalysis.twitter_sentiment_average(company_name)
    except:
        return render_template('error.html')
    if results == []:
        return render_template('noresults.html')
    dictionary = results[0]
    dates = results[1]
    print dictionary
    print dates
    hours = []
    sentiments = []
    for date in dates:
        hours.append(sentimentAnalysis.reformatted_date_subtraction(dates[0], date))
        sentiments.append(dictionary[date])
    pyl.plot(hours, sentiments, 'bo-')
    try: 
        pyl.axis([-10, numpy.amax(hours)+10, numpy.amin(sentiments)-.2, numpy.amax(sentiments)+.2])
    except:
        return render_template('error.html')
    pyl.xlabel('Hours Ago')
    pyl.ylabel('Sentiment')
    pyl.title('Sentiment Data')
    pyl.savefig('static/sentiment.png')
    pyl.clf()
    print Algorithm.Analyze(search)
    return render_template('sentiment.html', company_name=company_name, dates=dates, hours=hours, sentiments=sentiments, search=search)
    
if __name__ == "__main__":
    app.run()
    
