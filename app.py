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

@app.route("/login", methods = ["GET", "POST"])
def login():
    userFound = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            cur.execute("SELECT UserID from User WHERE Email=(?) AND Passwort=(?)", [(email), (password)])
            input = cur.fetchall()
            if len(input) > 0:
                print("login Success")
                userFound = 1
                session["UserID"] = cur.execute("SELECT UserID from User WHERE Email=(?)", [(email)]).fetchone()[0]
                return redirect(url_for("profile"))
            else: 
                print("error: user not found")
                userFound = 0
                
    return render_template("login.html", userFound = userFound)

@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("UserID", None)
    return redirect(url_for("login"))

@app.route("/register", methods = ["GET", "POST"])
def register():
    emptyField = None
    emailExists = None
    usernameExists = None
    pwNotMatching = None
    if request.method == "POST":
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
        if username == "" or firstName == "" or lastName == "" or email == "" or street == "" or houseNum == "" or city == "" or postalCode == "" or password == "" or passwordConfirm== "":
            print("empty field")
            emptyField = 1
        else:
            emptyField = 0
            with sqlite3.connect("database.sqlite") as con:
                cur = con.cursor()
                cur.execute("SELECT Email FROM User WHERE Email=(?)", [(email)])
                findEmail = cur.fetchall()
                cur.execute("SELECT Benutzername FROM User WHERE Benutzername=(?)", [(username)])
                findUsername = cur.fetchall()
                if len(findEmail) > 0:
                    print("email already exists")
                    emailExists = 1
                if len(findUsername) > 0:
                    print("username already exists")
                    usernameExists = 1
                if password != passwordConfirm:
                    print("password not matching")
                    pwNotMatching = 1
                if emailExists != 1 and usernameExists != 1 and pwNotMatching != 1:
                    cur.execute("INSERT INTO Adresse(Straße, Hausnummer, Ort, Postleitzahl) VALUES(?, ?, ?, ?)", (street, houseNum, city, postalCode))
                    cur.execute("SELECT * FROM Adresse ORDER BY AdressID DESC LIMIT 1")
                    addressID = cur.fetchone()[0]
                    cur.execute("INSERT INTO User(Benutzername, Vorname, Nachname, Email, Passwort, Guthaben, Adresse) VALUES(?, ?, ?, ?, ?, 0, ?)", (username, firstName, lastName, email, password, addressID))
                    con.commit()
                    print("registration successful")
                    return redirect(url_for("login"))

    return render_template("register.html", emptyField = emptyField, emailExists = emailExists, usernameExists = usernameExists, pwNotMatching = pwNotMatching)

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
    if request.method == "GET":
        if session.get("UserID") is None:
            with sqlite3.connect("database.sqlite") as con:
                cur = con.cursor()
                cur.fetchall()   
            return redirect(url_for("login"))
        else:
            with sqlite3.connect("database.sqlite") as con:
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
                periods = cur.execute("SELECT Verfuegbar.Datum FROM Verfuegbar LEFT JOIN Autobesitzer ON Autobesitzer.Auto = Verfuegbar.Auto LEFT JOIN User ON UserID = Autobesitzer.User WHERE UserID = (?)", [(session["UserID"])]).fetchall()
                print(periods)
            con.commit()
            with sqlite3.connect("database.sqlite") as con:
            # for displaying all the car the user has added
                cur = con.cursor()
                userID = session["UserID"]
                cars = cur.execute("SELECT AutoID, Hersteller, Modell, Fahrzeugtyp, PreisProTag FROM User LEFT JOIN Autobesitzer ON User.UserID = Autobesitzer.User LEFT JOIN Autos ON Autobesitzer.Auto = Autos.AutoID WHERE UserID=(?)", [(userID)]).fetchall()
                """for i in range(len(cars)): #later to show if a car was rented
                    for o in range(len(cur.execute("SELECT Auto FROM Mietauftrag").fetchall())):
                        if cars[i][0] == cur.execute("SELECT Auto FROM Mietauftrag").fetchall()[o][0]:
                            rented.append(1)
                        else:
                            rented.append(0)
                print(rented)"""
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

    elif request.method == 'POST' and request.form['formButton'] == "Hinzufügen":
        modell = request.form['modell']
        print(modell)
        fahrzeugtyp = request.form['fahrzeugtyp']
        print(fahrzeugtyp)
        hersteller = request.form['hersteller']
        print(hersteller)
        preis = request.form['preis']
        print(preis)
        current_user_id = session['UserID']
        with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Autos(Hersteller, Modell, Fahrzeugtyp, PreisProTag) VALUES((?), (?), (?), (?))", [(hersteller), (modell), (fahrzeugtyp), (preis)])
            car_id = cur.execute("SELECT AutoID FROM Autos WHERE AutoID=(SELECT max(AutoID) FROM Autos)").fetchone()[0]
            print(car_id)
            cur.execute("INSERT INTO Autobesitzer VALUES((?), (?))", [current_user_id, car_id])
        con.commit()
        return redirect(url_for("profile"))
    print(cars[0][0])
    return render_template("profile.html", email = email, username = username, firstName = firstName, lastName = lastName, street = street, houseNum = houseNum, city = city, postalCode = postalCode, credit = credit, password = password, cars = cars, rentCars = [], rented = rented, periods = periods[:5])

@app.route("/edit-car/<id>", methods=['GET', 'POST'])
def edit_car(id):
    print(id)
    modell = request.form['modell']
    fahrzeugtyp = request.form['fahrzeugtyp']
    hersteller = request.form['hersteller']
    preis = request.form['preis']

    with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            cur.execute("UPDATE Autos SET Hersteller=(?), Modell=(?), Fahrzeugtyp=(?), PreisProTag=(?) WHERE AutoID=(?)", [(hersteller), (modell), (fahrzeugtyp), (preis), (id)])
    con.commit()
    # TODO
    # fix the default dates and price in profile.html
    return redirect(url_for("profile"))

@app.route("/add-timeframe/<id>", methods=['GET', 'POST'])
def add_timeframe(id):
    print("arrived")
    print(id)
    start = request.form['startdate']
    print(start)
    end = request.form['enddate']
    print(end)
    # TODO: Einträge in der Vergangenheit löschen/ignorieren, auch beim Suchen und Mieten
    with sqlite3.connect("database.sqlite") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO Verfuegbar VALUES(?, ?)", [id, "2022-06-01"])
        # find all the dates where the car is available already
        available = cur.execute("SELECT Datum FROM Verfuegbar WHERE Auto=(?)", [(id)]).fetchall()[0]
        # find all the timeframes where the car is rented already  
        rented = cur.execute("SELECT Startdatum, Enddatum FROM Mietauftrag WHERE Auto=(?)", [(id)]).fetchall()
    con.commit() 
    print(available)  
    print(rented)

    startdate = datetime.date.fromisoformat(start)
    print("Startdate")
    print(startdate)
    enddate = datetime.date.fromisoformat(end)    

    available_dates = [datetime.date.fromisoformat(i) for i in available]
    print(available_dates)
    rented_dates = [(datetime.date.fromisoformat(i[0]), datetime.date.fromisoformat(i[1])) for i in rented]
    print(rented_dates)

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
        print("new date")
        print(date)

    print("not rented dates")
    print(not_rented_dates)

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

# TODO change startdate enddate references to its own table
@app.route("/findCar", methods=['GET', 'POST'])
def findCar():
    matchedUserCars = None
    cars = None
    if session.get("UserID") is None:
        return redirect(url_for("login"))
    else:
        with sqlite3.connect("database.sqlite") as con:
            # for displaying all the car the user has added
                cur = con.cursor()
                userID = session["UserID"]
                cars = cur.execute("SELECT AutoID, Hersteller, Modell, Fahrzeugtyp, PreisProTag FROM Autos").fetchall()
                """
                # rename cars in the above line to cardata
                cardates = cur.execute("SELECT Datum FROM Verfuegbar WHERE Auto=(?)", [(id)]).fetchall()[0]
                cardate = None
                while cardate == None:
                    for date in cardates:   # find first candidate in the future
                        if (cardate - date.today) > 0:
                            cardate = date
                            break
                if cardate == None:
                    ##error! nicht verfügbar, dieses car nicht anzeigen
                for date in cardates:
                    if (date - date.today)>0 and (date-date.today)<(cardate-date.today)

                cars = (cardata[0], cardata[1], cardata[2], cardata[3], cardata[4], cardate)    # TODO check if new Structure is used everywhere, so cars[5] is date and cars[6] nonexistent
                """
        if request.method == "POST":
            #change name to rentCar-i => i = AutoID 
            with sqlite3.connect("database.sqlite") as con:
                available = cur.execute("SELECT Datum FROM Verfuegbar WHERE Auto=(?)", [(id)]).fetchall()[0]
                available_dates = [datetime.date.fromisoformat(i) for i in available]

                cur = con.cursor()
                filteredCars =[]
                filterPlace = request.form["place"]
                if request.form.get("filter") == "Suchen":
                    filterPlace = request.form["place"]
                    filterStartdate = request.form["startdate"]
                    filterEnddate = request.form["enddate"]
                    filterClass = request.form["carclass"]
                    filterMaxPrice = request.form["maxprice"]
                    #cars = cur.execute(filter(filterPlace, filterStartdate, filterEnddate, filterClass, filterMaxPrice))
                    
                    #cur.execute("SELECT UserID FROM User INNER JOIN Adresse ON Adresse.AdressID = User.Adresse WHERE Adresse.Ort == (?)", [(filterPlace)]).fetchall() 
                    if filterPlace != "":
                        if filterStartdate != "":
                            if filterEnddate != "":
                                if filterClass != "":
                                    if filterMaxPrice != "":
                                        filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                        cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace), (filterClass), (filterPeriod), (filterMaxPrice), (session["UserID"])]).fetchall()
                                        #FILTERfor i in range(available):
                                        startdate = datetime.date.fromisoformat(filterStartdate)
                                        enddate = datetime.date.fromisoformat(filterEnddate)
                                        date = startdate
                                        while date <= enddate:
                                            # check each
                                            if not(date in available_dates):
                                                # do not show this car as it is not available for the selected timeperiod
                                                break                                              
                                            date = date + datetime.timedelta(days=1)
                                            
                                        if cars != None:
                                            for i in range(len(cars)):
                                                dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                    print("car found")
                                                    session["matchedCars"] = cars
                                                else:
                                                    print("no car found")
                                    else:
                                        filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                        cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND UserID != (?)", [(filterPlace), (filterClass), (session["UserID"])]).fetchall()
                                        if cars != None:
                                            for i in range(len(cars)):
                                                dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                    print("car found")
                                                    session["matchedCars"] = cars
                                                else:
                                                    print("no car found")
                                                    
                                        print("end")
                                else:
                                    if filterMaxPrice != "":
                                        filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                        cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace), (filterPeriod), (filterMaxPrice), (session["UserID"])]).fetchall()
                                        if cars != None:
                                            for i in range(len(cars)):
                                                dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                    print("car found")
                                                    session["matchedCars"] = cars
                                                else:
                                                    print("no car found")
                                                    
                                    else:
                                        filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                        cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace),(filterPeriod), (session["UserID"])]).fetchall()
                                        if cars != None:
                                            for i in range(len(cars)):
                                                dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                    print("car found")
                                                    session["matchedCars"] = cars
                                                else:
                                                    print("no car found")
                                                    
                            else:
                                if filterClass != "":
                                    if filterMaxPrice != "":
                                        filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                        cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace), (filterClass), (filterPeriod), (filterMaxPrice), (session["UserID"])]).fetchall()
                                        if cars != None:
                                            for i in range(len(cars)):
                                                dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                    print("car found")
                                                    session["matchedCars"] = cars
                                                else:
                                                    print("no car found")
                                    else:
                                        filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                        cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?)  AND UserID != (?)", [(filterPlace), (session["UserID"])]).fetchall()
                                        if cars != None:
                                            for i in range(len(cars)):
                                                dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                    print("car found")
                                                    session["matchedCars"] = cars
                                                else:
                                                    print("no car found")
                                        else: 
                                            filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                            cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace), (filterClass), (filterPeriod), (filterMaxPrice), (session["UserID"])]).fetchall()
                                            if cars != None:
                                                for i in range(len(cars)):
                                                    dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                        print("car found")
                                                        session["matchedCars"] = cars
                                                    else:
                                                        print("no car found")
                                    
                    else: 
                        if filterStartdate != "":
                            if filterEnddate != "":
                                if filterClass != "":
                                    if filterMaxPrice != "":
                                        filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                        cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace), (filterClass), (filterPeriod), (filterMaxPrice), (session["UserID"])]).fetchall()
                                        if cars != None:
                                            for i in range(len(cars)):
                                                dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                    print("car found")
                                                    session["matchedCars"] = cars
                                                else:
                                                    print("no car found")
                                    else:
                                        filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                        cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND UserID != (?)", [(filterPlace), (filterClass), (session["UserID"])]).fetchall()
                                        if cars != None:
                                            for i in range(len(cars)):
                                                dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                    print("car found")
                                                    session["matchedCars"] = cars
                                                else:
                                                    print("no car found")
                                        print("end")
                                else:
                                    if filterMaxPrice != "":
                                        filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                        cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace), (filterPeriod), (filterMaxPrice), (session["UserID"])]).fetchall()
                                        if cars != None:
                                            for i in range(len(cars)):
                                                dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                    print("car found")
                                                    session["matchedCars"] = cars
                                                else:
                                                    print("no car found")
                                    else:
                                        filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                        cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace),(filterPeriod), (session["UserID"])]).fetchall()
                                        if cars != None:
                                            for i in range(len(cars)):
                                                dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                    print("car found")
                                                    session["matchedCars"] = cars
                                                else:
                                                    print("no car found")
                            else:
                                if filterClass != "":
                                    if filterMaxPrice != "":
                                        filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                        cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace), (filterClass), (filterPeriod), (filterMaxPrice), (session["UserID"])]).fetchall()
                                        if cars != None:
                                            for i in range(len(cars)):
                                                dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                    print("car found")
                                                    session["matchedCars"] = cars
                                                else:
                                                    print("no car found")
                                    else:
                                        filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                        cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?)  AND UserID != (?)", [(filterPlace), (session["UserID"])]).fetchall()
                                        if cars != None:
                                            for i in range(len(cars)):
                                                dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                    print("car found")
                                                    session["matchedCars"] = cars
                                                else:
                                                    print("no car found")
                                        else: 
                                            filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                            cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace), (filterClass), (filterPeriod), (filterMaxPrice), (session["UserID"])]).fetchall()
                                            if cars != None:
                                                for i in range(len(cars)):
                                                    dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                        print("car found")
                                                        session["matchedCars"] = cars
                                                    else:
                                                        print("no car found")
                        else:
                            if filterStartdate != "":
                                if filterEnddate != "":
                                    if filterClass != "":
                                        if filterMaxPrice != "":
                                            filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                            cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace), (filterClass), (filterPeriod), (filterMaxPrice), (session["UserID"])]).fetchall()
                                            if cars != None:
                                                for i in range(len(cars)):
                                                    dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                        print("car found")
                                                        session["matchedCars"] = cars
                                                    else:
                                                        print("no car found")
                                                      
                                        else:
                                            filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                            cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND UserID != (?)", [(filterPlace), (filterClass), (session["UserID"])]).fetchall()
                                            if cars != None:
                                                for i in range(len(cars)):
                                                    dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                        print("car found")
                                                        session["matchedCars"] = cars
                                                    else:
                                                        print("no car found")
                                                       
                                            print("end")
                                    else:
                                        if filterMaxPrice != "":
                                            filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                            cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace), (filterClass), (filterPeriod), (filterMaxPrice), (session["UserID"])]).fetchall()
                                            if cars != None:
                                                for i in range(len(cars)):
                                                    dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                        print("car found")
                                                        session["matchedCars"] = cars
                                                    else:
                                                        print("no car found")
                                                       
                                        else:
                                            filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                            cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace),(filterPeriod), (session["UserID"])]).fetchall()
                                            if cars != None:
                                                for i in range(len(cars)):
                                                    dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                        print("car found")
                                                        session["matchedCars"] = cars
                                                    else:
                                                        print("no car found")
                                                        
                                else:
                                    if filterClass != "":
                                        if filterMaxPrice != "":
                                            filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                            cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace), (filterClass), (filterPeriod), (filterMaxPrice), (session["UserID"])]).fetchall()
                                            if cars != None:
                                                for i in range(len(cars)):
                                                    dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                        print("car found")
                                                        session["matchedCars"] = cars
                                                    else:
                                                        print("no car found")
                                        else:
                                            filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                            cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?)  AND UserID != (?)", [(filterPlace), (session["UserID"])]).fetchall()
                                            if cars != None:
                                                for i in range(len(cars)):
                                                    dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                    if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                        print("car found")
                                                        session["matchedCars"] = cars
                                                    else:
                                                        print("no car found")
                                            else: 
                                                filterPeriod = (datetime.strptime(request.form["enddate"], "%Y-%m-%d") - datetime.strptime(request.form["startdate"], "%Y-%m-%d")).days
                                                cars = cur.execute("SELECT UserID, AutoID FROM User LEFT JOIN Adresse ON Adresse.AdressID = User.Adresse LEFT JOIN Autobesitzer ON Autobesitzer.User = User.UserID LEFT JOIN Autos ON AutoID = Autobesitzer.Auto LEFT JOIN Verfuegbar ON Verfuegbar.Auto = Autobesitzer.Auto WHERE Autobesitzer.User = User.UserID AND Ort = (?) AND Fahrzeugtyp = (?) AND (?) * PreisProTag <= (?) AND UserID != (?)", [(filterPlace), (filterClass), (filterPeriod), (filterMaxPrice), (session["UserID"])]).fetchall()
                                                if cars != None:
                                                    for i in range(len(cars)):
                                                        dbStartDate = cur.execute("SELECT Startdatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                        dbEndDate = cur.execute("SELECT Enddatum FROM Verfuegbar WHERE Auto = (?)", [(cars[i][1])]).fetchall()
                                                        if dbStartDate[i][0] <= filterStartdate and dbEndDate[i][0] >= filterEnddate:
                                                            print("car found")
                                                            session["matchedCars"] = cars
                                                        else:
                                                            print("no car found")           
                        
                                    
                    print("Filtered Search: ", filterPlace, " ", filterStartdate, " ", filterEnddate, " ", filterClass, " ", filterMaxPrice)
                    #for i in range(cur.execute("SELECT COUNT(*) FROM Autos").fetchone()[0]):
                    """matchingUser = cur.execute("SELECT UserID FROM User INNER JOIN Adresse ON Adresse.AdressID = User.Adresse WHERE Adresse.Ort == (?)", [(filterPlace)]).fetchall()              
                    if matchingUser != []:
                        print(matchingUser[0][0])
                        matchedUserCars = cur.execute("SELECT AutoID, Hersteller, Modell, Fahrzeugtyp, PreisProTag, Startdatum, Enddatum FROM User LEFT JOIN Autobesitzer ON User.UserID = Autobesitzer.User LEFT JOIN Autos ON Autobesitzer.Auto = Autos.AutoID WHERE UserID=(?)", [(matchingUser[0][0])]).fetchall()
                        print(matchedUserCars[0])
                        if matchedUserCars != "":
                            for i in range(len(matchedUserCars)):
                                if filterClass in matchedUserCars[i][3]:
                                    if filterStartdate >= matchedUserCars[i][5] and filterStartdate <= matchedUserCars[i][6] and filterEnddate >= matchedUserCars[i][5] and filterEnddate <= matchedUserCars[i][6]:
                                        totalPrice = (datetime.strptime(filterEnddate, "%Y-%m-%d") - datetime.strptime(filterStartdate, "%Y-%m-%d")).days * matchedUserCars[i][4]
                                        if totalPrice <= int(filterMaxPrice):
                                            cars = matchedUserCars
                                            session["matchedCars"] = matchedUserCars
                                            return render_template("findCar.html", cars = cars)"""
                else:
                    matchedCars = cur.execute("SELECT AutoID, Hersteller, Modell, Fahrzeugtyp, PreisProTag from Autos LEFT JOIN Autobesitzer").fetchall()[0]  # where autobesitzer ungleich session user. TODO Autobesitzer tabelle killen
                    for i in range(len(matchedCars)):
                        print(matchedCars[i])
                        if request.form.get(str(session["matchedCars"][i][0])) == "mieten": # FIXEN!
                            print("selected car")
                            lessor = cur.execute("SELECT User FROM Autobesitzer WHERE Auto = (?)", [(matchedCars[i][0])]).fetchone()[0] #change 30 to variable
                            startDate = cur.execute("SELECT Startdatum FROM Autos WHERE AutoID = (?)", [(matchedCars[i][0])]).fetchone()[0] #change 30 to variable
                            endDate = cur.execute("SELECT Enddatum FROM Autos WHERE AutoID = (?)", [(matchedCars[i][0])]).fetchone()[0] #change 30 to variable
                            pricePerDay = cur.execute("SELECT PreisProTag FROM Autos WHERE AutoID = (?)", [(matchedCars[i][0])]).fetchone()[0] #change 30 to variable
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
                                    # abbrechen, popup-message 
                                allRentedDates.append(date)                           
                                date = date + datetime.timedelta(days=1)
                            guthaben = cur.execute("SELECT Guthaben FROM User WHERE UserID=(?)", [(session["UserID"])]).fetchone()[0]
                            if endPrice > guthaben:
                                checkflag = 2
                            if checkflag == 0:
                                cur.execute("INSERT INTO Mietauftrag(Mieter, Vermieter, Auto, Gesamtpreis, Startdatum, Enddatum, Ueberweisungsdatum) VALUES(?, ?, ?, ?, ?, ?, ?)", ((session["UserID"]), (lessor), (session["matchedCars"][i][0]), (endPrice), (startDate), (endDate), (startDate)))
                                cur.execute("UPDATE User SET Guthaben= Guthaben - (?) WHERE UserID=(?)", [(endPrice), (session["UserID"])])
                                cur.execute("UPDATE User SET Guthaben= Guthaben + (?) WHERE UserID=(?)", [(endPrice), (lessor)])
                                for date in allRentedDates:
                                    cur.execute("DELETE FROM Verfuegbar WHERE User=(?) AND Datum = (?)", (session["UserID"], date))
                                con.commit()
                            elif checkflag == 1:
                                # fehlermeldung 
                                print("Der angeforderte Zeitraum ist nicht verfügbar!") 
                            elif checkflag == 2:
                                # fehlermeldung zu wenig guthaben
                                print("Das Guthaben reicht nicht aus, um das Auto zu mieten!")
                            ###
                            
                            break
                    
    """            
    return render_template("findCar.html", cars = cars)#producer=producer, model=model, price=price)
            # for displaying all the cars the user has added
            cur = con.cursor()
            cars = cur.execute("SELECT AutoID, Hersteller, Modell, Fahrzeugtyp, PreisProTag, Startdatum, Enddatum FROM Autos").fetchall()
            # TODO: dont select the cars where the current user is the owner
            # TODO: call the table with all the timeframes where the cars have already been rented for the detail view
            # TODO: join with the owners' table
    # is called when the user clicked to rent the car
    """
    if request.method == 'POST':
        # TODO hier kommt rent car redirect hin!! 
        startdate = request.form['startdate']
        print(startdate)
        enddate = request.form['enddate']
        print(enddate)
        current_user_id = session['UserID']
        id_car = None
        # TODO: insert car renting order details into database.
        #with sqlite3.connect("database.sqlite") as con:
        #    cur.execute("INSERT INTO Autobesitzer VALUES((?), (?))", [current_user_id, car_id])
        #con.commit()
    return render_template("findCar.html", cars = cars)

@app.route("/rent-car/<id>", methods=['GET', 'POST'])
def rent_car(id):
    print("Lets rent a car!")
    print(id)
    start = request.form['startdate']
    startdate = datetime.date.fromisoformat(start)
    print(startdate)
    end = request.form['enddate']
    enddate = datetime.date.fromisoformat(end)
    print(enddate)

    allRentedDates = []
    with sqlite3.connect("database.sqlite") as con:
        cur = con.cursor()
        pricePerDay = cur.execute("SELECT PreisProTag FROM Autos WHERE AutoID = (?)", [(id)]).fetchone()[0] #change 30 to variable
        amountDays = startdate - enddate + datetime.timedelta(days=1)
        endPrice = amountDays * pricePerDay

        date = startdate

        available = cur.execute("SELECT * FROM User").fetchall()
        print(available)
        try:
            while date <= enddate:
                #available = cur.execute("SELECT Datum FROM Verfuegbar WHERE Auto=(?) and Datum=(?)", [(id), (date)]).fetchone()
                available = cur.execute("SELECT * FROM Verfuegbar").fetchall()[0]   # TUT NICHT
                print("all dates:")
                print(available)
                if available == None:
                    print("NOT AVAILABLE" + str(date))
                    raise Exception("Der angeforderte Zeitraum ist nicht verfügbar!")
                else:
                    print(available)
                    available = available[0] 
                    print(available[0])
                    allRentedDates.append(date)                           
                    date = date + datetime.timedelta(days=1)
            try:
                guthaben = cur.execute("SELECT Guthaben FROM User WHERE UserID=(?)", [(session["UserID"])]).fetchone()[0]
                if endPrice > guthaben:
                    raise Exception("Das Guthaben reicht nicht aus, um das Auto zu mieten!")
                else:
                    print("FIx")
                    cur.execute("INSERT INTO Mietauftrag(Mieter, Vermieter, Auto, Gesamtpreis, Startdatum, Enddatum, Ueberweisungsdatum) VALUES(?, ?, ?, ?, ?, ?, ?)", ((session["UserID"]), (2), (session["matchedCars"][i][0]), (endPrice), (startDate), (endDate), (startDate)))
                    cur.execute("UPDATE User SET Guthaben= Guthaben - (?) WHERE UserID=(?)", [(endPrice), (session["UserID"])])
                    cur.execute("UPDATE User SET Guthaben= Guthaben + (?) WHERE UserID=(?)", [(endPrice), (lessor)])
                    for date in allRentedDates:
                        cur.execute("DELETE FROM Verfuegbar WHERE User=(?) AND Datum = (?)", (session["UserID"], date))
            except:
                print("Das Guthaben reicht nicht aus, um das Auto zu mieten!")
        except:
            print("Der angeforderte Zeitraum ist nicht verfügbar!")
        finally:
            con.commit()
            return redirect(url_for("findCar"))

if __name__ == "__main__":
    app.run()