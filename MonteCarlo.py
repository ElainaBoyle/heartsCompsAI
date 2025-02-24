'''
Monte Carlo Agent

'''
from Player import Player
from Card import Card
import time
import copy
import random
import math

class Node:
    def __init__(self, board, curhand):
        self.board = board
        self.children = []
        self.curhand = curhand
        self.numVisit = 0
        self.value = 0
        self.curTrump = "Unset"
        self.parent = None

class otherPlayers:
    def __init__(self):
                
        self.hasClubs = True
        self.hasDiamonds = True
        self.hasSpades = True
        self.hasHearts = True
        
    def reset(self):

        self.hasClubs = True
        self.hasDiamonds = True
        self.hasSpades = True
        self.hasHearts = True  

        
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
        self.gameClubs = [Card(2,0), Card(3,0), Card(4,0), Card(5,0), Card(6,0), Card(7,0), Card(8,0), Card(9,0), Card(10 ,0), Card(11, 0), Card(12,0), Card(13,0), Card(14,0)]
        self.gameDiamonds = [Card(2,1), Card(3,1), Card(4,1), Card(5,1), Card(6,1), Card(7,1), Card(8,1), Card(9,1), Card(10 ,1), Card(11, 1), Card(12,1), Card(13,1), Card(14,1)]
        self.gameSpades = [Card(2,2), Card(3,2), Card(4,2), Card(5,2), Card(6,2), Card(7,2), Card(8,2), Card(9,2), Card(10 ,2), Card(11, 2), Card(12,2), Card(13,2), Card(14,2)]
        self.gameHearts = [Card(2,3), Card(3,3), Card(4,3), Card(5,3), Card(6,3), Card(7,3), Card(8,3), Card(9,3), Card(10 ,3), Card(11, 3), Card(12,3), Card(13,3), Card(14,3)]
        self.UCBConstant = 0.75
        

        self.player1 = otherPlayers()
        self.player2 = otherPlayers()
        self.player3 = otherPlayers()
        
        self.prevBoardNum = 0
        self.pastTrump = "Unset"
        
    def MonteSearch(self, root): #written
        """Monte Carlo Tree Search (calls helper functions)"""
        # amount of time 
        # 3 seconds = 10 min per game; 2 seconds = 7 mins per game; 1 second = 3min
        startTime = time.time()
        while(time.time() - startTime < 3):
            leaf = self.traverse(root)
            simulationResult = self.rollout(leaf)
            self.backProp(leaf, simulationResult)
    
        # amount of iterations 
        # for i in range(9000):
        #     leaf = self.traverse(root) #has children
        #     simulationResult = self.rollout(leaf)
        #     self.backProp(leaf, simulationResult)
        #     print(leaf)
        #     i = i + 1
        
        return self.bestChild(root)
        
    def traverse(self, node):#written
        """Traverses the tree"""
        while(node.numVisit != 0): #While explored
            if(self.score > 7):
                for cHeart in self.gameHearts:
                    if(cHeart in node.board):
                        self.UCBConstant *= -1
                        break
            else:
                self.UCBConstant = 0.75

            best = self.calculateUCB(node.children[0])
            bestNode = node.children[0]
            for child in node.children:
                if(best > self.calculateUCB(child)):
                    best = self.calculateUCB(child)
                    bestNode = child
            
        if(node.numVisit == 0): #if not explored
            self.expand(node)
            return node

        return bestNode
    
    def calculateUCB(self, node): #written - still working on constant picking
        #Best constant so far: 0.75
        parentVisit = 1
        selfVisit = 1
        
        if(node.parent != None):
            if(node.parent.numVisit > 0):
                parentVisit = node.parent.numVisit
        else:
            parentVisit = 1
        if(node.numVisit > 0):
            selfVisit = node.numVisit
        value = node.value + (self.UCBConstant * math.sqrt((math.log(parentVisit)/selfVisit)))
        return value
        

    def expand(self, node): #written
        """Adds branches to the tree"""
        if(self.score > 7):
            if(len(node.curhand.hearts) != 0 and (self.heartsBroken and self.hasOnlyHearts)):
                for card in node.curhand.hearts:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
            elif((Card(12,2) in node.curhand.spades) and (node.curTrump == "s")):
                hand = copy.deepcopy(node.curhand)
                hand = hand.removeCard("Qs")
                node = self.addBranches(node, hand, "Qs")
                         

        elif(node.curTrump == "h"):
            if(len(node.curhand.hearts) != 0):
                for card in node.curhand.hearts:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    node = self.addBranches(node, hand, card)
                    
            else: #No hearts
                if(len(node.curhand.clubs) != 0):
                    for card in node.curhand.clubs:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
                        
                if(len(node.curhand.diamonds) != 0):
                    for card in node.curhand.diamonds:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
                        
                if(len(node.curhand.spades) != 0):    
                    for card in node.curhand.spades:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
                        
            
        elif(node.curTrump == "s"):
            if(len(node.curhand.spades) != 0):
                for card in node.curhand.spades:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    node = self.addBranches(node, hand, card)
    
            else: #No spades
                if(len(node.curhand.hearts) != 0):
                    for card in node.curhand.hearts:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
        
                if(len(node.curhand.clubs) != 0):
                    for card in node.curhand.clubs:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
        
                if(len(node.curhand.diamonds) != 0):    
                    for card in node.curhand.diamonds:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
        
        
        elif(node.curTrump == "d"):
            if(len(node.curhand.diamonds) != 0):
                for card in node.curhand.diamonds:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    node = self.addBranches(node, hand, card)
                    
            else: #No diamonds
                if(len(node.curhand.hearts) != 0):
                    for card in node.curhand.hearts:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
                        
                if(len(node.curhand.clubs) != 0):
                    for card in node.curhand.clubs:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
                        
                if(len(node.curhand.spades) != 0):    
                    for card in node.curhand.spades:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
                        
        
        elif(node.curTrump == "c"):
            if(len(node.curhand.clubs) != 0):
                for card in node.curhand.clubs:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    node = self.addBranches(node, hand, card)
                    
            else: #No clubs
                if(len(node.curhand.hearts) != 0):
                    for card in node.curhand.hearts:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
                        
                if(len(node.curhand.diamonds) != 0):
                    for card in node.curhand.diamonds:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
                        
                if(len(node.curhand.spades) != 0):    
                    for card in node.curhand.spades:
                        hand = copy.deepcopy(node.curhand)
                        hand = hand.removeCard(card)
                        node = self.addBranches(node, hand, card)
                        
        else: # Unset
            if((len(node.curhand.hearts) != 0) and (self.heartsBroken or self.hasOnlyHearts)):
                for card in node.curhand.hearts:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    node = self.addBranches(node, hand, card)
                    
            if(len(node.curhand.clubs) != 0):
                for card in node.curhand.clubs:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    node = self.addBranches(node, hand, card)
                    
            if(len(node.curhand.diamonds) != 0):
                for card in node.curhand.diamonds:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    node = self.addBranches(node, hand, card)
                    
            if(len(node.curhand.spades) != 0):    
                for card in node.curhand.spades:
                    hand = copy.deepcopy(node.curhand)
                    hand = hand.removeCard(card)
                    node = self.addBranches(node, hand, card)
        
        return node
                     
    def addBranches(self, node, hand, card): #written
        
        suits = [self.gameClubs, self.gameDiamonds, self.gameSpades, self.gameHearts]
        
        player1Has = [self.player1.hasClubs, self.player1.hasDiamonds, self.player1.hasSpades, self.player1.hasHearts]
        player2Has = [self.player2.hasClubs, self.player2.hasDiamonds, self.player2.hasSpades, self.player2.hasHearts]
        player3Has = [self.player3.hasClubs, self.player3.hasDiamonds, self.player3.hasSpades, self.player3.hasHearts]
        
        player1Suits = []
        player2Suits = []
        player3Suits = []
        
        i = 0
        for has in player1Has:
            if(has):
                player1Suits.append(suits[i])
            i = i + 1
        
        i = 0
        for has in player2Has:
            if(has):
                player2Suits.append(suits[i])
            i = i + 1
            
        i = 0
        for has in player3Has:
            if(has):
                player3Suits.append(suits[i])
            i = i + 1
                
            
        
        if(len(node.board) == 3): # Only Monte has not played
            card1 = node.board[0]
            card2 = node.board[1]
            card3 = node.board[2]
            
            child = Node([card1, card2, card3, card], hand)
            child.parent = node
            child.curTrump = str(card1)[-1]
            node.children.append(child) 
            
        elif(len(node.board) == 2): # player 1 has not played
            
            card2 = node.board[0]
            card3 = node.board[1]
    
            for otherPlay3 in player1Suits:
                for card1 in otherPlay3:
                    if((card1 != card3) and (card2 != card3)):
                        child = Node([card1, card2, card3, card], hand)
                        child.parent = node
                        child.curTrump = str(card1)[-1]
                        node.children.append(child)  
            
        elif(len(node.board) == 1): # player 1 and player 2 have not played
            
            card3 = node.board[0]

            for otherPlay1 in player1Suits:
                for otherPlay2 in player2Suits:
                    for card1 in otherPlay1:
                        for card2 in otherPlay2:
                            if((card1 != card2) and (card1 != card3) and (card2 != card3)):
                                child = Node([card1, card2, card3, card], hand)
                                child.parent = node
                                child.curTrump = str(card1)[-1]
                                node.children.append(child) 
    
        else: # no one has played
            for otherPlay1 in player1Suits:
                for otherPlay2 in player2Suits:
                    for otherPlay3 in player3Suits:
                        for card1 in otherPlay1:
                            for card2 in otherPlay2:
                                for card3 in otherPlay3:
                                    if((card1 != card2) and (card1 != card3) and (card2 != card3)):
                                        child = Node([card1, card2, card3, card], hand)
                                        child.parent = node
                                        child.curTrump = str(card1)[-1]
                                        node.children.append(child)  
        
        return node
                                         
    def rollout(self, node): #written
        """Plays a random game to the finish, recording the total score"""
        
        score = 0
        if(node.curhand == None):
            print("ruh roh")
            return score
        
        copiedNode = copy.deepcopy(node)
        copyGameClubs = copy.deepcopy(self.gameClubs)
        copyGameDiamonds = copy.deepcopy(self.gameDiamonds)
        copyGameHearts = copy.deepcopy(self.gameHearts)
        copyGameSpades = copy.deepcopy(self.gameSpades)
        
        gameSuits = [copyGameClubs, copyGameDiamonds, copyGameHearts, copyGameSpades]
        gameCardList = []
        for suit in gameSuits:
            for card in suit:
                gameCardList.append(card)
    
        handSuits = [copiedNode.curhand.clubs, copiedNode.curhand.diamonds, copiedNode.curhand.hearts, copiedNode.curhand.spades]
        handCardList = []
        for suit in handSuits:
            for card in suit:
                handCardList.append(card)
               
        x = len(handCardList)
        while(x != 0): #while non terminal
            # print(x)
            
            if(len(copiedNode.board) == 4):
                trump = copiedNode.curTrump
                board = copiedNode.board
                
            elif(len(copiedNode.board) == 3):
                monteCard = random.choice(handCardList)
                handCardList.remove(monteCard)

                copiedNode.board.append(monteCard)
                trump = copiedNode.curTrump
                board = copiedNode.board
            
            elif(len(copiedNode.board) == 2):
                randPlayer1Card = random.choice(gameCardList)
                gameCardList.remove(randPlayer1Card)
                monteCard = random.choice(handCardList)
                handCardList.remove(monteCard)

                copiedNode.board.append(randPlayer1Card)
                copiedNode.board.append(monteCard)
                trump = copiedNode.curTrump
                board = copiedNode.board
                
            elif(len(copiedNode.board) == 1):
                randPlayer1Card = random.choice(gameCardList)
                gameCardList.remove(randPlayer1Card)
                randPlayer2Card = random.choice(gameCardList)
                gameCardList.remove(randPlayer2Card)
                monteCard = random.choice(handCardList)
                handCardList.remove(monteCard)
                
                copiedNode.board.append(randPlayer1Card)
                copiedNode.board.append(randPlayer2Card)
                copiedNode.board.append(monteCard)
                
                trump = copiedNode.curTrump
                board = copiedNode.board
                
            else:
                randPlayer1Card = random.choice(gameCardList)
                gameCardList.remove(randPlayer1Card)
                randPlayer2Card = random.choice(gameCardList)
                gameCardList.remove(randPlayer2Card)
                randPlayer3Card = random.choice(gameCardList)
                gameCardList.remove(randPlayer3Card)
                
                monteCard = random.choice(handCardList)
                handCardList.remove(monteCard)

                board = [randPlayer1Card, randPlayer2Card, randPlayer3Card, monteCard] 
                trump = str(random.choice(board))[-1] 
            
            high = random.choice(board)
            for card in board:
                if((str(card)[-1] == trump) and (card > high)):
                    high = card
                    
            if(board[3] == high):
                for card in board:
                    if(str(card)[-1] == "h"):
                        score = score + 1
                    if(str(card) == "Qs"):
                        score = score + 13 
            
            x = x - 1
            
        # print(score)
        return score
        # while(node.curhand is not None): #while non terminal (none because it is a hand)
        #     if(len(node.children) == 1):
        #         node = node.children[0]
        #     elif(len(node.children) != 0):
        #         node = self.bestMathPick(node)
        
        #     if(node.curTrump == "Unset"):
        #         node.curTrump == str(node.board[0])[-1]
        #     high = node.board[0]
        #     for card in node.board:
        #         if(node.curTrump == str(card)[-1]):     
        #             if(high.rank < card.rank):
        #                 high = card
                    
        #     score = 0
        #     if(node.board[1] == high):
        #         for card in node.board:
        #             if(str(card)[-1] == "h"):
        #                 score = score + 1
        #             if(str(card) == "Qs"):
        #                 score = score + 13 
        #     return score
                            
    def backProp(self, node, result): #written 
        """Back propagates the tree itteratively (also contains recursive code)"""
        
        while node.parent is not None:
            node.numVisit = node.numVisit + 1
            node.value = node.value + result
            node = node.parent
        
        # if(node == None):
        #     return
        # else:
        #     node.numVisit = node.numVisit + 1
        #     node.value = node.value + result
        #     self.backProp(node.parent, result)
    
    def bestChild(self, node): #written
        """Returns the "best" node of the one with the most visits - Can be modified to use confidence bounds (better)"""
        pick = Node([], node.curhand)
        pick.value = 30 #highest possible score is 26
        
        childrenInSuit = False
        
        for child in node.children:
            childTrump = str(child.board[1])[-1]
            
            if(self.trickNum == 0): #will consider everything but hearts and the queen of spades on first trick)
                if(childTrump != "h"): #if not a heart
                   if(str(child.board[-1]) != "Qs"): #or queen of spades on the first trick, consider it
                        if(childTrump == node.curTrump): #if in the correct suit, consider it (will consider anything in right suit)
                        # if(child.value < pick.value):
                        #     pick = child 
                            if (childrenInSuit == False):
                                pick = child
                                childrenInSuit = True
                            elif(pick is not None):
                                if(self.calculateUCB(child) < self.calculateUCB(pick)):
                                    pick = child 
                            else:
                                pick = child
                                # print("pick value is " + str(pick.value))
                                
                        elif(pick is not None and childrenInSuit == False):
                            if(self.calculateUCB(child) < self.calculateUCB(pick)):
                                pick = child 
                        elif(childrenInSuit == False):
                            pick = child
                            # print("pick value is " + str(pick.value))
            
                    # print("pick value is " + str(pick.value))

            elif(((self.heartsBroken == True) or (len(self.hand.hearts) == self.hand.size())) and (childrenInSuit == False)): #if hearts have been broken or monte only has hearts, consider it (only will consider hearts)
                # if(child.value < pick.value):
                #     pick = child
                if(pick is not None):
                    if(self.calculateUCB(child) < self.calculateUCB(pick)):
                        pick = child 
                else:
                    pick = child
                    # print("pick value is " + str(pick.value))
      
            elif((self.heartsBroken == False) and (childrenInSuit == False)): #if there are no children in suit and hearts have not been broken
                # if(child.value < pick.value):
                #     pick = childs
                if(childTrump != "h"):
                    if(pick is not None):
                        if(self.calculateUCB(child) < self.calculateUCB(pick)):
                            pick = child 
                    else:
                        pick = child
                
            # elif(childrenInSuit == False):  
            #     # if(child.value < pick.value):
            #     #     pick = childs
            #     if(pick is not None):
            #         if(self.calculateUCB(child) < self.calculateUCB(pick)):
            #             pick = child 
            #     else:
            #         pick = child
                    
        return pick
    
    def visualizeTree(self, node, file): #written
        
        file.write("Parent: ")
        printlist = []
        for card in node.board:
            printlist.append(str(card))
        printlist.append("\n")
        file.write(" ".join(printlist))
        
        if(len(node.children) != 0):
            printlist = []       
            for child in node.children:
                file.write(" Child")
                for card in child.board:
                    printlist.append(str(card))
                printlist.append("//")
                file.write(" ".join(printlist))
                file.write("\n")
                self.visualizeTree(child, file)
            
#Notes \/
#board is with ["", "", thing, thing]
#board state is with [thing, thing]

    def playCard(self): #written
        """Redefines playCard from player class to use MonteCarlo"""

        if(self.trickNum == 0 ^ (self.trickNum == 1 and self.hand.didContain2ofClubs)):

            self.gameClubs = [Card(2,0), Card(3,0), Card(4,0), Card(5,0), Card(6,0), Card(7,0), Card(8,0), Card(9,0), Card(10 ,0), Card(11, 0), Card(12,0), Card(13,0), Card(14,0)]
            self.gameDiamonds = [Card(2,1), Card(3,1), Card(4,1), Card(5,1), Card(6,1), Card(7,1), Card(8,1), Card(9,1), Card(10 ,1), Card(11, 1), Card(12,1), Card(13,1), Card(14,1)]
            self.gameSpades = [Card(2,2), Card(3,2), Card(4,2), Card(5,2), Card(6,2), Card(7,2), Card(8,2), Card(9,2), Card(10 ,2), Card(11, 2), Card(12,2), Card(13,2), Card(14,2)]
            self.gameHearts = [Card(2,3), Card(3,3), Card(4,3), Card(5,3), Card(6,3), Card(7,3), Card(8,3), Card(9,3), Card(10 ,3), Card(11, 3), Card(12,3), Card(13,3), Card(14,3)]
            
            ### remove what is in the hand ###
            for card in self.hand.clubs:
                for secondCard in self.gameClubs:
                    if card.isCard(secondCard):
                        self.gameClubs.remove(secondCard)
            
            for card in self.hand.diamonds:
                 for secondCard in self.gameDiamonds:
                    if card.isCard(secondCard):
                        self.gameDiamonds.remove(secondCard)
                    
            for card in self.hand.hearts:
                 for secondCard in self.gameHearts:
                    if card.isCard(secondCard):
                        self.gameHearts.remove(secondCard)
                    
            for card in self.hand.spades:
                 for secondCard in self.gameSpades:
                    if card.isCard(secondCard):
                        self.gameSpades.remove(secondCard)
                    
        ### remove what has been played already ###

        if(self.trickNum != 0):
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
        
        if(self.trickNum != 0):
            for card in self.boardState:
                if(str(card)[-1] == "c" and (card in self.gameClubs)):
                    self.gameClubs.remove(card)
                
                if(str(card)[-1] == "d" and (card in self.gameDiamonds)):
                    self.gameDiamonds.remove(card)
                
                if(str(card)[-1] == "h" and (card in self.gameHearts)):
                    self.gameHearts.remove(card)
                
                if(str(card)[-1] == "s" and (card in self.gameSpades)):
                    self.gameSpades.remove(card)
                
        # erCheck = []
        # for card in self.gameClubs:
        #     erCheck.append(str(card))
        # for card in self.gameHearts:
        #     erCheck.append(str(card))
        # for card in self.gameDiamonds:
        #     erCheck.append(str(card))
        # for card in self.gameSpades:
        #     erCheck.append(str(card))
        # print(erCheck)
        
        root = Node(self.boardState, self.hand)
        root.curTrump = self.curTrump
        card = self.MonteSearch(root) #do the algo and get the best card
        
        # board = []
        # for item in card.board:
        #     board.append(str(item))
        # print(board)
         
        # print(self.trickHistory)   
        
        # if(self.trickNum == 2): # Printed version exists at the moment for 1 round of tree stuff
        #     wFile = open("tree.txt", "w")
        #     self.visualizeTree(root, wFile)
        
        self.prevBoardNum = len(self.boardState)
        self.pastTrump = self.curTrump
        
        return card.board[1] #return the best
    
    def play(self, option='play', discarded=None, c=None, auto=True): #written - taken from player
        """Redefines play from player class to if auto call playCard defined above"""
        if auto:
            card = self.playCard()
        elif c is None:
            card = self.getInput(option)
        else:
            card = c
        if not auto:
            card = self.hand.hasCard(card)
        return card
    
### Next Steps ###

# Find a good constant
# Write in the consideration for what other players hands are
    # ex: Player 1 played off the suit, they do not have a suit do not consider that suit
        #could be expanded into do not consider that combination (will make the tree smaller, might need to adjust constant)
# Add in shoot the moon
    # might be as simple as changing the signs to pick greatest value
        #possible additions: bul to make it stick to one strat, conditions to switch strats (what val could be achevied as close to 26 as pos), etc.

