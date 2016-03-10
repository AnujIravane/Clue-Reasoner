#player class

import ClueGame, SATSolver
import random

# Initialize important variables
caseFile = "casefile"
players = ["scarlett", "mustard", "white", "green", "peacock", "plum"]
locations = players + [caseFile]
suspects = ["mustard", "plum", "green", "peacock", "scarlett", "white"]
weapons = ["knife", "candlestick", "revolver", "rope", "pipe", "wrench"]
rooms = ["hall", "lobby", "dining", "kitchen", "ballroom", "conservatory", "billiard", "library", "study"]
cards = suspects + weapons + rooms

class CluePlayer
        
    def __init__(self,name,hand,type):
        # do nothing
        self.hand = hand
        self.name = name
        self.type = type
        self.clauses = initialClauses()
        self.clauses.append(hand(hand))
        
    def makeMove(self):
        suspects = ClueGame.suspects
        weapons = ClueGame.weapons
        rooms = ClueGame.rooms
        players = ClueGame.players
        if (type == "reasoner"):
            guess = self.makeMoveReasoner()       

    # Initialize important variables

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
    # end hand
    
    
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

    def refute(cards):
        temp = [0,1,2]
        random.shuffle(temp)
        for i in temp:
            for card in cards:
                if (query(hand[i]) == card):
                    return card
        return None

    
    def makeMoveReasoner(clauses,hand):
        global players, suspects, weapons, rooms, locations, caseFile
    
        guess = []
    
        hasCard = False
        addedSuspectCard = True
        for pcard in suspects:
            for player in locations:
                if (query(player,pcard,clauses)):
                    hasCard = True
                    break
            if (not hasCard):
                guess.append(pcard)
                addedSuspectCard = True;
                break
            else:
                hasCard = False
    
            
        
        hasCard = False
        addedWeaponCard = False
        for wcard in weapons:
            for player in locations:
                if (query(player,wcard,clauses)):
                    hasCard = True
                    break
            if (not hasCard):
                guess.append(wcard)
                addedWeaponCard = True
                break
            else:
                hasCard = False
                
        
    
        hasCard = False
        addedRoomCard = False
        for rcard in rooms:
            for player in locations:
                if (query(player,rcard,clauses)):
                    hasCard = True
                    break
            if (not hasCard):
                guess.append(rcard)
                addedRoomCard = True
                break
            else:
                hasCard = False
        
    
    
        if ((not addedRoomCard) and (not addedWeaponCard) and (not addedSuspectCard)):
            for pcard in players:
                if (query(caseFile,pcard,clauses):
                    guess.append(pcard)
            for wcard in weapons:
                if (query(caseFile,wcard,clauses):
                    guess.append(wcard)
            for rcard in rooms:
                if (query(caseFile,rcard,clauses):
                    guess.append(rcard)
            guess.append("a")
        else:
            if (not addedSuspectCard):
                guess.append(suspects[random.randInt(0,len(suspects)-1)])
            if (not addedWeaponCard):
                guess.append(weapons[random.randInt(0,len(weapons)-1)])
            if (not addedRoomCard):
                guess.append(rooms[random.randInt(0,len(rooms)-1)])
            guess.append("s") 
        return guess
    # end makeMove
    
    
    def query(player,card,clauses):
        return SATSolver.testLiteral(getPairNumFromNames(player,card),clauses)
    # end query

    def queryString(returnCode):
        if returnCode == True:
            return 'Y'
        elif returnCode == False:
            return 'N'
        else:
            return '-'
    # end queryString

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
    # end printNotepad