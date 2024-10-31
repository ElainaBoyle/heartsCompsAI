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
            
        if(card[0].isnumeric()):
            return int(card[0])
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
        else:
            lowest = self.hand.hearts[0]
    
        if(len(self.hand.clubs) != 0):
            if(self.convertRank(lowest) > self.convertRank(self.hand.clubs[0])):
                lowest = self.hand.clubs[0]
    
        if(len(self.hand.diamonds) != 0):
            if(self.convertRank(lowest) > self.convertRank(self.hand.diamonds[0])):
                lowest = self.hand.diamonds[0]
        
        if(len(self.hand.spades) != 0):
            if(self.convertRank(lowest) > self.convertRank(self.hand.spades[0])):
                lowest = self.hand.spades[0]
            
        if(self.heartsBroken == True):
            if(len(self.hand.hearts) != 0):
                if(self.convertRank(lowest) > self.convertRank(self.hand.hearts[0])):
                    lowest = self.hand.hearts[0] 
        
        return lowest
                       
    def playHighest(self):
        """Picks the highest card"""
        if(len(self.hand.clubs) != 0):
            highest = self.hand.clubs[-1]
        elif(len(self.hand.diamonds) != 0):
            highest = self.hand.diamonds[-1]
        elif(len(self.hand.spades) != 0):
            highest = self.hand.spades[-1]
        else:
            highest = self.hand.hearts[-1]
    
        if(len(self.hand.clubs) != 0):
            if(self.convertRank(highest) < self.convertRank(self.hand.clubs[0])):
                highest = self.hand.clubs[-1]
    
        if(len(self.hand.diamonds) != 0):
            if(self.convertRank(highest) < self.convertRank(self.hand.diamonds[0])):
                highest = self.hand.diamonds[-1]
        
        if(len(self.hand.spades) != 0):
            if(self.convertRank(highest) < self.convertRank(self.hand.spades[0])):
                highest = self.hand.spades[-1]
            
        if(self.heartsBroken == True):
            if(len(self.hand.hearts) != 0):
                if(self.convertRank(highest) < self.convertRank(self.hand.hearts[0])):
                    highest = self.hand.hearts[-1] 
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
                    if(self.convertRank(play.rank) < self.convertRank(highCard)):
                        currentPlay = play
        return currentPlay
    
    def play(self, option='play', c=None, auto=False):
        """Redefined play in player class to modify auto"""
        if auto:  
            highCard = ""     
            if(self.curTrump == "Unset"):
                currentPlay = self.playLowest()
            else:
                highCard = ""
                for playedCard in self.board:
                    playedString = str(playedCard)
                    if (playedString != "" and highCard == ""):
                        highCard = playedString
                    elif((playedString != "" and highCard != "") and (self.convertRank(playedString) > self.convertRank(highCard))):
                        highCard = playedString
                        
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
            
        elif c is None:
            card = self.getInput(option)
        else:
            card = c
        if not auto:
            card = self.hand.playCard(card)
        return card

