import numpy as np 
import statsmodels.api as sm
import scipy.linalg as linalg
import matplotlib.pyplot as plt
from statsmodels.graphics.api import qqplot
import random
import dataFetcher as df
def Diff(l):
	out = []
	for i in range(len(l)-1):
		out.append(l[i+1]-l[i])
	return np.array(out)

def Sample(l,t):
	out = []
	for i in range(len(l)):
		if i%t==0:
			out.append(l[i])
	return out

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
	plt.plot(t,e)
	plt.show()
	print np.mean(e*e)
	return (coeff,errors)

def AR(Endog,order):
	n = len(Endog)
	model = sm.tsa.ARMA(Endog[:n*8/10],(order,0))
	model.fit()
	pred = model.predict()
	pred = pred[:2/10*n]
	t = range(len(pred))
	plt.plot(t,Endog[n*8/10:],t,pred)
	plt.show()

def Identify(data,lags):
	fig = plt.figure(figsize=(12,8))
	ax1 = fig.add_subplot(211)
	fig = sm.graphics.tsa.plot_acf(data, lags=lags, ax=ax1)
	ax2 = fig.add_subplot(212)
	fig = sm.graphics.tsa.plot_pacf(data, lags=lags, ax=ax2)
	plt.show()

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
	# (A,b) = Convert(Stocks,[x1,x2,x3,x4,x5,x6,x7])
	# (A_full,b_full) = Convert(Stocks,[x1,x2,x3,x4,x5,x6,x7])
	# MR(A,b,A_full,b_full)
