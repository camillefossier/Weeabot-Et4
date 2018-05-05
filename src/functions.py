import sys
import re
import time
import random

#returns a number between 0 and 1 to tell how much of b a contains
def contains_arr(a, b):
    sc = 0
    for i in a:
        for j in b:
            try:
                if i.lower()==j.lower():
                    sc+=1
            except:
                if i==j:
                    sc+=1
    return sc/len(b)

def max_index(arr, r=0):
    sc = arr[0]
    ind = 0
    if len(arr) > 1:
        for i in range(1, len(arr)):
            if arr[i] > sc:
                sc = arr[i]
                ind = i
    if sc>0:
        return ind
    else:
        return r

def type(stri):
    v=0
    sys.stdout.flush()
    time.sleep(0.7)
    for v in stri:
        if v == " ":
            time.sleep(random.randint(100,300)/1000)
        print(v, end='')        
        sys.stdout.flush()
        time.sleep(random.randint(10,50)/1000)
    sys.stdout.write("\n")
    return 1

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
