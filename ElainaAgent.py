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
			pygame.time.wait(500)

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
					self.myGame.cards.remove(cardspr)
					
					self.myGame.updateOverlap()
					self.myGame.updateGraphics()
					super().removeCard(card)
					return
 
