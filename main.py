import tkinter as tk, json, os
from functools import partial

loginWin = tk.Tk()
username = ""
passwd = ""
loggedIn = False


def openSector(index):
    username, passwd = getCredentials()
    sectors = open("C:/Users/Elin/Desktop/Programmieren/TownKing/Saves/{0}.json".format(username))
    unlockedSectors = open("C:/Users/Elin/Desktop/Programmieren/TownKing/Saves/{0}.json".format(username))


def load(username, passwd):
    try:
        with open("C:/Users/Elin/Desktop/Programmieren/TownKing/Saves/{0}.json".format(username), "r") as f:
            loaded = json.loads(f.read())
            print(loaded)
    except Exception as e:
        return e


def getCredentials():
    global usernameEntry, passwdEntry
    username = usernameEntry.get()
    passwd = passwdEntry.get()
    print(username, "\n", passwd)
    return (username, passwd)


def login():
    global loggedIn
    username, passwd = getCredentials()
    if not "{0}.json".format(username) in os.listdir("C:/Users/Elin/Desktop/Programmieren/TownKing/Saves"):
        print("What you trying")
        return
    elif passwd != json.load(open("C:/Users/Elin/Desktop/Programmieren/TownKing/Saves/{0}.json".format(username)))["password"]:
        print("Your computer has virus")
        return
    else:
        load(username, passwd)
        print("very good")
        loginWin.destroy()
        loggedIn = True
        return


def register():
    username, passwd= getCredentials()
    if username == "" or passwd == "":
        return
    with open("C:/Users/Elin/Desktop/Programmieren/TownKing/Saves/{0}.json".format(username), "x"):
        pass
    with open("C:/Users/Elin/Desktop/Programmieren/TownKing/Saves/{0}.json".format(username), "a") as f:
        toWrite = {
            "username": username,
            "password": passwd,
            "unlockedSectors": [0] #fortfahren
        }

        

loginWin.attributes("-fullscreen", True)
usernameEntry = tk.Entry(loginWin)
usernameEntry.place(x=600, y=390, height=30, width=300)
passwdEntry = tk.Entry(loginWin)
passwdEntry.place(x=600, y=450, height=30, width=300)
loginButton = tk.Button(loginWin, command=login, text="Login", bg="green")
loginButton.place(x=600, y=500)
registerButton = tk.Button(loginWin, command=register, text="Dein leben ist jetzt zu ende")
registerButton.place(x=650, y=500)

loginWin.mainloop()

if loggedIn:
    mainWin = tk.Tk()
    mainWin.attributes("-fullscreen", True)
    sectorOneButton = tk.Button(mainWin, command=partial(openSector, 0))
    sectorTwoButton = tk.Button(mainWin, command=partial(openSector, 1))
    sectorThreeButton = tk.Button(mainWin, command=partial(openSector, 2))
    sectorFourButton = tk.Button(mainWin, command=partial(openSector, 3))
    sectorFiveButton = tk.Button(mainWin, command=partial(openSector, 4))
    sectorSixButton = tk.Button(mainWin, command=partial(openSector, 5))
    sectorSevenButton = tk.Button(mainWin, command=partial(openSector, 6))
    sectorEightButton = tk.Button(mainWin, command=partial(openSector, 7))
    sectorNineButton = tk.Button(mainWin, command=partial(openSector, 8))
    mainWin.mainloop()

