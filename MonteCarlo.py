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
        self.parent = None

class MonteCarlo(Player):
        
    def __init__(self, name, auto=False):
        super().__init__(name, auto)
        self.gameHearts = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.gameSpades = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.gameClubs = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.gameDiamonds = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        
    def MonteSearch(self, root): #written
        """Monte Carlo Tree Search (calls helper functions)"""
        #if time? 5 seconds? 7 seconds? 10 seconds?
        startTime = time.time()
        while(time.time() - startTime < 3):
            leaf = self.traverse(root)
            simulationResult = self.rollout(leaf)
            self.backProp(leaf, simulationResult)
            
        return self.bestChild(root)
    
    def traverse(self, node): 
        """Traverses the tree"""
        while(node.numVisit != 0): 
            node = self.bestChild(node)
            
        if(node.numVisit == 0):
            node = self.expand(node)
            
        return node
        
    def expand(self, node): #written
        """Adds branches to the tree"""
        for card in node.curhand.clubs:
            hand = copy.deepcopy(node.curhand)
            hand = hand.removeCard(card)
            
            if(len(self.gameClubs) != 0):
                self.addBranches(node, hand, card, self.gameClubs)
            if(len(self.gameDiamonds) != 0):
                self.addBranches(node, hand, card, self.gameDiamonds)
            if(len(self.gameHearts) != 0 and (self.heartsBroken or self.hasOnlyHearts)):
                self.addBranches(node, hand, card, self.gameHearts)
            if(len(self.gameDiamonds) != 0):
                self.addBranches(node, hand, card, self.gameSpades)
            
            
        for card in node.curhand.hearts:
            hand = copy.deepcopy(node.curhand)
            hand = hand.removeCard(card)
            
            if(len(self.gameClubs) != 0):
                self.addBranches(node, hand, card, self.gameClubs)
            if(len(self.gameDiamonds) != 0):
                self.addBranches(node, hand, card, self.gameDiamonds)
            if(len(self.gameHearts) != 0):
                self.addBranches(node, hand, card, self.gameHearts)
            if(len(self.gameDiamonds) != 0):
                self.addBranches(node, hand, card, self.gameSpades)
            
        for card in node.curhand.spades:
            hand = copy.deepcopy(node.curhand)
            hand = hand.removeCard(card)

            if(len(self.gameClubs) != 0):
                self.addBranches(node, hand, card, self.gameClubs)
            if(len(self.gameDiamonds) != 0):
                self.addBranches(node, hand, card, self.gameDiamonds)
            if(len(self.gameHearts) != 0):
                self.addBranches(node, hand, card, self.gameHearts)
            if(len(self.gameDiamonds) != 0):
                self.addBranches(node, hand, card, self.gameSpades)

        for card in node.curhand.diamonds:
            hand = copy.deepcopy(node.curhand)
            hand = hand.removeCard(card)
                    
            if(len(self.gameClubs) != 0):
                self.addBranches(node, hand, card, self.gameClubs)
            if(len(self.gameDiamonds) != 0):
                self.addBranches(node, hand, card, self.gameDiamonds)
            if(len(self.gameHearts) != 0):
                self.addBranches(node, hand, card, self.gameHearts)
            if(len(self.gameDiamonds) != 0):
                self.addBranches(node, hand, card, self.gameSpades)
        return node
    
    def addBranches(self, node, hand, card, suite):
        
        if(suite[0] == suite[(int(len(suite)/2))-1] and suite[0] == suite[-1]): #all equal
            
            child = Node([suite[0], card], hand)
            child.parent = node  
            node.children.append(child) 
            suite.pop(0)
            
        elif(suite[-1] == suite[(int(len(suite)/2))-1] and suite[-1] != suite[0]): # high and mid equal
        
            child = Node([suite[0], card], hand)
            child.parent = node  
            node.children.append(child) 
            suite.pop(0)
            
            child = Node([suite[(int(len(suite)/2))-1], card], hand)
            child.parent = node  
            node.children.append(child) 
            suite.pop((int(len(suite)/2))-1)
            
        elif(suite[0] == suite[(int(len(suite)/2))-1] and suite[0] != suite[-11]): # low and mid equal
            
            child = Node([suite[-1], card], hand)
            child.parent = node  
            node.children.append(child) 
            suite.pop(0)
            
            child = Node([suite[(int(len(suite)/2))-1], card], hand)
            child.parent = node  
            node.children.append(child) 
            suite.pop((int(len(suite)/2))-1)
            
        elif(suite[0] != suite[(int(len(suite)/2))-1] and suite[0] == suite[1]): # low and high equal
        
            child = Node([suite[0], card], hand)
            child.parent = node  
            node.children.append(child) 
            suite.pop(0)
            
            child = Node([suite[(int(len(suite)/2))-1], card], hand)
            child.parent = node  
            node.children.append(child) 
            suite.pop((int(len(suite)/2))-1)
            
        else: # none equal
            
            child = Node([suite[0], card], hand)
            child.parent = node  
            node.children.append(child) 
            suite.pop(0)
            
            child = Node([suite[(int(len(suite)/2))-1], card], hand)
            child.parent = node  
            node.children.append(child) 
            suite.pop((int(len(suite)/2))-1)
            
            child = Node([suite[-1], card], hand)
            child.parent = node  
            node.children.append(child) 
            suite.pop(-1)
        
    
    def rollout(self, node):
        """rollout the the rules"""
        while(node.curhand is not None): #while non terminal
            if(len(node.children) == 1):
                node = node.children[0]
            elif(len(node.children) != 0):
                node = node.children[random.randint(0, len(node.children)-1)] #pick a random child node
        return 1 #visited
    
    def backProp(self, node, result): #written
        """Back propigates the tree"""
        if(node.parent == None):
            return
        else:
            node.numVisit = node.numVisit + result
            self.backProp(node.parent, result)
    
    def bestChild(self, node): #written
        """Returns the "best" node of the one with the most visits - Can be modified to use confidence bounds (better)"""
        holder = Node([], node.curhand)
        holder.numVisit = -1
        pick = holder
        for child in node.children:
            
            if(str(child.board[1])[-1] == self.curTrump):
                if(child.numVisit > pick.numVisit):
                    pick = child
            elif(str(child.board[1])[-1] == "h" and self.heartsBroken):
                if(child.numVisit > pick.numVisit):
                    pick = child
            elif(self.curTrump == "Unset"):
                if(child.numVisit > pick.numVisit):
                    pick = child 


        return pick
    
#board is with ["", "", thing, thing]
#board state is with [thing, thing]

    def playCard(self): #written        
        """Redefines playCard from player class to use MonteCarlo"""
        
        self.gameHearts = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.gameSpades = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.gameClubs = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.gameDiamonds = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        
        for card in self.trickHistory:
            if(card[1] == "c"):
                self.gameClubs.remove(card[0])
            if(card[1] == "d"):
                self.gameDiamonds.remove(card[0])
            if(card[1] == "h"):
                self.gameHearts.remove(card[0])
            if(card[1] == "s"):
                self.gameSpades.remove(card[0])


        root = Node(self.boardState, self.hand)
        card = self.MonteSearch(root) #do the algo and get the best card
        return card.board[1] #return the best
    
    def play(self, option='play', c=None, auto=False):
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