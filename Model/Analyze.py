import AlgorithmLimited as alg
import AlgorithmPerfecter as ap

#Runs a quick analyze function
def Analyze(ticker):
	(Today,Predicted,Shitty,error) = alg.Analyze(ticker,0)
	return (Today,Predicted,Shitty,error)

if (__name__ == "__main__"):
	print Analyze('MMM')
