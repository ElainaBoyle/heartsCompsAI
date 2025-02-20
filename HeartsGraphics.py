from Deck import Deck
from Card import Card
from Player import Player
from Trick import Trick
from Elek_Agent import Elek_Agent
from BreannaAgent import BreannaAgent
from LevelTen import Strong_agent

#from MarySue import Cbr_Agent
#from MonteCarlo import MonteCarlo 

#ELAINA ADD MARYSUE AND MONTE BACK IN


'''
A copy of Hearts.py with graphics instead of text-based interaction.
'''

#from GameGraphics import GameGraphics


'''
Change auto to False if you would like to play the game manually.
This allows you to make all passes, and plays for all four players.
When auto is True, passing is disabled and the computer plays the
game by "guess and check", randomly trying moves until it finds a
valid one.
'''
auto = False

randomOrder = True

totalTricks = 13
maxScore = 100
queen = 12
noSuit = 0
spades = 2
hearts = 3

class Hearts:
	
	'''
	 Initialize the game
	'''
	def __init__(self):  
		self.roundNum = 0
		self.trickNum = 0 # initialization value such that first round is round 0
		self.dealer = -1 # so that first dealer is 0
		self.currentTrick = Trick()
		self.trickWinner = -1
		self.heartsBroken = False
		self.losingPlayer = None
		self.memory = [] #Trick history

		# Make four players
		self.players = [Strong_agent("Elek", auto=True), Player("B", auto=True), Player("C", auto=True), Player("D", auto=True)]

		'''
		Player physical locations:
		Game runs clockwise

			p3
		p2		p4
			p1

		'''

		# Generate a full deck of cards and shuffle it
		self.newRound()
  
  
	'''
	 Start a new round
	'''
	def newRound(self):
		#Reset variables
		self.roundNum += 1
		self.trickNum = 0
		self.trickWinner = -1
		self.heartsBroken = False
		self.dealer = (self.dealer + 1) % len(self.players)
  
		#Reset Deck
		self.deck = Deck()
		self.deck.shuffle()
		self.dealCards()
  
		#Reset currentTrick
		self.currentTrick = Trick()
		self.currentTrick.setTrickSuit('c') #first suit will always be clubs
  
		#Reset variables for players
		for p in self.players:
			p.trickNum = 0
			p.discardTricks()
			p.heartsBroken = False


	'''
	 Update the scores for each player
	'''
	def handleScoring(self):
		p, highestScore = None, 0
  
		#Check if someone shot the moon
		for player in self.players:
			if player.roundScore == 26: 
				p = player
				player.roundScore = 0
				break

		#Handle shooting the moon
		if p is not None:
			print(p.name + " shot the moon!")
			for player in self.players:
				if player != p:
					player.roundScore = 26
			p = None

		#Add round scores to each player
		for player in self.players:
			player.score += player.roundScore
			player.roundScore = 0

		#Print scores
		print("\nScores:\n")
		for player in self.players:
			print(player.name + ": " + str(player.score))
			if player.score > highestScore:
				p = player
				highestScore = player.score
			self.losingPlayer = p
	
 
	'''
	 Find the player who will start the game
	 @RETURN int index of player with the 2 of Clubs UNLESS randomOrder = False. if not randomOrder, returns 0
	'''
	def getFirstTrickStarter(self):
		if not randomOrder: 
			self.trickWinner = 0
			return 0
		for i,p in enumerate(self.players):
			if p.hand.contains2ofclubs:
				print(i, p.hand.whatAreMyCards())
				self.trickWinner = i
				return i 


	'''
	 Deal cards to each player
	'''
	def dealCards(self):
		for player in self.players:
			for i in range(13):
				player.addCard(self.deck.deal())


	'''
	 Evaluate the trick, update trick history, update player stats
	'''
	def evaluateTrick(self): 
		self.updateTrickHistory() 
		self.trickWinner = self.currentTrick.winner
		p = self.players[self.trickWinner]
		p.trickWon(self.currentTrick)
		self.printCurrentTrick()
		print(p.name + " won the trick.")

		#Add the trick to memory
		#self.memory.append(self.currentTrick)
  
		#Reset the current trick
		self.currentTrick = Trick()
  
		#self.printMemory() #Take this out!
  
  
	'''
	 A helper function that will print all of the tricks stored in our memory. 
	''' 
	def printMemory(self):
		for trick in self.memory:
			trick.getTrickInfo()


	'''
	 Play a trick
	 @PARAM int start the index of the starting player
	'''
	def playTrick(self, start):
	 

		# Set up variables for the whole trick
		self.currentTrick.setTrickStarter(start)
		shift = 0 
		

		if self.trickNum == 0 and randomOrder:
	  
			startPlayer = self.players[start]
			startPlayer.curTrick = self.currentTrick
   
			playCard = startPlayer.play(option="play", c="2c")
			

   
			addCard = startPlayer.play(self.memory, option="play", c="2c")
			#Build removeCard into addCard???
			startPlayer.removeCard(addCard)

			self.currentTrick.addCard(playCard, start)
			self.currentTrick.addCard(addCard, start)
			self.memory[-1].append(addCard)

			shift = 1 # alert game that first player has already played
		
		# have each player take their turn
		for i in range(start + shift, start + len(self.players)):
	  
			#reset variables for each player
			self.printCurrentTrick()
			self.updatePlayerBoardState() #Added
			curPlayerIndex = i % len(self.players)
			self.printPlayer(curPlayerIndex)
			curPlayer = self.players[curPlayerIndex]
			playCard = None
			curPlayer.curTrick = self.currentTrick 


			while playCard is None: # wait until a valid card is passed
				playCard = self.playCard(curPlayer)

			print("Playing card", playCard.getIden())
			curPlayer.removeCard(playCard)
			self.currentTrick.addCard(playCard, curPlayerIndex)

		self.evaluateTrick()
		self.trickNum += 1
		for player in self.players:
			player.trickNum = self.trickNum


	'''
	 Pick a card from the player's hand that the player would like to play.
	 @PARAM Player player the player that is playing
	 @RETURN card playCard the card that this player will play
	'''
	def playCard(self, player):
		
		playCard = player.play(auto=False) # change auto to False to play manually
  
		if playCard is not None:
			#You tried to play a card that's in your hand!
   
			#Are you setting the suit for this trick?
			if self.currentTrick.cardsInTrick == 0:
				#You're the starting player for this trick! Did you pick a hearts card?
				if playCard.suit == "h" and not self.heartsBroken:
					#You're trying to start with a heart and hearts have not been broken!
					if player.hasOnlyHearts():
						#Okay, you can play this heart because you only have hearts left in your hand!
						self.breakHearts()
					else:
						print("You can't play a hearts card to start this trick, Hearts have not been broken!")
						playCard = None
						return None
				#Set the trick suit to the suit of the played card!
				self.currentTrick.setTrickSuit(playCard.suit)
			#You are not setting the suit for this trick. Did you play a card of the correct suit?
			elif playCard.suit != self.currentTrick.suit:
				#Do you have cards of the correct suit?
				if player.hasSuit(playCard):
					print("Play a card of the correct suit! The current suit is:", self.currentTrick.suit)
					playCard = None
   

			# If the player chose the Queen of Spades or a hearts card, hearts are broken.
		if playCard is not None:
			if (playCard.getIden() == "Qs" or playCard.suit == "h"):
				if self.trickNum == 0 and not player.hasOnlyHearts():
					print("Cannot play a point card on the first trick.") #unless you only have point cards.
					playCard = None
				elif not self.heartsBroken:
					self.breakHearts()
	 
		if playCard is None: #If we have not found a card for playCard, try again.
			playCard = self.playCard(player)
				
		return playCard

	 
	'''
	 A helper function for when hearts are broken
	'''
	def breakHearts(self):
		print("Hearts have been broken!")
		self.heartsBroken = True
		for player in self.players:
			player.heartsBroken = True
					

	'''
	 Print a single player's hand and round score
	 @PARAM int i the index of the player you want to print
	'''
	def printPlayer(self, i):
		p = self.players[i]
		print(p.name + "'s hand: ", p.hand.whatAreMyCards())
		print(p.name + "'s round score: " + str(p.roundScore))


	'''
	 Print all players' hands
	'''
	def printPlayers(self):
		for p in self.players:
			print(p.name + ": ", p.hand.whatAreMyCards())


	'''
	 Print the cards played in the current trick
	'''
	def printCurrentTrick(self):
		trickStr = '\nCurrent table:\n'
		trickStr += "Trick suit: " + self.currentTrick.suit.__str__() + "\n"
		for i, card in enumerate(self.currentTrick.trick):
			if (self.currentTrick.trick[i] != 0):
				trickStr += self.players[i].name + ": " + str(card) + "\n"
			else:
				trickStr += self.players[i].name + ": None\n"
  
  
	'''
	 Update the known board for the player in list format
	'''
	def updatePlayerBoardState(self):
		board = []
		boardState = []
		for i, card in enumerate(self.currentTrick.trick):
			if (self.currentTrick.trick[i] != 0):
				boardState.append(card)
				board.append(card)
			else:
				board.append("")
		for player in self.players:
			player.updateBoardState(boardState, board)
			player.updateCurTrump(self.currentTrick.suit.__str__())
	
	
	'''
	 Update the full history of tricks played during each round for the player in list format
	'''
	def updateTrickHistory(self):
		history = []
		for i, card in enumerate(self.currentTrick.trick):
			if (self.currentTrick.trick[i] != 0):
				history.append(card)
			else:
				history.append("")
		for player in self.players:
			player.updateHistory(history)		
  
  
	'''
	 Get the current player with the lowest score
	 @RETURN Player winner the player with the lowest score
	'''
	def getWinner(self):
		minScore = 200 # impossibly high
		winner = None
		for p in self.players:
			if p.score < minScore:
				winner = p
				minScore = p.score
		return winner



def main():
	hearts = Hearts()

	# play until someone loses
	while hearts.losingPlayer is None or hearts.losingPlayer.score < maxScore:
		hearts.memory = []
		while hearts.trickNum < totalTricks:
			print("Round", hearts.roundNum)
			if hearts.trickNum == 0:
				hearts.getFirstTrickStarter()
			print('\nPlaying trick number', hearts.trickNum + 1)
			hearts.memory.append([hearts.trickWinner])
			hearts.playTrick(hearts.trickWinner)

		# tally scores
		hearts.handleScoring()

		# new round if no one has lost
		if hearts.losingPlayer.score < maxScore:
			print("New round")
			hearts.newRound()

	print # spacing
	print(hearts.getWinner().name, "wins!")



if __name__ == '__main__':
	main()
