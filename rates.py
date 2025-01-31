import os
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

wFile = open("rates.txt", "w")

for i in range(10):
    result = os.popen("python3 Hearts.py").read()
    wFile.write(result)
    wFile.write("\n space \n")
    print("Played game:", i)
    
wFile.close()

ElekTrickWins = 0
ElekGameWins = 0
ElekTotalScore = 0

BreannaTrickWins = 0
BreannaGameWins = 0
BreannaTotalScore = 0

MarySueTrickWins = 0
MarySueGameWins = 0
MarySueTotalScore = 0

MonteTrickWins = 0
MonteGameWins = 0
MonteTotalScore = 0

ElekScoreLine = ""
BreannaScoreLine = ""
MarySueScoreLine = ""
MonteScoreLine = ""
previous = ""


rFile = open("rates.txt", "r")
#self.players = [Elek_Agent("Elek"), BreannaAgent("Breanna"), Player("MarySue"), Player("Monte")]
for line in rFile:
    
    if(previous.find("wins!") != -1):
        ElekScoreLineList = ElekScoreLine.split(" ")
        BreannaScoreLineList = BreannaScoreLine.split(" ")
        MarySueScoreLineList = MarySueScoreLine.split(" ")
        MonteScoreLineList = MonteScoreLine.split(" ")
        
        ElekTotalScore = ElekTotalScore + int(ElekScoreLineList[1])
        BreannaTotalScore = BreannaTotalScore + int(BreannaScoreLineList[1])
        MarySueTotalScore = MarySueTotalScore + int(MarySueScoreLineList[1])
        MonteTotalScore = MonteTotalScore + int(MonteScoreLineList[1])
    if(line.find("Elek wins!") != -1):
        ElekGameWins = ElekGameWins + 1
    if(line.find("Elek won the trick") != -1):
        ElekTrickWins = ElekTrickWins + 1
    if(line.find("Breanna wins!") != -1):
        BreannaGameWins = BreannaGameWins + 1
    if(line.find("Breanna won the trick") != -1):
        BreannaTrickWins = BreannaTrickWins + 1
    if(line.find("MarySue wins!") != -1):
        MarySueGameWins = MarySueGameWins + 1
    if(line.find("MarySue won the trick") != -1):
        MarySueTrickWins = MarySueTrickWins + 1
    if(line.find("Monte wins!") != -1):
        MonteGameWins = MonteGameWins + 1
    if(line.find("Monte won the trick") != -1):
        MonteTrickWins = MonteTrickWins + 1
        
    ElekScoreLine = BreannaScoreLine
    BreannaScoreLine = MarySueScoreLine
    MarySueScoreLine = MonteScoreLine
    MonteScoreLine = previous
    previous = line

print("\nElek Stats:\nTotal Games Won:", ElekGameWins, "\nTotal Tricks Won:", ElekTrickWins, "\nAverage Score:", (ElekTotalScore/1000))
print("\nBreanna Stats:\nTotal Games Won:", BreannaGameWins, "\nTotal Tricks Won:", BreannaTrickWins, "\nAverage Score:", (BreannaTotalScore/1000))
print("\nMarySue Stats:\nTotal Games Won:", MarySueGameWins, "\nTotal Tricks Won:", MarySueTrickWins, "\nAverage Score:", (MarySueTotalScore/1000))
print("\nMonte Stats:\nTotal Games Won:", MonteGameWins, "\nTotal Tricks Won:", MonteTrickWins, "\nAverage Score:", (MonteTotalScore/1000))
print("\n")

winnerList = []
winnerList.append(("Elek", ElekGameWins))
winnerList.append(("Breanna", BreannaGameWins))
winnerList.append(("MarySue", MarySueGameWins))
winnerList.append(("Monte", MonteGameWins))

winnerList = sorted(winnerList, key=lambda person: person[1])
winnerList.reverse()

place = 0
for person in winnerList:
    place = place + 1
    print(person[0], "came in", place, "place with", person[1], "games won!")

leftCords = [1, 2, 3, 4]
players = [winnerList[0][0], winnerList[1][0], winnerList[2][0], winnerList[3][0]]
wins = [winnerList[0][1], winnerList[1][1], winnerList[2][1], winnerList[3][1]]

plt.bar(players, wins, color=['green', 'blue', 'purple', 'red'])
plt.xlabel('Players')
plt.ylabel('Games Won')
plt.title('Games Won by Players')
plt.show()

rFile.close()
