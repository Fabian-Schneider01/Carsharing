import sqlite3

def createTabels():
    
    con = sqlite3.connect('database.sqlite')

    cur = con.cursor()

    cur.execute('''DROP TABLE Verfuegbar''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Adresse(
        AdressID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        Straße TEXT, 
        Hausnummer INT, 
        Ort TEXT, 
        Postleitzahl TEXT
        )
    ''')


    cur.execute('''
        CREATE TABLE IF NOT EXISTS User(
        UserID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
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
        AutoID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        Hersteller TEXT, 
        Modell TEXT, 
        Fahrzeugtyp TEXT,
        PreisProTag INT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Mietauftrag(
        Mieter INT,
        Auto INT,
        Gesamtpreis INT,
        Startdatum DATE,
        Enddatum DATE,
        FOREIGN KEY(Mieter) REFERENCES User(UserID),
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
        CREATE TABLE IF NOT EXISTS Verfuegbar(
        Auto INT,
        Datum DATE,
        FOREIGN KEY(Auto) REFERENCES Autos(AutoID)
        )
    ''')

    con.commit()
    cur.close()
