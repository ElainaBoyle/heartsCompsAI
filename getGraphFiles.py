"""Makes a file with however many games that are needed. Please make sure to change the file name in wFile = open"""

import os

wFile = open("RRCM.txt", "w")

for i in range(100):
    result = os.popen("python3 HeartsGraphics.py").read()
    wFile.write(result)
    wFile.write("\n space \n")
    print("Played game:", i)
    
wFile.close()