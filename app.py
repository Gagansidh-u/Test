
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import razorpay

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Razorpay setup from .env
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('games.db')
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, password_hash FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

@app.route('/')
def home():
    conn = sqlite3.connect("games.db")
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, thumbnail, price, original_price FROM games")
    games = cur.fetchall()
    conn.close()
    return render_template("index.html", games=games)

# More routes would go here...

if __name__ == "__main__":
    app.run(debug=True)
