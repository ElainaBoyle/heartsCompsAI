import pygame
import os
from CardDisp import CardDisp
from Card import Card






class GameGraphics:

    #game window, screen-related variables
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    BACKGROUND_COLOR = (3, 49, 3) #poker table green

    #frame rate
    clock = pygame.time.Clock()
    FPS = 60
    
    #Card-related variables
    cardwidth = 100
    cardheight = 140
    overlap = 50
    p1Card_y = 800 #y coordinate for the top of p1's cards
    
    cards = pygame.sprite.Group()
    
    middleCards = pygame.sprite.Group()
    
    
    waitTime = 300 #change how long it waits between actions

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Hearts")
        self.screen.fill(self.BACKGROUND_COLOR)

        self.reset()
        
        
        
        
    def reset(self):
        self.overlap = 50
        self.startPos = 500 - (6 * (self.cardwidth - self.overlap)) # 6 cards before the center, 100-overlap apart.
        



    
    def addCard(self, card):
        myCard = CardDisp(card, self.startPos, self.p1Card_y)
        self.startPos += (self.cardwidth - self.overlap)
        self.cards.add(myCard)
    
    def updateOverlap(self):
        self.overlap = len(self.cards) * 4
        pos = 525 - ((self.cardwidth - self.overlap) * len(self.cards)/2)
        
        x = pos
        y = self.p1Card_y
        
        for card in self.cards:
            card.rect.center = (x,y)
            x += (self.cardwidth - self.overlap)
        
        
    def clickACard(self):
        myTurn = True
        while(myTurn):
            # get all events
            ev = pygame.event.get()

            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickedSprites = []
                    for card in self.cards:
                        if card.rect.collidepoint(event.pos):
                            clickedSprites.append(card)
                    if len(clickedSprites) == 1:
                        clickedSprite = clickedSprites[0].getIden()
                        print("You clicked on card", clickedSprite)
                    elif len(clickedSprites) == 2:
                        clickedSprite = clickedSprites[-1].getIden()
                        print("You clicked on card", clickedSprite)
                    else:
                        clickedSprite = None
                        print("No card sprite clicked.")
                    return clickedSprite
                elif event.type == pygame.QUIT:
                    pygame.quit()
    
    def addCardToTrick(self, playerIdx, card):
        print("Player", playerIdx, "Played card", card.getIden())
        
        if playerIdx == 0:
            pos = (500, 600)
        elif playerIdx == 1:
            pos = (300, 500)
        elif playerIdx == 2:
            pos = (500, 300)
        elif playerIdx == 3:
            pos = (700, 500)
        else: return
            
        newCard = CardDisp(card, pos[0], pos[1])
        self.middleCards.add(newCard)
        self.updateGraphics()
        pygame.time.wait(500)
        
    def concludeTrick(self, winnerIdx):
        if winnerIdx == 0:
            direction = (0, 5)
        elif winnerIdx == 1:
            direction = (-5, 0)
        elif winnerIdx == 2:
            direction = (0, -5)
        elif winnerIdx == 3:
            direction = (5, 0)
            
        concluding = True
        
        while concluding:
            print("CONCLDUBNGIN")
            for card in self.middleCards:
                card.rect.move_ip(direction[0], direction[1])
                if (card.rect.top > self.SCREEN_HEIGHT) or (card.rect.bottom < 0) or (card.rect.left > self.SCREEN_WIDTH) or (card.rect.right < 0):
                    card.kill()
            self.updateGraphics()
            if len(self.middleCards) == 0:
                concluding = False
        
                    
                    

    
    def updateGraphics(self):
        
        
        
        
        self.clock.tick(self.FPS)
        
        #Update background
        self.screen.fill(self.BACKGROUND_COLOR)
        
        #Update card assets
        self.cards.update()
        self.cards.draw(self.screen)
        self.middleCards.draw(self.screen)
        
        #other player assets?
        #only display available cards
        #card pool?
        #card indicator?
        
        #Handle Events
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
        
        
        pygame.display.flip()
        return
            
    
    #def playCard(self)
    
    def test(self):
        self.updateGraphics()
        self.dealHand(self.myHand)
        self.updateGraphics()
        
        




#myGame = GameGraphics()
#myGame.test()





#pygame.time.wait(10000)

pygame.quit()



        
