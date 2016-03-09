
import SATSolver

# Initialize important variables
caseFile = "casefile"
players = ["scarlett", "mustard", "white", "green", "peacock", "plum"]
locations = players + [caseFile]
suspects = ["mustard", "plum", "green", "peacock", "scarlett", "white"]
weapons = ["knife", "candlestick", "revolver", "rope", "pipe", "wrench"]
rooms = ["hall", "lobby", "dining", "kitchen", "ballroom", "conservatory", "billiard", "library", "study"]
cards = suspects + weapons + rooms

def getPairNumFromNames(player,card):
    return getPairNumFromPositions(locations.index(player),
                                   cards.index(card))

def getPairNumFromPositions(player,card):
    return player*len(cards) + card + 1


def initialClauses():
    global players, locations, weapons, rooms, cards, suspects, caseFile

    clauses = []

    # Each card is in at least one place (including case file).
    for c in cards:
        clauses.append([getPairNumFromNames(p,c) for p in locations])

    # A card cannot be in two places.
    for card in cards:
        for l1 in locations:
            for l2 in locations:
                if l1 != l2:
                    clauses.append([(-1)*getPairNumFromNames(l1,card),(-1)*getPairNumFromNames(l2,card)])


    # At least one card of each category is in the case file.
        clauses.append([getPairNumFromNames(caseFile,w) for w in weapons])
        clauses.append([getPairNumFromNames(caseFile,r) for r in rooms])
        clauses.append([getPairNumFromNames(caseFile,p) for p in suspects])

    # No two cards in each category can both be in the case file.
    for w1 in weapons:
        for w2 in weapons:
            if w1 != w2:
                clauses.append([(-1)*getPairNumFromNames(caseFile,w1), (-1)*getPairNumFromNames(caseFile,w2)])

    for w1 in rooms:
        for w2 in rooms:
            if w1 != w2:
                clauses.append([(-1)*getPairNumFromNames(caseFile,w1), (-1)*getPairNumFromNames(caseFile,w2)])

    for w1 in suspects:
        for w2 in suspects:
            if w1 != w2:
                clauses.append([(-1)*getPairNumFromNames(caseFile,w1), (-1)*getPairNumFromNames(caseFile,w2)])

    return clauses
# end initialClauses


def hand(player,cards):
    clauses = []
    for card in cards:
        clauses.append([getPairNumFromNames(player,card)])
    return clauses


def suggest(suggester,card1,card2,card3,refuter,cardShown):
    global players

    clauses = []
    if refuter is None:
        for location in players:
            if location != suggester:
                clauses.append([(-1)*getPairNumFromNames(location,card1)])
                clauses.append([(-1)*getPairNumFromNames(location,card2)])
                clauses.append([(-1)*getPairNumFromNames(location,card3)])
    else:
        if not(cardShown is None):
            clauses.append([getPairNumFromNames(refuter,cardShown)])
        else:
            clauses.append([getPairNumFromNames(refuter,card1),getPairNumFromNames(refuter,card2),getPairNumFromNames(refuter,card3)])

        suggesterIndex = players.index(suggester) + 1
        suggesterIndex %= len(players)
        while(players[suggesterIndex] != refuter):
            clauses.append([(-1)*getPairNumFromNames(players[suggesterIndex],card1)])
            clauses.append([(-1)*getPairNumFromNames(players[suggesterIndex],card2)])
            clauses.append([(-1)*getPairNumFromNames(players[suggesterIndex],card3)])
            suggesterIndex += 1 
            suggesterIndex %= len(players)

    return clauses
# end suggest




def accuse(accuser,card1,card2,card3,isCorrect):
    global caseFile

    clauses = []
    clauses.append([(-1)*getPairNumFromNames(accuser,card1)])
    clauses.append([(-1)*getPairNumFromNames(accuser,card2)])
    clauses.append([(-1)*getPairNumFromNames(accuser,card3)])
    if isCorrect:
        clauses.append([getPairNumFromNames(caseFile,card1)])
        clauses.append([getPairNumFromNames(caseFile,card2)])
        clauses.append([getPairNumFromNames(caseFile,card3)])
    else:
        clauses.append([(-1)*getPairNumFromNames(caseFile,card1),(-1)*getPairNumFromNames(caseFile,card2),(-1)*getPairNumFromNames(caseFile,card3)])

    return clauses
# end accuse

def makeMove(clauses):
    global players, weapons, rooms

    guess = []

    hasCard = False


    # Account for if player knows all of one category 
    for pcard in players:
        for player in players:
            if (query(player,pcard,clauses)):
                hasCard = True
                break
        if (not hasCard):
            guess.append(pcard)
            break
        else:
            hasCard = False

    hasCard = False
    for wcard in weapons:
        for player in players:
            if (query(player,wcard,clauses)):
                hasCard = True
                break
        if (not hasCard):
            guess.append(wcard)
            break
        else:
            hasCard = False

    hasCard = False
    for wcard in weapons:
        for player in players:
            if (query(player,wcard,clauses)):
                hasCard = True
                break
        if (not hasCard):
            guess.append(wcard)
            break
        else:
            hasCard = False

    return guess
# end makeMove


def query(player,card,clauses):
    return SATSolver.testLiteral(getPairNumFromNames(player,card),clauses)

def queryString(returnCode):
    if returnCode == True:
        return 'Y'
    elif returnCode == False:
        return 'N'
    else:
        return '-'

def printNotepad(clauses):
    global players, caseFile, cards

    for player in players:
        print '\t', player[:2],
    print '\t', "cf"
    for card in cards:
        print card[:6],'\t',
        for player in players:
            print queryString(query(player,card,clauses)),'\t',
        print queryString(query(caseFile,card,clauses))

def playClue():
    clauses = initialClauses()
    clauses.extend(hand("scarlett",["white", "library", "study"]))
    clauses.extend(suggest("scarlett", "scarlett", "rope", "lobby", "mustard", "scarlett"))
    clauses.extend(suggest("mustard", "peacock", "pipe", "dining", "peacock", None))
    clauses.extend(suggest("white", "mustard", "revolver", "ballroom", "peacock", None))
    clauses.extend(suggest("green", "white", "knife", "ballroom", "plum", None))
    clauses.extend(suggest("peacock", "green", "candlestick", "dining", "white", None))
    clauses.extend(suggest("plum", "white", "wrench", "study", "scarlett", "white"))
    clauses.extend(suggest("scarlett", "plum", "rope", "conservatory", "mustard", "plum"))
    clauses.extend(suggest("mustard", "peacock", "rope", "ballroom", "white", None))
    clauses.extend(suggest("white", "mustard", "candlestick", "study", "green", None))
    clauses.extend(suggest("green", "peacock", "knife", "dining", "peacock", None))
    clauses.extend(suggest("peacock", "mustard", "pipe", "dining", "plum", None))
    clauses.extend(suggest("plum", "green", "knife", "conservatory", "white", None))
    clauses.extend(suggest("scarlett", "peacock", "knife", "lobby", "mustard", "lobby"))
    clauses.extend(suggest("mustard", "peacock", "knife", "dining", "white", None))
    clauses.extend(suggest("white", "peacock", "wrench", "hall", "green", None))
    clauses.extend(suggest("green", "white", "pipe", "conservatory", "plum", None))
    clauses.extend(suggest("peacock", "scarlett", "pipe", "hall", "mustard", None))
    clauses.extend(suggest("plum", "peacock", "pipe", "ballroom", None, None))
    clauses.extend(suggest("scarlett", "white", "pipe", "hall", "peacock", "hall"))
    clauses.extend(suggest("white", "peacock", "pipe", "hall", "peacock", None))
    clauses.extend(suggest("peacock", "peacock", "pipe", "hall", None, None))
    clauses.extend(suggest("scarlett", "green", "pipe", "study", "white", "green"))
    clauses.extend(suggest("mustard", "peacock", "pipe", "ballroom", "plum", None))
    clauses.extend(suggest("white", "peacock", "pipe", "study", "scarlett", "study"))
    clauses.extend(suggest("green", "white", "pipe", "study", "scarlett", "white"))
    clauses.extend(suggest("peacock", "white", "pipe", "study", "scarlett", "white"))
    clauses.extend(suggest("plum", "peacock", "pipe", "kitchen", "green", None))
    print 'Before accusation: should show a single solution.'
    printNotepad(clauses)
    print
    clauses.extend(accuse("scarlett", "peacock", "pipe", "billiard", True))
    print 'After accusation: if consistent, output should remain unchanged.'
    printNotepad(clauses)



if __name__ == '__main__':
    playClue()
