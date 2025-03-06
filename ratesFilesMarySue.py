import os

wFile = open("MarySueNewVersion.txt", "w")

for i in range(100):
    print("Playing game:", i)
    result = os.popen("python3 HeartsEdited.py").read()
    wFile.write(result)
    wFile.write("\n space \n")
    print("Played game:", i)
    
wFile.close()
