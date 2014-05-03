import numpy as np 
import statsmodels.api as sm
import scipy.linalg as linalg
import matplotlib.pyplot as plt
from statsmodels.graphics.api import qqplot
import random
import datetime
from matplotlib.dates import MONDAY
from matplotlib.finance import quotes_historical_yahoo
from matplotlib.dates import MonthLocator,WeekdayLocator,DateFormatter
def Analyze(ticker):
	dic = df.dataFetcher(ticker)
	comp = df.industryTickers(ticker)
	Stocks = dic['ClosingPrices']
	x1 = dic['DailyVolumes']
	x2 = dic['EarningsPerShare']
	x3 = dic['ShortInterests']
	var = [x1,x2,x3]
	for i in range(2):
		dic = df.dataFetcher(comp[i])
		w = dic['ClosingPrices']
		x = dic['DailyVolumes']
		y = dic['EarningsPerShare']
		z = dic['ShortInterests']
		var.extend([w,x,y,z])
	(A,b) = Convert(Stocks,var)
	(A_full,b_full) = Convert(Stocks,var)
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
	return (coeff,mean_error)

def Predict(s):
	diff11 = s[1] - s[0]
	diff12 = s[2] - s[1]
	diff2 = diff12 - diff11
	avgdiff1 = (diff12 + diff11)/2
	out = diff2*(2**2)/2 + avgdiff1*2 + s[1]
	s = np.append(s,out)
	plt.plot(s)
	plt.show()
	return out

def Evaluate(vals,coeffs):
	out = vals*coeffs
	return np.sum(out)

if (__name__ == "__main__"):
	pass