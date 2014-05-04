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
	out = []
	for i in range(len(l)):
		out.append(float(l[i]))
	return out

def Analyze(ticker,par):
	dic = df.internetData(ticker)
	comp = df.industryTickers(ticker)
	Stocks = FloatConvert(dic['Prices'])
	x = FloatConvert(dic['Volumes'])
	var = [x]
	for i in range(1):
		try:
			dic = df.internetData(comp[i])
			w = FloatConvert(dic['Prices'])
			x = FloatConvert(dic['Volumes'])
			var.extend([w,x])
			var_full.extend([w,x])
		except:
			pass
	(A,b) = Convert(Stocks,var)
	(A_full,b_full) = Convert(Stocks,var)
	coeff = MR(A,b,A_full,b_full,par)
	vals = VarPredict(var)
	Future_Stock_Price = Evaluate(vals,coeff)
	return (Stocks[-1],Future_Stock_Price)

def Convert(Stocks,ExogList):
	""" This function converts data from EXOG and stocks lists to the A and b parameters for Ax=b"""
	A = np.array(ExogList).T
	b = np.array(Stocks).T
	print np.dot(A.T,b)
	return (A,b)

def MR(A,b,A_full,b_full,par):
	""" Assumes inputs are simple arrays """
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
	return np.array(coeff)

def VarPredict(var):
	out = []
	for i in range(len(var)):
		x = var[i]
		pred = Predict(x[-3:])
		out.append(pred)
	return np.array(out)

def Predict(s):
	diff11 = s[1] - s[0]
	diff12 = s[2] - s[1]
	diff2 = diff12 - diff11
	avgdiff1 = (diff12 + diff11)/2
	out = diff2*(2**2)/2 + avgdiff1*2 + s[1]
	s = np.append(s,out)
	return out

def Evaluate(vals,coeffs):
	out = vals*coeffs
	return np.sum(out)

if (__name__ == "__main__"):
	Analyze('T',2000)