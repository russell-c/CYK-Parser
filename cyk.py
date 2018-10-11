'''
Author: Russell Coke
Program : Simple implementation of the CYK algorithm to parse strings containing a small set of defined words
Date: Sept. 24, 2018
'''
class Tree:
    def __init__(self, phrase = None, startPhrase = None, endPhrase = None, word = None, left = None, right = None, prob = 0.0):
        self.phrase = phrase
        self.startPhrase = startPhrase
        self.endPhrase = endPhrase
        self.word = word
        self.left = left
        self.right = right
        self.prob = prob

# I structured this differently from the rest of the rules to make lookup for each word easier during the initial loop of the function
wordRules = {
    "amy": [
        ["Noun", 0.1]
    ],
    "dinner": [
        ["Noun", 0.2]
    ],
    "fish": [
        ["Noun", 0.2]
    ],
    "streams": [
        ["Noun", 0.1],
        ["Verb", 0.1]
    ],
    "swim": [
        ["Noun", 0.2],
        ["Verb", 0.2]
    ],
    "tuesday": [
        ["Noun", 0.2]
    ],
    "for": [
        ["Prep", 0.5]
    ],
    "in": [
        ["Prep", 0.3]
    ],
    "on": [
        ["Prep", 0.2]
    ],
    "ate": [
        ["Verb", 0.7]
    ]
}

syntaxRules = {
    "S": [
        ["Noun", "Verb", 0.2],
        ["Noun", "VerbAndObject", 0.3],
        ["Noun", "VPWithPPList", 0.1],
        ["NP", "Verb", 0.2],
        ["NP", "VerbAndObject", 0.1],
        ["NP", "VPWithPPList", 0.1]
    ],
    "NP": [
        ["Noun", "PP", 0.8],
        ["Noun", "PPList", 0.2]
    ],
    "PP": [
        ["Prep", "Noun", 0.6],
        ["Prep", "NP", 0.4],
    ],
    "PPList": [
        ["PP", "PP", 0.6],
        ["PP", "PPList", 0.4]
    ],
    "VerbAndObject": [
        ["Verb", "Noun", 0.5],
        ["Verb", "NP", 0.5]
    ],
    "VPWithPPList": [
        ["Verb", "PP", 0.3],
        ["Verb", "PPList", 0.1],
        ["VerbAndObject", "PP", 0.4],
        ["VerbAndObject", "PPList", 0.2]
    ]
}

# Because these non-terminals need to be keys in chart P too, but they aren't in the syntaxRules dictionary, I list them here
notListed = ["Noun", "Verb", "Prep"]


def cykParse(sentence, wordRules, syntaxRules, notListed):
    N = len(sentence)
    P = {}

    # adding non-terms not listed in syntaxRules list to chart
    for m in notListed:
        P[m] = []
        # creating matrix of size NxN
        for i in range(N):
            P[m].append([])
            for j in range(N):
                # adding placeholder nodes of probability 0 and everything else set to null
                P[m][i].append(Tree())

    # adding keys from syntaxRules list to chart, otherwise same as above
    for m in syntaxRules:
        P[m] = []
        for i in range(N):
            P[m].append([])
            for j in range(N):
                P[m][i].append(Tree())

    # loop that enters the terminals into the chart
    for i in range(N):
        word = sentence[i].lower()

        # if entered word is not defined in the grammar of the language then return
        if(word not in wordRules):
            return "This sentence cannot be parsed"

        for rule in wordRules[word]:
            P[rule[0]][i][i] = Tree(rule[0], i, i, word, None, None, rule[1])
    
    # loop that builds graph by checking rules of the defined non-terms and creating new nodes
    for length in range(1, N):
        for i in range(N-length):
            j = i+length
            for m in syntaxRules:
                P[m][i][j] = Tree(m, i, j, None, None, None, 0.0)
                for k in range(i, j):
                    for rule in syntaxRules[m]:
                        if len(rule) == 2: 
                            continue
                        newProb = P[rule[0]][i][k].prob * P[rule[1]][k+1][j].prob * rule[2]
                        if newProb > P[m][i][j].prob:
                            P[m][i][j].left = P[rule[0]][i][k]
                            P[m][i][j].right = P[rule[1]][k+1][j]
                            P[m][i][j].prob = newProb
    
    return P

def printTree(tree, indent):
    if tree != None:
        for _ in range(indent):
            print(" ", end='')
        print(tree.phrase, end=' ')
        if tree.word != None:
            print(tree.word, end='')
        print()
        printTree(tree.left, indent+3)
        printTree(tree.right, indent+3)

def printChart(P, n):
    printTree(P["S"][0][n-1], 0)
    print("Probability =", P["S"][0][n-1].prob, "\n")

sentences = [
    "Fish swim in streams",
    "Fish in streams swim",
    "Amy ate fish for dinner",
    "Amy ate fish for dinner on Tuesday",
    "Amy ate for"
]

if __name__ == "__main__":
    print("<<<<<<TEST INPUT>>>>>>\n")
    for s in sentences:
        print("--------------------------------")
        print(s, "\n")
        sentence = s.lower().split()
        n = len(sentence)
        P = cykParse(sentence, wordRules, syntaxRules, notListed)

        # if the returned value is a string then print it
        if(isinstance(P, str)):
            print(P, "\n")
        #if probability is zero the string is invalid
        elif(P["S"][0][n-1].prob == 0.0):
            print("This sentence cannot be parsed\n")
        else:
            printChart(P, n)
        print("--------------------------------")
    
    while True:
        print(">>>>>>INPUT>>>>>>\n")
        sentence = (input("Enter a sentence (-1 exits program): ")).lower().split()
        if(sentence[0] == "-1"): break

        print("\n<<<<<<OUTPUT<<<<<<\n")
        n = len(sentence)
        P = cykParse(sentence, wordRules, syntaxRules, notListed)

        # if the returned value is a string then print it
        if(isinstance(P, str)):
            print(P, "\n")
        #if probability is zero the string is invalid
        elif(P["S"][0][n-1].prob == 0.0):
            print("This sentence cannot be parsed\n")
        else:
            printChart(P, n)
