import numpy as np 
import statsmodels.api as sm
import scipy.linalg as linalg
import matplotlib.pyplot as plt
from statsmodels.graphics.api import qqplot
import random
import dataFetcher as df
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
	plt.plot(t,b_full,'.',t,predicted) 
	plt.savefig('prediction.jpg')
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
