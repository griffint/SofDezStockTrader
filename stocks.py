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

#engine = create_engine("postgresql://postgres:griffin@localhost/stocks")

#Base = declarative_base()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:griffin@localhost/stocks"
db = SQLAlchemy(app)

class Stock(db.Model):
   __tablename__ = 'stockData'
   id = db.Column(Integer, primary_key=True)
   date = db.Column(DateTime)
   company = db.Column(String)
   ticker = db.Column(String)
   industry = db.Column(String)
   sector = db.Column(String)
   close = db.Column(Float)
   high = db.Column(Float)
   low = db.Column(Float)
   volume = db.Column(Float)
   shortInterest = db.Column(Float)
   eps = db.Column(Float)
   
   def __init__(self,id,date,company,ticker,industry,sector,close,high,low,volume,shortInterest,eps):
       self.id = id        
       self.date = date
       self.company = company
       self.ticker = ticker
       self.industry = industry
       self.sector = sector
       self.close = close
       self.high = high
       self.low = low
       self.volume = volume
       self.shortInterest = shortInterest
       self.eps = eps
       
   def __repr__(self):
       return 'butt sex'
  