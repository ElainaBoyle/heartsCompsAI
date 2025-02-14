import pygame
import os






class GameGraphics:

    #game window, screen-related variables
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000
    BACKGROUND_COLOR = (3, 49, 3) #poker table green

    #frame rate
    FPS = 60
    
    #Card-related variables
    cardwidth = 100
    cardheight = 140
    overlap = 50
    p1Card_y = 800 #y coordinate for the top of p1's cards
    cardLocations = [] #a list of lists containing the coordinate for the top left point of each card.
    
    waitTime = 500 #change how long it waits between actions

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Hearts")
        self.screen.fill(self.BACKGROUND_COLOR)
        #self.myHand = ["Ah", "5d", "7d", "Jd", "2s", "7s", "Js", "Ks", "As", "2h", "6h", "8h", "9h"] 
        
        
        
        
    def setHand(self, hand):
        self.myHand = hand
        #print(self.myHand)


    # Formats the cards in your hand to be used SPECIFICALLY FOR FETCHING .png FILES. Also updates overlap for display convenience.
    # PARAM hand a list of card idens (eg. ["2c", "5h"])
    # RETURN a list of card idens with ".png" appended (eg. ["2c.png", "5h.png"])
    def formatCards(self): 
        self.formattedHand = []
        for card in self.myHand:
            self.formattedHand.append(card + ".png")
        self.updateOverlap()
        return self.formattedHand 

    # Displays a hand of cards at the bottom of your screen.
    # PARAM hand a list of FORMATTED card idens (eg. ["2c.png", "5h.png"])
    # Global variables in this calculation: cardwidth, overlap, screen
    def dealHand(self): 
        self.formatCards()
        pos = 500 - (6 * (self.cardwidth - self.overlap)) # 6 cards before the center, 100-overlap apart.
        self.startPos = pos - (self.cardwidth/2) # move left by half of card width (position of card placement is defined by top left corner, not center)
        pos = self.startPos
        for card in self.formattedHand:
            myCard = pygame.image.load(os.path.join('pygamecards/cards', card))
            self.screen.blit(myCard, (pos, self.p1Card_y))
            self.cardLocations.append((pos, self.p1Card_y))
            pos += (self.cardwidth - self.overlap)
            pygame.display.update()
            pygame.time.wait(self.waitTime)
        return
    
    def updateOverlap(self):
        self.overlap = len(self.formattedHand) * 4
        self.startPos = 450 - ((self.cardwidth - self.overlap) * len(self.myHand)/2)
        
        
    def clickACard(self):
        myTurn = True
        while(myTurn):
            # get all events
            ev = pygame.event.get()

            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.getCardAtPos(pos) is not None:
                        print("I got a card!!")
                        return self.getCardAtPos(pos)
        return
    
    def getCardAtPos(self, pos):
        for cardLocation in self.cardLocations:
            if cardLocation[0] <= pos[0] <= cardLocation[0] + self.cardwidth - self.overlap: # CURRENTLY ONLY CHECKS x COORDINATE
                pickedCard = self.myHand[self.cardLocations.index(cardLocation)] #The card in your hand is at the same index as this card location
                print(pickedCard)
                return pickedCard
        print("No card here!")
        return
    
    
    def updateGraphics(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        
        #other player assets?
        #only display available cards
        #card pool?
        #card indicator?
        
        self.formatCards()
        pos = 500 - ((len(self.myHand)/2) * (self.cardwidth - self.overlap)) #half of the cards happen before it maybe
        print(self.formattedHand)
        
        for card in self.formattedHand:
            myCard = pygame.image.load(os.path.join('pygamecards/cards', card))
            self.screen.blit(myCard, (pos, self.p1Card_y))
            self.cardLocations.append((pos, self.p1Card_y))
            pos += (self.cardwidth - self.overlap)
        pygame.display.update()
        pygame.time.wait(self.waitTime)
        return
            
    
    #def playCard(self)
    
    def test(self):
        formatted_hand = self.formatCards(self.myHand) 
        self.dealHand(formatted_hand)




#myGame = GameGraphics()
#myGame.test()









#pygame.time.wait(10000)

pygame.quit()



        
