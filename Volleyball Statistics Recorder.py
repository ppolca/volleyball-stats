#!/usr/bin/python3

import tkinter,tkinter.filedialog,tkinter.simpledialog,tkinter.messagebox,sys,datetime
from tabulate import tabulate

## Author: Pierson Polcaro

bad = False
temp = tkinter.Tk()
width = temp.winfo_screenwidth()
height = temp.winfo_screenheight()
temp.destroy()

# Functions to make a box to collect the names of players
def gatherEntries():
    global players
    players = list(filter(None, ["_".join(eval("p" + str(i) + "name").get().split()) for i in range(1, 17)]))
    if len(players) < 6 or len(players) > 16:
        tkinter.messagebox.showwarning("Error","Please make sure you have between 6 and 16 players entered!")
    else:
        box.destroy()
def getPlayers():
    global p1name,p2name,p3name,p4name,p5name,p6name,p7name,p8name,p9name,p10name,p11name,p12name,p13name,p14name,p15name,p16name,box,bad
    box = tkinter.Tk()
    width = box.winfo_screenwidth()
    height = box.winfo_screenheight()
    box.title("Players")
    geo = "350x500+" + str(int(width/2-175)) + "+" + str(int(height/2-250))
    box.geometry(geo)
    for rows in range(100):
        box.rowconfigure(rows,weight=1)
        box.columnconfigure(rows,weight=1)
    instructions = tkinter.Label(box,text="Please enter the names of the players you wish to track")
    instructions.grid(row=5,column=50)
    instructionsPT2 = tkinter.Label(box,text="Leave boxes blank after you finish with your players")
    instructionsPT2.grid(row=7,column=50)
    p1 = tkinter.Label(box,text="1:")
    p2 = tkinter.Label(box,text="2:")
    p3 = tkinter.Label(box,text="3:")
    p4 = tkinter.Label(box,text="4:")
    p5 = tkinter.Label(box,text="5:")
    p6 = tkinter.Label(box,text="6:")
    p7 = tkinter.Label(box,text="7:")
    p8 = tkinter.Label(box,text="8:")
    p9 = tkinter.Label(box,text="9:")
    p10 = tkinter.Label(box,text="10:")
    p11 = tkinter.Label(box,text="11:")
    p12 = tkinter.Label(box,text="12:")
    p13 = tkinter.Label(box,text="13:")
    p14 = tkinter.Label(box,text="14:")
    p15 = tkinter.Label(box,text="15:")
    p16 = tkinter.Label(box,text="16:")
    a = 15
    for i in (p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16):
        i.grid(row=a,column=40)
        a+=4
    p1name = tkinter.Entry(box)
    p2name = tkinter.Entry(box)
    p3name = tkinter.Entry(box)
    p4name = tkinter.Entry(box)
    p5name = tkinter.Entry(box)
    p6name = tkinter.Entry(box)
    p7name = tkinter.Entry(box)
    p8name = tkinter.Entry(box)
    p9name = tkinter.Entry(box)
    p10name = tkinter.Entry(box)
    p11name = tkinter.Entry(box)
    p12name = tkinter.Entry(box)
    p13name = tkinter.Entry(box)
    p14name = tkinter.Entry(box)
    p15name = tkinter.Entry(box)
    p16name = tkinter.Entry(box)
    a = 15
    for i in (p1name,p2name,p3name,p4name,p5name,p6name,p7name,p8name,p9name,p10name,p11name,p12name,p13name,p14name,p15name,p16name):
        i.grid(row=a,column=50)
        a+=4
    submit = tkinter.Button(box,text="Submit",command=gatherEntries)
    submit.grid(row=90,column=50)
    box.mainloop()
    try:
        return players
    except NameError:
        bad = True
        return

# Functions to modify button text
def add(button,attempt,attNum):
    """
    Button is a tuple in the form (button reference, button name)
    Attempt is if an attempt must be added also
    attNum is 0 if attempt is false
    attNum is 1 if it is an attack
    attNum is 2 if it is a serve
    playNum is the x in "sX_Y"
    butNum is the y in "sX_Y"
    """
    playNum = button[1].split("_")[0][1:]
    butNum = int(button[1].split("_")[1])
    totalLabel = "t_" + button[1].split("_")[1]
    if not edit:
        button[0]["text"] = int(button[0]["text"]) + 1
        exec(totalLabel + "['text'] = int(" + totalLabel + "['text']) + 1")
        if attempt:
            addAtt(attNum,playNum)
    else:
        if attempt:
            if butNum in (2,3):
                temp = "_1"
            if butNum in (6,7):
                temp = "_5"
            if eval(button[1].split("_")[0] + temp)['text'] > 0 and button[0]["text"] > 0:
                button[0]["text"] = int(button[0]["text"]) - 1
                exec(totalLabel + "['text'] = int(" + totalLabel + "['text']) - 1")
                addAtt(attNum,playNum)
        elif button[0]["text"] > 0:
            if butNum == 1:  # check attempts >= kills+errors
                but1 = eval(button[1].split("_")[0] + "_2")
                but2 = eval(button[1].split("_")[0] + "_3")
                if but1['text'] + but2['text'] < button[0]['text']:
                    button[0]["text"] = int(button[0]["text"]) - 1
                    exec(totalLabel + "['text'] = int(" + totalLabel + "['text']) - 1")
            elif butNum == 5:
                but1 = eval(button[1].split("_")[0] + "_6")
                but2 = eval(button[1].split("_")[0] + "_7")
                if but1['text'] + but2['text'] < button[0]['text']:
                    button[0]["text"] = int(button[0]["text"]) - 1
                    exec(totalLabel + "['text'] = int(" + totalLabel + "['text']) - 1")
            else:
                button[0]["text"] = int(button[0]["text"]) - 1
                exec(totalLabel + "['text'] = int(" + totalLabel + "['text']) - 1")
    updateInfo()
def addAtt(attNum,playerNum):
    code = ""
    if attNum == 1:
        code = "s" + str(playerNum) + "_1"
    if attNum == 2:
        code = "s" + str(playerNum) + "_5"
    code = "add((" + code + ",'" + code + "'),False,0)"
    exec(code)
def play(button):
    """Button is a tuple in the form (button reference, button name)"""
    totalLabel = "t_" + button[1].split("_")[1]
    if button[0]['text'] == "N":
        button[0]['text'] = "Y"
        exec(totalLabel + "['text'] = int(" + totalLabel + "['text']) + 1")
    if edit and button[0]['text'] == "Y":
        button[0]["text"] = "N"
        exec(totalLabel + "['text'] = int(" + totalLabel + "['text']) - 1")
def pointScore(teamButton):
    if not edit:
        teamButton['text'] = int(teamButton['text']) + 1
        eval("set" + str(currSet["text"]) + "serves").append(homeTeam if teamButton == homeScore else awayTeam)
    else:
        if teamButton['text'] > 0:
            teamButton['text'] = int(teamButton['text']) - 1
            eval("set" + str(currSet["text"]) + "serves").pop(len(eval("set" + str(currSet["text"]) + "serves"))-1-eval("set" + str(currSet["text"]) + "serves")[::-1].index(homeTeam if teamButton == homeScore else awayTeam))
    setScoreStats(currSet["text"])
def getScoreStats(s):
    sideoutPotential = 0
    sideoutActual = 0
    serveHoldPotential = 0
    serveHoldActual = 0
    for serve in range(len(eval("set" + str(s) + "serves"))-1):
        if eval("set" + str(s) + "serves")[serve] != myTeam:
            sideoutPotential += 1
            if eval("set" + str(s) + "serves")[serve+1] == myTeam:
                sideoutActual += 1
        else:
            serveHoldPotential += 1
            if eval("set" + str(s) + "serves")[serve+1] == myTeam:
                serveHoldActual += 1
    return [sideoutActual,sideoutPotential,serveHoldActual,serveHoldPotential]
def setScoreStats(s):
    sideoutPotential = 0
    sideoutActual = 0
    serveHoldPotential = 0
    serveHoldActual = 0
    for serve in range(len(eval("set" + str(s) + "serves"))-1):
        if eval("set" + str(s) + "serves")[serve] != myTeam:
            sideoutPotential += 1
            if eval("set" + str(s) + "serves")[serve+1] == myTeam:
                sideoutActual += 1
        else:
            serveHoldPotential += 1
            if eval("set" + str(s) + "serves")[serve+1] == myTeam:
                serveHoldActual += 1
    try:
        sideoutNum["text"] = str(round(sideoutActual/sideoutPotential,5))
    except ZeroDivisionError:
        sideoutNum["text"] = 0
    try:
        serveHoldNum["text"] = str(round(serveHoldActual/serveHoldPotential,5))
    except ZeroDivisionError:
        serveHoldNum["text"] = 0
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
def updateInfo():
    pHAttempts,pHKills,pHErrors,pSAttempts,pSAces,pSErrors,pSRPoints,pSRNumber,pErrors = [0] * 9
    tHAttempts,tHKills,tHErrors,tSAttempts,tSAces,tSErrors,tSRPoints,tSRNumber,tErrors = [0] * 9
    for p in range(len(players)+1): # hitting info
        if p != len(players):
            pHAttempts = eval("s" + str(p+1) + "_1")['text']
            tHAttempts += pHAttempts
            pHKills = eval("s" + str(p+1) + "_2")['text']
            tHKills += pHKills
            pHErrors = eval("s" + str(p+1) + "_3")['text']
            tHErrors += pHErrors
            eval("i" + str(p+1) + "_0")['text'] = hittingPercentage(pHAttempts,pHKills,pHErrors)
        else:
            eval("te_0")['text'] = hittingPercentage(tHAttempts,tHKills,tHErrors)
    for p in range(len(players) + 1):  # serving info
        if p != len(players):
            pSAttempts = eval("s" + str(p+1) + "_5")['text']
            tSAttempts += pSAttempts
            pSAces = eval("s" + str(p+1) + "_6")['text']
            tSAces += pSAces
            pSErrors = eval("s" + str(p+1) + "_7")['text']
            tSErrors += pSErrors
            eval("i" + str(p+1) + "_1")['text'] = servePercentage(pSAttempts,pSErrors)
        else:
            eval("te_1")['text'] = servePercentage(tSAttempts,tSErrors)
    for p in range(len(players)+1): # serve receive info
        if p != len(players):
            pSRPoints = eval("s" + str(p+1) + "_10")['text']
            pSRPoints += 2*eval("s" + str(p+1) + "_11")['text']
            pSRPoints += 3*eval("s" + str(p+1) + "_12")['text']
            tSRPoints += pSRPoints
            pSRNumber = sum(eval("s" + str(p+1) + "_" + str(i))['text'] for i in (9,10,11,12))
            tSRNumber += pSRNumber
            eval("i" + str(p+1) + "_2")['text'] = srAverage(pSRPoints,pSRNumber)
        else:
            eval("te_2")['text'] = srAverage(tSRPoints,tSRNumber)
    for p in range(len(players)+1): # error info
        if p != len(players):
            pErrors = sum(eval("s" + str(p+1) + "_" + str(i))['text'] for i in (3,7,9,13,16))
            tErrors += pErrors
            eval("i" + str(p+1) + "_3")['text'] = pErrors
        else:
            eval("te_3")['text'] = tErrors

# Functions for grabbing all stats and managing it
def setChange(direction):
    global set1,set2,set3,set4,set5
    changed = False
    set = int(currSet['text'])
    exec("global set" + str(set) + "\nset" + str(set) + " = [[] for times in range(len(players)+2)]")
    eval("set" + str(set))[0].append(homeScore['text'])
    eval("set" + str(set))[0].append(awayScore['text'])
    for p in range(len(players)+1):
        eval("set" + str(set))[p+1].append(playerButtons1[p]['text'])
        for s in range(len(statItems)):
            if p == len(players):
                exec("eval('set' + str(set))" + "[p+1].append(t_" + str(s) + "['text'])")
            else:
                exec("eval('set' + str(set))" + "[p+1].append(s" + str(p+1) + "_" + str(s) + "['text'])")
        for i in range(len(infoItems)):
            if p == len(players):
                exec("eval('set' + str(set))" + "[p+1].append(te_" + str(i) + "['text'])")
            else:
                exec("eval('set' + str(set))" + "[p+1].append(i" + str(p+1) + "_" + str(i) + "['text'])")
    if direction == "prev":
        if set > 1:
            currSet['text'] = set - 1
            changed = True
    if direction == "next":
        if set < 5:
            currSet['text'] = set + 1
            changed = True
    set = int(currSet['text'])
    if changed:
        homeScore['text'] = eval("set" + str(set))[0][0]
        awayScore['text'] = eval("set" + str(set))[0][1]
        fsLabel2["text"] = homeTeam if (int(currSet["text"]) + fsHome) % 2 == 0 else awayTeam
        setScoreStats(currSet["text"])
        for p in range(len(players)+1):
            for s in range(len(statItems)):
                if p == len(players):
                    eval("t_" + str(s))['text'] = eval("set" + str(set))[p+1][s+1]
                else:
                    eval("s" + str(p+1) + "_" + str(s))['text'] = eval("set" + str(set))[p+1][s+1]
    updateInfo()
def save():
    setChange("none")
    file = tkinter.filedialog.asksaveasfile(mode='w',defaultextension='.txt')
    if file != None:
        homeSets = sum([1 for test in range(1,6) if eval("set" + str(test))[0][0] > eval("set" + str(test))[0][1]])
        awaySets = sum([1 for test in range(1,6) if eval("set" + str(test))[0][0] < eval("set" + str(test))[0][1]])
        data = "Statistics: " + ", ".join(["{} ({})".format(statNames[ind],statAbbreviations[ind]) for ind in range(len(statNames))])
        data = data[:data.index("SA")+4] + "\n" + " "*11 + data[data.index("SA")+4:data.index("SR3")+5] + "\n" + " "*11 + data[data.index("SR3")+5:]
        data += "\nCalculations: " + ", ".join(["{} ({})".format(infoNames[ind],infoAbbreviations[ind]) for ind in range(len(infoNames))])
        data += "\nStar (*) means first serve\nFormat is [home]-[away]\n\n\n" + teams.upper() + "\n" + startTime + "\n----------------------------------\n"
        d = datetime.datetime.now()
        data += d.strftime("%A %B %d, %Y %I:%M %p %Z") + "\n\n" + str(homeSets) + "-" + str(awaySets) + " "
        data += teams[teams.index("at")+3:] if homeSets > awaySets else teams[:teams.index("at")-1] if homeSets < awaySets else "Nobody"
        data += " wins\n\nStats for: "
        data += myTeam.upper() + "\n-------------------------------------------------\n"
        for set in range(1,6):
            setList = eval("set" + str(set))
            data += "SET " + str(set) + ":\n"
            data += "*" + str(setList[0][0]) + "-" + str(setList[0][1]) + " " if (set + fsHome) % 2 == 0 else str(setList[0][0]) + "-" + str(setList[0][1]) + "* "
            data += teams[teams.index("at")+3:] if setList[0][0] > setList[0][1] else teams[:teams.index("at")-1] if setList[0][0] < setList[0][1] else "Nobody"
            data += " wins\nSide out %- " + str(getScoreStats(set)[0]) + "/" + str(getScoreStats(set)[1]) + " --> "
            try:
                data += str(round(getScoreStats(set)[0]/getScoreStats(set)[1],5))
            except ZeroDivisionError:
                data += "0"
            data += "\nServe hold %- " + str(getScoreStats(set)[2]) + "/" + str(getScoreStats(set)[3]) + " --> "
            try:
                data += str(round(getScoreStats(set)[2]/getScoreStats(set)[3],5))
            except ZeroDivisionError:
                data += "0"
            data += "\n\n"
            data += tabulate(setList[1:],headers=("PLAYERS",*(item for item in statAbbreviations),*(item for item in infoAbbreviations)))
            data += "\n\n-----------------------\n"
        data += "TOTALS:\n" + str(sum(eval("set" + str(set))[0][0] for set in range(1,6))) + "-" + str(sum(eval("set" + str(set))[0][1] for set in range(1,6)))
        data += "\nSide out %- " + str(sum(getScoreStats(s)[0] for s in range(1,6))) + "/" + str(sum(getScoreStats(s)[1] for s in range(1,6))) + " --> "
        try:
            data += str(round(sum(getScoreStats(s)[0] for s in range(1,6))/sum(getScoreStats(s)[1] for s in range(1,6)),5))
        except ZeroDivisionError:
            data += "0"
        data += "\nServe hold %- " + str(sum(getScoreStats(s)[2] for s in range(1,6))) + "/" + str(sum(getScoreStats(s)[3] for s in range(1,6))) + " --> "
        try:
            data += str(round(sum(getScoreStats(s)[2] for s in range(1,6))/sum(getScoreStats(s)[3] for s in range(1,6)),5))
        except ZeroDivisionError:
            data += "0"
        data += "\n\n"
        dat = set1[1:]
        for player in range(len(dat)):
            if dat[player][1] == 'Y':
                dat[player][1] = 1
            elif dat[player][1] == 'N':
                dat[player][1] = 0
        for s in range(2,6):
            for p in range(1,len(set1)):
                for st in range(1,len(set1[1])):
                    if st == 1 and p != len(set1)-1:
                        if eval("set" + str(s))[p][st] == 'Y':
                            dat[p-1][st] += 1
                    else:
                        dat[p-1][st] += eval("set" + str(s))[p][st]
        for p in range(0,len(set1)-1):
            dat[p][18] = hittingPercentage(dat[p][2],dat[p][3],dat[p][4])
            dat[p][19] = servePercentage(dat[p][6],dat[p][8])
            temp = dat[p][11] + 2*dat[p][12] + 3*dat[p][13]
            temp2 = sum(dat[p][st] for st in (10,11,12,13))
            dat[p][20] = srAverage(temp,temp2)
        data += tabulate(dat,headers=("PLAYERS",*(item for item in statAbbreviations),*(item for item in infoAbbreviations)))
        data += "\n\n-----------------------\n"
        file.write(data)
        file.close()
        tkinter.messagebox.showinfo("Saved","Data saved successfully")
    else:
        tkinter.messagebox.showwarning("Error", "Data not saved")

#---------------------------------Now things will happen---------------------------------#

# Get starting time
d = datetime.datetime.now()
startTime = d.strftime("%A %B %d, %Y %I:%M %p %Z")

# Asks for teams and players and who has the first serve
temp = tkinter.Tk()
temp.withdraw()
homeTeam = tkinter.simpledialog.askstring("Teams","Who is the home team?")
awayTeam = tkinter.simpledialog.askstring("Teams","Who is the away team?")
homeOrAway = tkinter.messagebox.askyesno("Location","Are you the home team?")
if homeOrAway:
    myTeam = homeTeam
else:
    myTeam = awayTeam
temp.destroy()
def h():
    global fs,fsHome
    fsHome = 1
    fs.destroy()
def a():
    global fs,fsHome
    fsHome = 0
    fs.destroy()
fs = tkinter.Tk()
fs.geometry("250x100+" + str(int(width/2-125)) + "+" + str(int(height/2-50)))
for rows in range(100):
    fs.rowconfigure(rows,weight=1)
    fs.columnconfigure(rows,weight=1)
fs.title("First Serve")
title = tkinter.Label(fs,text="Which team has the first serve?")
title.grid(row=25,column=50)
home = tkinter.Button(fs,text=homeTeam,command=h)
home.grid(row=50,column=50)
away = tkinter.Button(fs,text=awayTeam,command=a)
away.grid(row=75,column=50)
fs.mainloop()
try:
    teams = awayTeam + " at " + homeTeam
except TypeError:
    sys.exit()
players = getPlayers()
if bad or players == []:
    sys.exit()

# Declares lists for saving data
set1 = [[0,0],*([players[p],"N",*(0 for t in range(20))] for p in range(len(players))),["TEAM",*(0 for v in range(21))]]
set2 = set1.copy()
set3 = set1.copy()
set4 = set1.copy()
set5 = set1.copy()
set1serves = [homeTeam if fsHome else awayTeam]
set2serves = [homeTeam if not fsHome else awayTeam]
set3serves = set1serves.copy()
set4serves = set2serves.copy()
set5serves = set1serves.copy()

# Creates stat entering window
stats = tkinter.Tk()
stats.title("Volleyball Statistics")

# Creates averages, totals, and percentages window
info = tkinter.Tk()
info.title("Useful Information")

# Sets window geometries
geoHeight = (30*len(players))+245
shared = (str(geoHeight) + "+" + str(int(width/2-750)) + "+",int(height/2-(geoHeight/2)))
geo = "1500x" + shared[0] + str(shared[1])
stats.geometry(geo)
geo = "400x" + shared[0] + str(shared[1]-40)
info.geometry(geo)

# Sets rows and columns in windows to 100x100
for conf in range(100):
    stats.rowconfigure(conf,weight=1)
    stats.columnconfigure(conf,weight=1)
    info.rowconfigure(conf,weight=1)
    info.columnconfigure(conf,weight=1)

# Creates edit mode to delete wrong stats
edit = False
def editSwitch(button):
    global edit
    if edit:
        edit = False
        button["text"] = "Edit off"
        button["relief"] = "sunken"
    else:
        edit = True
        button["text"] = "Edit on"
        button["relief"] = "raised"
editStatus = tkinter.Button(stats,relief="sunken",text="Edit off")
editStatus.grid(row=5,column=15)
editBut = tkinter.Button(stats,text="Edit",command=lambda:editSwitch(editStatus))
editBut.grid(row=5,column=5)

# Creates set number buttons and functionality
prevSet = tkinter.Button(stats,text="Previous set",command=lambda:setChange("prev"))
prevSet.grid(row=5,column=25)
currSet = tkinter.Button(stats,relief="sunken",text="1")
currSet.grid(row=5,column=30)
setLabel = tkinter.Label(stats,text="Set")
setLabel.grid(row=7,column=30)
nextSet = tkinter.Button(stats,text="Next set",command=lambda:setChange("next"))
nextSet.grid(row=5,column=35)

# Shows who has the first serve in each set
fsLabel = tkinter.Label(stats,text="First serve:")
fsLabel.grid(row=4,column=20)
fsLabel2 = tkinter.Label(stats,text=homeTeam if (int(currSet["text"]) + fsHome) % 2 == 0 else awayTeam)
fsLabel2.grid(row=5,column=20)

# Self plug
me1 = tkinter.Label(stats,text="Made by:")
me1.grid(row=4,column=45)
me2 = tkinter.Label(stats,text="Pierson Polcaro")
me2.grid(row=5,column=45)

# Makes buttons that tell which teams are playing
teamsBut = tkinter.Button(stats,relief="sunken",text=teams)
teamsBut.grid(row=5,column=55)
teamsBut2 = tkinter.Button(info,relief="sunken",text=teams)
teamsBut2.grid(row=5,column=40)

# Creates side out and serve holding percentage labels- need to save data so it can be replaced
sideout = 0
serveHold = 0
sideoutNum = tkinter.Label(stats,text=sideout)
sideoutNum.grid(row=5,column=65)
sideoutLabel = tkinter.Label(stats,text="Sideout")
sideoutLabel.grid(row=7,column=65)
serveHoldNum = tkinter.Label(stats,text=serveHold)
serveHoldNum.grid(row=5,column=70)
serveHoldLabel = tkinter.Label(stats,text="Srv hold")
serveHoldLabel.grid(row=7,column=70)

# Creates score and save buttons
scoreLabel = tkinter.Label(stats,text="Score:")
scoreLabel.grid(row=5,column=80)
homeScore = tkinter.Button(stats,text=0,command=lambda:pointScore(homeScore))
homeScore.grid(row=5,column=85)
awayScore = tkinter.Button(stats,text=0,command=lambda:pointScore(awayScore))
awayScore.grid(row=5,column=90)
homeLabel = tkinter.Label(stats,text="Home")
homeLabel.grid(row=7,column=85)
awayLabel = tkinter.Label(stats,text="Away")
awayLabel.grid(row=7,column=90)
saveButton = tkinter.Button(stats,text="Save",command=save)
saveButton.grid(row=5,column=95)

# Loads statistic and info categories
statItems = ["Played","Attempts","Kills","Errors","Assists","Service attempts","Service aces",
             "Service errors","Digs","Serve receive error","1 pass","2 pass","3 pass",
             "Blocking error","Solo block","Blocking assist","Ball handling error"]
infoItems = ["Hitting %","Serving %","Serve receive","Total errors"]
statNames = ("Played","Attempts","Kills","Errors","Assists","Service attempts","Service aces",
             "Service errors","Digs","Serve receive error","1 pass","2 pass","3 pass",
             "Blocking error","Solo block","Blocking assist","Ball handling error")
infoNames = ("Hitting %","Serving %","Serve receive","Total errors")
statAbbreviations = ("SP","TA","K","E","A","ATT","SA","SE","DIG","SRE","SR1","SR2","SR3","BE","BS","BA","BHE")
infoAbbreviations = ("HIT %","SRV %","SR","TE")
for num in range(len(statItems)):
    statItems[num] = tkinter.Button(stats,relief="sunken",text=statItems[num])
    statItems[num].grid(row=15,column=15+(5*num))
for num in range(len(infoItems)):
    infoItems[num] = tkinter.Button(info,relief="sunken",text=infoItems[num])
    infoItems[num].grid(row=15,column=20+(20*num))

# Makes player buttons with names supplied by user (1 is stat entering, 2 is info)
inc = int(round(80/len(players),0))
playerButtons1 = []
playerButtons2 = []
for i in range(len(players)):
    playerButtons1.append(players[i])
    playerButtons2.append(players[i])
playerButtons1.append("TEAM")
playerButtons2.append("TEAM")
for num in range(len(playerButtons1)):
    playerButtons1[num] = tkinter.Button(stats,relief="sunken",text=playerButtons1[num])
    playerButtons1[num].grid(row=20+(inc*num),column=5)
for num in range(len(playerButtons2)):
    playerButtons2[num] = tkinter.Button(info,relief="sunken",text=playerButtons2[num])
    playerButtons2[num].grid(row=20+(inc*num),column=2)

# Creates all buttons for stats
code = ""
for p in range(len(players)+1):
    for i in range(len(statItems)):
        if p == len(players):
            code = code + "t_" + str(i) + " = tkinter.Label(stats,text=0)\n"
        elif i == 0:
            code = code + "s" + str(p+1) + "_" + str(i) + " = tkinter.Button(stats,text='N',command=lambda:play((s" + str(p+1) + "_" + str(i) + ",'s" + str(p+1) + "_" + str(i) + "')))\n"
        elif i == 2 or i == 3: #attack attempt
            code = code + "s" + str(p+1) + "_" + str(i) + " = tkinter.Button(stats,text=0,command=lambda:add((s" + str(p+1) + "_" + str(i) + ",'s" + str(p+1) + "_" + str(i) + "'),True,1))\n"
        elif i == 6 or i == 7: #serve attempt
            code = code + "s" + str(p+1) + "_" + str(i) + " = tkinter.Button(stats,text=0,command=lambda:add((s" + str(p+1) + "_" + str(i) + ",'s" + str(p+1) + "_" + str(i) + "'),True,2))\n"
        else:
            code = code + "s" + str(p+1) + "_" + str(i) + " = tkinter.Button(stats,text=0,command=lambda:add((s" + str(p+1) + "_" + str(i) + ",'s" + str(p+1) + "_" + str(i) + "'),False,0))\n"
        if p != len(players):
            code = code + "s" + str(p+1) + "_" + str(i) + ".grid(row=" + str(20+(inc*p)) + ",column=" + str(15+(5*i)) + ")\n"
        else:
            code = code + "t_" + str(i) + ".grid(row=" + str(20+(inc*p)) + ",column=" + str(15+(5*i)) + ")\n"
exec(code)

# Creates all 'buttons' for info
code = ""
for p in range(len(players)+1):
    for i in range(len(infoItems)):
        if p == len(players):
            code = code + "te_" + str(i) + " = tkinter.Label(info,text=0)\n"
        elif i == 0:
            code = code + "i" + str(p+1) + "_" + str(i) + " = tkinter.Button(info,relief='sunken',text=0)\n"
        else:
            code = code + "i" + str(p+1) + "_" + str(i) + " = tkinter.Button(info,relief='sunken',text=0)\n"
        if p != len(players):
            code = code + "i" + str(p+1) + "_" + str(i) + ".grid(row=" + str(20+(inc*p)) + ",column=" + str(20+(20*i)) + ")\n"
        else:
            code = code + "te_" + str(i) + ".grid(row=" + str(20+(inc*p)) + ",column=" + str(20+(20*i)) + ")\n"
exec(code)

stats.mainloop()
