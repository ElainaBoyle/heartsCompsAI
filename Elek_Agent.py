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
    
    def playHeart(self):
        hearts = self.hand[3]
        if(len(hearts) != 0):
            currentPlay = hearts[0]
            for heart in hearts:
                if(heart.rank > currentPlay.rank):
                    currentPlay = heart
        else:
            currentPlay = self.hand.getRandomCard() #change to play highest card
        return currentPlay
        
    def playACard(self, suitCards, highCard):
        # if you don't have a card in the trump suit, play a heart
        if(len(suitCards) == 0):
            self.playHeart()
        
        # if you do have a card in the trump suit, play the highest card in hand that is below the high card of the current trick
        #if you don't have a card below the current highest, play the next highest 

        else:
            foundCard = False
            currentPlay = suitCards[0]
            for play in suitCards:
                if(play.rank < highCard):
                    foundCard = True
            if(foundCard):
                currentPlay = suitCards[0]
        return currentPlay




    def play(self, option='play', c=None, auto=True):

        cur_suit = self.curTrick.suit.string

        #plays the lowest card in the trump suit if possible, otherwise plays a random card
        if c == None:

            #first card of trick, can only play hearts if nothing else or already been broken
            if cur_suit == 'Unset':
                card = self.hand.getRandomCard()

            
            elif cur_suit == 's':
                if len(self.hand.spades) > 0:
                    card = self.hand.playCard(self.hand.spades[0].__str__())
                else:
                    card = self.hand.getRandomCard()

                for x in self.hand.spades:
                    if card.rank < x.rank:
                        card = x

            elif cur_suit == 'd':
                if len(self.hand.diamonds) > 0:
                    card = self.hand.playCard(self.hand.diamonds[0].__str__())
                else:
                    card = self.hand.getRandomCard()

                for x in self.hand.diamonds:
                    if card.rank < x.rank:
                        card = x

            elif cur_suit == 'c':
                if len(self.hand.clubs) > 0:
                    card = self.hand.playCard(self.hand.clubs[0].__str__())
                else:
                    card = self.hand.getRandomCard()

                for x in self.hand.clubs:
                    if card.rank < x.rank:
                        card = x

            else:
                if len(self.hand.hearts) > 0:
                    card = self.hand.playCard(self.hand.hearts[0].__str__())
                else:
                    card = self.hand.getRandomCard()

                for x in self.hand.hearts:
                    if card.rank < x.rank:
                        card = x
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
