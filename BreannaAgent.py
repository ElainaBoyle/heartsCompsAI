'''
Agent that play the lowest, high card it can. Otherwise plays hearts. 
If starting a new trick it plays the lowest card it can. 

'''
from Player import Player

class BreannaAgent(Player):
        
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
        if(len(suitCards) == 0):
            self.playHeart()
        else:
            foundCard = False
            currentPlay = suitCards[0]
            for play in suitCards:
                if(play.rank < highCard):
                    foundCard = True
            if(foundCard):
                currentPlay = suitCards[0]
        return currentPlay
    
    def play(self, option='play', c=None, auto=False):
        if auto:                
            if(self.curTrump == ""):
                for card in self.hand.clubs:
                    currentPlay = card
                    if(str(currentPlay.rank).isnumeric):
                        pass
                
                
                # for suit in self.hand:
                #     if(not self.heartsBroken):
                #         if (suit == self.hearts):
                #             break
                #     else:        
                #         for play in suit:
                #             if play.rank < currentPlay:
                #                 currentPlay = play
            else:
                highCard == ""
                for played in self.boardState:
                    if (played != "" and highCard == ""):
                        highCard = played
                    elif(played != "" and highCard != "" and played.rank > highCard.rank):
                        highCard = played
                        
                if(self.curTrump == "c"):
                    suitCards = self.hand[0]
                    currentPlay = self.playACard(suitCards, highCard)
                elif(self.curTrump == "d"):
                    suitCards = self.hand[1]
                    currentPlay = self.playACard(suitCards, highCard)
                elif(self.curTrump == "s"):
                    suitCards = self.hand[2]
                    currentPlay = self.playACard(suitCards, highCard)
                elif(self.curTrump == "h"):
                    suitCards = self.hand[3]
                    currentPlay = self.playACard(suitCards, highCard)
            
            card = self.hand.playCard(currentPlay)
         
        elif c is None:
            card = self.getInput(option)
        else:
            card = c
        if not auto:
            card = self.hand.playCard(card)
        return card

