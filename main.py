import tkinter as tk, os, json, threading, time
from functools import partial
from PIL import Image, ImageTk
import tkinter.font as font
import random
import math
from hashlib import sha256


def load(username, passwd):
    """
    A function to load the data of a user, sets the global variables "sectors" and "money".
    
    """
    global errorLabel, sectors, money, reputation, lastOnline
    if not "{0}.json".format(username) in os.listdir("Saves"):
        errorLabel.config(text="No save with that username!")
        return
    else:
        with open("Saves\{0}.json".format(username), "r") as f:
            loaded = json.load(f)
            if passwd != loaded["passwd"]:
                errorLabel.config(text="Password is incorrect!")
            else:
                #TODO set game data here from var "loaded"
                #! Globalize variables you are trying to load
                sectors = loaded["sectors"]
                money = loaded["money"]
                reputation = loaded["reputation"]
                lastOnline = loaded["lastOnline"]


def login():
    """
    Function that checks various login parameters and calls "load()" if everything is okay.
    """
    global username, passwd, inputWin, errorLabel, loggedIn
    username = usernameEntry.get()
    passwd = passwdEntry.get()
    if username == "" or passwd == "":
        errorLabel.config(text="Enter a username and a password\nto log in!")
        return
    try:
        if json.load(open("Saves/{0}.json".format(username)))["passwd"] != passwd:
            errorLabel.config(text="Password is incorrect.")
            return
        else:
            load(username, passwd)
            loggedIn = True
            inputWin.destroy()
    except:
        errorLabel.config(text="No save with that username.")
        return


def save():
    """
    Function to save the current user's data to the "Saves" directory as a .json file.
    """
    global username, passwd, sectors, money, reputation
    with open("Saves\{0}.json".format(username), "r") as f:
        #TODO save data as dict here
        loaded = {"username": username, "passwd": sha256(passwd.encode()).hexdigest(), "money": money, "reputation": reputation, "lastOnline": time.time(),
            "sectors": sectors
        }
        with open("Saves\{0}.json".format(username), "w") as g:
            toWrite = json.dumps(loaded)
            g.write(toWrite)


def register():
    """
    Function to register a new account with the data stored in "usernameEntry" and "passwordEntry".
    """
    global username, passwd
    username = usernameEntry.get()
    passwd = passwdEntry.get()
    if not "{0}.json".format(username) in os.listdir("Saves"):
        with open("Saves\{0}.json".format(username), "x"):
            pass
        with open("Saves\{0}.json".format(username), "a") as f:
            f.write('{}')
        save()


username = str()
passwd = str()

currentSector = int()
money = int()
# Defines the reputation of the leader with the villagers, the higher the better, and the more willing they are to work and pay taxes.
reputation = int()
# Represents the seconds since 1970 at which the logged in user has last logged in, used for calculating offline rewards.
lastOnline = int()
# Maximum amount of reputation which can be earned by being offline.
MAX_REPUTATION_OFFLINE = 100

sectors = list()
for i in range(9):
    sectors.append([])
    for x in range(25):
        sectors[i].append({})
sectorButtons = list()

loggedIn = False
# Variable that sets to True after the root was destroyed, used to end threads.
exitGame = False

inputWin = tk.Tk()
inputWin.title("Login")
inputWin.iconbitmap("Images/scroll.ico")
inputWin.geometry(("200x180"))

errorLabel = tk.Label(master=inputWin, text="", fg="red")
errorLabel.place(x=10, y=130)

usernameEntry = tk.Entry(master=inputWin); usernameEntry.place(x=10, y=10)
passwdEntry = tk.Entry(master=inputWin); passwdEntry.place(x=10, y=60)
getButton = tk.Button(master=inputWin, text="Login", command=login); getButton.place(x=10, y=100)
registerButton = tk.Button(master=inputWin, text="Register", command=register); registerButton.place(x=100, y=100)

inputWin.mainloop()



def mainMenu():
    mainMenuWindow = tk.Toplevel(master=mainWindow)
    mainMenuWindow.iconbitmap("Images/house.ico")
    tk.Button(text="Save", command=save, master=mainMenuWindow).place(x=10, y=10)
    tk.Button(text="Load", command=partial(load, username, passwd), master=mainMenuWindow).place(x=10, y=40)


def loadSector(index):
    global sectorButtons, sectors, currentSector
    selectedSector = sectors[index]
    currentSector = index
    for i in range(25):
        try:
            sectorButtons[i]["button"].config(text=selectedSector[i]["text"], command=partial(buildingMenu, i))
            sectorButtons[i]["values"] = selectedSector[i]["values"]
        except:
            sectorButtons[i]["button"].config(text="", command=partial(buildMenu, i))
            sectorButtons[i]["values"] = {}


def build(index, buildingDict, buildWin, errLabel):
    global currentSector, sectors, money
    if money >= buildingDict["cost"] and sectors[currentSector][index] == {}:
        sectors[currentSector][index] = buildingDict
        money -= buildingDict["cost"]
        buildWin.destroy()
        loadSector(currentSector)
    else:
        errLabel.config(text="You can't afford that.")


def buildingMenu(index):
    global buildingWin
    try:
        buildingWin.destroy()
    except:
        pass
    buildingDict = sectors[currentSector][index]
    buildingWin = tk.Toplevel(master=mainWindow)
    buildingWin.iconbitmap("Images/gear.ico")
    buildingWin.title("{0} - Building Menu".format(buildingDict["text"]))
    buildingWin.geometry("1600x300+-10+600")

    

    buildingWin.mainloop()


def buildMenu(index):
    buildWin = tk.Tk()
    buildWin.iconbitmap("Images/tools.ico")
    buildWin.title("Buildings")
    buildWin.attributes("-fullscreen", True)

    tk.Button(master=buildWin, text="Back", bg="red", command=buildWin.destroy).place(x=1400, y=10, height=50, width=75)
    errLabel = tk.Label(master=buildWin, text="", fg="red", font=font.Font(size=20)); errLabel.place(x=10, y=10)

    buttonWidth, buttonHeight = 100, 100
    line, y = 1, 1
    for info in json.load(open("builds.json")):
        if line == 10:
            y += 1
            line = 1
        tk.Button(master=buildWin, text="{0}\nCost: {1}".format(info["text"], info["cost"]), command=partial(build, index, info, buildWin, errLabel)).place(x=line * (buttonWidth + 10), y=y*(buttonHeight+10), width=buttonWidth, height=buttonHeight)
        line += 1
    buildWin.mainloop()


def saveAndExit():
    global mainWindow
    save()
    time.sleep(0.1)
    mainWindow.destroy()


def collectTax():
    """
    Function to collect a given amount of taxes "tax" from the villagers, decreasing your reputation.
    """
    global money, reputation, sectors
    totalTax = int()
    for sector in sectors:
        for building in sector:
            try:
                totalTax += building["values"]["taxes"]
            except:
                pass
    money += totalTax
    reputation -= random.randint(10, 50)



if loggedIn:

    diffTime = int(math.floor(time.time() - lastOnline))
    if (reputationReward := diffTime / 900) > MAX_REPUTATION_OFFLINE:
        reputationReward = MAX_REPUTATION_OFFLINE
    reputation += reputationReward

    mainWindow = tk.Tk()
    mainWindow.attributes("-fullscreen", True)
    mainWindow.iconbitmap("Images/crown.ico")
    mainWindow.title("Town King")

    coinSym = tk.Label(master=mainWindow, image=ImageTk.PhotoImage(Image.open("Images/coin.ico")))
    coinSym.place(x=1200, y=10)

    mainMenuButton = tk.Button(master=mainWindow, text="Main Menu", command=mainMenu)
    mainMenuButton.place(x=10, y=10)

    sectorOneButton = tk.Button(master=mainWindow, bg="green", command=partial(loadSector, 0), text="1"); sectorOneButton.place(x=100, y=10, width=30, height=30)
    sectorTwoButton = tk.Button(master=mainWindow, bg="blue", command=partial(loadSector, 1), text="2"); sectorTwoButton.place(x=130, y=10, width=30, height=30)
    sectorThreeButton = tk.Button(master=mainWindow, bg="red", command=partial(loadSector, 2), text="3"); sectorThreeButton.place(x=160, y=10, width=30, height=30)
    sectorFourButton = tk.Button(master=mainWindow, bg="lime", command=partial(loadSector, 3), text="4"); sectorFourButton.place(x=100, y=40, width=30, height=30)
    sectorFiveButton = tk.Button(master=mainWindow, bg="light blue", command=partial(loadSector, 4), text="5"); sectorFiveButton.place(x=130, y=40, width=30, height=30)
    sectorSixButton = tk.Button(master=mainWindow, bg="orange", command=partial(loadSector, 5), text="6"); sectorSixButton.place(x=160, y=40, width=30, height=30)
    sectorSevenButton = tk.Button(master=mainWindow, bg="magenta", command=partial(loadSector, 6), text="7"); sectorSevenButton.place(x=100, y=70, width=30, height=30)
    sectorEightButton = tk.Button(master=mainWindow, bg="gray", command=partial(loadSector, 7), text="8"); sectorEightButton.place(x=130, y=70, width=30, height=30)
    sectorNineButton = tk.Button(master=mainWindow, bg="yellow", command=partial(loadSector, 8), text="9"); sectorNineButton.place(x=160, y=70, width=30, height=30)

    tk.Button(master=mainWindow, command=saveAndExit, text="Save & exit", bg="red").place(x=1400, y=10, height=50, width=75)
    taxButton = tk.Button(text="Collect taxes", command=collectTax, master=mainWindow); taxButton.place(x=10, y=300)

    coinLabel = tk.Label(master=mainWindow, text="Coins: {0}".format(money)); coinLabel.place(x=1300, y=10)
    def updateCoinLabel():
        global coinLabel, money
        while True:
            time.sleep(0.1)
            coinLabel.config(text="Coins: {0}".format(money))
            if exitGame:
                return
    
    def regenerateReputation():
        global reputation
        while True:
            time.sleep(5)
            reputation += random.randint(1, 3)
            if exitGame:
                return
    
    threading.Thread(target=updateCoinLabel).start()
    threading.Thread(target=regenerateReputation).start()

    line = 1
    y = 1
    sectorButtons = list()
    buttonHeight, buttonWidth = 100, 100
    for n in range(25):
        if line == 6:
            y += 1
            line = 1
        sectorButtons.append({"button": tk.Button(master=mainWindow), "values": {}})
        sectorButtons[n]["button"].place(x=line*(buttonWidth + 10) + 300, y=y*(buttonHeight + 10) - 80, height=buttonHeight, width=buttonWidth)
        line += 1
    loadSector(currentSector)

    mainWindow.mainloop()
