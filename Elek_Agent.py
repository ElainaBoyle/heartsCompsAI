'''
Agent which always plays the lowest card possible. 
In the passing phase, it will pass its highest cards first
'''
from Player import Player

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
            if(card.rank < highCard.rank) and (card.rank > play.rank):
                play = card

        return play


    #gets the highest value card of the current trick (thats in the trump suit)
    def getHighCard(self):
        highCard = self.boardState[0]
        
        for played in self.boardState:
            if((played.rank > played.rank)) and (self.suit == self.curTrick.suit.string):
                highCard = played

        return highCard






    def play(self, option='play', c=None, auto=True):

        cur_suit = self.curTrick.suit.string

        #plays the lowest card in the trump suit if possible, otherwise plays a random card
        if c == None:

            #first card of trick, can only play hearts if nothing else or already been broken
            if cur_suit == 'Unset':
                #do something interesting
                card = self.hand.getRandomCard()
                return card


            if(cur_suit == "c"):
                suitCards = self.hand.clubs
            elif(cur_suit == "d"):
                suitCards = self.hand.diamonds
            elif(cur_suit == "s"):
                suitCards = self.hand.spades
            else:
                suitCards = self.hand.hearts

            #if can play trump, play trump
            if len(suitCards) > 0:
                highCard = self.getHighCard()
                card = self.playTrump(suitCards, highCard)
            #if can't play trump, play heart
            else:
                card = self.playHearts()

        else:
            card = self.hand.playCard(c)


        return card



    #takes the first 3 cards in hand that aren't in the most common suit and passes those

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
