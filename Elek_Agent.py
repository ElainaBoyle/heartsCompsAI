'''
Agent which always plays the lowest card possible. 
In the passing phase, it will pass its highest cards first
'''
from Player import Player

class Elek_Agent(Player):


    def most_common_suit(self):

        
        if(max(len(self.hand.clubs), len(self.hand.diamonds), len(self.hand.spades), len(self.hand.hearts)) == len(self.hand.clubs)):
            return 'c'
        elif(len(self.hand.clubs), len(self.hand.diamonds), len(self.hand.spades), len(self.hand.hearts) == len(self.hand.diamonds)):
            return 'd'
        elif(max(len(self.hand.clubs), len(self.hand.diamonds), len(self.hand.spades), len(self.hand.hearts)) == len(self.hand.spades)):
            return 's'
        else:
            return 'h'
    

    def play(self, option='play', c=None, auto=True):

        cur_suit = self.curTrick.suit.string

        #plays the lowest card in the trump suit if possible, otherwise plays a random card
        if c == None:
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
