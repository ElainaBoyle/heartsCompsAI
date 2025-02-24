import random as rand
from Card import Card

minRank = 2
maxRank = 15
suits = ["c", "d", "s", "h"]

class Deck:
	def __init__(self): 
		self.deck = []
		for suit in suits:
			for rank in range(minRank,maxRank):
				self.deck.append(Card(rank, suit))

	def __str__(self):
		deckStr = ''
		for card in self.deck:
			deckStr += card.__str__() + '\n'
		return deckStr

	def shuffle(self):
		rand.shuffle(self.deck)

	def deal(self): 
		return self.deck.pop(0)

	def sort(self):
		self.deck.sort()

	def size(self):
		return len(self.deck)

	def addCards(self, cards):
		self.deck += cards