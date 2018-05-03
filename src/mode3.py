import requests
import pickle
#import myanimelist.manga
#import myanimelist.session as mals
import functions as f
import random

sorted_manga = []
list_genre = []
list_manga_matched = []

curr1 = None
curr2 = None
last_theme=9


# TODO: Faire comme pour le mode 2
# Un fichier qui contient les mots à détecter et des formulations pour répondre
vocabSubject = [
        ['title', 'name', 'called'],
        ['rank', 'ranked'],
        ['genre', 'type'],
        ['favorites'],
        ['rated', 'score', 'mark', 'good', 'bad'],
        ['number', 'chapters', 'long', 'short', 'finished', 'over'],
        ['When', 'old', 'recent', 'published', 'date'],
        ['author', 'wrote', 'written', 'created'],
        ['characters', 'character']
        ]

actionToDo = [
        [], # info about the current one
        ['are', 'compare', 'between', 'and', 'two'], # compare curr1 and curr2 on a criteria
        ['the', 'best', 'highest', 'biggest', 'all', 'first'], # give the best on one criteria
        ['the', 'worst', 'all', 'last'], # and the worst
        ['which', 'manga', 'can', 'suggest', 'and'] # find a manga with a particularity
        ]

def act(nb, ac, crit=None, second=0):
        if ac==0:
                return give_info(nb)
        elif ac==1:
                return compare(nb)
        elif ac==2:
                return highest(nb, sorted_manga)
        elif ac==4:
        		return find_manga(crit, sorted_manga, second)
  

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
        		#TODO mode 1 ou 2 ?
                return get_subject(random.randint(0,8), manga)

def give_info(nb):
        if curr1 == None:
            	#print("Bot: ",end='')
                return 'What manga are you talking about ?'
        else:
                return get_subject(nb, curr1)

def compare(nb):
        if curr1 == None:
                return 'You did not give me any manga name...'
        elif curr2 == None:
                return 'You forgot to mention another manga...'
        else:
                return str(get_subject(nb, curr1))+" and "+str(get_subject(nb, curr2))

def highest(nb, mlist):
        if nb==0 or nb==2 or nb==6 or nb==7 or nb==8:
                return "You did not give me a good criteria..."
        else:
                if nb == 1:
                        coef=-1
                else:
                        coef=1
                sc = coef*get_subject(nb, mlist[0])
                manga = mlist[0]
        for m in mlist:
                try:
                        tmp = coef*get_subject(nb, m)
                        if tmp > sc:
                                sc = tmp
                                manga = m
                except:
                        1
        return str(manga.title)+" : "+str(get_subject(nb, manga))
                        
                


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
        
def update_manga(sent, mlist):
        global curr1
        global curr2
        count = 0
        for m in mlist:
                titl=f.tokenise_en(m.title)
                if m.title != curr1 and f.contains_arr(sent, titl) >= 0.6:
                    curr2 = curr1
                    curr1 = m
                    break
                    # EUH attention aux histoires de copies là c ptet du pointeur

def determine_genre(sent):
	global list_genre
	genres = []
	for w in sent:
		for genre in list_genre:
			if w == genre:
				genres.append(genre)
	return genres

def find_manga(crit, sorted_manga, second):
	global list_manga_matched
	if crit is not None:
		nb_crit = len(crit)
		if nb_crit==0:
			return "There is no manga with this genres"
		for manga in sorted_manga:
			print("here")
			if set(crit).issubset(manga.genres):
				if second==0:
					return "It's a perfect match with " + manga.title
				if second==1:
					second -= 1
					continue	
			for genre in manga.genres:
				if genre in crit:
					return "It's match partly with " + manga.title
	return "no match"

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
	listemangafini = []
	listemangafini = pickle.load(file)
	sorted_manga = order_by_rank(listemangafini)
	nbmanga = 0
	for manga in listemangafini:
		for genres in manga.genres:
			if genres not in list_genre:
				list_genre.append(genres)
	print(list_genre)
	#for manga in sorted_manga:
		#nbmanga = nbmanga + 1
		#manga.informations()
		#print("~~~~~~~~~~")
		#print("")
		#print(nbmanga)
		#i = 0
	#for i in range (0, 100):
		#print(sorted_manga[i].title, sorted_manga[i].rank)
	new = 0
	while(True):
		sent = f.tokenise_en(input("You: "))
		th = determine_most(sent, vocabSubject)
		update_manga(sent, sorted_manga)
		action = determine_act(sent, actionToDo)
		print("Bot: ",end='')
		if action==4:
			g = []
			g = determine_genre(sent)
			second = 0
			for w in sent:
				if "another"==w:
					second += 1
				else:
					second += 0
			f.type(str(act(th, action, g, second)))
		else:
        #f.type(str(get_subject(th, curr1)))
			f.type(str(act(th, action)))





	
		

		
	
	
	
    

