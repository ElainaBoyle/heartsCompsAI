'''
Agent which always plays the lowest card possible. 
'''
from Player import Player
from Card import Card

class Elek_Agent(Player):


    def most_common_suit(self):

        
        if(max(len(self.hand.clubs), len(self.hand.diamonds), len(self.hand.spades), len(self.hand.hearts)) == len(self.hand.clubs)):
            return 'c'
        elif(max(len(self.hand.clubs), len(self.hand.diamonds), len(self.hand.spades), len(self.hand.hearts)) == len(self.hand.diamonds)):
            return 'd'
        elif(max(len(self.hand.clubs), len(self.hand.diamonds), len(self.hand.spades), len(self.hand.hearts)) == len(self.hand.spades)):
            return 's'
        else:
            return 'h'
    
    #plays highest heart (if no hearts play the highest card in hand)
    def playHearts(self):
        hearts = self.hand.hearts
        if(len(hearts) != 0):
            play = hearts[0]
            for heart in hearts:
                if(heart.rank > play.rank):
                    play = heart
        else:
            play = self.playHighest()
        return play


    #plays the highest card left in hand. Doesn't look at suits at all
    def playHighest(self):
        play = None
        for suit in self.hand.hand:
            for card in suit:
                if play is None:
                    play = card
                elif (card.rank > play.rank):
                    play = card
        
        return play

        
    def playTrump(self, suitCards, highCard):

        # if you do have a card in the trump suit, play the highest card in hand that is below the high card of the current trick
        #if you don't have a card below the current highest, play the next highest 

        play = suitCards[0]
        for card in suitCards:
            print(card.getIden())

            if(card.rank > highCard.rank) and (card.rank > play.rank):
                print(card.getIden())
                play = card

        return play


    #gets the highest value card of the current trick (thats in the trump suit)
    def getHighCard(self):
        highCard = Card(0,"c")
        
        for played in self.boardState:
            if((played.rank > highCard.rank)) and (played.suit == self.curTrick.suit):
                highCard = played

        return highCard






    def play(self, discarded =[], option='play', c=None, auto=True):
        print("getting to play")

        cur_suit = self.curTrick.suit
        

        #plays the lowest card in the trump suit if possible, otherwise plays a random card
        if c == None:

            #first card of trick, can only play hearts if nothing else or already been broken
            if cur_suit == "":
                legalCards = self.getLegalMoves(self.hand.fullHand, self.heartsBroken, (self.trickNum == 1), trump = self.curTrick.suit)
                card = self.getRandom(legalCards)
                return card


            print("cur_suit:", cur_suit)
            if(cur_suit == "c"):
                suitCards = self.hand.clubs
            elif(cur_suit == "d"):
                suitCards = self.hand.diamonds
            elif(cur_suit == "s"):
                suitCards = self.hand.spades
            else:
                suitCards = self.hand.hearts

            
            firstTrick = False
            if len(discarded) == 1:
                firstTrick = True


            print(suitCards)
            #if can play trump, play trump
            if len(suitCards) > 0:
                highCard = self.getHighCard()
                card = self.playTrump(suitCards, highCard)

            elif firstTrick:
                legalCards = self.getLegalMoves(self.hand.fullHand, self.heartsBroken, (self.trickNum == 1), trump = self.curTrick.suit)
                card = self.getRandom(legalCards)
            #if can't play trump, play hearts
            else:
                card = self.playHearts()

        else:
            
            for card in self.hand.fullHand:
                if card.getIden() == c:
                    return card

            

        return card



