def parseVocab(vocab_file):
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
    return theme

def run():
    vocab_file = "../vocab/vocab.txt"
    theme = parseVocab(vocab_file)
    print(theme)
    return 0

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
