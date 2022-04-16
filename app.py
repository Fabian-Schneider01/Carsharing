from flask import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("login.html")
def login():
    return render_template("login.html")
def register():
    return render_template("register.html")

if __name__ == '__main__':
    app.run()
