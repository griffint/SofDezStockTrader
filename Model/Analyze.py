import AlgorithmLimited as alg
import AlgorithmPerfecter as ap

#Runs a quick analyze function
def Analyze(ticker):
	"""This function calls AlgorithmPerfecter and AlgorithmLimited to make a perect model, and then model it.
	Input is ticker
	Outputs are the outputs of analyze in AlgorithmLimited
	"""
	(Today,Predicted,Shitty,error) = alg.Analyze(ticker,0)
	return (Today,Predicted,Shitty,error)

if (__name__ == "__main__"):
	print Analyze('MMM')
