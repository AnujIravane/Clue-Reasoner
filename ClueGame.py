import CluePlayer, random

caseFile = []
players = ["scarlett", "mustard", "white", "green", "peacock", "plum"]
locations = players + [caseFile]
suspects = ["mustard", "plum", "green", "peacock", "scarlett", "white"]
weapons = ["knife", "candlestick", "revolver", "rope", "pipe", "wrench"]
rooms = ["hall", "lobby", "dining", "kitchen", "ballroom", "conservatory", "billiard", "library", "study"]
cards = suspects + weapons + rooms
numPlayers = 6
# Initialize important variables
class ClueGame:
    def __init__(self, humans=0, reasoners=6):
    	while (humans + reasoners < 1) or (humans + reasoners > 6):
            print "please enter between 1 and 6 total players"
            humans = int(raw_input("Human players: "))
            reasoners = int(raw_input("Reasoners: "))
    	global numPlayers
        self.playerReasoners = []
        self.playerTurn = 0
        numPlayers = humans + reasoners
        cards = suspects + weapons + rooms
        random.shuffle(cards)
        self.hands = {}
        caseFile.append(suspects[random.randint(0,len(suspects)-1)])
        caseFile.append(weapons[random.randint(0,len(weapons)-1)])
        caseFile.append(rooms[random.randint(0,len(suspects)-1)])

        areHumans = False
        if (humans == 0):
            print "case file:",caseFile
        else:
            areHumans = True
            print "Suspects: ", suspects
            print "Weapons: ", weapons
            print "Rooms: ", rooms

        del cards[cards.index(caseFile[0])]
        del cards[cards.index(caseFile[1])]
        del cards[cards.index(caseFile[2])]

        for i in xrange(0, numPlayers):
            self.hands[i] = []

        for j in xrange(0,len(cards)):
            self.hands[j%numPlayers].append(cards[j])

        cards = suspects + weapons + rooms
            
        for k in xrange(0, numPlayers):
            if (k < humans):
                self.playerReasoners.append(CluePlayer.CluePlayer(players[k], self.hands[k], "human",areHumans))
            else:
                self.playerReasoners.append(CluePlayer.CluePlayer(players[k],self.hands[k],"reasoner",areHumans))


    def startGame(self):
        turns = 0
        while (self.playNextTurn()):
            turns = turns + 1
            self.playerTurn = (self.playerTurn + 1)%numPlayers
        self.reset()
        print "Won in ",turns," moves"

    def reset(self):
        del caseFile[:]
    
    def playNextTurn(self):
        while (self.playerReasoners[self.playerTurn].falseAccuse):
            self.playerTurn = (self.playerTurn + 1)%numPlayers
        guess = self.playerReasoners[self.playerTurn].makeMove()
        index = (self.playerTurn + 1) % numPlayers
        if (guess[-1] == "s"):
            refuteResult = None
            didRefute = False
            while (index != self.playerTurn):
                refuteResult = self.playerReasoners[index].refute(guess[0:3],self.playerReasoners[self.playerTurn].name)
                if not(refuteResult is None):
                    didRefute = True
                    break
                index = (index + 1) % numPlayers
            if not(refuteResult is None):
                print self.playerReasoners[self.playerTurn].name + " SUGGESTS " + guess[0] + " killed with a " + guess[1] + " in the " + guess[2] + ". Refuted by " + self.playerReasoners[index].name + " with card " + refuteResult
            else:
                print self.playerReasoners[self.playerTurn].name + " SUGGESTS " + guess[0] + " killed with a " + guess[1] + " in the " + guess[2] + ". Not refuted."

            for j in range(0,numPlayers):
                if not(refuteResult is None):
                    if (j==self.playerTurn):
                        if(self.playerReasoners[j].type == "reasoner"):
                            self.playerReasoners[j].suggest(self.playerReasoners[self.playerTurn].name,guess[0],guess[1],guess[2],self.playerReasoners[index].name,refuteResult)
                    else:

                        if(self.playerReasoners[j].type == "reasoner"):
                            self.playerReasoners[j].suggest(self.playerReasoners[self.playerTurn].name,guess[0],guess[1],guess[2],self.playerReasoners[index].name,None)
                else:
                    if(self.playerReasoners[j].type == "reasoner"):
                        self.playerReasoners[j].suggest(self.playerReasoners[self.playerTurn].name,guess[0],guess[1],guess[2],None,None)
        else:
            if (self.playerReasoners[self.playerTurn].type == "human" and self.playerReasoners[self.playerTurn].checkHuman(guess[0:3])):
                print "Making an accusation with a card in your hand is not smart. Turn lost."
                return True
            isCorrect = True
            for accusedCards in guess[0:-1]:
                if not(accusedCards in caseFile):
                    isCorrect = False
            for j in range(0,len(self.playerReasoners)):
                self.playerReasoners[j].accuse(self.playerReasoners[self.playerTurn].name,guess[0],guess[1],guess[2],isCorrect)

            if isCorrect:
                print self.playerReasoners[self.playerTurn].name + " ACCUSES " + guess[0] + " killed with a " + guess[1] + " in the " + guess[2] + ". CORRECT GUESS"
                print "Game Over"
                return False
            else:
                print self.playerReasoners[self.playerTurn].name + " ACCUSES " + guess[0] + " killed with a " + guess[1] + " in the " + guess[2] + ". WRONG GUESS"
                self.playerReasoners[self.playerTurn].falseAccuse = True
        return True



                






    
    
