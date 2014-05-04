import AlgorithmLimited as alg
import AlgorithmPerfecter as ap

def Analyze(ticker):
	(par,error) = ap.Perfecter(ticker)
	(Today,Predicted) = alg.Analyze(ticker,par)
	return (Today,Predicted,error)
