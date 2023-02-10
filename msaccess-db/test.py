import pyodbc

conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/Users/redpe/dev/school-projects/msaccess-db/N11info-test.accdb;")
cursor = conn.cursor()
cursor.execute("INSERT INTO Devs (ID,Users,RealName,Description) VALUES (5,'users','realname','desc');")