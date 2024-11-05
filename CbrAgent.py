'''

'''
from Player import Player

class Cbr_Agent(Player):



    #get the specified card from hand and returns it
    def playCard(self, cardString):
        return cardString



    def play(self, option='play', c=None, auto=True):

        cur_suit = self.curTrick.suit.string

        #if c was specified, plays c (should probably only really happen w/ 2c), else does cbr stuff
        if c == None:
            #set up variables for easy access to information
            heartsPlayed = []
                #etc


            #do cbr stuff here, querying the case base






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
