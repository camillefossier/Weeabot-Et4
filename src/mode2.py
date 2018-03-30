import argparse
import re
import random
import mode1 as m1
import copy

vocab = []
constVocab = []

def parseVocab(vocab_file):
    global vocab
    global constVocab
    fileV = open(vocab_file, 'r')
    theme = []
    th = -1
    for line in fileV:
        if line == '###\n':
            th = th+1
            i=0
            theme.append({})
            theme[th][i] = []
        elif line == '#\n':
            i=1
            theme[th][i] = []
        else:
            if line == '':
                break
            else:
                theme[th][i].append(line[:-1])
    vocab = theme
    constVocab = copy.copy(theme)

def run():
    vocab_file = "../vocab/vocab.txt"
    parseVocab(vocab_file)
    last = 'NIL'
    over = False
    while(not over):
        print(vocab)
        inp = input('You: ')
        last = answer(inp)
        print('Bot: '+last)
        if inp == 'exit':
            over = True

def answer(sentence):
    # ici il faudra decider si on pose une question par rapport à un certain theme
    # ou si on detecte un "je suis X" etc.
 
    return questionFinder(sentence)

def questionFinder(sentence):
    global vocab
    global constVocab
    sent = tokenise_en(sentence)
    for word in sent:
        i=-1
        for theme in vocab:
            i+=1
            for words in theme[0]:
                
                if word == words : 
                    if len(theme[1])==0:
                        print(constVocab[i][1])
                        theme[1] = constVocab[i][1]
                    question = pickQuestion(theme[1])
                    return question
    return "Hummm"

def pickQuestion(theme):
    question = random.choice(theme)
    theme.remove(question)
    return question


def tokenise_en(sent):

    # deal with apostrophes
    sent = re.sub("([^ ])\'", r"\1 '", sent) # separate apostrophe from preceding word by a space if no space to left
    sent = re.sub(" \'", r" ' ", sent) # separate apostrophe from following word if a space if left

    # separate on punctuation by first adding a space before punctuation that should not be stuck to
    # the previous word and then splitting on whitespace everywhere
    cannot_precede = ["M", "Prof", "Sgt", "Lt", "Ltd", "co", "etc", "[A-Z]", "[Ii].e", "[eE].g"] #non-exhaustive list
                                        
    # creates a regex of the form (?:(?<!M)(?<!Prof)(?<!Sgt)...), i.e. whatever follows cannot be
    # preceded by one of these words (all punctuation that is not preceded by these words is to be
    # replaced by a space plus itself
    regex_cannot_precede = "(?:(?<!"+")(?<!".join(cannot_precede)+"))" 
    
    sent = re.sub(regex_cannot_precede+"([\.\,\;\:\)\(\"\?\!]( |$))", r" \1", sent)

    # then restick several consecutive fullstops ... or several ?? or !! by removing the space
    # inbetween them
    sent = re.sub("((^| )[\.\?\!]) ([\.\?\!]( |$))", r"\1\2", sent) 

    sent = sent.split() # split on whitespace
    return sent

# chatbot psychologue Eliza

# — Quand l’utilisateur dit " Je suis X ", répondre qqchose comme "Pourquoi est-ce que tu es X ? "
# Pensez à implémenter cela pour tous les temps du verbe "être" 

# — Identifiez quelques mots-clés ( "famille" , "parents" . . .) qui correspondent à des sujets de dis-
# cussion avec un psychologue (l’enfance en famille). Lorsque l’un de ces mots-clés est employé par
# l’utilisateur, le chatbot répondra par une question liée à ce sujet. Par exemple, si l’utilisateur écrit
# " On allait souvent en vacances avec mes parents. " , le chatbot pourra répondre " Est-ce que 1vous pensez que la famille est importante ? " .

# Définissez au moins 10 mots clés associés à au
# moins 5 sujets de discussion, et rédigez au moins 2 réponses possibles pour chaque sujet, parmi
# lesquelles le chabot effectuera un choix aléatoire, sans répéter le choix précédent le cas échéant
# (comme pour les backchannels du mode 1).





# fichier à parser :
#       vocabulaire
#       questions associées
#       quand on parse on remplit 2 tableaux, un qui ne bougera plus, et un qui se videra quand on dira une question
#       des que le deuxième est vide on le refill avec le premier
#       plusieurs thèmes possibles : donc un ensemble de themes dans un dossier
#       dans le code cela donnera 
#       comment chercher dans le vocabulaire ? est-ce qu'on fait du most recent used en premier ? parce qu'une discussion reste dans un meme theme
#       donc si on parle de famille, qu'il aille pas a chaque fois rechecker le vocabulaire de la nourriture en premier
#       au final, il nous faut un tableau de themes, chaque case est un tableau a deux dimensions : vocabulaire et questions possibles
