import pygame
import os
from Card import Card





#Create a class for displaying cards
class CardDisp(pygame.sprite.Sprite):
    #card should be a card
    def __init__(self, card, x, y):
        if isinstance(card, Card):
            self.iden = card.getIden()
        else:
            self.iden = card
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(os.path.join('pygamecards/cards', self.formatCard(card)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
    # Formats the cards in your hand to be used SPECIFICALLY FOR FETCHING .png FILES. Also updates overlap for display convenience.
    # PARAM card a card or card iden
    # RETURN string the card iden followed by .png eg: "2c.png"
    def formatCard(self, card):
        if isinstance(card, Card):    
            return card.getIden() + ".png"
        elif isinstance(card, str):
            return card + ".png"
        else:
            print("Invalid card for formatting.")
            return None
        
        
    def update(self):
        return
    
    def getIden(self):
        return self.iden





