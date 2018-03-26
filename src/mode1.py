import random

vocab = ['hmm', 'ok', 'i see', 'keep going', 'wow', 'amazing']

def getRandomWord(vocab, last):
    new = vocab[random.randint(0, len(vocab)-1)]
    while new == last:
        new = vocab[random.randint(0, len(vocab)-1)]
    return new

def run():
    last = 'NIL'
    over = False
    while(not over):
        inp = input('You: ')
        last = getRandomWord(vocab, last)
        print('Bot: '+last)
        if inp == 'exit':
            over = True
