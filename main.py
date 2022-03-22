import tkinter as tk, os, json, threading, time
from functools import partial
from PIL import Image, ImageTk
import tkinter.font as font
import random
import math
from hashlib import sha512


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
        if json.load(open("Saves/{0}.json".format(username)))["passwd"] != sha512(passwd.encode()).hexdigest():
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
    with open("Saves\{0}.json".format(username), "r"):
        #TODO save data as dict here
        loaded = {"username": username, "passwd": sha512(passwd.encode()).hexdigest(), "money": money, "reputation": reputation, "lastOnline": time.time(),
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
    else:
        errorLabel.config(text="There is already another save with that username.")


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
# Defines the function which is used to calculate the reputation which is subtracted in the "collectTax" function.
"""
    The higher the number submitted to this function as x, the lower the number returned, representing a probability between 0 and 100, will be and vice versa.
    If the number entered as x is squared greater than y*10, the function returns 0.0. (e.g. RETURN_PROB(15, 20) will return 0.0
    because 15**2=225 is greater than 20*10=200, so y*10-x**2=200-225=-25, which the max function sets to 0. And 0/a always equals 0)
    The last variable is used to make the calculation relative meaning its more likely to be inside a certain frame because the higher the result in the dividend,
    the higher the difference will be to the actually returned number. (e.g. 100/10=10, the difference being 90, though 1000/10=100, the difference being 900)
    If you imagine the function as a graph, the variable a edits the curve., though not the min value to return 0.0.
"""
RETURN_PROB = lambda x, y, a: max(0, y*10-x**2)/a

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
    buildingWin.geometry("1600x300")

    

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
    global mainWindow, exitGame
    save()
    time.sleep(0.1)
    exitGame = True
    mainWindow.destroy()


def collectTax():
    """
    Function to collect a given amount of taxes "tax" from the villagers, decreasing your reputation.
    Decreasing the reputation will prevent the user from collecting too much tax.
    """
    global money, reputation, sectors

    if reputation <= 50:
        pass

    while True:
        if reputationSubtract := random.randint(0, 100) < RETURN_PROB(random.randint(10, 50), 2750, 27.49):
            break
    
    reputation -= reputationSubtract

    if reputation < 0:
        reputation = 0

    totalTax = int()
    for sector in sectors:
        for building in sector:
            try:
                totalTax += building["values"]["taxes"]
            except:
                # if the building currently iterating through has no "taxes" value, then skip it (e.g. an empty building space)
                pass
    money += totalTax



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


    y = 1
    x = 1

    sectorButtons = list()
    buttonsize = 30
    colorsList = ["#ff0000", "#ff6464", "#ff9696","#00ff00", "#64ff64", "#96ff96", "#0000ff", "#6464ff", "#9696ff"]

    for i in range(9):
            if x == 4:
                x = 1
                y += 1
            sectorButtons.append(tk.Button(master=mainWindow, bg=colorsList[i], command=partial(loadSector, i), text=str(i)))
            sectorButtons[i].place(x=x*buttonsize+200, y=y*buttonsize+40, height=buttonsize, width=buttonsize)
            x += 1


    tk.Button(master=mainWindow, command=saveAndExit, text="Save & exit", bg="red").place(x=1400, y=10, height=50, width=75)
    taxButton = tk.Button(text="Collect taxes", command=collectTax, master=mainWindow); taxButton.place(x=10, y=300)
    taxNotifications = tk.Label(master=mainWindow, text="", fg="red")

    coinLabel = tk.Label(master=mainWindow, text="Coins: {0}".format(money)); coinLabel.place(x=1300, y=10)


    def updateCoinLabel():
        global coinLabel, money, exitGame
        while not exitGame:
            time.sleep(0.1)
            coinLabel.config(text="Coins: {0}".format(money))
    
    def regenerateReputation():
        global reputation, exitGame
        while True:
            time.sleep(5)
            reputation += random.randint(1, 3)
            if exitGame:
                return
    
    def returnRunningThreads():
        while True:
            print(threading.enumerate())
            time.sleep(5)

    threads = [threading.Thread(target=returnRunningThreads), threading.Thread(target=updateCoinLabel), threading.Thread(target=regenerateReputation)]

    for i in range(len(threads)):
        threads[i].setDaemon(True)
        threads[i].start()

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
