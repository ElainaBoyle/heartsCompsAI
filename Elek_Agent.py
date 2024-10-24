'''
Agent which always plays the lowest card possible. 
In the passing phase, it will pass its highest cards first
'''
from Player import Player

class EleksAgent(Player):


    def most_common_suit(my_cards):
        s = 0
        c = 0
        h = 0
        d = 0
        for x in my_cards:
            if x[-1:] == 's':
                s += 1
            elif x[-1:] == 'c':
                c += 1
            elif x[-1:] == 'h':
                h += 1
            elif x[-1:] == 'd':
                d += 1
        if(max(s,c,h,d) == c):
            return 'c'
        elif(max(s,c,h,d) == d):
            return 'd'
        elif(max(s,c,h,d) == s):
            return 's'
        else:
            return 'h'
    

    def play(self, player_num):
        my_cards = self.boardState[player_num-1].split()
        card = my_cards[0]
        cur_suit = self.curTrump
        #cur_suit = 's'

        #if it doesn't have something in the suit it just plays a random card
        for x in my_cards:
            if x[-1:] == cur_suit:
                if int(x[:-1]) < int(card[:-1]):
                    card = x

        # to be expanded later
        # if card[-1:] != cur_suit:

        return card



    #takes the first 3 cards in hand that aren't in the most common suit and passes those
    def passing(self, player_num):
        my_cards = self.boardState[player_num-1].split()
        passing_cards = []

        com_suit = most_common_suit(my_cards)
        
        for x in my_cards:
            if x[-1:] != com_suit:
                passing_cards.append(x)
                if(len(passing_cards) == 3):
                    return passing_cards
        return passing_cards
