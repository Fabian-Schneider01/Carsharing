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

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/findCar')
def findCar():
    return render_template('findCar.html')

if __name__ == '__main__':
    app.run()
