from random import randint
from Card import Card

clubs = 0
diamonds = 1
spades = 2
hearts = 3
suits = ["c", "d", "s", "h"]

class Hand:
	'''
	 Initialize hand
	'''
	def __init__(self):

		self.clubs = []
		self.diamonds = []
		self.spades = []
		self.hearts = []

		self.fullHand = []

		# create hand of cards split up by suit
		self.hand = [self.clubs, self.diamonds,
					self.spades, self.hearts]

		self.contains2ofclubs = False
		self.didContain2ofClubs = False


	'''
	 @RETURN int how many cards in this hand
	'''
	def size(self):
		return len(self.clubs) + len(self.diamonds) + len(self.spades) + len(self.hearts)


	'''
	 Add a card to this hand
	 @PARAM Card card the card you're adding to this hand
	'''
	def addCard(self, card):
  
		self.fullHand.append(card) #add to fullHand variable, previously unused
  
		if card.suit == "c":
			if card.value == 2:
				self.contains2ofclubs = True
				self.didContain2ofClubs = True
			self.clubs.append(card)
		elif card.suit == "d":
			self.diamonds.append(card)
		elif card.suit == "s":
			self.spades.append(card)
		elif card.suit == "h":
			self.hearts.append(card)
		else:
			print('Invalid card')
		return

	def updateHand(self): 
		self.hand = [self.clubs, self.diamonds,
					self.spades, self.hearts]

	def getRandomCard(self):
		cardIndex = randint(0,len(self.fullHand) - 1)
		return self.fullHand[cardIndex]


	'''
	 Checks to see if there is an instance of the specified card in your hand.
	 Note: was written to take in cardStr as a card or as a string.
	 @PARAM cardStr the card you're checking for
	 @RETURN the card object from your hand
	'''
	def hasCard(self, cardStr): 
		if isinstance(cardStr, Card):
			cardStr = cardStr.getIden()
	 
		# see if player has that card in hand
		for card in self.fullHand:
			#print(card.getIden(), cardStr)
			if card.getIden() == cardStr:
				return card

	def removeCard(self, card): 
		cardRemoved = False
  
		#print(card)		
		suit = card.getSuitInt()
   
   
		if card.getIden() == "2c":
			self.contains2ofclubs = False

		for myCard in self.hand[suit]:
			if card.getIden() == myCard.getIden():
				self.hand[suit].remove(myCard)
				self.fullHand.pop(self.fullHand.index(myCard))
				cardRemoved = True
				
		if not cardRemoved:
			print("Error: could not find card ", card.getIden(), " in suit ", card.suit, " which has suitIden ", str(suit))
			return
   
		return card

	def hasOnlyHearts(self):
		return len(self.hearts) == self.size()


	def whatAreMyCards(self): 
		outList = []
		for playerhand in self.hand:
			for card in playerhand:
				outList.append(card.getIden()) 
		return outList
