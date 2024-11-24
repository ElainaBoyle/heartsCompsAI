'''

'''
from Player import Player
import psycopg2





class Cbr_Agent(Player):


    myCardSuits = [3, 4, 1, 2] #number of clubs, diamonds, spades, hearts in my hand
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

    def countTotalRank(hand):
        total = 0
        for card in hand:
            total += card.rank
        return total


    #Check each hand for similarity, return id with highest similarity
    def determineSimilarity(self, array):
        #to start, just pick the hand with the closest total rank
        myTotal = self.countTotalRank(self.hand)
        closestHandValue = 10000000000000


        for game in array: #game[0] is hand, game[1] is next move.
            if abs(self.countTotalRank(game[0]) - myTotal) < closestHandValue:
                winMove = game[1]
                closestHandValue = self.countTotalRank(game[0])

        return winMove
                
 
    




    def findSimilar(self, myCardSuits, curTrump):

        database = "mock_data" 
        user = "aicomps"
        host= 'localhost'
        password = "12345"
        port = 5432
        

        outputArray = []

        try:
            conn = psycopg2.connect(database, user, password, host, port)
            print("Database connected successfully. MS")
        except:
            print("Database not connected successfully. MS")

        cur = conn.cursor()
        cur.execute("SELECT * FROM heartsai_data WHERE cardSuits = " + myCardSuits + " AND Trump =" + curTrump) 
        rows = cur.fetchall()
        for data in rows:
            outputArray.append([data[2], data[4]]) #[[Hand, nextMove], [hand, nextMove], ....]
            
        return outputArray


    def interpolateMove(self, move):
        
            theirRank = move[0]
            theirSuit = move[1]
            if theirSuit == 'c': theirSuit = 0
            elif theirSuit == 'd': theirSuit = 1
            elif theirSuit == 's': theirSuit = 2
            elif theirSuit == 'h': theirSuit = 3
            else: print("Invalid suit for theirWinMove in pickMyMove. MS")
    
            myCardsOfSuit = self.hand[theirSuit]

            difference = 13
            myMove = card(10, -1) #Mary Sue's default card to play is the 10 of Nothings
            for card in myCardsOfSuit:
                curDiff = abs(move.rank - card.rank())
                if curDiff < difference:
                    myMove = card
                    difference = curDiff
            if difference == 13: print("No similar cards in interpolateMove. MS")

            return myMove

        
            
            
            

    def play(self, option='play', c=None, auto=True):

        curTrump = self.curTrick.suit.string

        #if c was specified, plays c (should probably only really happen w/ 2c), else does cbr stuff
        if c == None:
            #set up variables for easy access to information
            numHearts = len(self.hand.hearts)
            numSpades = len(self.hand.spades)
            numClubs = len(self.hand.clubs)
            numDiamonds = len(self.hand.diamonds)





            myCardSuits = [numClubs, numDiamonds, numSpades, numHearts]

            array = self.findSimilar(myCardSuits, curTrump)


            

            if array.count() == 0:
                return self.hand.getRandomCard()
            else:
                move = self.determineSimilarity(array)
                
                return self.interpolateMove(move)




            





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
