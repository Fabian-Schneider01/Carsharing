from flask import *
import sqlite3
from models import createTabels
from datetime import datetime

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
            con.commit()
            with sqlite3.connect("database.sqlite") as con:
            # for displaying all the car the user has added
                cur = con.cursor()
                userID = session["UserID"]
                cars = cur.execute("SELECT AutoID, Hersteller, Modell, Fahrzeugtyp, PreisProTag, Startdatum, Enddatum FROM User LEFT JOIN Autobesitzer ON User.UserID = Autobesitzer.User LEFT JOIN Autos ON Autobesitzer.Auto = Autos.AutoID WHERE UserID=(?)", [(userID)]).fetchall()
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
        startdate = request.form['startdate']
        print(startdate)
        enddate = request.form['enddate']
        print(enddate)
        current_user_id = session['UserID']
        with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Autos(Hersteller, Modell, Fahrzeugtyp, PreisProTag, Startdatum, Enddatum) VALUES((?), (?), (?), (?), (?), (?))", [(hersteller), (modell), (fahrzeugtyp), (preis), (startdate), (enddate)])
            car_id = cur.execute("SELECT AutoID FROM Autos WHERE AutoID=(SELECT max(AutoID) FROM Autos)").fetchone()[0]
            print(car_id)
            cur.execute("INSERT INTO Autobesitzer VALUES((?), (?))", [current_user_id, car_id])
        con.commit()
        return redirect(url_for("profile"))
        
        
    return render_template("profile.html", email = email, username = username, firstName = firstName, lastName = lastName, street = street, houseNum = houseNum, city = city, postalCode = postalCode, credit = credit, password = password, cars = cars, rentCars = [], rented = rented)

@app.route("/edit-car/<id>", methods=['GET', 'POST'])
def edit_car(id):
    print(id)
    modell = request.form['modell']
    fahrzeugtyp = request.form['fahrzeugtyp']
    hersteller = request.form['hersteller']
    preis = request.form['preis']
    startdate = request.form['startdate']
    enddate = request.form['enddate']

    with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            cur.execute("UPDATE Autos SET Hersteller=(?), Modell=(?), Fahrzeugtyp=(?), PreisProTag=(?), Startdatum=(?), Enddatum=(?) WHERE AutoID=(?)", [(hersteller), (modell), (fahrzeugtyp), (preis), (startdate), (enddate), (id)])
    con.commit()
    # TODO
    # fix the default dates and price in profile.html
    return redirect(url_for("profile"))

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
                cars = cur.execute("SELECT AutoID, Hersteller, Modell, Fahrzeugtyp, PreisProTag, Startdatum, Enddatum FROM Autos").fetchall()
        if request.method == "POST":
            #change name to rentCar-i => i = AutoID 
            with sqlite3.connect("database.sqlite") as con:
                cur = con.cursor()
                if request.form.get("filter") == "Suchen":
                    filterPlace = request.form["place"]
                    filterStartdate = request.form["startdate"]
                    filterEnddate = request.form["enddate"]
                    filterClass = request.form["carclass"]
                    filterMaxPrice = request.form["maxprice"]
                    print("Filtered Search: ", filterPlace, " ", filterStartdate, " ", filterEnddate, " ", filterClass, " ", filterMaxPrice)
                    #for i in range(cur.execute("SELECT COUNT(*) FROM Autos").fetchone()[0]):
                    matchingUser = cur.execute("SELECT UserID FROM User INNER JOIN Adresse ON Adresse.AdressID = User.Adresse WHERE Adresse.Ort == (?)", [(filterPlace)]).fetchall()              
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
                                            return render_template("findCar.html", cars = cars)
                else:
                    for i in range(len(session["matchedCars"])):
                        print(session["matchedCars"][i][0])
                        if request.form.get(str(session["matchedCars"][i][0])) == "mieten":
                            print("selected car")
                            lessor = cur.execute("SELECT User FROM Autobesitzer WHERE Auto = (?)", [(session["matchedCars"][i][0])]).fetchone()[0] #change 30 to variable
                            startDate = cur.execute("SELECT Startdatum FROM Autos WHERE AutoID = (?)", [(session["matchedCars"][i][0])]).fetchone()[0] #change 30 to variable
                            endDate = cur.execute("SELECT Enddatum FROM Autos WHERE AutoID = (?)", [(session["matchedCars"][i][0])]).fetchone()[0] #change 30 to variable
                            pricePerDay = cur.execute("SELECT PreisProTag FROM Autos WHERE AutoID = (?)", [(session["matchedCars"][i][0])]).fetchone()[0] #change 30 to variable
                            ammountDays = cur.execute("SELECT JULIANDAY(Enddatum) - JULIANDAY(Startdatum) AS difference FROM Autos WHERE AutoID = (?)", [(session["matchedCars"][i][0])]).fetchone()[0]
                            endPrice = ammountDays * pricePerDay
                            print(session["UserID"])
                            print(lessor)
                            print(endPrice)
                            print(startDate)
                            print(endDate)
                            
                            cur.execute("INSERT INTO Mietauftrag(Mieter, Vermieter, Auto, Gesamtpreis, Startdatum, Enddatum, Ueberweisungsdatum) VALUES(?, ?, ?, ?, ?, ?, ?)", ((session["UserID"]), (lessor), (session["matchedCars"][i][0]), (endPrice), (startDate), (endDate), (startDate)))
                            cur.execute("UPDATE User SET Guthaben= Guthaben - (?) WHERE UserID=(?)", [(endPrice), (session["UserID"])])
                            cur.execute("UPDATE User SET Guthaben= Guthaben + (?) WHERE UserID=(?)", [(endPrice), (lessor)])
                            con.commit()
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

if __name__ == "__main__":
    app.run()
