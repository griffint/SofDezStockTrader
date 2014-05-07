#Created Maor Bernstein

import numpy as np 
import scipy.linalg as linalg
import matplotlib.pyplot as plt
import random
import datetime
from matplotlib.dates import MONDAY
from matplotlib.finance import quotes_historical_yahoo
from matplotlib.dates import MonthLocator,WeekdayLocator,DateFormatter
import dataFetcher as df

def FloatConvert(l):
	""" Converts lists of strings to lists of floats.
	Input: List of strings
	Output: List of floats
	Useful because Datafetcher outputs lists of strings
	"""
	out = []
	for i in range(len(l)):
		out.append(float(l[i]))
	return out

def Analyze(ticker,par=0):
	"""The wrapper function to make a complete prediction.
	Inputs: Ticker for the Stock ticker, and par for the ridge regresion paramter. If none inputted, assume 0.
	Output: Prediction for stock price tomorrow, today's stock price, a shitty prediction of stock price tomorrow, and the mean error.
	"""
	dic = df.internetData(ticker)
	comp = df.industryTickers(ticker)
	print "Num vars is " + str(len(comp))
	Stocks = FloatConvert(dic['Prices'])
	x = FloatConvert(dic['Volumes'])
	var = [x]
	for i in range(15):
		try:
			dic = df.internetData(comp[i])
			w = FloatConvert(dic['Prices'])
			x = FloatConvert(dic['Volumes'])
			if len(w)==1008:
				var.extend([w,x])
		except:
			pass
	(A,b) = Convert(Stocks,var)
	(A_full,b_full) = Convert(Stocks,var)
	(coeff,e) = MR(A,b,A_full,b_full,par)
	vals = VarPredict(var)
	Future_Stock_Price = Evaluate(vals,coeff)
	Shitty_Future_Stock_Price = Predict(Stocks[-50:],8)
	return (Stocks[-1],Future_Stock_Price,Shitty_Future_Stock_Price,e)

def Convert(Stocks,ExogList):\
	""" This function converts data from EXOG and stocks lists to the A and b parameters for Ax=b"""
	A = np.array(ExogList).T
	b = np.array(Stocks).T
	return (A,b)

def MR(A,b,A_full,b_full,par):
	""" This function computes the Linear Regression parameters and the error of that model.
	It takes as inputs, the A and b for the amount of points you want to model, and A_full and b_full are all of the  points of interest.
	A_full and b_full are used to compute the total error. Par is the Ridge Regresion Parameter
	The output is a  list of coeffs and the error as a percent. It also produces a plot and saves it into Static.
	"""
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

	# every monday
	mondays   = WeekdayLocator(MONDAY)

	# every 3rd month
	months    = MonthLocator(range(1,13), bymonthday=1, interval=4)
	monthsFmt = DateFormatter("%b '%y")

	fig, ax = plt.subplots()
	ax.plot_date(dates2,b_full, '.', label='Actual Data')
	ax.plot_date(dates2,predicted, 'r-', label='Predicted Data')
	ax.xaxis.set_major_locator(months)
	ax.xaxis.set_major_formatter(monthsFmt)
	ax.xaxis.set_minor_locator(mondays)
	ax.autoscale_view()
        plt.xlabel('Date')
        plt.ylabel('Stock Prices ($)')
        plt.title('Stock Prices and Predictions')
	plt.legend(loc=0)
	
	try:
		plt.savefig('static/prediction.jpg')
	except:
		plt.show()
	errors = predicted - b_full
	e = errors/b_full
	mean_error =  np.mean(np.abs(e))
	return (np.array(coeff),mean_error)

def VarPredict(var):
	"""Predicts a what the next value will be for a list of variables (each variable is a list)
	Uses Predict to do the prediction.
	Input: List of list of variables
	Output: List of next values for each variable"""
	out = []
	for i in range(len(var)):
		x = var[i]
		pred = Predict(x[-50:],8)
		out.append(pred)
	return np.array(out)

def Predict(s,deg):
	"""Creates a simply polynomial fit for a np array of time series data
	Input: numpy array of time series data, and degree of the model
	Output: Prediction of next point.
	"""
	t = range(len(s))
	t = np.array(t)
	t_next = t[-1] + 1
	p = np.polyfit(t,s,deg)
	return np.polyval(p,t_next)


def Evaluate(vals,coeffs):
	"""Evaluates the model created in MR
	Input: Coeffs is the output of MR, and vals is the output of VarPredict
	Output: THe predicted Stock price tomorrow
	"""
	out = vals*coeffs
	return np.sum(out)

if (__name__ == "__main__"):
	Analyze('T',2000)
