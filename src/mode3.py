import requests
import pickle
import functions as f
import random
import mode2 as m2

class Manga(dict):

	def __init__(self, title = None, rank = None, genres = None, nb_favorites = None, 
	 					score = None, nb_chapters = None, datePublication = None, authors = None, characters = None):

	 	self.title = title
	 	self.rank = rank
	 	self.genres = genres
	 	self.nb_favorites = nb_favorites
	 	self.score = score
	 	self.nb_chapters = nb_chapters
	 	self.datePublication = datePublication
	 	self.authors = authors
	 	self.characters = characters

	def informations(self):

		print(self.title)
		print("rank:", self.rank)
		for g in self.genres:
			print(g)

		print("number of favorites:", self.nb_favorites)
		print ("score:", float(self.score))
		print("number of chapters:", self.nb_chapters)
		print("date publication:", self.datePublication)
		for a in self.authors:
			print(a)
		print("les personnages sont: -------")
		for c in self.characters:
			print(c)

sentence = ""

sorted_manga = []
list_genre = []

proposed_mangas = [] # list of mangas proposed by the weeabot
proposed_mangas = [] # list of mangas proposed by the weeabot

# so that the user doesn't have to always re-type the manga
curr1 = None # current manga in memory
curr2 = None # second current
last_theme=9 # subject of discussion (author, genre, etc.)

# Data related to the database for comparisons
avg_mark = []
avg_chap = []
avg_fav = []
avg_year = []
avg_char = []

# vocabulary to detect a subject of discussion
vocabSubject = [
        ['title', 'name', 'called'],
        ['rank', 'ranked', 'best'],
        ['genre', 'type'],
        ['favorites'],
        ['rated', 'score', 'mark', 'marks', 'good', 'bad'],
        ['number', 'chapters', 'long', 'short', 'finished', 'over'],
        ['when', 'recent', 'published', 'date'],
        ['author', 'wrote', 'written', 'created'],
        ['characters', 'character']
        ]

# vocabulary to detect an action
actionToDo = [
        [], # info about the current one
        ['are', 'both', 'compare', 'between', 'and', 'two'], # compare curr1 and curr2 on a criteria
        ['best', 'highest', 'biggest', 'all', 'first', 'most'], # give the best on one criteria
        ['worst', 'all', 'last', 'least'], # and the worst
        ['give', 'manga', 'suggest', 'and'], # find a manga with a particularity
        ['like', 'love', 'enjoy', 'favorite', 'favourite', 'prefer'],
		['not', 'like', 'dislike', 'hate']
        ]

# has a manga already been proposed by the bot
def in_manga_list(m, arr, g):
	for a in arr:
		try:
			if a[0].lower()==g.lower():
				for i in a[1]:
					if m.lower()==i.lower():
						return True
		except:
			1
	return False

# adds a proposed manga to the list of already proposed ones
def new_proposition(m, g):
	global proposed_mangas
	for prop in proposed_mangas:
		try:
			if prop[0].lower()==g.lower():
				prop[1].append(m.title)
				break
		except:
			1

# is the sentence a question
def is_question(sent):
	nb=0
	arr=['why', 'you', '?']
	for i in sent:
		if i in arr:
			nb+=1
	if nb>=2:
		return True
	else:
		return False

# adds a proposed manga to the list of already proposed ones (several genres)
def new_propositions(m, cr):
	global proposed_mangas
	for g in cr:
		for prop in proposed_mangas:
			try:
				if prop[0].lower()==g.lower():
					prop[1].append(m.title)
					break
			except:
				1

# calculates the average number for a given parameter
def calc_avg(n):
	mark = 0
	nb = 0
	for m in sorted_manga:
		try:
			if n==8:
				val=len(get_subject(n, m))
			elif n==6:
				val=float(get_subject(n, m).year)
			else:
				val=float(get_subject(n, m))
			mark+=val
			nb+=1
			try:
				if val<min:
					min=val
			except (NameError):
				min=val
			try:
				if val>max:
					max=val
			except (NameError):
				max=val

		except:
			1
	try:
		return [min, mark/nb, max]
	except:
		return None

# updates the current manga stored in memory (global variable)
def new_current(m):
		global curr1
		global curr2
		try:
			curr2 = curr1
			curr1 = m
		except:
			1

# updates both of the current mangas
def new_currents(m1, m2):
		global curr1
		global curr2
		try:
			curr1 = m1
			curr2 = m2
		except:
			1

# tells by which criteria a certain manga is different from the average (how is it original ?)
def evaluate(m):
	subject=[5,3,6,8]
	norm=[
		normalize(m.nb_chapters, avg_chap),
		normalize(m.nb_favorites, avg_fav),
		normalize(m.datePublication, avg_year),
		normalize(len(m.characters), avg_char)
	]
	c = 0
	for i in range(1, 3):
		if abs(norm[i])>abs(norm[c]):
			c=i
	if random.randint(0,4) >=3:
		c=random.randint(0,3)
	return subject[c], norm[c]

# returns a value between 0 and 1 to indicate how far of the average is another value inside of a set
def normalize(val, arr):
	try:
		return (val-arr[1])/(arr[2]-arr[0])
	except:
		return 0


# RETURN SENTENCES


def like_manga():
	sub, val = evaluate(curr1)
	return "I like "+curr1.title+" "+describe(sub, val, curr1)

def dislike_manga():
	sub, val = evaluate(curr1)
	return "I hate "+curr1.title+" "+describe(sub, val, curr1)

def describe(sub, val, manga):
	if (random.randint(0,10) >= 4):
		if sub==5:
			if val>0:
				return "because it has "+str(manga.nb_chapters)+" chapters, which is a lot"
			else:
				return "because it is quite short with its "+str(manga.nb_chapters)+" chapters"
		elif sub==3:
			if val>0:
				return ", a lot of people like this manga"
			else:
				return ", very few people like it"
		elif sub==6:
			if val>0:
				return "because it is from "+str(manga.datePublication.year)+" so it is recent"
			else:
				return "because it is quite old, since it was written in "+str(manga.datePublication.year)
		elif sub==8:
			if val>0:
				return "because it has about "+str(len(manga.characters))+" characters"
			else:
				return "because it has very few characters, about "+str(len(manga.characters))
		else:
			1
	else:
		a = random.randint(0,3)
		if a==0:
			return "because I like its title"
		elif a==1:
			return "because I like the author "+f.arr_to_str(manga.authors)
		elif a==2:
			return "because I like the genre "+f.arr_to_str(f.get_random_elements(manga.genres,1,1))
		else:
			return "because I like the characters "+f.arr_to_str(f.get_random_elements(manga.characters, 2, 3))
		
# determines wether it must compare or give information...
def act(nb, ac, question=False, crit=None):
	try:
		if ac==0:
			return give_info(nb)
		elif ac==1:
			return compare(nb)
		elif ac==2:
			return highest(nb, sorted_manga)
		elif ac==3:
			return highest(nb, sorted_manga, -1)
		elif ac==4:
			return find_manga(crit, sorted_manga)
		elif ac==5:
			if curr1.score >= avg_mark[1]:
				res = "I agree with you, " if question==False else ""
				return res+like_manga()
			else:
				res = "I disagree with you, " if question==False else ""
				return res+dislike_manga()
		elif ac==6:
			if curr1.score >= avg_mark[1]:
				res = "I disagree with you, " if question==False else ""
				return res+like_manga()
			else:
				res = "I agree with you, " if question==False else ""
				return res+dislike_manga()
	except:
		if random.randint(0,2)==0:
			return "That is not very clear..."
		else:
			return m2.answer(sentence, "")
  
# Only returns the data of a manga by its number of subject
def get_subject(nb, manga):
        if nb == -1:
                return "Yeah what about it ?"
        elif nb == 0:
                return manga.title
        elif nb == 1:
                return manga.rank
        elif nb == 2:
                return manga.genres
        elif nb == 3:
                return manga.nb_favorites
        elif nb == 4:
                return manga.score
        elif nb == 5:
                return manga.nb_chapters
        elif nb == 6:
                return manga.datePublication
        elif nb == 7:
                return manga.authors
        elif nb == 8:
                return manga.characters
        else:
                return get_subject(random.randint(0,8), manga)

# gives information with a proper formulation
def get_formulation(nb, manga, pronoun=True):
	noun = manga.title
	if pronoun:
		noun = f.get_random_elements([manga.title, 'it', 'this'], 1, 1)
		noun=noun[0]
	if nb == -1:
		return "Yeah what about "+str(get_subject(0, manga))+" ?"
	elif nb == 0:
		return f.upper(noun)+" is called "+str(get_subject(nb, manga))+" of course"
	elif nb == 1:
		return f.upper(noun)+"'s rank is "+str(get_subject(nb, manga))
	elif nb == 2:
		return f.arr_to_str(f.get_random_elements(manga.genres, 2, 4),",")+" are some of the genres of "+noun
	elif nb == 3:
		return f.upper(noun)+" is the favorite manga of "+str(manga.nb_favorites)+" persons"
	elif nb == 4:
		return f.upper(noun)+" is rated "+str(manga.score)+"/10"
	elif nb == 5:
		return f.upper(noun)+" has "+str(manga.nb_chapters)+" chapters"
	elif nb == 6:
		return f.upper(noun)+" was written on "+str(manga.datePublication)
	elif nb == 7:
		return +f.arr_to_str(manga.authors)+" wrote "+noun
	elif nb == 8:
		return f.arr_to_str(f.get_random_elements(manga.characters,2,4),',')+" are characters of "+manga.title
	else:
		if random.randint(0,2)>=1:
			return m2.answer(sentence, "")
		else:
			return get_formulation(random.randint(0,8), manga)

def give_info(nb):
        if curr1 == None:
            if random.randint(0,2)==0:
                return 'What manga are you talking about ?'
            else:
                return m2.answer(sentence, "")
        else:
                return get_formulation(nb, curr1)

def compare(nb):
        if curr1 == None:
                return 'You did not give me any manga name...'
        elif curr2 == None:
                return 'You forgot to mention another manga...'
        else:
                return str(get_formulation(nb, curr1, False))+" and "+str(get_formulation(nb, curr2, False))

def highest(nb, mlist, high=1):
        if nb==0 or nb==2 or nb==7 or nb==8:
                return "You did not give me a good criteria..."
        else:
                if nb == 1:
                        coef=-1
                else:
                        coef=1
                coef=coef*high
                try:
                    sc = coef*int(get_subject(nb, mlist[0]).year)
                except:
                    sc = coef*get_subject(nb, mlist[0])
                manga = mlist[0]
        for m in mlist:
                try:
                        try:
                            tmp = coef*int(get_subject(nb, m).year)
                        except:
                            tmp = coef*get_subject(nb, m)
                        if tmp > sc:
                                sc = tmp
                                manga = m
                except:
                        1
        new_current(manga)
        return str(get_formulation(nb, manga, False))


def create_manga_list(nombre):
	session = mals.Session()
	list_manga = []
	for i in range (1, nombre):
		try:
			l = session.manga(i)
			title = (l.title)
			list_manga.append(l)
		except myanimelist.manga.InvalidMangaError:
			continue
	return list_manga

def create_anime_list(nombre):
	session = mals.Session()
	list_anime = []
	for i in range (1, nombre):
		try:
			l = session.anime(i)
			title = l.title
			list_anime.append(l)
		except myanimelist.anime.InvalidAnimeError:
			continue
	return list_anime

def order_by_rank(listemanga):
	sorted_list = []
	sorted_list = sorted(listemanga, key = lambda x: (x.rank))
	return sorted_list

def determine_most(sent, arr):
        global last_theme
        scores = []
        for i in range(len(arr)):
                sc = 0
                for s in arr[i]:
                        for w in sent:                                
                                if s==w:
                                        sc+=1
                scores.append(sc)
        i = f.max_index(scores, last_theme)
        last_theme = i
        return i

def determine_act(sent, arr):
        scores = []
        for i in range(len(arr)):
                sc = 0
                for s in arr[i]:
                        for w in sent:                                
                                if s==w:
                                        sc+=1
                scores.append(sc)
        i = f.max_index(scores, 0)
        return i

# detects manga name in a sentence
def update_manga(sent, mlist):
        global curr1
        global curr2
        first = 0
        count = 0
        for m in mlist:
                titl=f.tokenise_en(m.title)
                if m.title != curr1 and f.contains_arr(sent, titl) >= 0.6:
                    new_current(m)

# detects manga gere in a sentence
def determine_genre(sent):
	global list_genre
	genres = []
	for w in sent:
		for genre in list_genre:
			if w.lower() == genre.lower():
				genres.append(genre)
	return genres

# find manga corresponding to a set of genres
def find_manga(crit, sorted_manga):
	global proposed_mangas
	if crit is not None:
		nb_crit = len(crit)
		if nb_crit==0:
			return "There is no manga with these genres"
		for manga in sorted_manga:
			flag=True
			for c in crit:
				if in_manga_list(manga.title,proposed_mangas,c):
					flag=False
					break
			if set(crit).issubset(manga.genres) and flag:
				new_propositions(manga, crit)
				new_current(manga)
				return "This matches perfectly with " + manga.title

		for manga in sorted_manga:	
			for genre in manga.genres:
				if genre in crit and in_manga_list(manga.title,proposed_mangas, genre)==False:
					new_proposition(manga, genre)
					new_current(manga)
					return "I could propose you " + manga.title
	return None

def run():
	file = open('mangalistfinal', 'r+b')
	

	#Uncomment the following part to create the mangalist file containing the number of mangas you chose with the create_manga_list function. 

	'''manga_list = []
	list_manga = create_manga_list(500)
	for manga in list_manga:
		genres = []
		for g in manga.genres:
			genres.append(g.name)

		authors = []
		for a in manga.authors:
				authors.append(a.name)

		characters = []
		for c in manga.characters:
			characters.append(c.name)

		m = Manga(manga.title, manga.popularity, genres, manga.favorites, float(manga.score[0]), manga.chapters, manga.published[0], authors, characters)
		manga_list.append(m)


	pickle.dump(manga_list, file)
	print("ajout manga---")'''
	
	global sorted_manga
	global list_genre
	global proposed_mangas
	global sentence

	listemangafini = []
	listemangafini = pickle.load(file)
	sorted_manga = order_by_rank(listemangafini)
	nbmanga = 0
	for manga in listemangafini:
		for genres in manga.genres:
			if genres not in list_genre:
				list_genre.append(genres)
				newGenre = []
				newGenre.append(genres)
				newGenre.append([])
				proposed_mangas.append(newGenre)

	new = 0
	
	global avg_mark
	global avg_chap
	global avg_fav
	global avg_year
	global avg_char
	
	avg_mark = calc_avg(4)
	avg_chap = calc_avg(5)
	avg_fav = calc_avg(3)
	avg_year = calc_avg(6)
	avg_char = calc_avg(8)
	
	while(True):
		sentence = input("You: ")
		sent = f.tokenise_en(sentence)
		
		th = determine_most(sent, vocabSubject)
		update_manga(sent, sorted_manga)
		action = determine_act(sent, actionToDo)
		print("Bot: ",end='')
		if action==4:
			g = []
			g = determine_genre(sent)
			f.type(str(act(th, action, is_question(sent), g)))
		else:
			f.type(str(act(th, action, is_question(sent))))
		# TODO : Avec une certaine proba appeler le mode 2 ?




	
		

		
	
	
	
    

