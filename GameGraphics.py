import pygame
import os

pygame.init()





#Create game window, screen-related variables
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BACKGROUND_COLOR = (3, 49, 3) #poker table green
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hearts")
screen.fill(BACKGROUND_COLOR)

#frame rate
clock = pygame.time.Clock()
FPS = 60

#Card-related variables
cardwidth = 100
cardheight = 140
overlap = 50
p1Card_y = 800 #y coordinate for the top of p1's cards

#testing variables
myHand = ["4c", "5d", "7d", "Jd", "2s", "7s", "Js", "Ks", "As", "2h", "6h", "8h", "9h"]






# PARAM hand a list of card idens (eg. ["2c", "5h"])
# RETURN a list of card idens with ".png" appended (eg. ["2c.png", "5h.png"])
def formatCards(hand): 
    formatted_hand = []
    for card in hand:
        formatted_hand.append(card + ".png")
    return formatted_hand 

# Displays a hand of cards at the bottom of your screen.
# PARAM hand a list of FORMATTED card idens (eg. ["2c.png", "5h.png"])
# Global variables in this calculation: cardwidth, overlap, screen
def dealCards(hand):
    pos = 500 - (6 * (100 - overlap)) # 6 cards before the center, 100-overlap apart.
    pos = pos - (cardwidth/2) # move left by half of card width (position of card placement is defined by top left corner, not center)
    for card in hand:
        myCard = pygame.image.load(os.path.join('pygamecards/cards', card))
        screen.blit(myCard, (pos, p1Card_y))
        pos += overlap
        pygame.display.update()
        pygame.time.wait(1000)
    return





formatted_hand = formatCards(myHand)
dealCards(formatted_hand)







#thisfuckingcard = pygame.image.load(os.path.join('pygamecards/cards', '2c.png'))
#screen.blit(thisfuckingcard, (250, 250))
#pygame.display.update()
#pygame.time.wait(1000)




#!ACTION NEEDED! You want the cards to be 100x140.
#!! Cards are labelled 2c, 3d, 4h, 5s.... Jh, Qd, Ks, Ac [face cards]
#!! 13 cards in a hand
#!! 50px overlap with central (7th) card at 500,100. 
#!! [200, 100],[250, 100],[300, 100],[350, 100],[400, 100],[450, 100],[500, 100]




















# #Create class for cards
# class cardsprite(pygame.sprite.Sprite):
#     def __init__(self, iden, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         #iden is "c2" or "d6" etc
#         self.iden = iden

#         self.image = pygame.Surface((100,145))
#         self.image.fill((255,255,255))
#         self.rect = self.image.get_rect()
#         self.rect.center = (x,y)
        
#     def set_position(self, x, y):
#         self.rect.x = x
#         self.rect.y = y
        
#     def set_image(self, filename = None):
#         if (filename != None):
#             self.image = pygame.image.load(os.path.join('pygamecards/cards', '2_of_clubs.png')) #replace with iden
#             self.rect = self.image.get_rect()
        
        
# #create a card
# thisCard = cardsprite("c2", 250, 250)
# thisCard.set_image("anyhtng")
# thisCard.set_position(250, 250)
# cards = pygame.sprite.Group()
# cards.add(thisCard)

# screen.blit(thisCard, (250, 250))

# #pygame.sprite.Group.draw(cards)
# #pygame.display.flip()
# pygame.time.wait(1000)

# #Game loop
# run = True
# while run:
#     clock.tick(FPS)
    
#     #update background
#     screen.fill((0, 255, 0))
    
    
#     #update sprite group (unnecessary for right now?)
#     cards.update()
    
#     #draw sprite group
#     cards.draw(screen)
#     #pygame.display.flip()
#     pygame.time.wait(1000)
    
    
    
#     #event handler
    
        
        
        
        






# #First: drawing the background

# #deal the cards
# #13 card-shaped rectangles at the bottom ish of the screen
# #The cards are 500x726 pixels each (as of right now)
# #left = 50
# #top = 800

# #c2 = pygame.image.load(os.path.join("pygamecards/cards", "2_of_clubs.png"))


# #pygame.display.flip()
# #pygame.time.wait(1000)


# #myHand = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
# #for myCard in myHand:
# #    pygame.draw.rect(screen, BLACK, pygame.Rect(left, top, 100, 145)) #will probably have to distinguish rect separately
# #    pygame.display.flip()
# #    pygame.time.wait(1000)
# #    left += 65

pygame.quit()



        
