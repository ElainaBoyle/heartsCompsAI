from Card import Card

class Trick:
	
	'''
	Initialize the trick
	'''
	def __init__(self):
		self.trick = [0, 0, 0, 0]
		self.suit = ""
		self.cardsInTrick = 0
		self.points = 0
		self.highest = 0 # rank of the high trump suit card in hand
		self.winner = -1
		self.starter = -1


	'''
	 Reset the trick
	'''
	def reset(self):
		self.trick = [0, 0, 0, 0]
		self.suit = ""
		self.cardsInTrick = 0
		self.points = 0
		self.highest = 0
		self.winner = -1


	'''
	 Set the starter of this trick
	 @PARAM num an integer representing the index of the player who is starting this trick
	'''
	def setTrickStarter(self, num):
		self.starter = num


	'''
	 Set the suit of this trick
	 @PARAM suit a string representing the suit. eg: "s"
	'''
	def setTrickSuit(self, suit):
		self.suit = suit


	'''
	 Add a card to this trick at the specified index
	 @PARAM card a Card that a player is playing
	 @PARAM index an integer representation of the index of the current player
	 Note: cards are stored in the order of Player Indexes. so, even if P1 goes 3rd, their card will be stored in the 0th position.
	'''
	def addCard(self, card, index):
		if self.cardsInTrick == 0: # if this is the first card added, set the trick suit
			self.setTrickSuit(card.suit)
			print('Current trick suit:', self.suit)

		self.trick[index] = card
		self.cardsInTrick += 1

		if card.suit == "h":
			self.points += 1
		elif card.getIden() == "Qs":
			self.points += 13

		if card.suit == self.suit:
			if card.rank > self.highest:
				self.highest = card.rank
				self.winner = index
				print("Highest:",self.highest)
	
 
	'''
	 Prints information about the trick
	 @RETURN list outList a list containing the index of the starter followed by the cards played in the trick. eg: [0, [2c, 5c, 9c, 10c]]
	'''
	def getTrickInfo(self):
		print("Trick Winner:", self.winner)
		print("Trick Starter:", self.starter)
		print("Cards in trick:", self.trick[0].getIden(), self.trick[1].getIden(), self.trick[2].getIden(), self.trick[3].getIden())
		outList = [0,0]
		outList[0] = self.starter
		outList[1] = self.trick
		return outList
