'''
Agent that play the lowest, high card it can. Otherwise plays hearts. 
If starting a new trick it plays the lowest card it can. 

'''
from Player import Player

class BreannaAgent(Player):
    
    def convertRank(self, card):
        """Converts a card's rank into a number"""
        
        if(type(card) != type("String")):
            card = str(card)
            
        if(card[:-1].isnumeric()):
            return int(card[:-1])
        elif(card.find("J") != -1):
            return 11
        elif(card.find("Q") != -1):
            return 12
        elif(card.find("K") != -1):
            return 13
        elif(card.find("A") != -1):
            return 14
    
    def playLowest(self):
        """Picks the lowest card"""
        if(len(self.hand.clubs) != 0):
            lowest = self.hand.clubs[0]
        elif(len(self.hand.diamonds) != 0):
            lowest = self.hand.diamonds[0]
        elif(len(self.hand.spades) != 0):
            lowest = self.hand.spades[0]
        elif(self.heartsBroken):
            lowest = self.hand.hearts[0]
        else:
            legalCards = self.getLegalMoves(self.hand.fullHand, self.heartsBroken, (self.trickNum == 1), trump = self.curTrick.suit)
            lowest = self.getRandom(legalCards)
                
        if(len(self.hand.clubs) != 0):
            if(lowest.rank > self.hand.clubs[0].rank):
                lowest = self.hand.clubs[0]
    
        if(len(self.hand.diamonds) != 0):
            if(lowest.rank > self.hand.diamonds[0].rank):
                lowest = self.hand.diamonds[0]
        
        if(len(self.hand.spades) != 0):
            if(lowest.rank > self.hand.spades[0].rank):
                lowest = self.hand.spades[0]
                
        

        return lowest
                       
    def playHighest(self):
        """Picks the highest card"""
        if(len(self.hand.clubs) != 0):
            highest = self.hand.clubs[-1]
        elif(len(self.hand.diamonds) != 0):
            highest = self.hand.diamonds[-1]
        else:
            highest = self.hand.spades[-1]
    
        if(len(self.hand.clubs) != 0):
            if(highest.rank < self.hand.clubs[0].rank):
                highest = self.hand.clubs[-1]
    
        if(len(self.hand.diamonds) != 0):
            if(highest.rank < self.hand.diamonds[0].rank):
                highest = self.hand.diamonds[-1]
        
        if(len(self.hand.spades) != 0):
            if(highest.rank < self.hand.spades[0].rank):
                highest = self.hand.spades[-1]
            
        return highest
                
    def playHeart(self):
        """Picks a heart or picks the highest card"""
        hearts = self.hand.hearts
        if(len(hearts) != 0):
            currentPlay = hearts[-1]
        else:
            currentPlay = self.playHighest()
        return currentPlay
    
    def playACard(self, suitCards, highCard):
        """Picks the lowest highest card that is still the lowest it can. If not cards in suit picks to play a heart."""
        if(len(suitCards) == 0):
            currentPlay = self.playHeart()
        else:
            currentPlay = suitCards[0]
            for play in suitCards:
                    if(play.value) < highCard:
                        currentPlay = play
        return currentPlay
    
    def play(self, discarded = [], option='play', c=None, auto=False):
        """Redefined play in player class to modify auto"""
        if c is None:
            trickNum = len(self.trickHistory)
            if(trickNum == 13 or trickNum == 0):
                if(len(self.hand.clubs) != 0):
                    currentPlay = self.hand.clubs[-1]
                elif(len(self.hand.diamonds) != 0):
                    currentPlay = self.hand.diamonds[-1]
                else:
                    if(str(self.hand.spades[-1]).find("Q")):
                        currentPlay = self.hand.spades[-2]
                    else:
                        currentPlay = self.hand.spades[-1]
            else:
                highCard = 0     
                if(self.curTrump == ""):
                    currentPlay = self.playLowest()
                else:
                    highCard = 0
    
                    for card in self.boardState:
                        if card.rank > highCard:
                            highCard = card.rank

                            
                    if(self.curTrump == "c"):
                        suitCards = self.hand.clubs
                        currentPlay = self.playACard(suitCards, highCard)
                    elif(self.curTrump == "d"):
                        suitCards = self.hand.diamonds
                        currentPlay = self.playACard(suitCards, highCard)
                    elif(self.curTrump == "s"):
                        suitCards = self.hand.spades
                        currentPlay = self.playACard(suitCards, highCard)
                    elif(self.curTrump == "h"):
                        suitCards = self.hand.hearts
                        currentPlay = self.playACard(suitCards, highCard)
            
            card = currentPlay
            
        else:
            for card in self.hand.fullHand:
                if card.getIden() == c:
                    return card

        return card

