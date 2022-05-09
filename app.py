from flask import *
import sqlite3
from models import createTabels

app = Flask(__name__)
app.secret_key = "4khJ7Ggljy"

with app.app_context():
    createTabels()

@app.route('/')
def home():
    return render_template("index.html")

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

    if session.get("UserID") is None:
        return redirect(url_for("login"))
    else:
        with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            userID = session["UserID"]
            email = cur.execute("SELECT Email from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
            username =cur.execute("SELECT Benutzername from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
            firstName = cur.execute("SELECT Vorname from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
            lastName = cur.execute("SELECT Nachname from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
            addressID = cur.execute("SELECT Adresse from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
            street = cur.execute("SELECT Straße from Adresse WHERE AdressID=(?)", [(addressID)]).fetchone()[0]
            houseNum = cur.execute("SELECT Hausnummer from Adresse WHERE AdressID=(?)", [(addressID)]).fetchone()[0]
            city = cur.execute("SELECT Ort from Adresse WHERE AdressID=(?)", [(addressID)]).fetchone()[0]
            postalCode = cur.execute("SELECT Postleitzahl from Adresse WHERE AdressID=(?)", [(addressID)]).fetchone()[0]
            credit = cur.execute("SELECT Guthaben from User WHERE UserID=(?)", [(userID)]).fetchone()[0]
        con.commit()
        with sqlite3.connect("database.sqlite") as con:
            # for displaying all the cars the user has added
            cur = con.cursor()
            userID = session["UserID"]
            cars = cur.execute("SELECT AutoID, Hersteller, Modell, Fahrzeugtyp, PreisProTag, Startdatum, Enddatum FROM User LEFT JOIN Autobesitzer ON User.UserID = Autobesitzer.User LEFT JOIN Autos ON Autobesitzer.Auto = Autos.AutoID WHERE UserID=(?)", [(userID)]).fetchall()

    car_added = None
    if request.method == 'POST':
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
            #input = cur.fetchall()
            #print(input)
        #    if len(input) > 0:
        #        print('login Success')
        #        user_found = 1
        #        return redirect(url_for('profile'))
        #    else: 
        #        print("error: user not found")
        #        user_found = 0
        con.commit()
        
        
    return render_template("profile.html", email = email, username = username, firstName = firstName, lastName = lastName, street = street, houseNum = houseNum, city = city, postalCode = postalCode, credit = credit, cars = cars)

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

@app.route("/findCar")
def findCar():
    if session.get("UserID") is None:
        return redirect(url_for("login"))
    return render_template("findCar.html")

if __name__ == "__main__":
    app.run()
