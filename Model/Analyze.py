import AlgorithmLimited as alg
import AlgorithmPerfecter as ap

def Analyze(ticker):
	(par,error) = ap.Perfecter(ticker)
	(Today,Predicted,Shitty) = alg.Analyze(ticker,par)
	return (Today,Predicted,Shitty,error)

if (__name__ == "__main__"):
	print Analyze('MMM')
