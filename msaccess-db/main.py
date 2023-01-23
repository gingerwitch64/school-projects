import pyodbc
from guizero import App, Window, TextBox, Text, PushButton, Combo

conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/Users/redpe/dev/school-projects/msaccess-db/N11info-test.accdb;")
cursor = conn.cursor()

def selectquery(column,condition):
    str = f"SELECT {column} FROM Devs {condition};"
    output = cursor.execute(str).fetchall()
    outputwin = Window(app,title=str)
    TextBox(outputwin,text=output,multiline=True,enabled=False,width="fill",height="fill")

def insertquery(users,realname,desc):
    str = f"INSERT INTO Devs (Users,RealName,Description) VALUES ('{users}','{realname}','{desc}');"
    cursor.execute(str)
    cursor.commit()

    outputwin = Window(app,title=str)
    TextBox(outputwin,text="Done",multiline=True,enabled=False,width="fill",height="fill")

def updatequery(column,text,condition):
    str = f"UPDATE Devs SET {column} = '{text}' {condition};"
    print(str)
    cursor.execute(str)
    cursor.commit()

    outputwin = Window(app,title=str)
    TextBox(outputwin,text="Done",multiline=True,enabled=False,width="fill",height="fill")

def deletequery(column,text):
    str = f""
    match column:
        case "ID":
            str = f"DELETE FROM Devs WHERE {column} = {text};"
        case _:
            str = f"DELETE FROM Devs WHERE {column} = '{text}';"
    cursor.execute(str)
    cursor.commit()

    outputwin = Window(app,title=str)
    TextBox(outputwin,text="Done",multiline=True,enabled=False,width="fill",height="fill")

def launchwindow():
    match operation.value:
        case "Select":
            selectapp = Window(app,title="Select Query Generator")
            Text(selectapp,text="Select")
            columncombo = Combo(selectapp,options=["*","ID","Users","RealName","Description"])
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
            columncombo = Combo(updateapp,options=["Users","RealName","Description"])
            Text(updateapp,text="=")
            text = TextBox(updateapp,text="",width="fill")
            Text(updateapp,text="Format: WHERE ColumnName = \"text\"")
            condition = TextBox(updateapp,text="WHERE",width="fill")
            PushButton(updateapp,text="Run",command=lambda:updatequery(columncombo.value,text.value,condition.value))
        case "Delete":
            deleteapp = Window(app,title="Delete Query Generator")
            Text(deleteapp,text="Delete from Devs where:")
            columncombo = Combo(deleteapp,options=["ID","Users","RealName","Description"])
            Text(deleteapp,text="=")
            text = TextBox(deleteapp,text="",width="fill")
            PushButton(deleteapp,text="Run",command=lambda:deletequery(columncombo.value,text.value))

app = App(title="N11 MSDB",width=250)
operation = Combo(app,options=["Select", "Insert", "Update", "Delete"],width=20,height=2)
PushButton(app,text="Open Query Generator",command=launchwindow,width=19,height=2)
#output = TextBox(app,text="Output will appear here.",multiline=True,enabled=False,width=20,height=50)

app.display()
