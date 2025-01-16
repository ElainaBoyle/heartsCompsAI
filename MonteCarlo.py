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
        self.gameHearts = ["2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "Jh", "Qh", "Kh", "Ah"]
        self.gameSpades = ["2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "Js", "Qs", "Ks", "As"]
        self.gameClubs = ["2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "Jc", "Qc", "Kc", "Ac"]
        self.gameDiamonds = ["2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "Jd", "Qd", "Kd", "Ad"]
        
    def MonteSearch(self, root): #written
        """Monte Carlo Tree Search (calls helper functions)"""
        #if time? 5 seconds? 7 seconds? 10 seconds?
        startTime = time.time()
        while(time.time() - startTime < 1):
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
        
    def expand(self, node): # Fixing - written?
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
                    
         
    def addBranches(self, node, hand, card):
        for otherPlay1 in self.gameDiamonds:
            for otherPlay2 in self.gameDiamonds:
                
                for otherPlay3 in self.gameDiamonds:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
                for otherPlay3 in self.gameSpades:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node  
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
                for otherPlay3 in self.gameClubs:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
                for otherPlay3 in self.gameHearts:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
            
            for otherPlay2 in self.gameClubs:
                for otherPlay3 in self.gameHearts:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
                for otherPlay3 in self.gameClubs:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child)
                for otherPlay3 in self.gameSpades:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
           
            for otherPlay2 in self.gameClubs:
                for otherPlay3 in self.gameHearts:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
                for otherPlay3 in self.gameClubs:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child)
                for otherPlay3 in self.gameSpades:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child)
           
            for otherPlay2 in self.gameHearts:
                for otherPlay3 in self.gameHearts:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
                for otherPlay3 in self.gameSpades:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child)
            
            for otherPlay2 in self.gameSpades:
                for otherPlay3 in self.gameSpades:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
        
        
        for otherPlay1 in self.gameClubs:
            for otherPlay2 in self.gameClubs:
                for otherPlay3 in self.gameHearts:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
                for otherPlay3 in self.gameClubs:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child)
                for otherPlay3 in self.gameSpades:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child)

            for otherPlay2 in self.gameHearts:
                for otherPlay3 in self.gameHearts:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
                for otherPlay3 in self.gameSpades:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child)          
                        
            for otherPlay2 in self.gameSpades:
                for otherPlay3 in self.gameSpades:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child)  


        for otherPlay1 in self.gameHearts:
            for otherPlay2 in self.gameHearts:
                for otherPlay3 in self.gameHearts:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
                for otherPlay3 in self.gameSpades:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child)
                        
            for otherPlay2 in self.gameSpades:
                for otherPlay3 in self.gameSpades:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child)  
                        
                        
        for otherPlay1 in self.gameSpades:
            for otherPlay2 in self.gameSpades:
                for otherPlay3 in self.gameSpades:
                    if((otherPlay1 != otherPlay2) and (otherPlay1 != otherPlay3) and (otherPlay2 != otherPlay3)):
                        child = Node([otherPlay1, card, otherPlay2, otherPlay3], hand)
                        child.parent = node
                        child.curTrump = otherPlay1[-1]
                        node.children.append(child) 
        
    def rollout(self, node): #should probably have better logic than pick a random child
        """rollout the the rules"""
        while(node is not None): #while non terminal (none because it is a hand)
            if(len(node.children) == 1):
                node = node.children[0]
            elif(len(node.children) != 0):
                node = self.bestMathPick(node)
        
            high = "blank"
            highCheck = 0
            cardCheck = 0
            for card in node.board:
                if(high == "blank"):
                    card = high
                else:
                    if(type(card) != type("string")):
                        card = str(card)
                        
                    if(high[-1] == card[-1]):
                        if(high[0] == 1):
                            cardCheck = 10
                        elif(high[0] == "J"):
                            cardCheck = 11
                        elif(high[0] == "Q"):
                            cardCheck = 12
                        elif(high[0] == "K"):
                            cardCheck = 13
                        elif(high[0] == "A"):
                            cardCheck = 14
                        else:
                            cardCheck = int(card[0])
                    
                    if(type(high) != type("string")):
                        high = str(high)
                        
                    if(high[-1] == high[-1]):
                        if(high[0] == 1):
                            highCheck = 10
                        elif(high[0] == "J"):
                            highCheck = 11
                        elif(high[0] == "Q"):
                            highCheck = 12
                        elif(high[0] == "K"):
                            highCheck = 13
                        elif(high[0] == "A"):
                            highCheck = 14
                        else:
                            highCheck = int(high[0])
                            
                    if(highCheck < cardCheck):
                        high = card
                    
            score = 0
            if(type(high) != type("string")):
                for card in node.board:
                    if(type(card) != type("string")):
                        card = str(card)
                    if(card[-1] == "h"):
                        score = score + 1
                    if(card == "Qs"):
                        score = score + 13 
            return score
                            
    def bestMathPick(self, node):
        return self.bestChild(node)
        #return node.children[random.randint(0, len(node.children)-1)] #pick a random child node    

    def backProp(self, node, result): #written - maybe needs rewritten
        """Back propigates the tree"""
        if(node == None):
            return
        else:
            node.numVisit = node.numVisit + 1
            node.value = node.value + result
            self.backProp(node.parent, result)
    
    def bestChild(self, node): #written - needs updating
        """Returns the "best" node of the one with the most visits - Can be modified to use confidence bounds (better)"""
        holder = Node([], node.curhand)
        holder.value = -1
        pick = holder
        
        for child in node.children:
            
            if(str(child.board[1])[-1] == node.curTrump):
                if(child.value > pick.value):
                    pick = child

            elif(self.heartsBroken or (len(self.hand.hearts) == self.hand.size())):
                if(child.value > pick.value):
                    pick = child
            
            else:
                if(str(child.board[1])[-1] != "h"):
                    if(str(child.board[1]) != "Qs"):
                        if(child.value > pick.value): 
                            pick = child    

        return pick
    
#Notes \/
#board is with ["", "", thing, thing]
#board state is with [thing, thing]

    def playCard(self): #written - rewritten with some more logic 
        """Redefines playCard from player class to use MonteCarlo"""
        
        self.gameHearts = ["2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "Jh", "Qh", "Kh", "Ah"]
        self.gameSpades = ["2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "Js", "Qs", "Ks", "As"]
        self.gameClubs = ["2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "Jc", "Qc", "Kc", "Ac"]
        self.gameDiamonds = ["2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "Jd", "Qd", "Kd", "Ad"]
        
        ### remove what has been played already ###
        
        for card in self.trickHistory:
            if(card[-1] == "c"):
                self.gameClubs.remove(card)

            if(card[-1] == "d"):
                self.gameDiamonds.remove(card)

            if(card[-1] == "h"):
                self.gameHearts.remove(card)

            if(card[-1] == "s"):
                self.gameSpades.remove(card)

                    
        ### remove what is in the hand ###
                    
        for card in self.hand.clubs:
            self.gameClubs.remove(str(card))
         
        for card in self.hand.diamonds:
            self.gameDiamonds.remove(str(card))
                
        for card in self.hand.hearts:
            self.gameHearts.remove(str(card))
                
        for card in self.hand.spades:
            self.gameSpades.remove(str(card))
            
        ### remove what is in the current board ###
        
        for card in self.boardState:
            if(str(card)[-1] == "c"):
                self.gameClubs.remove(str(card))
            
            if(str(card)[-1] == "d"):
                self.gameDiamonds.remove(str(card))
            
            if(str(card)[-1] == "h"):
                self.gameHearts.remove(str(card))
            
            if(str(card)[-1] == "s"):
                self.gameSpades.remove(str(card))

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