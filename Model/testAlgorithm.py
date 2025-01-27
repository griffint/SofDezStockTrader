# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 14:31:10 2014

@author: sawyer
"""

import numpy as np 
import statsmodels.api as sm
import scipy.linalg as linalg
import matplotlib.pyplot as plt
from statsmodels.graphics.api import qqplot
import random
import dataFetcher as df
import datetime
from matplotlib.dates import MONDAY
from matplotlib.finance import quotes_historical_yahoo
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter

def Analyze(ticker):
	dic = df.dataFetcher(ticker)
	ind = df.getIndustry(ticker)
	comp = df.industryTickers(ind)
	comp = comp[2]
	dic2 = df.dataFetcher(comp)
	Stocks = dic['ClosingPrices']
	x1 = dic['DailyVolumes']
	x2 = dic['ShortInterests']
	x3 = dic['EarningsPerShare']
	x4 = dic2['ClosingPrices']
	x5 = dic2['DailyVolumes']
	x6 = dic2['ShortInterests']
	x7 = dic2['EarningsPerShare']
	(A,b) = Convert(Stocks,[x1,x2,x3,x4,x5,x6,x7])
	(A_full,b_full) = Convert(Stocks,[x1,x2,x3,x4,x5,x6,x7])
	MR(A,b,A_full,b_full)

def Convert(Stocks,ExogList):
	""" This function converts data from EXOG and stocks lists to the A and b parameters for Ax=b"""
	A = np.array(ExogList).T
	b = np.array(Stocks).T
	return (A,b)

def MR(A,b,A_full,b_full):
	""" Assumes inputs are simple arrays """
	par = 10000
	ATB = np.dot(A.transpose(),b)
	numvars = ATB.shape[0]
	ATA = np.dot(A.transpose(),A) + par*np.identity(numvars)
	coeff = np.dot(linalg.inv(ATA),ATB)
	predicted = np.dot(A_full,coeff)
	t = range(len(predicted))
	
	date2 = datetime.date.today()
	timedelta = datetime.timedelta(len(t))
	date1 = date2 - timedelta
	print date2
	print date1

	dates2 = []
	for i in range(735353-len(t), 735353):
	    dates2.append(i)

	print len(dates2)
	print len(t)

	# every monday
	mondays   = WeekdayLocator(MONDAY)

	# every 3rd month
	months    = MonthLocator(range(1,13), bymonthday=1, interval=4)
	monthsFmt = DateFormatter("%b '%y")

	fig, ax = plt.subplots()
	ax.plot_date(dates2,b_full, '.')
	ax.plot_date(dates2,predicted, 'r-')
	ax.xaxis.set_major_locator(months)
	ax.xaxis.set_major_formatter(monthsFmt)
	ax.xaxis.set_minor_locator(mondays)
	ax.autoscale_view()
	
	try:
		plt.savefig('static/prediction.jpg')
	except:
		plt.show()
	errors = predicted - b_full
	e = errors/b_full
	mean_error =  np.mean(e*e)
	return mean_error

if (__name__ == "__main__"):
	dic = df.dataFetcher('AAPL')
	ind = df.getIndustry('AAPL')
	comp = df.industryTickers(ind)
	comp = comp[2]
	dic2 = df.dataFetcher(comp)
	Stocks = dic['ClosingPrices']
	x1 = dic['DailyVolumes']
	x2 = dic['ShortInterests']
	x3 = dic['EarningsPerShare']
	x4 = dic2['ClosingPrices']
	x5 = dic2['DailyVolumes']
	x6 = dic2['ShortInterests']
	x7 = dic2['EarningsPerShare']
	t = range(len(Stocks))
	plt.plot(t,x3)
	plt.show()
	(A,b) = Convert(Stocks,[x1,x2,x3,x4,x5,x6,x7])
	(A_full,b_full) = Convert(Stocks,[x1,x2,x3,x4,x5,x6,x7])
	MR(A,b,A_full,b_full)
