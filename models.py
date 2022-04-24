import sqlite3

con = sqlite3.connect('database.sqlite')

cur = con.cursor()

cur.execute('''
    CREATE TABLE User(
    UserID INTEGER NOT NULL PRIMARY KEY,
    Benutzername TEXT, 
    Vorname TEXT, 
    Nachname TEXT, 
    Email TEXT, 
    Passwort TEXT, 
    Guthaben INT, 
    FOREIGN KEY(Adresse) REFERENCES Adresse(AdressID)
    )
''')

cur.execute('''
    CREATE TABLE Adresse(
    AdressID INTEGER NOT NULL PRIMARY KEY, 
    Straße TEXT, 
    Hausnummer INT, 
    Ort TEXT, 
    Postleitzahl TEXT
    )
''')

cur.execute('''
    CREATE TABLE Autos(
    AutoID INT INTEGER NOT NULL PRIMARY KEY, 
    Hersteller TEXT, 
    Modell TEXT, 
    Fahrzeugtyp TEXT,
    PreisProTag INT,
    Startdatum DATE,
    Enddatum DATE
    );
''')

cur.execute('''
    CREATE TABLE Mietauftrag(
    FOREIGN KEY(Mieter) REFERENCES User(UserID),
    FOREIGN KEY(Vermieter) REFERENCES User(UserID),
    FOREIGN KEY(Auto) REFERENCES Autos(AutoID),
    Startdatum DATE,
    Enddatum DATE,
    Überweisungsdatum DATE,
    Gesamtpreis INT
    )
''')

cur.execute('''
    CREATE TABLE Mietauftrag(
    FOREIGN KEY(User) REFERENCES User(UserID),
    FOREIGN KEY(Auto) REFERENCES Autos(AutoID)
    )
''')
