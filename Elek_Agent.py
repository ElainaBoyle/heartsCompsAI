'''
This is a simple hard-coded agent which always prefers to play the lowest card above the high card
We refer to this in our comps work as Heuristic Agent 2. This agent is not designed to be as strong
as possible, but rather was an exercise in working with the code base and getting used to building
an agent. It is overall quite weak and performs only slightly better than random bots.
'''
from Player import Player
from Card import Card

class Elek_Agent(Player):

    '''
    @returns {string} the suit in which the player currently has the most cards
    '''
    def most_common_suit(self):
        if(max(len(self.hand.clubs), len(self.hand.diamonds), len(self.hand.spades), len(self.hand.hearts)) == len(self.hand.clubs)):
            return 'c'
        elif(max(len(self.hand.clubs), len(self.hand.diamonds), len(self.hand.spades), len(self.hand.hearts)) == len(self.hand.diamonds)):
            return 'd'
        elif(max(len(self.hand.clubs), len(self.hand.diamonds), len(self.hand.spades), len(self.hand.hearts)) == len(self.hand.spades)):
            return 's'
        else:
            return 'h'
    
    '''
    @returns {card} the highest hearts card in hand. If there are no hearts cards in hand,
    it returns the highest rank card possible
    '''
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

    '''
    @returns {card} the highest card left in hand
    '''
    def playHighest(self):
        play = None
        for suit in self.hand.hand:
            for card in suit:
                if play is None:
                    play = card
                elif (card.rank > play.rank):
                    play = card
        
        return play
        
    '''
    @params {array, card} Takes in the array of suit counds and the current high card
    @returns {card} the lowest card in hand above the current high card
    '''
    def playTrump(self, suitCards, highCard):

        # if you do have a card in the trump suit, play the highest card in hand that is below the high card of the current trick
        #if you don't have a card below the current highest, play the next highest 

        play = suitCards[0]
        for card in suitCards:
            if(card.rank > highCard.rank) and (card.rank > play.rank):
                play = card
        return play

    '''
    @returns {card} the highcard of the current trick
    '''
    def getHighCard(self):
        highCard = Card(0,"c")
        
        for played in self.boardState:
            if((played.rank > highCard.rank)) and (played.suit == self.curTrick.suit):
                highCard = played

        return highCard



    '''
    De facto main method for the player class, called when hearts.py wants the player to play a card
    Takes in discarded (the hand history) which defaults to an empty array.
    @returns {card} the card object which the agent has decided to play.
    '''
    def play(self, discarded =[], option='play', c=None, auto=True):
        cur_suit = self.curTrick.suit
        #plays the lowest card in the trump suit if possible, otherwise plays a random card
        if c == None:

            
            if cur_suit == "": #first card of trick, can only play hearts if nothing else or already been broken
                legalCards = self.getLegalMoves(self.hand.fullHand, self.heartsBroken, (self.trickNum == 1), trump = self.curTrick.suit)
                card = self.getRandom(legalCards)
                return card
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

            #if can play trump, play trump
            if len(suitCards) > 0:
                highCard = self.getHighCard()
                card = self.playTrump(suitCards, highCard)

            elif firstTrick:
                legalCards = self.getLegalMoves(self.hand.fullHand, self.heartsBroken, (self.trickNum == 1), trump = self.curTrick.suit)
                card = self.getRandom(legalCards)
            else: #can't play trump, so play hearts
                card = self.playHearts()
        else:
            for card in self.hand.fullHand:
                if card.getIden() == c:
                    return card

        return card



