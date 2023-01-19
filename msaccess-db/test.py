import pyodbc

conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:/Users/redpe/dev/school-projects/msaccess-db/N11info.accdb;")
cursor = conn.cursor()
print(cursor.execute("SELECT * FROM Devs WHERE Users='gingerwitch64';"))