import sqlite3

con = sqlite3.connect('database.sqlite')

cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS Adresse(
    AdressID INTEGER NOT NULL PRIMARY KEY, 
    Straße TEXT, 
    Hausnummer INT, 
    Ort TEXT, 
    Postleitzahl TEXT
    )
''')


cur.execute('''
    CREATE TABLE IF NOT EXISTS User(
    UserID INTEGER NOT NULL PRIMARY KEY,
    Benutzername TEXT, 
    Vorname TEXT, 
    Nachname TEXT, 
    Email TEXT, 
    Passwort TEXT, 
    Guthaben INT, 
    Adresse INT,
    FOREIGN KEY(Adresse) REFERENCES Adresse(AdressID)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Autos(
    AutoID INT INTEGER NOT NULL PRIMARY KEY, 
    Hersteller TEXT, 
    Modell TEXT, 
    Fahrzeugtyp TEXT,
    PreisProTag INT,
    Startdatum DATE,
    Enddatum DATE
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Mietauftrag(
    Mieter INT,
    Vermieter INT,
    Auto INT,
    Gesamtpreis INT,
    Startdatum DATE,
    Enddatum DATE,
    Ueberweisungsdatum DATE,
    FOREIGN KEY(Mieter) REFERENCES User(UserID),
    FOREIGN KEY(Vermieter) REFERENCES User(UserID),
    FOREIGN KEY(Auto) REFERENCES Autos(AutoID)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Autobesitzer(
    User INT,
    Auto INT,
    FOREIGN KEY(User) REFERENCES User(UserID),
    FOREIGN KEY(Auto) REFERENCES Autos(AutoID)
    )
''')

cur.execute('''
    INSERT INTO Adresse VALUES(123, "Testweg", 456, "Testort", 789)
''')

cur.execute('''
    INSERT INTO Autos VALUES(123, "Mercedes", "EQS", "Kombi", 50, "2022-04-24", "2022-04-27")
''')

cur.execute('''
    SELECT * FROM Adresse
''')

print(cur.fetchall())

cur.execute('''
    SELECT * FROM Autos
''')

print(cur.fetchall())

cur.close()