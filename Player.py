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


	'''
	Add a card to this player's hand
	@PARAM card a Card that you want to add to this player's hand
 	'''
	def addCard(self, card):
		print("adding:", card.getIden())
		self.hand.addCard(card)


	'''
	Get input from the player about which card they would like to select
	@PARAM option a string stating if the player would like to play or pass; a relic from passing
	@RETURN str card a string representation of the selected card
 	'''
	def getInput(self, option):
		print("getting input!")
		card = None
		while card is None:
			card = input(self.name + ", select a card to " + option + ": ")
		print("You have selected card", card)
		return card

	
	'''
	Returns the card object stored inside the current player's hand.
	@PARAM c the STRING representation of a card [eg: "2c"]
	@RETURN Card card the corresponding card object from inside the current player's hand
	 '''
	def play(self, option='play', c=None, auto=False):
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


	'''
 	Add the points from the trick to the winning player's score
	@PARAM trick the Trick that we are evaluating
  	'''
	def trickWon(self, trick):
		self.roundScore += trick.points


	'''
	Check to see if this player has cards of the corresponding suit
	@PARAM card a Card of the suit you'd like to check
	Note: card can be a string or a Card
	@RETURN int how many cards of the suit are left in the player's hand
 	'''
	def hasSuit(self, card):
		if isinstance(card, str):
			suit = Card(5, card).getSuitInt() #arbitrarily chose the 5 of whatever suit
		else:
			suit = card.getSuitInt()

		return len(self.hand.hand[suit]) > 0


	'''
	Remove a card from this player's hand
	@PARAM card the Card representation of the card you'd like to remove
	Note: card can be a string or a card, either way should work.
 	'''
	def removeCard(self, card):
		if self.hand.hasCard(card):
			self.hand.removeCard(card)
		else:
			try:
				print("Error: No card", card.getIden(), "in ", self.name, "'s hand")
			except:
				print("Error: No cardstring", card, "in ", self.name, "'s hand")
		return


	'''
 	Discard this player's won tricks
  	'''
	def discardTricks(self):
		self.tricksWon = []


	'''
	Check if this player only has hearts left
	@RETURN bool True if this player only has hearts left
 	'''
	def hasOnlyHearts(self):
		return self.hand.hasOnlyHearts()


	'''
	Update the history of the tricks for each round
	I assume this is used for Monte? 
 	'''
	def updateHistory(self, history):
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
   
   
	'''
 	Update the history of the board
  	'''
	def updateBoardState(self, boardState, board):
		self.boardState = boardState
		self.board = board


	'''
	Updates the current trump. Is "unset" if there is no current trump
 	'''
	def updateCurTrump(self, trump):
		self.curTrump = trump
   