'''
LevelTen is designed to be a very strong player, at the level of an intermediate to advanced human
It generally uses the 'void' strategy in which it prioritizes creating a void suit which can be used
to dump dangerous cards. Beyond that, it tries to play out the higher cards towards the beginning of
each hand, and attempts to pass control in the last few tricks of the hand. 
'''
from Player import Player
from Card import Card
import random

class Strong_agent(Player):
    
    # Gets the number of cards still in play (not discarded, in hand or in trick) 
    # which are above and in the same suit as the specified card
    def numAbove(self, card, discarded, hand):
        numAbove = 14 - card.value
        for x in hand:
            if x.suit == card.suit and x.value > card.value:
                numAbove -= 1
        for trick in discarded:
            for x in trick[1:]:
                if x.suit == card.suit and x.value > card.value:
                    numAbove -= 1
        return numAbove

    

    # Returns false if there is no effective difference between any of the legal moves
    # and true otherwise. This should cut down on unnecessary computation
    # not yet built, currently just returns true
    def moveMatters(self, adjustedLegalHand):
        if len(adjustedLegalHand) > 1:
            return True
        else:
            return False
    

    #returns all of the possible legal moves
    def getLegalMoves(self, hand, heartsBroken, firstTrick, trump = ''):
        legalMoves = []
        if trump != '':
            for card in hand:
                if card.suit == trump:
                    legalMoves.append(card)
            if len(legalMoves) == 0:
                if not firstTrick:
                    for card in hand:
                        legalMoves.append(card)
                else:
                    for card in hand:
                        if card.suit != 'h' and not card.getIden() == 'Qs':
                            legalMoves.append(card)
        else: # trump is unset
            for card in hand:
                if heartsBroken:
                    legalMoves.append(card)
                elif card.suit != 'h':
                    legalMoves.append(card)

        if len(legalMoves) == 0: #should only happen in some weird edge cases with hands of all hearts, not common at all
            print("You got really lucky to have so many hearts -- or -- there is a bug in the code in getLegalMoves")
            for card in hand:
                legalMoves.append(card)
        return legalMoves

    # not yet built, may never get added
    # Decides if it is worth staying open to shooting the moon
    # Consider if you control a suit well, have lots of high hearts or spades, don't have low hearts, etc
    def shootingMoon(self):
        return False
    
    # Take in a suit and returns the assocated int
    def suitToInt(self, suit): 
        if suit == "c":
            return 0
        elif suit == "d":
            return 1
        elif suit == "s":
            return 2
        elif suit =="h":
            return 3
        else: 
            return 4
        
    # Takes in an int and returns the associated suit    
    def intToSuit(self, int):
        if int == 0:
            return 'c'
        elif int == 1:
            return 'd'
        elif int == 2:
            return 's'
        elif int == 3:
            return 'd'
        else: 
            return "unset"

    # Searches the hand, discard, and trick to find Qs, returns 1, 2, or 3 respectively
    # Returns 4 if Qs is in none of those places (and therefore in someone elses hand)
    def findQs(self, hand, discarded):
        for card in hand:
            if card.getIden() == "Qs":
                return 1
        for trick in discarded[:-1]:
            for card in trick [1:]:
                if card.getIden() == "Qs":
                    return 2
        for card in discarded[-1][1:]:
            if card.getIden() == "Qs":
                return 3
        return 4
    
    # returns the highest card in the specified suit that is below the given rank (high) card
    # if there is no card below the rank card, returns the lowest card in the suit
    def highestBelow(self, hand, suit, high):
        highest = 0
        highestBelow = None
        for card in hand:
            if card.suit == suit:
                if card.value < high and card.value > highest:
                    highest = card.value
                    highestBelow = card
        
        if highestBelow is not None:
            return highestBelow
        
        lowestCard = None
        for card in hand:
            if card.suit == suit:
                if lowestCard is None:
                    lowestCard = card
                elif lowestCard.value > card.value:
                    lowestCard = card

        if lowestCard == None:
            print("highestBelow returned tried to return a None card")
            for card in hand:
                print(card.getIden())
            print(suit)
            #lowestCard = self.getRandom(hand)
        return lowestCard
    
    # Returns the suit that you are currently the longest in (have the most cards in)
    def getLongestSuit(self, suitCounts):
        length = max(suitCounts)
        for i in range (0,4):
            if suitCounts[i] == length:
                return self.intToSuit(i)
            
    # Returns an array with counts for the number of each suit left in play (not discarded or in your hand)
    # [Clubs, Diamonds, Spades, Hearts]
    def getSuitsinPlay(self, suitCounts, discarded):
        suitsinPlay = [13, 13, 13, 13]
        for i in range(0,4):
            suitsinPlay[i] = suitsinPlay[i] - suitCounts[i]
        for trick in discarded:
            for i in range (1,len(trick)):
                if trick[i].suit == 'c':
                    suitsinPlay[0] -= 1
                elif trick[i].suit == 'd':
                    suitsinPlay[1] -= 1
                elif trick[i].suit == 's':
                    suitsinPlay[2] -= 1
                elif trick[i].suit == 'h':
                    suitsinPlay[3] -= 1
        return suitsinPlay
    
    # returns true if any of the players have demonstrated that they do not have any of the suits
    # suits should be an array of chars and players should be an array of integers 0-3
    def playersOut(self, players, suits, discarded):
        for trick in discarded[:-1]:
            trick_starter = trick[0]
            trump = trick[1].suit
            if trump in suits:
                for card in trick[1:]:
                    if card.suit != trump:
                        return True
        return False
    
    # Gets the value of the highcard of the passed in trick
    def getHighCard(self, trick):
        starter = trick[0]
        trump = trick[1].suit
        highCard = 0
        for card in trick[1:]:
            if card.value > highCard and card.suit == trump:
                highCard = card.value
        return highCard

    def getRandom(self, hand):
        return hand[random.randint(0,len(hand)-1)]

    # Determines which card is played when called in hearts.py
    def play(self, discarded = [], option='play', c=None, auto=True):
        
        # for trick in discarded:
        #     print(trick[0])
        #     for card in trick[1:]:
        #         print(card.getIden())
        # print(self.curTrick.suit)
       # print(self.hand.fullHand)

        # for card in self.hand.fullHand:
        #     print(card.getIden())



        if c == None:

            hand = self.hand.fullHand            
            trump = self.curTrick.suit
            trickPosition = len(discarded[-1])
            suitCounts = [len(self.hand.clubs), len(self.hand.diamonds), len(self.hand.spades), len(self.hand.hearts)]
            qsLocation = self.findQs(hand, discarded)
            longestSuit = self.getLongestSuit(suitCounts)
            suitsinPlay = self.getSuitsinPlay(suitCounts, discarded)
            heartsBroken = self.heartsBroken
            firstTrick = False
            if len(discarded) == 1:
                firstTrick = True
            legalMoves = self.getLegalMoves(hand, heartsBroken, firstTrick, trump)

            
            if self.moveMatters(legalMoves):
                if self.shootingMoon():
                    return self.getRandom(legalMoves)
                else: #try to create a void
                    if trickPosition == 1: #you are starting the trick
                        print("starting trick")

                        if suitCounts[2] > 0:
                            if qsLocation != 1 or (suitCounts[2] >= 5): # Qs not in hand or you just have a ton of spades
                                print("tried to play a spades")
                                print(qsLocation)
                                print(suitCounts)
                                return self.highestBelow(legalMoves, 's', 12) # This is a temporary fix, could be improved to consider Ks and As
                            
                        if suitCounts[0] == 1 and not self.playersOut([1,2,3,4], ['c'], discarded):
                            return self.highestBelow(legalMoves, 'c', 15)

                        if suitCounts[1] == 1 and not self.playersOut([1,2,3,4], ['d'], discarded):
                            return self.highestBelow(legalMoves, 'd', 15)


                        #don't want to lead a suit where someone else is out, esp if the Qs is unknown
                        # This stuff is fine but lots could be added, should add more here once I have confirmed that everything generally works
                        #consider how many of the suit you are going to lead in have been played


                        #if none of the above logic is relevant, just lead a high card early and a low card late
                        if len(discarded) > 7:
                            lowest = None
                            for card in legalMoves:
                                if lowest is None:
                                    lowest = card
                                elif self.numAbove(card, discarded, hand) > self.numAbove(lowest, discarded, hand):
                                    lowest = card
                            return lowest
                        else: #early in the game
                            highest = None
                            for card in legalMoves:
                                if highest is None:
                                    highest = card
                                elif self.numAbove(card, discarded, hand) < self.numAbove(highest, discarded, hand):
                                    highest = card
                            return highest

            
                    else: #playing 2-4 in the trick
                        print("not starting trick")
                        if suitCounts[self.suitToInt(trump)] > 0:
                            highCard = self.getHighCard(discarded[-1])
                            if qsLocation == 4: #Qs location unkown
                                if  trump == 's':
                                    if trickPosition == 4:
                                        return self.highestBelow(legalMoves, 's', 15)
                                    else:
                                        return self.highestBelow(legalMoves, 's', 12)
                                elif (self.playersOut([1,2,3,4], [trump], discarded) or suitsinPlay[self.suitToInt(trump)] < 7 or len(discarded) > 7):
                                    return self.highestBelow(legalMoves, trump, highCard)
                                else: #early in the game only, risk is low
                                    return self.highestBelow(legalMoves, trump, 15)
                            if qsLocation == 3: #lose this trick at all costs
                                return self.highestBelow(legalMoves, trump, highCard)
                            if qsLocation == 2:
                                if len(discarded) > 7: #playing the 8th trick or later
                                    return self.highestBelow(legalMoves, trump, highCard)
                                else: #happy enough to win, could change this
                                    return self.highestBelow(legalMoves, trump, 15)
                            else: #qslocation == 1 -> in hand
                                if trump == 's':
                                    if highCard > 12:
                                        return self.highestBelow(legalMoves, trump, 13) #play Qs
                                    else: 
                                        temp = self.highestBelow(legalMoves, trump, highCard)
                                        if temp.getIden() == 'Qs':
                                            return self.highestBelow(legalMoves, trump, 15)
                                        return temp
                        else: #can't play trump
                            if not firstTrick: #if not first trick
                                if qsLocation == 1: #Qs in hand, get rid of at first opportunity
                                    for card in hand:
                                        if card.getIden() == "Qs":
                                            return card
                                elif suitCounts[3] > 0:
                                    return self.highestBelow(legalMoves, 'h', 15)
                                else:
                                    return self.highestBelow(legalMoves, longestSuit, 15)
                            else: #first trick so can't play hearts or Qs. Want to dump a bad card
                                if qsLocation != 1:
                                    for card in hand:
                                        if card.getIden() == 'Ks' or card.getIden() == 'As':
                                            return card
                                if suitCounts[1] > 0:     
                                    return self.highestBelow(legalMoves, 'd', 15)
                                elif suitCounts[2] > 0:
                                    if qsLocation == 1:
                                        return self.highestBelow(legalMoves, 's', 12)
                                elif suitCounts[0] > 0:
                                    return self.highestBelow(legalMoves, 'c', 15)
                                else:
                                    return self.getRandom(legalMoves)
                                    
                    return self.getRandom(legalMoves)

            else:
                #Play a random card, ideally from legal moves
                return self.getRandom(legalMoves)

        else:
            for card in self.hand.clubs:
                if card.rank == 2:
                    return card

            

        return card



