import numpy as np
import scipy.linalg as linalg
import matplotlib.pyplot as plt
import dataFetcher as df

def Perfecter(tick):
	dic = df.internetData(tick)
	comp = df.industryTickers(tick)
	comp = df.internetData(comp[0])
	pars = range(0,1000000,100)
	error = []
	for i in range(len(pars)):
		error.append(ParFinder(pars[i],dic,comp))
	minimum = min(error)
	ideal_par = pars[error.index(minimum)]
	return (ideal_par,minimum)

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

def FloatConvert(l):
	out = []
	for i in range(len(l)):
		out.append(float(l[i]))
	return out

def ParFinder(par,dic,comp):
	Stocks = FloatConvert(dic['Prices'])
	x1 = FloatConvert(dic['Volumes'])
	x2 = FloatConvert(comp['Prices'])
	x3 = FloatConvert(comp['Volumes'])
	n = len(Stocks)*9/10
	(A,b) = Convert(Stocks[:n],x1[:n],x2[:n],x3[:n])
	(A_full,b_full) = Convert(Stocks,x1,x2,x3)
	ATB = np.dot(A.transpose(),b)
	numvars = ATB.shape[0]
	ATA = np.dot(A.transpose(),A) + par*np.identity(numvars)
	coeff = np.dot(linalg.inv(ATA),ATB)
	predicted = np.dot(A_full,coeff)
	errors = predicted[n:] - b_full[n:]
	errors = errors/b_full[n:]
	return np.mean(np.abs(errors))

if __name__ == "__main__":
	tick = 'MMM'
	dic = df.internetData(tick)
	comp = df.industryTickers(tick)
	comp = df.internetData(comp[0])
	pars = range(0,100000,1000)
	out = []
	for i in range(len(pars)):
		out.append(ParFinder(pars[i],dic,comp))
	plt.plot(pars,out)
	plt.show()
	print Perfecter('MMM')