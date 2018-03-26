import mode1 as m1
import mode2 as m2
import mode3 as m3

def runChatbot (mode):
    if mode == '1':
        print('Launching Weeabot 1')
        m1.run()
    elif mode == '2':
        print('Launching Weeabot 2')
        m2.run()
    elif mode == '3':
        print('Launching Weeabot 3')
        m3.run()
    else:
        print("Error, wrong number.")
    
    return 0

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mode')
    args = parser.parse_args()
    mode = (args.mode)
    runChatbot(mode)
