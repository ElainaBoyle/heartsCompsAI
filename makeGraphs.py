
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

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

fileName = "RRRM"

rFile = open(fileName + ".txt", "r")
players = ["Random 1", "Random 2", "Random 3", "Monte Carlo"]
# "Hueristic 1"  #Breanna 
# "Hueristic 2" #Elek
# "Random 1" #Random 1
# "Random 2" #Random 2
# "Random 3" #Random 3
# "Monte Carlo" #Monte
# "CBR" #MarySue
# "Strong Agent" #Strong

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

print("\nElek Stats:\nTotal Games Won:", ElekGameWins, "\nTotal Tricks Won:", ElekTrickWins, "\nAverage Score:", (ElekTotalScore/100))
print("\nBreanna Stats:\nTotal Games Won:", BreannaGameWins, "\nTotal Tricks Won:", BreannaTrickWins, "\nAverage Score:", (BreannaTotalScore/100))
print("\nMarySue Stats:\nTotal Games Won:", MarySueGameWins, "\nTotal Tricks Won:", MarySueTrickWins, "\nAverage Score:", (MarySueTotalScore/100))
print("\nMonte Stats:\nTotal Games Won:", MonteGameWins, "\nTotal Tricks Won:", MonteTrickWins, "\nAverage Score:", (MonteTotalScore/100))
print("\n")

winnerList = []
winnerList.append((players[0], ElekGameWins))
winnerList.append((players[1], BreannaGameWins))
winnerList.append((players[2], MarySueGameWins))
winnerList.append((players[3], MonteGameWins))

winnerList = sorted(winnerList, key=lambda person: person[1])
winnerList.reverse()

colors = []
for winner in winnerList:
    if(winner[0] == "Hueristic 1"): #Breanna 
        colors.append("#454AE2")
    elif(winner[0] == "Hueristic 2"):#Elek
        colors.append("#696EFF")
    elif(winner[0] == "Random 1"):#Random 1
        colors.append("#8AEA7A")
    elif(winner[0] == "Random 2"):#Random 2
        colors.append("#57B656")
    elif(winner[0] == "Random 3"):#Random 3
        colors.append("#248232")
    elif(winner[0] == "Monte Carlo"):#Monte
        colors.append("#C279D6")
    elif(winner[0] == "CBR"):#MarySue
        colors.append("#34F9DC")
    elif(winner[0] == "Strong Agent"):#Strong
        colors.append("#F991CC")
        
    
place = 0
for person in winnerList:
    place = place + 1
    print(person[0], "came in", place, "place with", person[1], "games won!")

leftCords = [1, 2, 3, 4]
players = [winnerList[0][0], winnerList[1][0], winnerList[2][0], winnerList[3][0]]
wins = [winnerList[0][1], winnerList[1][1], winnerList[2][1], winnerList[3][1]]

plt.bar(players, wins, color=colors)
plt.xlabel('Agents')
plt.ylabel('Games Won')
plt.title('Games Won by Agents')
plt.savefig(fileName)
plt.show()

rFile.close()
