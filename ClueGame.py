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
    def __init__(self, totalPlayers=6):
    	if (totalPlayers < 1) or (totalPlayers > 6):
    		print "please enter between 1 and 6 players"
    		exit(10)
    	global numPlayers
        self.playerReasoners = []
        self.playerTurn = 0
        numPlayers = totalPlayers
        cards = suspects + weapons + rooms
        random.shuffle(cards)
        self.hands = {}
        caseFile.append(suspects[random.randint(0,len(suspects)-1)])
        caseFile.append(weapons[random.randint(0,len(weapons)-1)])
        caseFile.append(rooms[random.randint(0,len(suspects)-1)])
        print "case file:",caseFile

        del cards[cards.index(caseFile[0])]
        del cards[cards.index(caseFile[1])]
        del cards[cards.index(caseFile[2])]

        for i in xrange(0, numPlayers):
            self.hands[i] = []

        for j in xrange(0,len(cards)):
            self.hands[j%numPlayers].append(cards[j])

        cards = suspects + weapons + rooms
            
        for k in xrange(0, numPlayers):
            self.playerReasoners.append(CluePlayer.CluePlayer(players[k],self.hands[k],"reasoner"))

    def startGame(self):
        while (self.playNextTurn()):
            self.playerTurn = (self.playerTurn + 1)%numPlayers
        del caseFile[:]
    
    def playNextTurn(self):
        guess = self.playerReasoners[self.playerTurn].makeMove()
        index = (self.playerTurn + 1) % numPlayers
        if (guess[-1] == "s"):
            refuteResult = None
            didRefute = False
            while (index != self.playerTurn):
                refuteResult = self.playerReasoners[index].refute(guess[0:3])
                if not(refuteResult is None):
                    didRefute = True
                    break
                index = (index + 1) % numPlayers
            if not(refuteResult is None):
                print self.playerReasoners[self.playerTurn].name + " SUGGESTS " + guess[0] + " killed with a " + guess[1] + " in the " + guess[2] + ". Refuted by " + self.playerReasoners[index].name + " with card " + refuteResult
            else:
                print self.playerReasoners[self.playerTurn].name + " SUGGESTS " + guess[0] + " killed with a " + guess[1] + " in the " + guess[2] + ". Not refuted."

            for j in range(0,numPlayers-1):
                if not(refuteResult is None):
                    if (j==self.playerTurn):
                        self.playerReasoners[j].suggest(self.playerReasoners[self.playerTurn].name,guess[0],guess[1],guess[2],self.playerReasoners[index].name,refuteResult)
                    else:
                        self.playerReasoners[j].suggest(self.playerReasoners[self.playerTurn].name,guess[0],guess[1],guess[2],self.playerReasoners[index].name,None)
                else:
                    self.playerReasoners[j].suggest(self.playerReasoners[self.playerTurn].name,guess[0],guess[1],guess[2],None,None)
        else:
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
        return True



                






    
    
