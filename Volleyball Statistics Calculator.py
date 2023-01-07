#!/usr/bin/python3

import tkinter,tkinter.filedialog,tkinter.messagebox,sys
from tabulate import tabulate

## Author: Pierson Polcaro

statNames = ("Sets Played","Attempts","Kills","Errors","Assists","Service attempts","Service aces",
             "Service errors","Digs","Serve receive error","1 pass","2 pass","3 pass",
             "Blocking error","Solo block","Blocking assist","Ball handling error")
infoNames = ("Hitting %","Serving %","Serve receive","Total errors")
other = ("Matches Played","MP")
statAbbreviations = ("SP","TA","K","E","A","ATT","SA","SE","DIG","SRE","SR1","SR2","SR3","BE","BS","BA","BHE")
infoAbbreviations = ("HIT %","SRV %","SR","TE")
emptyLine = ["TEAM",'0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
stats = ["",*(0 for item in range(len(statNames + infoNames)))]
data = []
def askForMore():
    return tkinter.messagebox.askyesno("More files","Are there more save files to load?")
def newDivide(top,bot):
    try:
        return str(round(top/bot,5))
    except ZeroDivisionError:
        return "0"


# Asks for save file and loads data into array of files- files[file][line][char]
files = []
while True:
    try:
        dat = tkinter.filedialog.askopenfilename(filetypes=[("Text files","*.txt")])
        with open(dat,"r") as f:
            files.append(f.read().splitlines())
        if files != [""] and not askForMore():
            break
    except:
        res = tkinter.messagebox.askyesno("No file","You did not select a file, would you like to quit?")
        if res:
            sys.exit()


# Finds number of sets played, points, and side out/serve holding %s for the team
# Also finds the number of players and adds their names to data
totalSets = 0
myPoints = 0
theirPoints = 0
players = 0
sideoutPotential = 0
sideoutActual = 0
serveholdPotential = 0
serveholdActual = 0
check = False
for file in range(len(files)):
    try:
        totalSets += int(files[file][13][0]) + int(files[file][13][2])
        if files[file][8].index(files[file][15][11:]) == 0:
            home = False
        else:
            home = True
    except:
        tkinter.messagebox.showwarning("Error", "Invalid file selected\nProgram exiting")
        sys.exit()
    for line in range(len(files[file])):
        if files[file][line][:7] == "TOTALS:":
            check = True
            homePoints = int(files[file][line+1][:files[file][line+1].index("-")])
            awayPoints = int(files[file][line+1][files[file][line+1].index("-")+1:])
            sideoutActual += int(files[file][line+2].split()[3].split("/")[0])
            sideoutPotential += int(files[file][line+2].split()[3].split("/")[1])
            serveholdActual += int(files[file][line+3].split()[3].split("/")[0])
            serveholdPotential += int(files[file][line+3].split()[3].split("/")[1])
        if check and files[file][line+6][:4] == "TEAM":
            check = False
            break
        if check:
            data.append(stats.copy())
            data[players][0] = files[file][line+7].split()[0]
            players += 1
    myPoints += homePoints if home else awayPoints
    theirPoints += awayPoints if home else homePoints


# Finds each player's stats and puts their totals into data
player = -1
check = False
check2 = False
for file in range(len(files)):
    for line in range(len(files[file])):
        if check:
            player += 1
        if files[file][line][:7] == "TOTALS:":
            check = True
            if not check2:
                player = -1
                check2 = True
            continue
        if check:
            chopped = files[file][line+6].split()
            for stat in range(1,len(chopped)):
                if stat > len(chopped) - 5 and stat < len(chopped) - 1:
                    continue
                else:
                    data[player][stat] += int(chopped[stat])
        if check and files[file][line+6][:4] == "TEAM":
            check = False


# Combines entries for players with the same name based on spelling (capitalization does not matter)
data = sorted(data)
newData = []
first = data.pop(0)
name = first[0].lower()
datt = [first]
for ind in range(len(data)):
    if data[0][0].lower() == name:
        datt.append(data.pop(0))
    else:
        newData.append([" ".join(n.capitalize() if not n == "team" else n.upper() for n in name.split("_")),*(sum(datt[i][j] for i in range(len(datt))) for j in range(1,len(datt[0])))])
        first = data.pop(0)
        name = first[0].lower()
        datt = [first]
newData.append([" ".join(n.capitalize() if not n == "team" else n.upper() for n in name.split("_")),*(sum(datt[i][j] for i in range(len(datt))) for j in range(1,len(datt[0])))])


# Moves team stats to the end and sets team sets
for i in range(len(newData)):
    if newData[i][0] == "TEAM":
        ind = i
        break
newData[ind][1] = totalSets
newData += [newData.pop(ind)]


# Recalculates averages
def hittingPercentage(att,kill,err):
    try:
        return round((kill-err)/att,5)
    except ZeroDivisionError:
        return 0
def servePercentage(att,err):
    try:
        return round((att-err)/att,5)
    except ZeroDivisionError:
        return 0
def srAverage(points,total):
    try:
        return round(points/total,5)
    except ZeroDivisionError:
        return 0
for player in range(len(newData)):
    newData[player][18] = hittingPercentage(newData[player][2],newData[player][3],newData[player][4])
    newData[player][19] = servePercentage(newData[player][6],newData[player][8])
    temp = newData[player][11] + 2*newData[player][12] + 3*newData[player][13]
    temp2 = sum(newData[player][st] for st in (10,11,12,13))
    newData[player][20] = srAverage(temp,temp2)


# Finds matches played for each player and for the team
matchesPlayed = {}
for p in range(len(newData)):
    matchesPlayed[newData[p][0].lower()] = 0
teamMatches = 0
for file in range(len(files)):
    teamMatches += 1
    for line in range(len(files[file])):
        if files[file][line][:7] == "TOTALS:":
            check = True
            continue
        if check and files[file][line+6][:4] == "TEAM":
            matchesPlayed["team"] = teamMatches
            check = False
            break
        if check:
            splitLine = files[file][line+6].split()
            if int(splitLine[1]) > 0:
                matchesPlayed[splitLine[0].lower()] += 1


# Creates output and adds season totals
output = "Statistics: " + ", ".join(["{} ({})".format(statNames[ind],statAbbreviations[ind]) for ind in range(len(statNames))])
output = output[:output.index("SA")+4] + "\n" + " "*11 + output[output.index("SA")+4:output.index("SR3")+5] + "\n" + " "*11 + output[output.index("SR3")+5:]
output += "\nCalculations: " + ", ".join(["{} ({})".format(infoNames[ind],infoAbbreviations[ind]) for ind in range(len(infoNames))])
output += "\nOther: " + other[0] + " (" + other[1] + ")\nPoints are formatted [your team]-[opponents]"
output += "\n\n-------------------------------------------------\nSeason totals:\nPoints: " + str(myPoints) + "-" + str(theirPoints)
output += "\nSide out %- " + str(sideoutActual) + "/" + str(sideoutPotential) + " --> " + newDivide(sideoutActual,sideoutPotential)
output += "\nServe hold %- " + str(serveholdActual) + "/" + str(serveholdPotential) + " --> " + newDivide(serveholdActual,serveholdPotential) + "\n\n"
for p in range(len(newData)):
    newData[p].insert(1,matchesPlayed[newData[p][0].lower()])
output += tabulate(newData,headers=("PLAYERS",other[1],*(item for item in statAbbreviations),*(item for item in infoAbbreviations)))
for p in range(len(newData)):
    newData[p].pop(1)
output += "\n\n-----------------------\nPer set averages:\nPoints: " + newDivide(myPoints,newData[-1][1]) + "-" + newDivide(theirPoints,newData[-1][1])
output += "\nSide out %- " + newDivide(sideoutActual,newData[-1][1]) + "/" + newDivide(sideoutPotential,newData[-1][1])
output += " --> " + newDivide(sideoutActual,sideoutPotential) + "\nServe hold %- " + newDivide(serveholdActual,newData[-1][1])
output += "/" + newDivide(serveholdPotential,newData[-1][1]) + " --> " + newDivide(serveholdActual,serveholdPotential)
output += "\n\n"
for player in range(len(newData)):
    for stat in range(2,len(newData[player])):
        if stat not in (18,19,20):
            newData[player][stat] = newDivide(newData[player][stat],newData[player][1])
output += tabulate(newData,headers=("PLAYERS",*(item for item in statAbbreviations),*(item for item in infoAbbreviations))) 


# Saves output to file
file = tkinter.filedialog.asksaveasfile(mode='w',defaultextension='.txt')
if file != None:
    file.write(output)
    file.close()
    tkinter.messagebox.showinfo("Saved","Data saved successfully")
else:
    tkinter.messagebox.showwarning("Error", "Data save cancelled\nProgram exiting")
