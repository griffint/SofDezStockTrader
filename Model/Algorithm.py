import numpy as np 
import statsmodels.api as sm
import scipy.linalg as linalg
import matplotlib.pyplot as plt
from statsmodels.graphics.api import qqplot
import random
import dataFetcher as df
def Analyze(ticker):
	dic = df.dataFetcher(ticker)
	comp = df.industryTickers(ticker)
	Stocks = dic['ClosingPrices']
	x1 = dic['DailyVolumes']
	x2 = dic['EarningsPerShare']
	x3 = dic['ShortInterests']
	var = [x1,x2,x3]
	for i in range(len(comp)):
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
	plt.plot(t,b_full,'.',t,predicted)
	try:
		plt.savefig('static/prediction.jpg')
	except:
		plt.show()
	errors = predicted - b_full
	e = errors/b_full
	mean_error =  np.mean(e*e)
	return mean_error

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
	print Predict(np.array([0,1,4]))