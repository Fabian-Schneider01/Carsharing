# coding=utf-8
from flask import *
import sqlite3
from models import createTabels
import datetime


app = Flask(__name__)
app.secret_key = "4khJ7Ggljy"

with app.app_context():
    createTabels()

@app.route('/')
def home():
    return render_template("login.html")

#login seite
@app.route("/login", methods = ["GET", "POST"])
def login():
    userFound = None
    #post methode für login button
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            #in datenbank nachschauen ob email und password übereinstimmt
            cur.execute("SELECT UserID from User WHERE Email=(?) AND Passwort=(?)", [(email), (password)])
            input = cur.fetchall()
            #wenn input gegeben und login button aktiv
            if len(input) > 0:
                print("login Success")
                userFound = 1
                session["UserID"] = cur.execute("SELECT UserID from User WHERE Email=(?)", [(email)]).fetchone()[0]
                return redirect(url_for("profile"))
            #user nicht gefunden
            else: 
                print("error: user not found")
                userFound = 0
                
    return render_template("login.html", userFound = userFound)

#logout funktion
@app.route("/logout", methods=["POST", "GET"])
def logout():
    #session beenden
    session.pop("UserID", None)
    #zurück zur login seite leiten, nach logout
    return redirect(url_for("login"))

#registrierungsseite
@app.route("/register", methods = ["GET", "POST"])
def register():
    emptyField = None
    emailExists = None
    usernameExists = None
    pwNotMatching = None
    #registrierungsbutton aktiv
    if request.method == "POST":
        #benötigte Felder
        username = request.form["username"]
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        email = request.form["email"]
        street = request.form["street"]
        houseNum = request.form["houseNum"]
        city = request.form["city"]
        postalCode = request.form["postalCode"]
        password = request.form["password"]
        passwordConfirm = request.form["passwordConfirm"]
        #error, wenn nicht alle felder ausgefüllt wurden
        if username == "" or firstName == "" or lastName == "" or email == "" or street == "" or houseNum == "" or city == "" or postalCode == "" or password == "" or passwordConfirm== "":
            print("empty field")
            emptyField = 1
        else:
            #alle Felder ausgefüllt
            emptyField = 0
            with sqlite3.connect("database.sqlite") as con:
                cur = con.cursor()
                cur.execute("SELECT Email FROM User WHERE Email=(?)", [(email)])
                findEmail = cur.fetchall()
                cur.execute("SELECT Benutzername FROM User WHERE Benutzername=(?)", [(username)])
                findUsername = cur.fetchall()
                #überprüfen ob email bereits existiert
                if len(findEmail) > 0:
                    print("email already exists")
                    emailExists = 1
                #überprüfen ob username existiert
                if len(findUsername) > 0:
                    print("username already exists")
                    usernameExists = 1
                #überprüfen ob passwörter übereinstimmen
                if password != passwordConfirm:
                    print("password not matching")
                    pwNotMatching = 1
                #lege user an, wenn kein error auftritt
                if emailExists != 1 and usernameExists != 1 and pwNotMatching != 1:
                    cur.execute("INSERT INTO Adresse(Straße, Hausnummer, Ort, Postleitzahl) VALUES(?, ?, ?, ?)", (street, houseNum, city, postalCode))
                    cur.execute("SELECT * FROM Adresse ORDER BY AdressID DESC LIMIT 1")
                    addressID = cur.fetchone()[0]
                    cur.execute("INSERT INTO User(Benutzername, Vorname, Nachname, Email, Passwort, Guthaben, Adresse) VALUES(?, ?, ?, ?, ?, 0, ?)", (username, firstName, lastName, email, password, addressID))
                    con.commit()
                    print("registration successful")
                    #nach erfolgreicher registrierung zur login seite leiten
                    return redirect(url_for("login"))

    return render_template("register.html", emptyField = emptyField, emailExists = emailExists, usernameExists = usernameExists, pwNotMatching = pwNotMatching)

#profil seite
@app.route("/profile", methods = ["GET", "POST"])
def profile():
    email = None
    username = None
    firstName = None
    lastName = None
    addressID = None
    street = None
    houseNum = None
    city = None
    postalCode = None
    credit = None
    password = None
    rented = []
    periods = []
    #wenn nicht eingeloggt, zurück zur login
    if request.method == "GET":
        if session.get("UserID") is None:
            with sqlite3.connect("database.sqlite") as con:
                cur = con.cursor()
                cur.fetchall()   
            return redirect(url_for("login"))
        else:
            with sqlite3.connect("database.sqlite") as con:
                #profilansicht mit userdaten füllen
                cur = con.cursor()
                userID = session["UserID"]
                email = cur.execute("SELECT Email from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
                username =cur.execute("SELECT Benutzername from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
                firstName = cur.execute("SELECT Vorname from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
                lastName = cur.execute("SELECT Nachname from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
                password = cur.execute("SELECT Passwort from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
                addressID = cur.execute("SELECT Adresse from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
                street = cur.execute("SELECT Straße from Adresse WHERE AdressID=(?)", [(addressID)]).fetchone()[0]
                houseNum = cur.execute("SELECT Hausnummer from Adresse WHERE AdressID=(?)", [(addressID)]).fetchone()[0]
                city = cur.execute("SELECT Ort from Adresse WHERE AdressID=(?)", [(addressID)]).fetchone()[0]
                postalCode = cur.execute("SELECT Postleitzahl from Adresse WHERE AdressID=(?)", [(addressID)]).fetchone()[0]
                credit = cur.execute("SELECT Guthaben from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
                print(periods)
            con.commit()
            with sqlite3.connect("database.sqlite") as con:
                #zeige alle Fahrzeuge in eigene Autos und gemietete Autos an
                cur = con.cursor()
                userID = session["UserID"]
                cars = cur.execute("SELECT AutoID, Hersteller, Modell, Fahrzeugtyp, PreisProTag FROM User LEFT JOIN Autobesitzer ON User.UserID = Autobesitzer.User LEFT JOIN Autos ON Autobesitzer.Auto = Autos.AutoID WHERE UserID=(?)", [(userID)]).fetchall()
                all_dates = []
                all_rented = []
                for car in cars:
                    dates = cur.execute("SELECT Datum From Verfuegbar WHERE Auto=(?)", [(car[0])]).fetchall()
                    all_dates.append(dates)
                    rented = cur.execute("SELECT Startdatum, Enddatum FROM Mietauftrag WHERE Auto=(?)", [(car[0])]).fetchall()
                    all_rented.append(rented)
    #profil verändern ansicht
    if request.method == "POST" and request.form['formButton'] == "Speichern":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        passwordConfirm = request.form["passwordConfirm"]
        street = request.form["street"]
        houseNum = request.form["houseNum"]
        city = request.form["city"]
        postalCode = request.form["postalCode"]
        credit = request.form["credit"]
        with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            #überprüfen ob alle felder ausgefüllt sind, bevor ein update der daten stattfindet
            if username!="":
                cur.execute("UPDATE User SET Benutzername=(?) WHERE UserID=(?)", [username, session["UserID"]])
            if email!="":
                cur.execute("UPDATE User SET Email=(?) WHERE UserID=(?)", [email, session["UserID"]])
            if password != "":
                cur.execute("UPDATE User SET Passwort=(?) WHERE UserID=(?)", [password, session["UserID"]])
                print(password)
            if street!="":
                cur.execute("UPDATE Adresse SET Straße=(?) WHERE AdressID=(?)", [street, session["UserID"]])
            if houseNum!="":
               cur.execute("UPDATE Adresse SET Hausnummer=(?) WHERE AdressID=(?)", [houseNum, session["UserID"]])
            if city!="":
                cur.execute("UPDATE Adresse SET Ort=(?) WHERE AdressID=(?)", [city, session["UserID"]])
            if postalCode!="":
                cur.execute("UPDATE Adresse SET Postleitzahl=(?) WHERE AdressID=(?)", [postalCode, session["UserID"]])
            if credit!="":
                cur.execute("UPDATE User SET Guthaben=(?) WHERE UserID=(?)", [credit, session["UserID"]])
            cur.fetchall()
        con.commit()
        return redirect(url_for("profile"))
    #button um eigene autos hinzuzufügen
    elif request.method == 'POST' and request.form['formButton'] == "Hinzufügen":
        #nach modell, fahrzeugtyp, hersteller und preis abfragen => bezogen auf user session
        modell = request.form['modell']
        fahrzeugtyp = request.form['fahrzeugtyp']
        hersteller = request.form['hersteller']
        preis = request.form['preis']
        current_user_id = session['UserID']
        with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Autos(Hersteller, Modell, Fahrzeugtyp, PreisProTag) VALUES((?), (?), (?), (?))", [(hersteller), (modell), (fahrzeugtyp), (preis)])
            car_id = cur.execute("SELECT AutoID FROM Autos WHERE AutoID=(SELECT max(AutoID) FROM Autos)").fetchone()[0]
            cur.execute("INSERT INTO Autobesitzer VALUES((?), (?))", [current_user_id, car_id])
        con.commit()
        return redirect(url_for("profile"))
    print(cars[0][0])
    return render_template("profile.html", email = email, username = username, firstName = firstName, lastName = lastName, street = street, houseNum = houseNum, city = city, postalCode = postalCode, credit = credit, password = password, cars = cars, rentCars = [], rented = rented, periods = periods, all_dates = all_dates, all_rented = all_rented)

#methoden um autos zu verändern
@app.route("/edit-car/<id>", methods=['GET', 'POST'])
def edit_car(id):
    modell = request.form['modell']
    fahrzeugtyp = request.form['fahrzeugtyp']
    hersteller = request.form['hersteller']
    preis = request.form['preis']

    with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            cur.execute("UPDATE Autos SET Hersteller=(?), Modell=(?), Fahrzeugtyp=(?), PreisProTag=(?) WHERE AutoID=(?)", [(hersteller), (modell), (fahrzeugtyp), (preis), (id)])
    con.commit()
    return redirect(url_for("profile"))

"""
redirect for adding new timeframes where the user wants to rent their car
checks if given values are allowed and stores them
"""
@app.route("/add-timeframe/<id>", methods=['GET', 'POST'])
def add_timeframe(id):
    start = request.form['startdate']
    end = request.form['enddate']
    with sqlite3.connect("database.sqlite") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO Verfuegbar VALUES(?, ?)", [id, "2022-06-01"])
        # find all the dates where the car is available already
        available = cur.execute("SELECT Datum FROM Verfuegbar WHERE Auto=(?)", [(id)]).fetchall()[0]
        # find all the timeframes where the car is rented already  
        rented = cur.execute("SELECT Startdatum, Enddatum FROM Mietauftrag WHERE Auto=(?)", [(id)]).fetchall()
    con.commit() 

    startdate = datetime.date.fromisoformat(start)
    enddate = datetime.date.fromisoformat(end)    

    available_dates = [datetime.date.fromisoformat(i) for i in available]
    rented_dates = [(datetime.date.fromisoformat(i[0]), datetime.date.fromisoformat(i[1])) for i in rented]
    # check for overlap with rented times
    not_rented_dates = []
    date = startdate
    while date <= enddate:
        flag = 0    # hypothesis: not overlapping with a timeframe
        for timeframe in rented_dates:
            if not(date>timeframe[1] or date<timeframe[0]): # overlap
                flag = 1
                break
        if flag == 0:
            not_rented_dates.append(date)
        date = date + datetime.timedelta(days=1)

    # check for overlap with dates already marked as available
    dates_to_add = []
    for date in not_rented_dates:
        for available in available_dates:
            if not(date==available): # no overlap
                dates_to_add.append(date)          

    # only add the dates that are still available and not marked as available yet
    with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            for date in dates_to_add:
                cur.execute("INSERT INTO Verfuegbar(Auto, Datum) VALUES((?), (?))", [(id), (date)])               
    con.commit()
    return redirect(url_for("profile"))

"""
displays the explore page
filters the results shown when the filters have been selected
"""
@app.route("/findCar", methods=['GET', 'POST'])
def findCar():
    matchedUserCars = None
    cars = None
    incompleteFilter = 0
    if session.get("UserID") is None:
        return redirect(url_for("login"))
    else:
        with sqlite3.connect("database.sqlite") as con:
            # for displaying all the car the user has added
                cur = con.cursor()
                userID = session["UserID"]
                cars = cur.execute("SELECT AutoID, Hersteller, Modell, Fahrzeugtyp, PreisProTag FROM Autos").fetchall()

        if request.method == "POST":
            with sqlite3.connect("database.sqlite") as con:

                cur = con.cursor()
                filterPlace = request.form["place"]
                if request.form.get("filter") == "Suchen":
                    filterPlace = request.form["place"]
                    filterStartdate = request.form["startdate"]
                    filterEnddate = request.form["enddate"]
                    filterClass = request.form["carclass"]
                    filterMaxPrice = request.form["maxprice"]
                    incompleteFilter = 0
                    if filterPlace == "" and filterStartdate == "" and filterEnddate == "" and filterClass == "Fahrzeugklasse" and filterMaxPrice == "":
                        print("Bitte alle Felder ausfüllen")
                        incompleteFilter = 1
                    else:
                        incompleteFilter = 0

                    
                    print("Filtered Search: ", filterPlace, " ", filterStartdate, " ", filterEnddate, " ", filterClass, " ", filterMaxPrice)
                    matchingUser = cur.execute("SELECT UserID FROM User INNER JOIN Adresse ON Adresse.AdressID = User.Adresse WHERE Adresse.Ort == (?)", [(filterPlace)]).fetchall()              
                    if matchingUser != []:
                        matchedUserCars = cur.execute("SELECT AutoID, Hersteller, Modell, Fahrzeugtyp, PreisProTag FROM User LEFT JOIN Autobesitzer ON User.UserID = Autobesitzer.User LEFT JOIN Autos ON Autobesitzer.Auto = Autos.AutoID WHERE UserID=(?)", [(matchingUser[0][0])]).fetchall()
                        if matchedUserCars != "":
                            for i in range(len(matchedUserCars)):
                                if filterClass in matchedUserCars[i][3]:
                                    if matchedUserCars != []:
                                        return render_template("findCar.html", cars = matchedUserCars)
                        
                                                       
                    print("Filtered Search: ", filterPlace, " ", filterStartdate, " ", filterEnddate, " ", filterClass, " ", filterMaxPrice)
                else:
                    matchedCars = cur.execute("SELECT AutoID, Hersteller, Modell, Fahrzeugtyp, PreisProTag from Autos LEFT JOIN Autobesitzer").fetchall()[0]
                    for i in range(len(matchedCars)):
                        print(matchedCars[i])
                        if request.form.get(str(session["matchedCars"][i][0])) == "mieten":
                            print("selected car")
                            lessor = cur.execute("SELECT User FROM Autobesitzer WHERE Auto = (?)", [(matchedCars[i][0])]).fetchone()[0]
                            startDate = cur.execute("SELECT Startdatum FROM Autos WHERE AutoID = (?)", [(matchedCars[i][0])]).fetchone()[0]
                            endDate = cur.execute("SELECT Enddatum FROM Autos WHERE AutoID = (?)", [(matchedCars[i][0])]).fetchone()[0]
                            pricePerDay = cur.execute("SELECT PreisProTag FROM Autos WHERE AutoID = (?)", [(matchedCars[i][0])]).fetchone()[0]
                            ammountDays = cur.execute("SELECT JULIANDAY(Enddatum) - JULIANDAY(Startdatum) AS difference FROM Autos WHERE AutoID = (?)", [(matchedCars[i][0])]).fetchone()[0]
                            endPrice = ammountDays * pricePerDay
                            print(session["UserID"])
                            print(lessor)
                            print(endPrice)
                            print(startDate)
                            print(endDate)

                            ### check if dates are available
                            date = startdate
                            checkflag = 0
                            allRentedDates = []
                            while date <= enddate:
                                available = cur.execute("SELECT Datum FROM Verfuegbar WHERE Auto=(?) AND Datum=(?)", [(id), (date)]).fetchall()[0]
                                print("AVAILABLE?")
                                print(available)
                                if available == None:
                                    checkflag = 1
                                    break
                                allRentedDates.append(date)                           
                                date = date + datetime.timedelta(days=1)
                            guthaben = cur.execute("SELECT Guthaben FROM User WHERE UserID=(?)", [(session["UserID"])]).fetchone()[0]
                            if endPrice > guthaben:
                                checkflag = 2
                            if checkflag == 0:
                                cur.execute("INSERT INTO Mietauftrag(Mieter, Vermieter, Auto, Gesamtpreis, Startdatum, Enddatum, Ueberweisungsdatum) VALUES(?, ?, ?, ?, ?, ?, ?)", ((session["UserID"]), (lessor), (session["matchedCars"][i][0]), (endPrice), (startDate), (endDate), (startDate)))
                                cur.execute("UPDATE User SET Guthaben = Guthaben - (?) WHERE UserID = (?)", [(endPrice), (session["UserID"])])
                                cur.execute("UPDATE User SET Guthaben = Guthaben + (?) WHERE UserID = (?)", [(endPrice), (lessor)])
                                for date in allRentedDates:
                                    cur.execute("DELETE FROM Verfuegbar WHERE User=(?) AND Datum = (?)", (session["UserID"], date))
                                con.commit()
                            elif checkflag == 1:
                                print("Der angeforderte Zeitraum ist nicht verfügbar!") 
                            elif checkflag == 2:
                                print("Das Guthaben reicht nicht aus, um das Auto zu mieten!")
                            
                            break
                    
    if request.method == 'POST':
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        print(enddate)

    return render_template("findCar.html", cars = cars, incompleteFilter = incompleteFilter)

"""
redirect for renting a car selected by the user on the findCar-page
"""
@app.route("/rent-car/<id>", methods=['GET', 'POST'])
def rent_car(id):
    start = request.form['startdate']
    startdate = datetime.date.fromisoformat(start)
    end = request.form['enddate']
    enddate = datetime.date.fromisoformat(end)

    # get price information from database
    with sqlite3.connect("database.sqlite") as con:
        cur = con.cursor()
        pricePerDay = cur.execute("SELECT PreisProTag FROM Autos WHERE AutoID = (?)", [(id)]).fetchone()[0]
        amountDays = (enddate - startdate).days + 1
        endPrice = amountDays * pricePerDay

        try:
            # only rentable if car is available for selected timeframe
            allRentedDates = []
            date = startdate
            while date <= enddate:
                available = cur.execute("SELECT Datum FROM Verfuegbar WHERE Auto=(?) and Datum=(?)", [(id), (date)]).fetchone()
                if available == None:
                    raise Exception("Der angeforderte Zeitraum ist nicht verfügbar!")
                else:
                    available = available[0] 
                    allRentedDates.append(date)                           
                    date = date + datetime.timedelta(days=1)
            try:
                # only rentable if enough money left
                guthaben = cur.execute("SELECT Guthaben FROM User WHERE UserID=(?)", [(session["UserID"])]).fetchone()[0]
                if endPrice > guthaben:
                    raise Exception("Das Guthaben reicht nicht aus, um das Auto zu mieten!")
                else:
                    cur.execute("INSERT INTO Mietauftrag(Mieter, Auto, Gesamtpreis, Startdatum, Enddatum) VALUES(?, ?, ?, ?, ?)", ((session["UserID"]), (id), (endPrice), (startdate), (enddate)))
                    cur.execute("UPDATE User SET Guthaben = (Guthaben - (?)) WHERE UserID = (?)", [(endPrice), (session["UserID"])])
                    vermieter = cur.execute("SELECT UserID FROM User JOIN Autobesitzer ON User.UserID = Autobesitzer.User LEFT JOIN Autos ON Autobesitzer.Auto = Autos.AutoID WHERE AutoID = (?)", [(id)]).fetchone()[0]
                    cur.execute("UPDATE User SET Guthaben = (Guthaben + (?)) WHERE UserID = (?)", [(endPrice), (vermieter)])
                    for date in allRentedDates:
                        cur.execute("DELETE FROM Verfuegbar WHERE Auto=(?) AND Datum = (?)", (id, date))
            except:
                print("Das Guthaben reicht nicht aus, um das Auto zu mieten!")
        except:
            print("Der angeforderte Zeitraum ist nicht verfügbar!")
        finally:
            con.commit()
            return redirect(url_for("findCar"))

if __name__ == "__main__":
    app.run()