from flask import *
import sqlite3
from models import createTabels

app = Flask(__name__)

current_user_id = None

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    user_found = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            cur.execute("SELECT UserID from User WHERE Email=(?) AND Passwort=(?)", [(email), (password)])
            input = cur.fetchall()
            if len(input) > 0:
                print('login Success')
                user_found = 1
                return redirect(url_for('profile'))
            else: 
                print("error: user not found")
                user_found = 0
                
    return render_template("login.html", user_found = user_found)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    return render_template("register.html")

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
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
        car_id = 456
        global current_user_id
        current_user_id = 1 # for testing purposes
        with sqlite3.connect("database.sqlite") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Autos VALUES((?), (?), (?), (?), (?), (?), (?))", [(car_id), (hersteller), (modell), (fahrzeugtyp), (preis), (startdate), (enddate)])
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
        
        car_added = 1
    return render_template('profile.html', car_added = car_added)

@app.route('/findCar')
def findCar():
    return render_template('findCar.html')

if __name__ == '__main__':
    createTabels()
    app.run()
