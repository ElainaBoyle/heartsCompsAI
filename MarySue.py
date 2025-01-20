'''

'''
from Player import Player
import psycopg2





class Cbr_Agent(Player):


    #myCardSuits = [3, 4, 1, 2] #number of clubs, diamonds, spades, hearts in my hand
    curTrump = 0


    #get the specified card from hand and returns it
    def playCard(self, cardString):
        return cardString
    
    def update(self, curTrick): #to be called at the beginning of each trick
        curTrump = curTrick.suit



    #hand/trickNum, [Location of cards], winning player, card played, [winning player’s hand]
    #ADD to database:
    #game IDs
    #trump suit
    #suitNums = [numclubs, numdiamonds, numspades, numhearts] //for game-winning player’s hand



    def countTotalRankObj(self, hand):
        total = 0
        for card in hand.clubs:
            total += card.value
        for card in hand.diamonds:
            total += card.value
        for card in hand.spades:
            total += card.value
        for card in hand.hearts:
            total += card.value
        return total
    
    def countTotalRankStr(self, hand):
        hand = hand[1:-1].split(", ")
        total = 0
        for card in hand:
            total += int(card[:-1])
        return total

    #Checks each frame in the array for similarity, return the next move of the frame with highest similarity
    def mostSimilar(self, array):
        #to start, just pick the hand with the closest total rank
        myTotal = self.countTotalRankObj(self.hand)
        closestHandValue = 10000000000000

        for game in array: #game[0] is hand, game[1] is next move.
            if abs(self.countTotalRankStr(game[0]) - myTotal) < closestHandValue:
                winMove = game[1]
                chosen_game = game[2]
                closestHandValue = self.countTotalRankStr(game[0])
        #print(chosen_game)
        return winMove
                
    #finds similar game moments to the current one and returns them in a list
    def findSimilarFrames(self, myCardSuits, curTrump):

        database = "heartsai_data" 
        user = "aicomps"
        host= 'localhost'
        password = "12345"
        port = 5432
        


        try:
            conn = psycopg2.connect(database = "heartsai_data", user = "aicomps", host= 'localhost', password = "12345", port = 5432)
            #print("Database connected successfully. MS")
        except:
            print("Database not connected successfully. MS")

        cur = conn.cursor()
        cur.execute(("SELECT winning_hand, card_played, trick_id FROM heartsai_data WHERE clubs = cast({0} as varchar)" +
                    " AND diamonds = CAST({1} as Varchar)" +
                    " AND spades = CAST({2} as Varchar)" +
                    " AND hearts = CAST({3} as Varchar)" +
                    " AND trump_suit = CAST('{4}' as Varchar)").format (myCardSuits[0], myCardSuits[1], myCardSuits[2], myCardSuits[3], curTrump)) 
        
        frames = cur.fetchall()
            
        return frames

    #takes in a move and plays the closet move possible
    def interpolateMove(self, move):
        
            theirRank = move[:-1]
            theirSuit = move[-1:]
            if theirSuit == 'c': theirSuit = 0
            elif theirSuit == 'd': theirSuit = 1
            elif theirSuit == 's': theirSuit = 2
            elif theirSuit == 'h': theirSuit = 3
            else: print("Invalid suit for theirWinMove in pickMyMove. MS")
    
            myCardsOfSuit = self.hand.hand[theirSuit]

            difference = 13
            myMove = None
            for card in myCardsOfSuit:
                curDiff = abs(int(move[:-1]) - card.value)
                if curDiff < difference:
                    #print("found a better card", card)
                    myMove = card
                    difference = curDiff
                #else:
                    #print("didn't find a better card")
            if difference == 13: 
                print("No similar cards in interpolateMove. MS")
                myMove = self.hand.getRandomCard()

            return myMove

    #de facto main method, where the play pattern is usually run
    def play(self, option='play', c=None, auto=True):

        curTrump = self.curTrick.suit.string

        #if c was specified, plays c (should probably only really happen w/ 2c), else does cbr stuff
        if c == None:

            #Key Variables
            numHearts = len(self.hand.hearts)
            numSpades = len(self.hand.spades)
            numClubs = len(self.hand.clubs)
            numDiamonds = len(self.hand.diamonds)

            myCardSuits = [numClubs, numDiamonds, numSpades, numHearts]
            frames = self.findSimilarFrames(myCardSuits, curTrump)
            #print(curTrump)

            if len(frames) == 0:
                return self.hand.getRandomCard()
            else:
                move = self.mostSimilar(frames)
                #print("ideal move is %s" % move)
                actualmove = self.interpolateMove(move)
                #print("actual move is %s" % move)
                return actualmove

        #sets card equal to the card specified by c, currently only used for the 2 of clubs
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
