# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 16:13:27 2014

@author: sawyer
"""
 
from pattern.web import *
from pattern.en import *
from Model.symbolToName import get_company_name
from Model.sentimentAnalysis import savefig_twitter_average
from flask import Flask, render_template, request, redirect
from Model.Analyze import Analyze
#from Model.stocks import db

app = Flask(__name__)
#app.config.from_pyfile("config.py")
#db.init_app(app)



@app.route('/', methods = ['POST', 'GET'])
def hello_world():
    ''' Renders the default html template '''
    return render_template('index.html')

@app.route('/search', methods = ['POST', 'GET'])
def search():
    ''' This function gets the requested search from the website, and runs the algorithm and sentiment analysis, and renders the template for the results. '''
    search = request.form['searchkey']
    #try:
    company_name = get_company_name(search)
    search=search.upper()
    data = Analyze(search)
    current_price = data[0]
    next_price= data[1]
    error= data[3]
    error = error*100
    savefig_twitter_average(company_name)
    x = next_price/current_price
    if x>1.02:
        recommendation = 'buying'
    elif x>.98:
        recommendation = 'holding on'
    else:
        recommendation = 'selling'
    #except:
        #return redirect('/error')
    return render_template('sentiment.html', recommendation=recommendation, company_name=company_name, search=search, current_price=current_price, next_price=next_price, error=error)
    
@app.route('/about', methods = ['POST', 'GET'])
def about():
    ''' This renders the template for the 'About Us' section'''
    return render_template('about.html')
    
@app.route('/error', methods = ['POST', 'GET'])
def error():
    ''' Renders the template for the error page '''
    return render_template('error.html')
    
if __name__ == "__main__":
    app.run()
    
