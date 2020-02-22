fileName = 'a.in'

def score(theOut):
	return
	# score

def writeToOut(fileName):
	f = open(fileName+'.out', "w+")
	# f.write()

	f.close()

bestScore = 0
bestOut = []
f = open(fileName, "r")

# input and generate a greedy or smth

while True:
	newOut = bestOut.copy()

	# do random change(s)

	newScore = score(newOut)
	if newScore > bestScore:
		bestScore = newScore
		bestOut = newOut
		writeToOut(newOut)
		print(bestScore)