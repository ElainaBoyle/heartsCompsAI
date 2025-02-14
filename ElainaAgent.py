from Player import Player
from Card import Card
from GameGraphics import GameGraphics
from Hand import Hand

class ElainaAgent(Player):
    	def __init__(self, name="Elaina", auto=False):
			self.name = name
			self.hand = Hand()
			self.score = 0
			self.roundScore = 0
			self.tricksWon = []															#p1, p2, p3, p4
			self.boardState = [] #Hold the current known board state by player index ex [8c, "", "" ,2c]
			self.board = [] #Hold the current known board state as played cards [8c, 2c]
			self.curTrump = ""
			self.heartsBroken = False
			self.curTrick = None
			self.trickHistory = [] #Holds the history of the each rounds of tricks in string form
			self.cardObjTrickHistory = [] #Holds the history of the each rounds of tricks in card object form
			self.trickNum = 0
   
            self.myGame = GameGraphics()
            
            
        def addCard(self, card):
            #Add cards with graphics
            return
            
        def play(self):
            self.myGame.setHand(curPlayer.hand.whatAreMyCards())
			print("YAHOOOO")

            self.myGame.formatCards()
            self.myGame.updateGraphics()

            cardIden = self.myGame.clickACard()
            print(cardIden)

            faces = ["J", "Q", "K", "A"]
            suits = ["c", "d", "s", "h"]

            if cardIden[0] in faces:
                thisCardRank = 11 + faces.index(cardIden[0])
            else:
                thisCardRank = int(cardIden[0])

            if cardIden[1] in suits:
                thisCardSuit = int(suits.index(cardIden[1]))
            else:
                thisCardSuit = cardIden[1]

            addCard = Card(thisCardRank, thisCardSuit)
            
            
            
            self.myGame.setHand(curPlayer.hand.whatAreMyCards())
			self.myGame.updateGraphics()
            
        def getInput(self, option):
		    card = None
		    while card is None:
			    card = input(self.name + ", select a card to " + option + ": ")
		    return card