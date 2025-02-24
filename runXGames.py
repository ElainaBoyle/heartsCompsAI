import os

"""This file is the chopped up version of rates.py in which it just runs the games and outputs them to a file for running the games 
the computer that we are assigned to by Mike Tie so that it can be done remotely. If you would like to have an account of the comptuter 
you need to contact and set up a meeting with Mike Tie. The computer we are on address is olin312-05.mathcs.carleton.edu"""

wFile = open("GamesRan.txt", "w")

numOfGames = 100
for i in range(numOfGames):
    result = os.popen("python3 Hearts.py").read()
    wFile.write(result)
    wFile.write("\n space \n")
    
wFile.close()

