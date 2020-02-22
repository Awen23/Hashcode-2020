file_name = "b_read_on"
f = open(file_name+".txt", "r")

numBooks, numLibraries, numDays = [*map(int, f.readline().split())]

book_scores = [*map(int, f.readline().split())]
book_scanned = [False]*numBooks

lib_data = []
lib_added = [False]*numLibraries

# output stuff
lib_started = []
book_orders = [[] for _ in range(numLibraries)]
lib_scores = []

for x in range(0, numLibraries):
	thisLib = [*map(int, f.readline().split()), [*map(int, f.readline().split())]]
	thisLib.pop(0)
	lib_data.append(thisLib)
	lib_scores.append([x,0])

lib_signup = []
for i in range(numLibraries):
	lib_signup.append([i,lib_data[i][0]])
lib_signup.sort(key = lambda x:x[1])
print(lib_signup)
book_orders = []
for i in range(numLibraries):
	book_orders.append(lib_data[i][2])

lib_started = []
day = 0
for i in range(numLibraries):
	day += lib_signup[i][1]
	lib_started.append(lib_signup[i][0])

def Score():
	book_scored = [False for x in range(numBooks)]
	day = 0
	for x in lib_started: #goes through every library in order
		 day += lib_data[x][0]
		 if day > numDays:
			 break;
		 books_to_scan = (numDays - day) * lib_data[x][1] #finds amount of books library can scan before time limit
		 for i in range(books_to_scan):
			 if i >= len(book_orders[x]):
				 break
			 book_scored[book_orders[x][i]] = True
	score = 0
	for i in range(numBooks):
		if book_scored[i]:
			score += book_scores[i]
	print(score)
Score()

def output_file(filename):
	f = open(filename+'.out', "w+")
	f.write(str(len(lib_started)))
	f.write('\n')
	for i in lib_started:
		f.write(str(i) + " " +str(len(book_orders[i])))
		f.write('\n')
		# print(book_orders)
		for b in book_orders[i]:
			f.write(str(b) + ' ')
		f.write('\n')
		# f.write(' '.join(book_orders[i]))
	# f.write()

	f.close()	

output_file(file_name)