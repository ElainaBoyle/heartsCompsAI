'''
Monte Carlo Agent

'''
from Player import Player
from Card import Card
from Hand import Hand
import time
import copy
import random


class Node:
    def __init__(self, board, curhand):
        self.board = board
        self.children = []
        self.curhand = curhand
        self.numVisit = 0
        self.value = 0
        self.curTrump = "Unset"
        self.parent = None

class MonteCarlo(Player):
        
    def __init__(self, name, auto=False):
        super().__init__(name, auto)
        
        '''
        Suit identification (iden)
        0: clubs
        1: diamonds
        2: spades
        3: hearts
        
        Ranks indicated by numbers 2-14, Ace = 14
        '''
        self.gameClubs = []
        self.gameDiamonds = []
        self.gameSpades = []
        self.gameHearts = []
        
    def MonteSearch(self, root): #written
        """Monte Carlo Tree Search (calls helper functions)"""
        #if time? 5 seconds? 7 seconds? 10 seconds?
        startTime = time.time()
        while(time.time() - startTime < 3):
            leaf = self.traverse(root)
            simulationResult = self.rollout(leaf)
            self.backProp(leaf, simulationResult)
            
        return self.bestChild(root)
    
    def traverse(self, node):#written
        """Traverses the tree"""
        while(node.numVisit != 0): #While explored
            node = self.bestChild(node) #change to math?
            
        if(node.numVisit == 0): #if not explored
            node = self.expand(node)
            
        return node
        
    def expand(self, node): #written
        """Adds branches to the tree"""
        
        if(node.curTrump == "h"):
            if(len(node.curhand.hearts) != 0):
                for card in node.curhand.hearts:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    self.addBranches(node, hand, card)
                    
            else: #No hearts
                if(len(node.curhand.clubs) != 0):
                    for card in node.curhand.clubs:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        self.addBranches(node, hand, card)
                        
                if(len(node.curhand.diamonds) != 0):
                    for card in node.curhand.diamonds:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        self.addBranches(node, hand, card)
                        
                if(len(node.curhand.spades) != 0):    
                    for card in node.curhand.spades:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        self.addBranches(node, hand, card)
                        
            
        elif(node.curTrump == "s"):
            if(len(node.curhand.spades) != 0):
                for card in node.curhand.spades:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    self.addBranches(node, hand, card)
    
            else: #No spades
                if(len(node.curhand.hearts) != 0):
                    for card in node.curhand.hearts:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        self.addBranches(node, hand, card)
        
                if(len(node.curhand.clubs) != 0):
                    for card in node.curhand.clubs:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        self.addBranches(node, hand, card)
        
                if(len(node.curhand.diamonds) != 0):    
                    for card in node.curhand.diamonds:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        self.addBranches(node, hand, card)
        
        
        elif(node.curTrump == "d"):
            if(len(node.curhand.diamonds) != 0):
                for card in node.curhand.diamonds:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    self.addBranches(node, hand, card)
                    
            else: #No diamonds
                if(len(node.curhand.hearts) != 0):
                    for card in node.curhand.hearts:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        self.addBranches(node, hand, card)
                        
                if(len(node.curhand.clubs) != 0):
                    for card in node.curhand.clubs:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        self.addBranches(node, hand, card)
                        
                if(len(node.curhand.spades) != 0):    
                    for card in node.curhand.spades:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        self.addBranches(node, hand, card)
                        
        
        elif(node.curTrump == "c"):
            if(len(node.curhand.clubs) != 0):
                for card in node.curhand.clubs:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    self.addBranches(node, hand, card)
                    
            else: #No clubs
                if(len(node.curhand.hearts) != 0):
                    for card in node.curhand.hearts:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        self.addBranches(node, hand, card)
                        
                if(len(node.curhand.diamonds) != 0):
                    for card in node.curhand.diamonds:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        self.addBranches(node, hand, card)
                        
                if(len(node.curhand.spades) != 0):    
                    for card in node.curhand.spades:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        self.addBranches(node, hand, card)
                        
        else: # Unset
            if((len(node.curhand.hearts) != 0) and (self.heartsBroken or self.hasOnlyHearts)):
                for card in node.curhand.hearts:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    self.addBranches(node, hand, card)
                    
            if(len(node.curhand.clubs) != 0):
                for card in node.curhand.clubs:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    self.addBranches(node, hand, card)
                    
            if(len(node.curhand.diamonds) != 0):
                for card in node.curhand.diamonds:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    self.addBranches(node, hand, card)
                    
            if(len(node.curhand.spades) != 0):    
                for card in node.curhand.spades:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    self.addBranches(node, hand, card)
                          
    def addBranches(self, node, hand, card): #written
        
        suits = [self.gameDiamonds, self.gameSpades, self.gameClubs, self.gameHearts]
        for otherPlay1 in suits:
            for otherPlay2 in suits:
                for otherPlay3 in suits:
                    for card1 in otherPlay1:
                        for card2 in otherPlay2:
                            for card3 in otherPlay3:
                                if((card1 != card2) and (card1 != card3) and (card2 != card3)):
                                    child = Node([card1, card, card2, card3], hand)
                                    child.parent = node
                                    child.curTrump = str(card1)[-1]
                                    node.children.append(child)  
                                         
    def rollout(self, node): #written
        """rollout the the rules"""
        while(node is not None): #while non terminal (none because it is a hand)
            if(len(node.children) == 1):
                node = node.children[0]
            elif(len(node.children) != 0):
                node = self.bestMathPick(node)
        
            high = None
            for card in node.board:
                if(high == None):
                    card = high
                else:
                    # if(type(card) != type("string")):
                    #     card = str(card)
                        
                    # if(high[-1] == card[-1]):
                    #     if(high[0] == 1):
                    #         cardCheck = 10
                    #     elif(high[0] == "J"):
                    #         cardCheck = 11
                    #     elif(high[0] == "Q"):
                    #         cardCheck = 12
                    #     elif(high[0] == "K"):
                    #         cardCheck = 13
                    #     elif(high[0] == "A"):
                    #         cardCheck = 14
                    #     else:
                    #         cardCheck = int(card[0])
                    
                    # if(type(high) != type("string")):
                    #     high = str(high)
                        
                    # if(high[-1] == high[-1]):
                    #     if(high[0] == 1):
                    #         highCheck = 10
                    #     elif(high[0] == "J"):
                    #         highCheck = 11
                    #     elif(high[0] == "Q"):
                    #         highCheck = 12
                    #     elif(high[0] == "K"):
                    #         highCheck = 13
                    #     elif(high[0] == "A"):
                    #         highCheck = 14
                    #     else:
                    #         highCheck = int(high[0])
                    
                    if(str(high)[-1] == str(card)[-1]):     
                        if(high.rank < card.rank):
                            high = card
                    
            score = 0
            if(type(high) != type("string")):
                for card in node.board:
                    # if(type(card) != type("string")):
                    #     card = str(card)
                    if(str(card)[-1] == "h"):
                        score = score + 1
                    if(str(card) == "Qs"):
                        score = score + 13 
            return score
                            
    def bestMathPick(self, node): # needs to be written
        return self.bestChild(node)
    

    def backProp(self, node, result): #written 
        """Back propigates the tree itteratively (also contains noniterative code)"""
        
        while node is not None:
            node.numVisit = node.numVisit + 1
            node.value = node.value + result
            node = node.parent
        
        # if(node == None):
        #     return
        # else:
        #     node.numVisit = node.numVisit + 1
        #     node.value = node.value + result
        #     self.backProp(node.parent, result)
    
    def bestChild(self, node): #written - needs updating (probably)
        """Returns the "best" node of the one with the most visits - Can be modified to use confidence bounds (better)"""
        pick = Node([], node.curhand)
        pick.value = 10000
        
        for child in node.children:
            childTrump = str(child.board[1])[-1]
            if(childTrump == node.curTrump):
                if(child.value < pick.value):
                    pick = child

            elif(self.heartsBroken or (len(self.hand.hearts) == self.hand.size())):
                if(child.value < pick.value):
                    pick = child
            
            else:
                if((childTrump != "h") and (str(child.board[1]) != "Qs")):
                        if(child.value < pick.value): 
                            pick = child    

        return pick
    
#Notes \/
#board is with ["", "", thing, thing]
#board state is with [thing, thing]

    def playCard(self): #written - needs to rewritten faster
        """Redefines playCard from player class to use MonteCarlo"""
        
        if((len(self.cardObjTrickHistory) == 12) or (len(self.cardObjTrickHistory) == 0)):

            self.gameClubs = [Card(2,0), Card(3,0), Card(4,0), Card(5,0), Card(6,0), Card(7,0), Card(8,0), Card(9,0), Card(10 ,0), Card(11, 0), Card(12,0), Card(13,0), Card(14,0)]
            self.gameDiamonds = [Card(2,1), Card(3,1), Card(4,1), Card(5,1), Card(6,1), Card(7,1), Card(8,1), Card(9,1), Card(10 ,1), Card(11, 1), Card(12,1), Card(13,1), Card(14,1)]
            self.gameSpades = [Card(2,2), Card(3,2), Card(4,2), Card(5,2), Card(6,2), Card(7,2), Card(8,2), Card(9,2), Card(10 ,2), Card(11, 2), Card(12,2), Card(13,2), Card(14,2)]
            self.gameHearts = [Card(2,3), Card(3,3), Card(4,3), Card(5,3), Card(6,3), Card(7,3), Card(8,3), Card(9,3), Card(10 ,3), Card(11, 3), Card(12,3), Card(13,3), Card(14,3)]
            
            ### remove what is in the hand ###
            for card in self.hand.clubs:
                self.gameClubs.remove(card)
            
            for card in self.hand.diamonds:
                self.gameDiamonds.remove(card)
                    
            for card in self.hand.hearts:
                self.gameHearts.remove(card)
                    
            for card in self.hand.spades:
                self.gameSpades.remove(card)
        
        ### remove what has been played already ###
        if(len(self.cardObjTrickHistory) != 0):
            for card in self.cardObjTrickHistory[-1]:
                if(str(card)[-1] == "c" and (card in self.gameClubs)):
                    self.gameClubs.remove(card)

                if(str(card)[-1] == "d" and (card in self.gameDiamonds)):
                    self.gameDiamonds.remove(card)

                if(str(card)[-1] == "h" and (card in self.gameHearts)):
                    self.gameHearts.remove(card)

                if(str(card)[-1] == "s" and (card in self.gameSpades)):
                    self.gameSpades.remove(card)
        
        ### remove what is in the current board ###
        
        for card in self.boardState:
            if(str(card)[-1] == "c"):
                self.gameClubs.remove(card)
            
            if(str(card)[-1] == "d"):
                self.gameDiamonds.remove(card)
            
            if(str(card)[-1] == "h"):
                self.gameHearts.remove(card)
            
            if(str(card)[-1] == "s"):
                self.gameSpades.remove(card)
                
        erCheck = []
        for card in self.gameClubs:
            erCheck.append(str(card))
        for card in self.gameHearts:
            erCheck.append(str(card))
        for card in self.gameDiamonds:
            erCheck.append(str(card))
        for card in self.gameSpades:
            erCheck.append(str(card))
        print(erCheck)
        
        root = Node(self.boardState, self.hand)
        root.curTrump = self.curTrump
        card = self.MonteSearch(root) #do the algo and get the best card
        return card.board[1] #return the best
    
    def play(self, option='play', c=None, auto=False): #written - taken from player
        """Redefines play from player class to if auto call playCard defined above"""
        if auto:
            card = self.playCard()
        elif c is None:
            card = self.getInput(option)
        else:
            card = c
        if not auto:
            card = self.hand.playCard(card)
        return card