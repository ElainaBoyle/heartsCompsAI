from Player import Player
from Card import Card
from GameGraphics import GameGraphics
from Hand import Hand
import pygame
from CardDisp import CardDisp
from Hand import Hand

class ElainaAgent(Player):
		def __init__(self, name="Elaina", auto=False, game=None):
			Player.__init__(self, name, auto)
			self.myGame = game
   
   
			
			
		
		def addCard(self, card):
			#Add cards with graphics
			self.myGame.addCard(card)
			self.hand.addCard(card)

			self.myGame.updateGraphics()
			return

		def play(self, discarded = [], option='play', c=None):
			if c == None:
				cardIden = self.myGame.clickACard()
			else:
				cardIden = c
			print(cardIden)
			card = self.hand.hasCard(cardIden)
			print("Elaina, you picked card", cardIden)
			return card

		def removeCard(self, card):
			for cardspr in self.myGame.cards:
				print(cardspr.getIden(), card.getIden())
				if cardspr.getIden() == card.getIden():
					print("ITS HAPPENING")
					#Move this card to the middle
					cardspr.rect.center = (500, 600)
					self.myGame.cards.remove(cardspr)
					self.myGame.middleCards.add(cardspr)
					
					self.myGame.updateOverlap()
					self.myGame.updateGraphics()
					super().removeCard(card)
					return
			


			
		'''
		def play(self):
			print("YAHOOOO")


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
	'''