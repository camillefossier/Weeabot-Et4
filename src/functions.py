import sys
import time
import random

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
