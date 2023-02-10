import csv, os.path
from time import sleep
from guizero import App, Window, TextBox, PushButton, ListBox

devlist = []
with open("devs.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        devlist.append(row[0] + ": " + row[1])

def fetchdevinfo():
    if listbox.value == None:
        pass
    selval = int(listbox.value.split(": ")[0])
    with open("devs.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if int(row[0]) == selval:
                devapp = Window(app,title=f"Developer information: {row[1]}")
                #devapp.show(wait=True)
                devtext = TextBox(devapp,text=f"Username: {row[1]}\nName: {row[2]}\nDescription: {row[3]}",width="fill",height="fill",multiline=True,enabled=False)

def fetchrepos():
    if listbox.value == None:
        pass

    selval = int(listbox.value.split(": ")[0])
    devname = listbox.value.split(": ")[1]
    finalstr = f"{devname} has contributed to the following N11 Repositories:\n"
    
    with open("repos.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if int(row[0]) == selval:
                with open("repodesc.csv", "r") as file2:
                    iterrepos = csv.reader(file2)
                    for descrow in iterrepos:
                        if int(descrow[0]) == int(row[1]):
                            finalstr = finalstr + f"{descrow[1]}: {descrow[2]}\n"
    conapp = Window(app,title=f"{devname}'s Contributed Repositories")
    context = TextBox(conapp,text=finalstr,width="fill",height="fill",multiline=True,enabled=False)




app = App(title="N11 Devs (relationaldbs)",layout="grid",width=375,height=230)
listbox = ListBox(app,items=devlist,align="left",grid=[0,0])
text = TextBox(app,text="Select any developer's profile, then click one of the two buttons to get information on them or projects they've contributed to.",align="left",multiline=True,enabled=False,grid=[1,0],width="31",height="10")
devinfo = PushButton(app,text="Developer Info",align="bottom",grid=[0,1],command=fetchdevinfo)
contributions = PushButton(app,text="Contributions",align="bottom",grid=[1,1],command=fetchrepos)

app.display()
