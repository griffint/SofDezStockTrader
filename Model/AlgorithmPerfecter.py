#Created Maor Bernstein
""" Do not run this script. Functionality still has yet to be restored. """

import numpy as np
import scipy.linalg as linalg
import matplotlib.pyplot as plt
import dataFetcher as df

def Perfecter(tick):
	"""This function takes a ticker, and outputs the perfect Ridge regression parameter and error.
	"""
	(A,b,A_full,b_full,n) = Pull(tick)
	pars = range(0,1000000,100)
	error = []
	for i in range(len(pars)):
		error.append(ParFinder(A,b,A_full,b_full,pars[i],n))
	plt.plot(pars,error)
	plt.show()
	minimum = min(error)
	ideal_par = pars[error.index(minimum)]
	return (ideal_par,minimum)

def Convert(Stocks,ExogList):
	""" This function converts data from EXOG and stocks lists to the A and b parameters for Ax=b"""
	A = np.array(ExogList).T
	b = np.array(Stocks).T
	return (A,b)

def sumsqrs(l):
	"""Outputs the sum of squares of a list.
	Input: List of numbers
	Output: Sum of squares of the list"""
	out = 0
	for i in range(len(l)):
		out += l[i]**2
	return out

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

def Pull(ticker):
	"""This function pulls data for a ticker and converts it into A,b,A_full,b_full, and what percentage of the data  is the model to be built on
	Input: ticker
	Ouput: A,b,A_full,b_full,n """
	dic = df.internetData(ticker)
	comp = df.industryTickers(ticker)
	print "Num vars is " + str(len(comp))
	Stocks_full = FloatConvert(dic['Prices'])
	n = len(Stocks_full)*5/10
	Stocks = Stocks_full[:n]
	x_full = FloatConvert(dic['Volumes'])
	x = x_full[:n]
	var_full = [x_full]
	var = [x]
	for i in range(10):
		try:
			dic = df.internetData(comp[i])
			w_full = FloatConvert(dic['Prices'])
			w = w_full[:n]
			x_full = FloatConvert(dic['Volumes'])
			x = x_full[:n]
			if len(w)==1008:
				var.extend([w,x])
				var_full.extend([w_full,x_full])
		except:
			pass
	(A,b) = Convert(Stocks,var)
	(A_full,b_full) = Convert(Stocks_full,var_full)
	return (A,b,A_full,b_full,n)

def ParFinder(A,b,A_full,b_full,par,n):
	"""This function finds the ideal parameter from the data pulled from pull.
	Inputs: Ouputs of pull,  and the ridge regression paramer.
	Ouput: The error given a parameter input"""
	ATB = np.dot(A.transpose(),b)
	numvars = ATB.shape[0]
	ATA = np.dot(A.transpose(),A) + par*np.identity(numvars)
	coeff = np.dot(linalg.inv(ATA),ATB)
	predicted = np.dot(A_full,coeff)
	errors = predicted[n:] - b_full[n:]
	errors = errors/b_full[n:]
	return np.mean(np.abs(errors)**2)

if __name__ == "__main__":
	print Perfecter('MMM')