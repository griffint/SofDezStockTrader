import numpy as np 
import statsmodels.api as sm
import scipy.linalg as linalg
import matplotlib.pyplot as plt
from statsmodels.graphics.api import qqplot
import random
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

def Convert(Stocks,Exog1,Exog2,Exog3):
	""" This function converts data from EXOG and stocks lists to the A and b parameters for Ax=b"""
	A = np.array([Exog1,Exog2,Exog3]).T
	b = np.array(Stocks).T
	return (A,b)


def MR(A,b):
	""" Assumes inputs are numpy arrays in the form of the output of Convert """
	ATB = np.dot(A.transpose(),b)
	ATA = np.dot(A.transpose(),A)
	coeff = linalg.solve(ATA,ATB)
	predicted = np.dot(A,coeff)
	t = range(len(Stocks))
	plt.plot(t,Stocks,'.',t,predicted)
	plt.show()
	errors = predicted - Stocks
	plt.plot(t,error)
	plt.show()
	return (coeffs,errors)

def Identify(data,lags):
	fig = plt.figure(figsize=(12,8))
	ax1 = fig.add_subplot(211)
	fig = sm.graphics.tsa.plot_acf(data, lags=lags, ax=ax1)
	ax2 = fig.add_subplot(212)
	fig = sm.graphics.tsa.plot_pacf(data, lags=lags, ax=ax2)
	plt.show()
Stocks = random.sample(range(10000),100)
x1 = random.sample(range(100),100)
x2 = random.sample(range(1000),100)
x3 = random.sample(range(100000),100)
(A,b) = Convert(Stocks,x1,x2,x3)
print MR(A,b)
