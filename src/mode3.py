import requests
import pickle
import myanimelist.manga
import myanimelist.session as mals
import functions as f
import random

vocabSubject = [
        ['title', 'name', 'called'],
        ['rank', 'ranked'],
        ['genre', 'type'],
        ['favourites'],
        ['score', 'mark'],
        ['number', 'chapters', 'long', 'short', 'finished', 'over'],
        ['when', 'old', 'recent', 'published', 'date'],
        ['who', 'wrote', 'written', 'created'],
        ['characters', 'character']
        ]

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
        if nb == 0:
                return manga.title
        elif nb == 1:
                return manga.rank
        elif nb == 2:
                return manga.genres
        elif nb == 3:
                return manga.nb_favourites
        elif nb == 4:
                return manga.score
        elif nb == 5:
                return manga.nb_chapters
        elif nb == 6:
                return manga.datePublication
        elif nb == 7:
                return manga.authors
        else:
                return get_subject(random.randint(0,7), manga)
        

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

#TODO:
def determine_theme(sent):
        scores = []
        for i in range(len(vocabSubject)):
                sc = 0
                for s in vocabSubject[i]:
                        for w in sent:                                
                                if s==w:
                                        sc+=1
                scores.append(sc)
        return f.max_index(scores)
                        


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
	listemangafini = []
	listemangafini = pickle.load(file)
	sorted_manga = order_by_rank(listemangafini)
	nbmanga = 0
	for manga in sorted_manga:
		nbmanga = nbmanga + 1
		#manga.informations()
		#print("~~~~~~~~~~")
		#print("")
	print(nbmanga)
	i = 0
	for i in range (0, 100):
		print(sorted_manga[i].title, sorted_manga[i].rank)
	while(True):
                th = determine_theme(f.tokenise_en(input("You : ")))
                print(get_subject(th, sorted_manga[0]))






	
		

		
	
	
	
    

