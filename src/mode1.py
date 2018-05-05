import random
import functions as f

vocab = []

def parseVocab(vocab_file):
    global vocab
    file = open(vocab_file, 'r')
    for v in file:
        if len(v) > 1:
            vocab.append(v[:-1])
    #print(vocab)

def getRandomWord(last):
    if len(vocab)==0:
        parseVocab('../vocab/vocab_mode1.txt')
    new = vocab[random.randint(0, len(vocab)-1)]
    while new == last:
        new = vocab[random.randint(0, len(vocab)-1)]
    return new

def run():
    last = 'NIL'
    over = False
    while(not over):
        inp = input('You: ')
        last = getRandomWord(last)
        if inp == 'exit':
            over = True
            print('Bot: ', end='')
            f.type('Bye !')
        else:
            print('Bot: ', end='')
            f.type(last)
