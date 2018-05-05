import argparse
import re
import random
import mode1 as m1
import copy
import functions as f

vocab = []
constVocab = []

toBe = [[['I', 'am'], ['Why are you']],
        [['I', 'was'], ['Why were you']],
        [['I', 'have'], ['Why have you']]]

translations = [['my', 'your'],
                ['me', 'you'],
                ['I', 'you'],
                ['was', 'were']]

irregular = []
regular = []

dejaVu = ['I have a feeling of déjà vu', "Haven't you already said that ?", "Stop saying the same thing over and over !", 'You parrot !', 'Morgan would hate the way you keep repeating yourself !', "You know what, I'll pretend this is normal..."]
dejaVuCursor = -1

def parseIrregular(irregular_file):
    global irregular
    file = open(irregular_file, 'r')
    for v in file:
        irregular.append(v.split(','))

def parseRegular(regular_file):
    global regular
    file = open(regular_file, 'r')
    for v in file:
        regular.append(v[:-1])
        
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
    last = ""
    lastInp = ""
    while(not over):
        inp = input('You: ')
        if inp == 'exit':
            over = True
            print('Bot: ', end='')
            f.type('Bye !')
        else:
            readDejaVu(inp, lastInp)
            last = answer(inp, last)
            print('Bot: ', end='')
            f.type(last)
        lastInp = copy.deepcopy(inp)

def readDejaVu(inp, last):
    global dejaVuCursor
    if inp == last:
        if dejaVuCursor < len(dejaVu)-1:
            dejaVuCursor+=1
            print("Bot: ",end='')
            f.type(dejaVu[dejaVuCursor])

    else:
        if dejaVuCursor >= 0:
            dejaVuCursor -= 1
        

def answer(sentence, last):

    sent = f.tokenise_en(sentence)
    useMode1 = False
    ans = questionFinder(sent)
    if ans == False:
        ans = findVerb(sent)
    if ans == False:
        ans = findBe(sent)
    
    
    if ans==False:
        useMode1 = True
        ans = m1.getRandomWord(last)
    if ans == last and useMode1 == True:
        ans = answer(sentence, last)
    return ans

def questionFinder(sent):
    global vocab
    for word in sent:
        i=-1
        for theme in vocab:
            i+=1
            for words in theme[0]:
                
                if word.lower() == words.lower() : 
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

# finds a verb and returns the correct answer with adapted tense
def findVerb(sent):
    w=0
    while w < len(sent):
        if (sent[w]=='I'):
            cod=findCOD(sent, w+2)
            tens = findTense(sent,w+1)
            if tens != False:
                if len(cod)>0:
                    return ('Why '+str(tens)+cod+' ?')
                else:
                    return ('What '+str(tens)+' ?')
            else:
                return False
        w+=1
    return False

# determines the tense of a sentence
def findTense(sent, w):
    word = sent[w]
    tense = False
    for v in irregular:
        if tense == False:
            if word==v[0]:
                return 'do you '+v[0]
            elif word==v[1]:
                return 'did you '+v[0]
            elif word=='will':
                return 'will you'
            elif word=='would':
                return 'would you'
        else:
            break
    if tense == False:
        for v in regular:
            if word==v:
                return 'do you '+v
            elif word[len(word)-1]=='d' and word[len(word)-2]=='e' and (word[:-1]==v or word[:-2]==v):
                return 'did you '+v
            elif word=='will':
                return 'will you'
            elif word=='would':
                return 'would you'
    return False

# when addressing directly to the bot, the bot has to change the order
# you becomes I, etc.
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
