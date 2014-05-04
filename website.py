# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 16:13:27 2014

@author: sawyer
"""
 
from pattern.web import *
from pattern.en import *
from Model.symbolToName import get_company_name
from flask import Flask, render_template, request, redirect
#from Model.stocks import db

app = Flask(__name__)
#app.config.from_pyfile("config.py")
#db.init_app(app)



@app.route('/', methods = ['POST', 'GET'])
def hello_world():
    return render_template('index.html')

@app.route('/search', methods = ['POST', 'GET'])
def search():
    search = request.form['searchkey']
    try:
        company_name = get_company_name(search)
        search=search.upper()
    except:
        company_name = 'AAAAAAAAAAAAAAAAA'
        #return redirect('/error')
        pass
    return render_template('sentiment.html', company_name=company_name, search=search)
    
@app.route('/about', methods = ['POST', 'GET'])
def about():
    return render_template('about.html')
    
@app.route('/error', methods = ['POST', 'GET'])
def error():
    return render_template('error.html')
    
if __name__ == "__main__":
    app.run()
    
