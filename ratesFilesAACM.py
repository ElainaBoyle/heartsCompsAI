import os

wFile = open("AACM.txt", "w")

for i in range(120):
    print("Playing game:", i)
    result = os.popen("python3 HeartsEditedAACM.py").read()
    wFile.write(result)
    wFile.write("\n space \n")
    print("Played game:", i)
    
wFile.close()
