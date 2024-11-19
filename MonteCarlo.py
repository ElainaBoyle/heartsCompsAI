'''
Monte Carlo Agent
Tree Structure: [ board, [ [ board w/played card, [], curhand, numVisit,  value] [ board w/played card, [], curhand, numVisit, value] ], curhand, numVisit, value]?

'''
from Player import Player
import time
import random

class Node:
    def __init__(self, board, curhand):
        self.board = board
        self.children = []
        self.curhand = curhand
        self.numVisit = 0
        self.value = 0
        self.parent = None

class MonteCarlo(Player):
        
    def MonteSearch(self, root): #written
        #if time? 5 seconds? 10 seconds?
        startTime = time.time()
        while(time.time() - startTime < 10):
            leaf = self.traverse(root)
            simulation = self.rollout(leaf)
            self.backProp(leaf, simulation)
            
        return self.bestChild(root)
    
    def movesMath(self, node):
        """How many moves can be generated based on a branch of the tree"""
        
    
    def traverse(self, node): #written
        while(len(node.children) == self.movesMath(node)): #while fullly expanded
            node = self.bestChild(node)
        
        for child in node.children: #if a child has no children, explore it
            if(len(node.children) == 0):
                return child
        
        return node #otherwise return the node

    def rollout(self, node):
        while(self.hand.size() != 0): #while non terminal
            node = self.rolloutRules(node)
        
        return node #results(node)??????
    
    def rolloutRules(self, node): #written
        pick = random.randint(0, len(node.children)-1)
        return node.children[pick]
    
    def backProp(self, node, result):
        if(node.parent == None):
            return
        else:
            node.value = node.value + result
            node.numVisit = node.numVisit + 1
            self.backProp(node.parent, result)
    
    def bestChild(self, node): #written
        pick = node.children[0]
        for child in node.children:
            if(child.numVisit > pick.numVisit):
                pick = child

        return pick
    
#board is with ["", "", thing, thing]
#board state is with [thing, thing]

    def playCard(self):
        root = Node(self.boardState, self.hand)
        card = self.MonteSearch(root) #do the algo and get the best card
        return card #return the best
    
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