
f = open("f_libraries_of_the_world.txt", "r")
file_name = "f_libraries_of_the_world"
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
	return (score_sum/lib_data[library][0])

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
	books_not_added = []
	for book in books:
		if day >= numDays:
			break
		if book_scanned[book]:
			books_not_added.append(book)
			continue
		amount_curr_day += 1
		book_scanned[book] = True
		book_orders[lib].append(book)
		if amount_curr_day == throughput:
			amount_curr_day = 0
			day += 1
	book_orders[lib] += books_not_added

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
	return score

def output_file(filename):
	f = open(filename+'.out', "w+")
	if len(book_orders[lib_started[-1]]) == 0:
		f.write(str(len(lib_started)-1))
	else:
		f.write(str(len(lib_started)))
	
	f.write('\n')
	for x in range(len(lib_started)):
		i = lib_started[x]
		if len(book_orders[i]) != 0:
			f.write(str(i) + " " +str(len(book_orders[i])))
			f.write('\n')
			#print(book_orders)
			for b in book_orders[i]:
				f.write(str(b) + ' ')
			if x != len(lib_started)-1:
				f.write('\n')
		# f.write(' '.join(book_orders[i]))
	# f.write()

	f.close()	
prevMax = 0

from random import randint
def genetic():
	while True:
		global prevMax
		global lib_started
		global book_orders
		numOps = randint(1, 1)
		old_libstart = lib_started.copy()
		old_bookorders = book_orders.copy()
		for _ in range(numOps):
			which = randint(0, 0)
			if which == 0:
				reshuffle()
			elif which == 1:
				take_out_and_insert()
		newScore = Score()
		print(prevMax, newScore)
		if newScore > prevMax:
			prevMax = newScore
			output_file(file_name)
		else:
			lib_started = old_libstart
			book_orders = old_bookorders

def reshuffle():
	time = 0
	book_scanned = [False]*numBooks
	book_orders = [[] for _ in range(numLibraries)]
	books_not_added = []
	for i in range(len(lib_started)):
		j = randint(i, len(lib_started)-1)
		lib_started[i], lib_started[j] = lib_started[j], lib_started[i]
		idx = lib_started[i]
		time += lib_data[idx][0]
		book_time = 0
		through = lib_data[idx][1]
		thrSoFar = 0
		for b in lib_data[idx][2]:
			if time >= numDays:
				break
			if book_scanned[b]:
				books_not_added.append(b)
				continue
			book_scanned[b] = True
			thrSoFar += 1
			book_orders[idx].append(b)
			if thrSoFar == through:
				book_time += 1
				thrSoFar = 0
		book_orders[idx] += books_not_added
			
		



pool = []
def not_used():
	for i in range(numLibraries):
		if i not in lib_started:
			pool.append(i)

def take_out_and_insert():
	print("takeot")
	changes = randint(0, int(len(lib_started)/2))
	taken_out = {}
	for i in range(changes):
		rand = randint(0, len(lib_started)-1)
		while lib_started[rand] not in taken_out:
			rand = randint(0, len(lib_started)-1)
		taken_out.add(lib_started[rand])
		for j in book_orders[lib_started[rand]]:
			book_scanned[j] = False
		lib_started[rand] = None
		pool.append(lib_started[rand])
		
	for i in range(len(lib_started)):
		if lib_started[i] == None:
			rand = randint(0, len(pool)-1)
			lib_started[i] = pool[rand]
			scanned = []
			book_orders[pool[rand]] = []

			for j in range(len(lib_data[pool[rand][2]])):
				if book_scanned[lib_data[pool[rand]][2][j]] :
					scanned.append(lib_data[pool[rand]][2][j])
				else:
					book_orders[pool[rand]].append(lib_data[pool[rand]][2][j])
					book_scanned[lib_data[pool[rand]][2][j]] = True
			
			for book in scanned:
				book_orders[pool[rand]].append(book)




# print("done")
assign_lib_from_scores(rescore_every = 1)
#print(lib_started)
#print(book_orders)
prevMax = Score()
not_used()
output_file(file_name)
genetic()



