import sys
import re
import time
import random

def max_index(arr):
    sc = arr[0]
    ind = 0
    if len(arr) > 1:
        for i in range(1, len(arr)):
            if arr[i] > sc:
                sc = arr[i]
                ind = i
    return ind

def type(stri):
    v=0
    sys.stdout.flush()
    time.sleep(0.7)
    for v in stri:
        if v == " ":
            time.sleep(random.randint(200,500)/1000)
        print(v, end='')        
        sys.stdout.flush()
        time.sleep(random.randint(30,100)/1000)
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
