'''

'''
from Player import Player
import psycopg2


#corgi9812phone



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



    def getDifferenceBuckets(self, hand):

        myLows = 0
        myHighs = 0
        myMeds = 0

        for card in hand.clubs:
            if card.value > 1 and card.value < 8:
                myLows += 1
            elif card.value >= 8 and card.value <= 11:
                myMeds += 1
            else:
                myHighs += 1
        for card in hand.diamonds:
            if card.value > 1 and card.value < 8:
                myLows += 1
            elif card.value >= 8 and card.value <= 11:
                myMeds += 1
            else:
                myHighs += 1
        for card in hand.spades:
            if card.value > 1 and card.value < 8:
                myLows += 1
            elif card.value >= 8 and card.value <= 11:
                myMeds += 1
            else:
                myHighs += 1
        for card in hand.hearts:
            if card.value > 1 and card.value < 8:
                myLows += 1
            elif card.value >= 8 and card.value <= 11:
                myMeds += 1
            else:
                myHighs += 1

        return [myLows, myMeds, myHighs]
    
    def countTotalRankStr(self, hand):
        hand = hand[1:-1].split(", ")
        total = 0
        for card in hand:
            total += int(card[:-1])
        return total
        

    #Checks each frame in the array for similarity, return the next move of the frame with highest similarity

    #Things to add:
    #plays to win trick or not -- requires knowing highest card played so far that trick
    #difference in number of each suit already played out in the game -- may require updating of numbering


    def mostSimilar(self, array):
        #
        buckets = self.getDifferenceBuckets(self.hand)

        for game in array:

            #variables
            #print("trick id is" + game[3])
            hand = game[0]
            cardPlayed = game[1]
            trick_score = int(game[3])
            newTrick = False
            if game[2] == "NA":
                newTrick = True
            highCardRank = None
            highCardSuit = None
            if not newTrick:
                highCardRank = int(game[2][:-1])
                highCardSuit = game[2][-1:]
            cardPlayedRank = int(cardPlayed[:-1])
            cardPlayedSuit = cardPlayed[-1:]
            bestSimilarity = 100000
            winMove = None
            lows = 0
            highs = 0
            meds = 0
            noSimilarCardPenalty = 10
            playingToWin = False
            alignmentPenalty = 10
            queenOfSpades = False
            queenOfSpadesPenalty = 1000

            #calculates alignment penalty
            if not newTrick:
                if cardPlayedRank > highCardRank:
                    playingToWin = True
                index = -1
                if highCardSuit == 'c':
                    index = 0
                if highCardSuit == 'd':
                    index = 1
                if highCardSuit == 's':
                    index = 2
                if highCardSuit == 'h':
                    index = 3
                for card in self.hand.hand[index]:
                    if playingToWin:
                        if card.value > highCardRank:
                            alignmentPenalty = 0
                    else:
                        if card.value < highCardRank:
                            alignmentPenalty = 0
            else: 
                if cardPlayedRank >= 10:
                    playingToWin = True
                for suit in self.hand.hand:
                    for card in suit:
                        if playingToWin:
                            if card.value >= 10:
                                alignmentPenalty = 0
                        else:
                            if card.value < 10:
                                alignmentPenalty = 0


            point_dif = abs(self.curTrick.points - trick_score)

            
            
                        
                 

            

            #counts difference in card value buckets
            for card in hand[1:-1].split(", "):
                if card == '12s':
                    queenOfSpades = True
                rank = int(card[:-1])
                suit = card[-1:]
                if suit == cardPlayedSuit and abs(rank - cardPlayedRank) <= 2:
                    noSimilarCardPenalty = 0
                if rank > 1 and rank < 8:
                    lows += 1
                elif rank >= 8 and rank <= 11:
                    meds += 1
                else:
                    highs += 1
            diffLow = abs(buckets[0] - lows)
            diffMed = abs(buckets[1] - meds)
            diffHigh = abs(buckets[2] - highs)

            #Queen of spades penalty
            if self.hand.hasCard("Qs"): #fix this
                if queenOfSpades:
                    queenOfSpadesPenalty = 0
            else:
                if not queenOfSpades:
                    queenOfSpadesPenalty = 0

            #Big importatant equation, open to lots of changes, this is still pretty simple
            similarityScore = diffLow + diffMed + diffHigh + noSimilarCardPenalty + alignmentPenalty + point_dif + queenOfSpadesPenalty

            if similarityScore < bestSimilarity:
                winMove = game[1]
                bestSimilarity = similarityScore

        return winMove
                
    #finds similar game moments to the current one and returns them in a list
    def findSimilarFrames(self, myCardSuits, curTrump):

        try:
            conn = psycopg2.connect(database = "thomastothe", user = "thomastothe", host= 'localhost', password = "corgi981phone", port = 5432)
            #print("Database connected successfully. MS")
        except:
            print("Database not connected successfully. MS")

        cur = conn.cursor()
        cur.execute(("SELECT winning_hand, card_played, high_card, trick_score, trick_id FROM WoCG_data WHERE clubs = cast({0} as varchar)" +
                    " AND diamonds = CAST({1} as Varchar)" +
                    " AND spades = CAST({2} as Varchar)" +
                    " AND hearts = CAST({3} as Varchar)" +
                    " AND trump_suit = CAST('{4}' as Varchar)").format (myCardSuits[0], myCardSuits[1], myCardSuits[2], myCardSuits[3], curTrump)) 
        
        frames = cur.fetchall()
            
        return frames

    #takes in a move and plays the closet move possible
    def interpolateMove(self, move):
        
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
                    #if card is queen of spades
                    if card.value == 12 and theirSuit == 2:
                        if curDiff == 0:
                            myMove = card
                            difference = curDiff
                    else:
                        myMove = card
                        difference = curDiff
            if difference == 13: 
                print("No similar cards in interpolateMove. MS")
                legalCards = self.getLegalMoves(self.hand.fullHand, self.heartsBroken, (self.trickNum == 1), trump = self.curTrick.suit)
                myMove = self.getRandom(legalCards)

            return myMove

    #de facto main method, where the play pattern is usually run
    def play(self, discarded = [], option='play', c=None, auto=True):

        curTrump = self.curTrick.suit

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
                legalCards = self.getLegalMoves(self.hand.fullHand, self.heartsBroken, (self.trickNum == 1), trump = self.curTrick.suit)
                return self.getRandom(legalCards)
            else:
                move = self.mostSimilar(frames)
                #print("ideal move is %s" % move)
                actualmove = self.interpolateMove(move)
                #print("actual move is %s" % move)
                if actualmove.getIden() == "Qs": #backup method to prevent illegal 12s moves, should be rarely used
                    legalCards = self.getLegalMoves(self.hand.fullHand, self.heartsBroken, (self.trickNum == 1), trump = self.curTrick.suit)
                    return self.getRandom(legalCards)


                return actualmove

        #sets card equal to the card specified by c, currently only used for the 2 of clubs
        else:
            for card in self.hand.fullHand:
                if card.getIden() == c:
                    return card
            
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
