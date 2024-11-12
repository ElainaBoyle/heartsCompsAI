'''

'''
from Player import Player

class Cbr_Agent(Player):



    #get the specified card from hand and returns it
    def playCard(self, cardString):
        return cardString




    #hand/trickNum, [Location of cards], winning player, card played, [winning player’s hand]
    #ADD to database:
    #game IDs
    #trump suit
    #suitNums = [numclubs, numdiamonds, numspades, numhearts] //for game-winning player’s hand



    #Check each hand for similarity, return id with highest similarity
    def determineSimilarity(array):
        #to start, just pick the hand with the closest total rank
        myTotal = countTotalRank(self.Hand)
        closestHand = hand()
        closestHandValue = 10000000000000


        for hand in array:
            if abs(countTotalRank(hand) - myTotal) < closestHandValue:
                closestHand = hand
                closestHandValue = countTotalRank(hand)

        return ClosestHand.move
                
    def countTotalRank(hand):
        total = 0
        for card in hand:
            total += card.rank
        return total
    




    def findSimilar(myCardSuits, trump):

        searchString = 'SELECT ID, [winning player’s hand], move FROM CaseBase WHERE suitNums = myCardSuits AND trump suit = trump suit'

        #^ returns array of ids and hands

        #look at all games at the current trick num
        #where the winning player has the same number of each suit
        return array
    

    def interpolateMove(move):
            suit = move.suit #  or something
            myCardsOfSuit = []

            if suit == 0:		#rewrite this as a helper function AFTER looking at database
                myCardsOfSuit = self.clubs
            elif suit == 1:
                myCardsOfSuit = self.diamonds
            elif suit == 2:
                myCardsOfSuit = self.spades
            else:
                myCardsOfSuit = self.hearts

            difference = 13
            myMove = card()
            for card in myCardsOfSuit:
                curDiff = abs(move.rank - card.rank())
                if curDiff < difference:
                    myMove = card
                    difference = curDiff

            return myMove
    

    def play(self, option='play', c=None, auto=True):

        cur_suit = self.curTrick.suit.string

        #if c was specified, plays c (should probably only really happen w/ 2c), else does cbr stuff
        if c == None:
            #set up variables for easy access to information
            numHearts = len(self.hand.hearts)
            numSpades = len(self.hand.spades)
            numClubs = len(self.hand.clubs)
            numDiamonds = len(self.hand.diamonds)





            myCardSuits = [numClubs, numDiamonds, numSpades, numHearts]

            array = self.findSimilar(myCardSuits, cur_suit)


            

            if array is empty:
                return hand.getRandomCard()
            Else:
                move = determineSimilarity(array)
                
                return interpolateMove(move)




            





        #sets card equal to the card specified by c
        else:
            for suit in self.hand.hand:
                for potential in suit:
                    if potential.__str__() == c:
                        card = potential
            


        return card




    ### BROKEN ###
    def passing(self, player_num):
        my_cards = self.boardState[player_num-1].split()
        passing_cards = []

        com_suit = self.most_common_suit(my_cards)
        
        for x in my_cards:
            if x[-1:] != com_suit:
                passing_cards.append(x)
                if(len(passing_cards) == 3):
                    return passing_cards
        return passing_cards
