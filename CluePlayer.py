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

class CluePlayer:
        
    def __init__(self,name,hand,type):
        # do nothing
        self.playerHand = hand
        self.name = name
        self.type = type
        self.clauses = self.iClauses()
        self.clauses.extend(self.hand(self.name,hand))
        print self.name, ": ", self.playerHand
        
    def makeMove(self):
        suspects = ClueGame.suspects
        weapons = ClueGame.weapons
        rooms = ClueGame.rooms
        players = ClueGame.players
        if (self.type == "reasoner"):
            guess = self.makeMoveReasoner(self.clauses,self.playerHand) 
            return guess
        return None

    # Initialize important variables

    def getPairNumFromNames(self,player,card):
        return self.getPairNumFromPositions(locations.index(player),
                                       cards.index(card))
    
    def getPairNumFromPositions(self,player,card):
        return player*len(cards) + card + 1
    
    
    def iClauses(self):
        global players, locations, weapons, rooms, cards, suspects, caseFile
    
        clauses = []
    
        # Each card is in at least one place (including case file).
        for c in cards:
            clauses.append([self.getPairNumFromNames(p,c) for p in locations])
    
        # A card cannot be in two places.
        for card in cards:
            for l1 in locations:
                for l2 in locations:
                    if l1 != l2:
                        clauses.append([(-1)*self.getPairNumFromNames(l1,card),(-1)*self.getPairNumFromNames(l2,card)])
    
    
        # At least one card of each category is in the case file.
            clauses.append([self.getPairNumFromNames(caseFile,w) for w in weapons])
            clauses.append([self.getPairNumFromNames(caseFile,r) for r in rooms])
            clauses.append([self.getPairNumFromNames(caseFile,p) for p in suspects])
    
        # No two cards in each category can both be in the case file.
        for w1 in weapons:
            for w2 in weapons:
                if w1 != w2:
                    clauses.append([(-1)*self.getPairNumFromNames(caseFile,w1), (-1)*self.getPairNumFromNames(caseFile,w2)])
    
        for w1 in rooms:
            for w2 in rooms:
                if w1 != w2:
                    clauses.append([(-1)*self.getPairNumFromNames(caseFile,w1), (-1)*self.getPairNumFromNames(caseFile,w2)])
    
        for w1 in suspects:
            for w2 in suspects:
                if w1 != w2:
                    clauses.append([(-1)*self.getPairNumFromNames(caseFile,w1), (-1)*self.getPairNumFromNames(caseFile,w2)])
    
        return clauses
    # end initialClausess
    
    
    def hand(self,player,cards):
        clauses = []
        for card in cards:
            clauses.append([self.getPairNumFromNames(player,card)])
        return clauses
    # end hand
    
    
    def suggest(self,suggester,card1,card2,card3,refuter,cardShown):
        global players
        #print refuter
        #print cardShown
        clauses = []
        if refuter is None:
            for location in players:
                if location != suggester:
                    clauses.append([(-1)*self.getPairNumFromNames(location,card1)])
                    clauses.append([(-1)*self.getPairNumFromNames(location,card2)])
                    clauses.append([(-1)*self.getPairNumFromNames(location,card3)])
        else:
            if not(cardShown is None):
                clauses.append([self.getPairNumFromNames(refuter,cardShown)])
            else:
                clauses.append([self.getPairNumFromNames(refuter,card1),self.getPairNumFromNames(refuter,card2),self.getPairNumFromNames(refuter,card3)])
    
            suggesterIndex = players.index(suggester) + 1
            suggesterIndex %= len(players)
            while(players[suggesterIndex] != refuter):
                clauses.append([(-1)*self.getPairNumFromNames(players[suggesterIndex],card1)])
                clauses.append([(-1)*self.getPairNumFromNames(players[suggesterIndex],card2)])
                clauses.append([(-1)*self.getPairNumFromNames(players[suggesterIndex],card3)])
                suggesterIndex += 1 
                suggesterIndex %= len(players)
    
        self.clauses.extend(clauses)
    # end suggest
    
    
    
    
    def accuse(self,accuser,card1,card2,card3,isCorrect):
        global caseFile
    
        clauses = []
        clauses.append([(-1)*self.getPairNumFromNames(accuser,card1)])
        clauses.append([(-1)*self.getPairNumFromNames(accuser,card2)])
        clauses.append([(-1)*self.getPairNumFromNames(accuser,card3)])
        if isCorrect:
            clauses.append([self.getPairNumFromNames(caseFile,card1)])
            clauses.append([self.getPairNumFromNames(caseFile,card2)])
            clauses.append([self.getPairNumFromNames(caseFile,card3)])
        else:
            clauses.append([(-1)*self.getPairNumFromNames(caseFile,card1),(-1)*self.getPairNumFromNames(caseFile,card2),(-1)*self.getPairNumFromNames(caseFile,card3)])
    
        self.clauses.extend(clauses)
    # end accuse

    def refute(self,rcards):
        temp = range(0,len(self.playerHand))
        random.shuffle(temp)
        for i in temp:
            for card in rcards:
                if (self.playerHand[i] == card):
                    return card
        return None

    
    def makeMoveReasoner(self,clauses,hand):
        global players, suspects, weapons, rooms, locations, caseFile
    
        guess = []
        accuseGuess = []
        knowSuspect = False
        knowWeapon = False
        knowRoom = False
        for pcard in suspects:
            if (self.query(caseFile,pcard,clauses)):
                accuseGuess.append(pcard)
                knowSuspect = True
                break
        for wcard in weapons:
            if (self.query(caseFile,wcard,clauses)):
                accuseGuess.append(wcard)
                knowWeapon = True
                break
        for rcard in rooms:
            if (self.query(caseFile,rcard,clauses)):
                accuseGuess.append(rcard)
                knowRoom = True
                break
        if (knowSuspect and knowWeapon and knowRoom):
            accuseGuess.append('a')
            return accuseGuess
        
    
        
        addedSuspectCard = False
        randomSuspects = suspects
        random.shuffle(randomSuspects)
        for pcard in randomSuspects:
            if (self.query(caseFile,pcard,clauses) is None):
                guess.append(pcard)
                addedSuspectCard = True
                break
        if (not addedSuspectCard):
            guess.append(suspects[random.randint(0,len(suspects)-1)])       
    
            
        
        addedWeaponCard = False
        randomWeapons = weapons
        random.shuffle(randomWeapons)
        for wcard in randomWeapons:
            if (self.query(caseFile,wcard,clauses)):
                guess.append(wcard)
                addedWeaponCard = True
                break
        if (not addedWeaponCard):
            guess.append(weapons[random.randint(0,len(weapons)-1)])        

    
        addedRoomCard = False
        randomRooms = rooms
        random.shuffle(randomRooms)
        for rcard in randomRooms:
            if (self.query(caseFile,rcard,clauses)):
                guess.append(rcard)
                addedRoomCard = True
                break
        if (not addedRoomCard):
            guess.append(rooms[random.randint(0,len(rooms)-1)])
        guess.append("s") 
        return guess
    # end makeMove
    
    
    def query(self,player,card,clauses):
        return SATSolver.testLiteral(self.getPairNumFromNames(player,card),clauses)
    # end self.query

    def queryString(self,returnCode):
        if returnCode == True:
            return 'Y'
        elif returnCode == False:
            return 'N'
        else:
            return '-'
    # end self.queryString

    def printNotepad(self,clauses):
        global players, caseFile, cards
    
        for player in players:
            print '\t', player[:2],
        print '\t', "cf"
        for card in cards:
            print card[:6],'\t',
            for player in players:
                print self.queryString(self.query(player,card,clauses)),'\t',
            print self.queryString(self.query(caseFile,card,clauses))
    # end printNotepad
