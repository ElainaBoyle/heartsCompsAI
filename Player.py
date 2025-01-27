from Hand import Hand

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
		self.hand.addCard(card)


	def getInput(self, option):
		card = None
		while card is None:
			card = input(self.name + ", select a card to " + option + ": ")
		return card

	def play(self, option='play', c=None, auto=False):
		if auto:
			card = self.hand.getRandomCard()
		elif c is None:
			card = self.getInput(option)
		else:
			card = c
		if not auto:
			card = self.hand.playCard(card)
		return card


	def trickWon(self, trick):
		self.roundScore += trick.points


	def hasSuit(self, suit):
		return len(self.hand.hand[suit.iden]) > 0

	def removeCard(self, card):
		self.hand.removeCard(card)

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
   