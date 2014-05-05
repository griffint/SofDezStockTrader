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
	print "Num vars is " + str(len(comp))
	Stocks = FloatConvert(dic['Prices'])
	x = FloatConvert(dic['Volumes'])
	var = [x]
	for i in range(len(comp)/3):
		try:
			dic = df.internetData(comp[i])
			w = FloatConvert(dic['Prices'])
			x = FloatConvert(dic['Volumes'])
			if len(w)==1008:
				var.extend([w,x])
				var_full.extend([w,x])
		except:
			pass
	(A,b) = Convert(Stocks,var)
	(A_full,b_full) = Convert(Stocks,var)
	coeff = MR(A,b,A_full,b_full,par)
	vals = VarPredict(var)
	Future_Stock_Price = Evaluate(vals,coeff)
	Shitty_Future_Stock_Price = Predict(Stocks[-50:],8)
	return (Stocks[-1],Future_Stock_Price,Shitty_Future_Stock_Price)

def Convert(Stocks,ExogList):
	""" This function converts data from EXOG and stocks lists to the A and b parameters for Ax=b"""
	A = np.array(ExogList).T
	b = np.array(Stocks).T
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
	mean_error =  np.mean(e*e)
	return np.array(coeff)

def VarPredict(var):
	out = []
	for i in range(len(var)):
		x = var[i]
		pred = Predict(x[-50:],8)
		out.append(pred)
	return np.array(out)

def Predict(s,deg):
	t = range(len(s))
	t = np.array(t)
	t_next = t[-1] + 1
	p = np.polyfit(t,s,deg)
	return np.polyval(p,t_next)


def Evaluate(vals,coeffs):
	out = vals*coeffs
	return np.sum(out)

if (__name__ == "__main__"):
	Analyze('T',2000)
