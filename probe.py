file_name = "e_so_many_books"
f = open(file_name + ".txt", "r")

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

#score all unassigned libraries
def library_score_all():
	for library in lib_scores:
		if not lib_added[library[0]]:
			library[1] = library_score(library[0])

#score a library
def library_score(library):
	score_sum = 0
	# max_books_can_ship = 
	for book in lib_data[library][2]:
		if not book_scanned[book]:
			score_sum += book_scores[book]
	return (score_sum/lib_data[library][1])

def resort():
	global lib_scores
	new_lib_scores = []
	for i in range(len(lib_scores)):
		if not lib_added[lib_scores[i][0]]:
			new_lib_scores.append(lib_scores[i])
	lib_scores = new_lib_scores
	library_score_all()
	lib_scores.sort(key = lambda x:x[1], reverse=True)
			

def assign_lib_from_scores(rescore_every = 100):
	time = 0
	toRestart = True
	while toRestart:
		toRestart = False
		curr_rescore_count = 0
		for i in range(len(lib_scores)):
			if time >= numDays:
				break
			if curr_rescore_count == rescore_every:
				toRestart = True
				break
			idx, score = lib_scores[i]
			timetakes, amoperday, books = lib_data[idx]
			lib_added[idx] = True
			time += timetakes
			add_books_scanned(idx, time)
			lib_started.append(idx)
			
			curr_rescore_count += 1
		if toRestart:
			resort()


def add_books_scanned(lib, timeLibAdded):
	_, throughput, books = lib_data[lib]
	if throughput == 0:
		return
	day = timeLibAdded
	amount_curr_day = 0
	for book in books:
		if day >= numDays:
			break
		if book_scanned[book]:
			continue
		amount_curr_day += 1
		book_scanned[book] = True
		book_orders[lib].append(book)
		if amount_curr_day == throughput:
			amount_curr_day = 0
			day += 1

def output_file(filename):
	f = open(filename+'.out', "w+")
	f.write(str(len(lib_started)))
	f.write('\n')
	for i in lib_started:
		f.write(str(i) + " " +str(len(book_orders[i])))
		f.write('\n')
		#print(book_orders)
		for b in book_orders[i]:
			f.write(str(b) + ' ')
		f.write('\n')
		# f.write(' '.join(book_orders[i]))
	# f.write()

	f.close()	

# print("done")
assign_lib_from_scores(rescore_every = 1)
#print(lib_started)
#print(book_orders)
output_file(file_name)
