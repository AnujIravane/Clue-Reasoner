import CluePlayer, random

caseFile = []
players = ["scarlett", "mustard", "white", "green", "peacock", "plum"]
locations = players + [caseFile]
suspects = ["mustard", "plum", "green", "peacock", "scarlett", "white"]
weapons = ["knife", "candlestick", "revolver", "rope", "pipe", "wrench"]
rooms = ["hall", "lobby", "dining", "kitchen", "ballroom", "conservatory", "billiard", "library", "study"]
cards = suspects + weapons + rooms
# Initialize important variables
class ClueGame:
    
    
    caseFile.append(players[random.randInt(0,len(players)-1)])
    caseFile.append(suspects[random.randInt(0,len(suspects)-1)])
    caseFile.append(weapons[random.randInt(0,len(weapons)-1)])
    
    del cards[cards.index(caseFile[0])]
    del cards[cards.index(caseFile[1])]
    del cards[cards.index(caseFile[2])]
    
    numPlayers = 6
    
    def __init__(self):
        # nothing to see here. Move along
        self.playerReasoners = []
        self.playerTurn = 0
        random.shuffle(cards)
        self.hands = {}
        for i in xrange(0, numPlayers-1):
            hands[i] = []
            
        for j in xrange(0,len(cards)-1):
            hands[j%numPlayers].append(cards[j])
           
        for k in xrange(0, numPlayers-1):
            playerReasoners.append(CluePlayer.CluePlayer(players[k],hand[k],"reasoner"))
    
    def playNextTurn(self):
    	

    
    
