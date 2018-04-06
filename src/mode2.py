import argparse
import re
import random
import mode1 as m1
import copy

vocab = []
constVocab = []

toBe = [[['I', 'am'], ['Why are you']],
        [['I', 'was'], ['Why were you']],
        [['I', 'have'], ['Why have you']]]

translations = [['my', 'your'],
                ['I', 'you'],
                ['me', 'you']]

irregular = []
regular = []

def parseIrregular(irregular_file):
    global irregular
    file = open(irregular_file, 'r')
    for v in file:
        irregular.append(v.split(','))

def parseRegular(regular_file):
    global regular
    file = open(regular_file, 'r')
    fileW = open('regular.txt', 'w')
    for v in file:
        if v != ''
            irregular.append(v.split(','))
            fileW.print(v)
        
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
    vocab = copy.deepcopy(theme)
    constVocab = copy.deepcopy(theme)

def run():
    vocab_file = "../vocab/vocab.txt"
    irregular_file = '../vocab/irregular.txt'
    parseVocab(vocab_file)
    parseIrregular(irregular_file)
    parseRegular("../vocab/regular.txt")
    last = 'NIL'
    over = False
    while(not over):
        inp = input('You: ')
        last = answer(inp, last)
        print('Bot: '+last)
        if inp == 'exit':
            over = True

def answer(sentence, last):
    # ici il faudra decider si on pose une question par rapport à un certain theme
    # ou si on detecte un "je suis X" etc.
    sent = tokenise_en(sentence)

    ans = findBe(sent)
    if ans == False:
        ans = findVerb(sent)
    if ans == False:
        ans = questionFinder(sent)
    
    if ans==False:
        ans = m1.getRandomWord(ans)
    if ans == last:
        ans = answer(sentence, last)
    return ans

def questionFinder(sent):
    global vocab
    for word in sent:
        i=-1
        for theme in vocab:
            i+=1
            for words in theme[0]:
                
                if word == words : 
                    if len(theme[1])==0:
                        #print(constVocab[i][1])
                        theme[1] = copy.deepcopy(constVocab[i][1])
                    question = pickQuestion(theme[1])
                    return question
    return False

def pickQuestion(theme):
    question = random.choice(theme)
    theme.remove(question)
    return question

# Function to find a use of the verb 'to be'
# Returns a question with the appropriate tense : why are you, why were you
# Or return false if there is not this verb
def findBe(sent):
    for tense in toBe:
        w=0
        while w < len(sent):
            wTmp = w
            i = 0
            ok = True
            while ok==True and i<len(tense[0]):
                if sent[wTmp] != tense[0][i]:
                    ok = False
                i+=1
                wTmp+=1
            if ok==True:
                return (tense[1][0]+findCOD(sent, wTmp)+'?')
            w+=1
    return False

def findVerb(sent):
    w=0
    while w < len(sent):
        if (sent[w]=='I'):
            return (findTense(sent,w+1)+findCOD(sent, w+2)+' ?')
        w+=1
    return False

def findTense(sent, w):
    word = sent[w]
    tense = False
    for v in irregular:
        if tense == False:
            tense = getFormula(v, word)
        else:
            break
    if tense == False:
        for v in regular:
            tense = getFormula(v, word)
    return tense

def getFormula(v,word):
    if word==v[0]:
        return 'Why do you '+v[0]
    elif word==v[1]:
        return 'Why did you '+v[0]
    elif word[len(word)-1] == 'd' and word[len(word)-2] == 'e':
        return 'Why did you '+word[:-1]
    elif word=='will':
        return 'Why will you'
    else:
        return False

def translate(word):
    for w in translations:
        if w[0]==word:
            return w[1]
        elif w[1]==word:
            return w[0]
    return word

def findCOD(sent, w):
    ans=''
    for i in range(w, len(sent)):
        ans+=' '+translate(sent[i])
    return ans

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
