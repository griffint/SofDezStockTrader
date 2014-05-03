# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 18:15:09 2014

@author: griffin
"""

import csv
from sqlalchemy import *
from datetime import date
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

#stuff to set up the database in Flask
app = Flask(__name__)
#config file tells where postgres URL is
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

#this class describes what each row of the table will be
#setting up all the columns for each stock data piece
class Stock(db.Model):
   __tablename__ = 'stockData'
   id = db.Column(Integer, primary_key=True)
   date = db.Column(DateTime)
   company = db.Column(String)
   ticker = db.Column(String)
   industry = db.Column(String)
   close = db.Column(Float)
   volume = db.Column(Float)
   
   
   def __init__(self,id,date,company,ticker,industry,close,volume):
       self.id = id        
       self.date = date
       self.company = company
       self.ticker = ticker
       self.industry = industry
       self.close = close
       self.volume = volume
       
  
