import Clue_Reasoner, random

# Initialize important variables
caseFile = []
players = ["scarlett", "mustard", "white", "green", "peacock", "plum"]
locations = players + [caseFile]
suspects = ["mustard", "plum", "green", "peacock", "scarlett", "white"]
weapons = ["knife", "candlestick", "revolver", "rope", "pipe", "wrench"]
rooms = ["hall", "lobby", "dining", "kitchen", "ballroom", "conservatory", "billiard", "library", "study"]
cards = suspects + weapons + rooms

caseFile.append(players[random.randInt(0,len(players)-1)])
caseFile.append(suspects[random.randInt(0,len(suspects)-1)])
caseFile.append(weapons[random.randInt(0,len(weapons)-1)])

del cards[cards.index(caseFile[0])]
del cards[cards.index(caseFile[1])]
del cards[cards.index(caseFile[3])]
