file_name = "c_incunabula"
f = open(file_name+".txt", "r")
numBooks, numLibraries, numDays = [*map(int, f.readline().split())]

book_scores = [*map(int, f.readline().split())]
book_scanned = [False]*numBooks

maxscore = 0
for score in book_scores:
	maxscore += score
print(maxscore)