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
#add discard pile groups of 5 - [playerIndex, C1, C2, C3, C4]


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
	 '''
	def playTrick(self, start):
		
		#Set the start player for the trick
		self.currentTrick.setTrickStarter(start)
		shift = 0
		if self.trickNum == 0 and randomOrder:
			startPlayer = self.players[start]
			startPlayer.curTrick = self.currentTrick
			

   
			addCard = startPlayer.play(self.memory, option="play", c="2c")
			#Build removeCard into addCard???
			startPlayer.removeCard(addCard)

			self.currentTrick.addCard(addCard, start)
			self.memory[-1].append(addCard)

			shift = 1 # alert game that first player has already played
		
		# have each player take their turn
		for i in range(start + shift, start + len(self.players)):
			self.printCurrentTrick()
			self.updatePlayerBoardState() #Added
			curPlayerIndex = i % len(self.players)
			self.printPlayer(curPlayerIndex)
			curPlayer = self.players[curPlayerIndex]
			addCard = None
			curPlayer.curTrick = self.currentTrick 


			while addCard is None: # wait until a valid card is passed
				print(curPlayer.name)
				addCard = curPlayer.play(self.memory, auto=True) # change auto to False to play manually
				print(addCard.getIden())
	

				# the rules for what cards can be played
				# card set to None if it is found to be invalid
				if addCard is not None:

					# if it is not the first trick and no cards have been played,
					# set the first card played as the trick suit if it is not a heart
					# or if hearts have been broken
					if self.trickNum != 0 and self.currentTrick.cardsInTrick == 0:
						if addCard.suit == "h" and not self.heartsBroken:
							# if player only has hearts but hearts have not been broken,
							# player can play hearts
							if not curPlayer.hasOnlyHearts():
								print("Hearts have not been broken.")
								print(curPlayer.hand.whatAreMyCards())
								addCard = None
							else:
								self.currentTrick.setTrickSuit(addCard.suit)
						else:
							self.currentTrick.setTrickSuit(addCard.suit)

					# player tries to play off suit but has trick suit
					if addCard is not None and addCard.suit != self.currentTrick.suit:
						if curPlayer.hasSuit(self.currentTrick.suit):
							print("Must play the suit of the current trick.")
							addCard = None
						elif addCard.suit == "h":
							self.heartsBroken = True
							for player in self.players:
								player.heartsBroken = True	

					if self.trickNum == 0:
						if addCard is not None:
							if addCard.suit == "h":
								#print(curPlayer) #commenting this out because it breaks with player objects
								print("Hearts cannot be broken on the first hand.")
								self.heartsBroken = False
								addCard = None
							elif addCard.getIden() == "Qs":
								print("The queen of spades cannot be played on the first hand.")
								addCard = None

					if addCard is not None and self.currentTrick.suit == "":
						if addCard.suit == "h" and not self.heartsBroken:
							print("Hearts not yet broken.")
							addCard = None


					if addCard is not None:
						if addCard == Card(queen, spades):
							self.heartsBroken = True
						curPlayer.removeCard(addCard)

			print("Playing card", addCard.getIden())
			self.currentTrick.addCard(addCard, curPlayerIndex)
			self.memory[-1].append(addCard)
		self.evaluateTrick()
		self.trickNum += 1
		for player in self.players:
			player.trickNum = self.trickNum

	'''
	 Print a single player's hand and round score
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
