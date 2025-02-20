from Hand import Hand
from Card import Card

class Player:
	def __init__(self, name, auto=False):
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

	def addCard(self, card):
		print("adding:", card.getIden())
		self.hand.addCard(card)

	def getInput(self, option):
		print("getting input!")
		card = None
		while card is None:
			card = input(self.name + ", select a card to " + option + ": ")
		print("You have selected card", card)
		return card

	#Takes in c as string format
	
	'''
	Returns the card object stored inside the current player's hand.
	@PARAM c the STRING representation of a card [eg: "2c"]
	@RETURN card the corresponding card object from inside the current player's hand
	 '''
	def play(self, discarded, option='play', c=None, auto=False):
		#Check if c is already a card
		if isinstance(c, Card):
			print("Error; Passed in card", c.getIden(), "by", self.name)
			c = c.getIden()
	   
		if c is not None:
			card = self.hand.hasCard(c) #returns card in hand
		elif auto:
			card = self.hand.getRandomCard()
		else: #c is none and auto
			strCard = self.getInput(option)
			card = self.hand.hasCard(strCard)

		print("Selected card", card.getIden())
		return card


	def trickWon(self, trick):
		self.roundScore += trick.points


	def hasSuit(self, card):
		if isinstance(card, str):
			print("Passed in string", card, "in Player.hasSuit")
			suit = Card(5, card).getSuitInt()
		else:
			suit = card.getSuitInt()

		return len(self.hand.hand[suit]) > 0

	def removeCard(self, card):
		if self.hand.hasCard(card):
			self.hand.removeCard(card)
		else:
			print("Error: No card", card.getIden(), "in ", self.name, "'s hand")
		return

	def discardTricks(self):
		self.tricksWon = []

	def hasOnlyHearts(self):
		return self.hand.hasOnlyHearts()

	def updateHistory(self, history):
		"""Updates the history of the tricks for each round"""
		if len(self.trickHistory) < 13:
			  
			strHistory = []
			for item in history:
				strHistory.append(str(item))
			self.trickHistory.append(strHistory)
			self.cardObjTrickHistory.append(history)
		else:
			self.cardObjTrickHistory = []
			self.cardObjTrickHistory.append(history)

			strHistory = []
			for item in history:
				strHistory.append(str(item))
			self.trickHistory = []
			self.trickHistory.append(strHistory)
   
	def updateBoardState(self, boardState, board):
		"""Updates the history of the board"""
		self.boardState = boardState
		self.board = board

	def updateCurTrump(self, trump):
		"""Updates the current trump. Is "unset" if there is no current trump"""
		self.curTrump = trump
   