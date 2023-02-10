import pyodbc
from guizero import App, Window, TextBox, PushButton, ListBox, Combo

conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/Users/redpe/dev/school-projects/msaccess-db/N11info-test.accdb;")
cursor = conn.cursor()
#cursor.execute("SELECT * FROM Repos FROM ;")

#for row in cursor.fetchall():
#    print(row)
def fetchdevusers():
    holding = [""]
    users = cursor.execute("SELECT Users FROM Devs;").fetchall()
    for username in users:
        holding.append(f"WHERE Users='{username[0]}'")
    return holding

def fetchdevinfo():
    result = cursor.execute(f"SELECT {field.value} FROM Devs {filter.value};").fetchall()
    finalbox.value = result

def executesql():
    match operation.value:
        case "Fetch":
            result = cursor.execute(f"SELECT {field.value} FROM Devs {filter.value};").fetchall()
            finalbox.value = result
        case "Insert":
            print("Placeholder Text")
        case "Update":
            print("Placeholder Text")
        case "Delete":
            print("Placeholder Text")

app = App(title="N11 MSDB",layout="grid",width=500,height=150)
operation = Combo(app,options=["Fetch", "Insert", "Update", "Delete"],width=11,height=1,grid=[0,0])
field = Combo(app,options=["*","ID","RealName","Description"],width=11,height=1,grid=[1,0])
filter = Combo(app,options=fetchdevusers(),width=27,height=1,grid=[2,0])
label = TextBox(app,text="from Devs",multiline=True,enabled=False,width=9,height=1,grid=[3,0])
devinfo = PushButton(app,text="Fetch",align="bottom",grid=[1,1],command=fetchdevinfo)
finalbox = TextBox(app,text="Output will show up here.",multiline=True,enabled=False,scrollbar=True,width=22,height=7,grid=[2,1])


app.display()
