import pyodbc
from guizero import App, Window, TextBox, Text, PushButton, Combo

conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/Users/redpe/dev/school-projects/msaccess-db/N11info-test.accdb;")
cursor = conn.cursor()

def selectquery(column,condition):
    output = cursor.execute(f"SELECT {column} FROM Devs {condition};").fetchall()
    outputwin = Window(app,title=f"SELECT {column} FROM Devs {condition};")
    TextBox(outputwin,text=output,multiline=True,enabled=False,width="fill",height="fill")

def insertquery(users,realname,desc):
    str = f"INSERT INTO Devs (Users,RealName,Description) VALUES ('{users}','{realname}','{desc}');"
    cursor.execute(str)
    outputwin = Window(app,title=str)
    TextBox(outputwin,text="Done",multiline=True,enabled=False,width="fill",height="fill")

def launchwindow():
    match operation.value:
        case "Select":
            selectapp = Window(app,title="Select Query Generator")
            Text(selectapp,text="Select")
            columncombo = Combo(selectapp,options=["*","ID","Users","Realname","Description"])
            Text(selectapp,text="from Devs")
            condition = TextBox(selectapp,text="",width="fill")
            PushButton(selectapp,text="Run",command=lambda:selectquery(columncombo.value,condition.value))
        case "Insert":
            insertapp = Window(app,title="Insert Query Generator")
            Text(insertapp,text="Insert into Devs")
            Text(insertapp,text="Boxes are Username, Real Name and Description respectfully.")
            users = TextBox(insertapp,text="",width="fill")
            realname = TextBox(insertapp,text="",width="fill")
            desc = TextBox(insertapp,text="",width="fill")
            PushButton(insertapp,text="Run",command=lambda:insertquery(users.value,realname.value,desc.value))
        case "Update":
            updateapp = Window(app,title="Update Query Generator")
            Text(updateapp,text="Update Devs, Set")
            columncombo = Combo(updateapp,options=["Users","Realname","Description"])
            Text(updateapp,text="from Devs")
            condition = TextBox(updateapp,text="",width="fill")
            PushButton(updateapp,text="Run",command=lambda:selectquery(columncombo.value,condition.value))
        case "Delete":
            deleteapp = Window(app,title="Delete Query Generator")

app = App(title="N11 MSDB",width=250)
operation = Combo(app,options=["Select", "Insert", "Update", "Delete"],width=20,height=2)
PushButton(app,text="Open Query Generator",command=launchwindow,width=19,height=2)
#output = TextBox(app,text="Output will appear here.",multiline=True,enabled=False,width=20,height=50)

app.display()
