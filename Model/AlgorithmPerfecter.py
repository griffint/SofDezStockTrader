import numpy as np
import scipy.linalg as linalg
import matplotlib.pyplot as plt
import dataFetcher as df
def Convert(Stocks,Exog1,Exog2,Exog3):
	""" This function converts data from EXOG and stocks lists to the A and b parameters for Ax=b"""
	A = np.array([Exog1,Exog2,Exog3]).T
	b = np.array(Stocks).T
	return (A,b)

def sumsqrs(l):
	out = 0
	for i in range(len(l)):
		out += l[i]**2
	return out

def ParFinder(par):
	dic = df.dataFetcher('AAPL')
	Stocks = dic['ClosingPrices']
	x1 = dic['DailyVolumes']
	x2 = dic['ShortInterests']
	x3 = dic['EarningsPerShare']
	(A,b) = Convert(Stocks[:500],x1[:500],x2[:500],x3[:500])
	(A_full,b_full) = Convert(Stocks,x1,x2,x3)
	ATB = np.dot(A.transpose(),b)
	numvars = ATB.shape[0]
	ATA = np.dot(A.transpose(),A) + par*np.identity(numvars)
	coeff = np.dot(linalg.inv(ATA),ATB)
	predicted = np.dot(A_full,coeff)
	errors = predicted - b_full
	return sumsqrs(errors)

if __name__ == "__main__":
	pars = range(-0,100000,1000)
	out = []
	for i in range(len(pars)):
		out.append(ParFinder(pars[i]))
	print out
	plt.plot(pars,out)
	plt.show()