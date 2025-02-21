class Card: #value = int representation of rank
	def __init__(self, rank, suit):
     
		
		#Added to allow suits to be written as integers, for Monte convenience.
		suits = ["c","d","s","h"]
		if isinstance(suit, int):
			suit = suits[suit]
  
  
		self.stringRank = str(rank)
		self.suit = suit
		self.value = int(rank)

		if self.value == 11:
			self.stringRank = "J"
		elif self.value == 12:
			self.stringRank = "Q"
		elif self.value == 13:
			self.stringRank = "K"
		elif self.value == 14:
			self.stringRank = "A"
		else:
			self.stringRank = str(rank)

   
		self.rank = self.value # for now.
   		

	def rank(self):
		return self.value

	def getSuitInt(self): 
		suits = ["c","d","s","h"]
		if self.suit in suits:
			return suits.index(self.suit)
		else: return 

	def stringRank(self):
		return str(self.rank)

	def getIden(self): #returns as string
		return self.stringRank + self.suit

	def suit(self):
		return self.suit #will always be a string


	def __lt__(self, other):
		if self.rank() < other.rank():
			return True
		else:
			return False
