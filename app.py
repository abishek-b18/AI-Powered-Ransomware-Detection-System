from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = "ransomware_secret_key"

# Load Model
model = pickle.load(open("models/ransomware_model.pkl", "rb"))

# Database Connection
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create User Table
def create_tables():
    conn = get_db_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

create_tables()

# Home
@app.route("/")
def home():
    return render_template("index.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        conn.execute(
            "INSERT INTO users(username,email,password) VALUES(?,?,?)",
            (username,email,password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# Login
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email,password)
        ).fetchone()

        conn.close()

        if user:
            session["username"] = user["username"]
            return redirect("/dashboard")

    return render_template("login.html")

# Dashboard
@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["username"]
    )

# Threat Detection
@app.route("/monitor", methods=["GET","POST"])
def monitor():

    prediction = None

    if request.method == "POST":

        cpu = float(request.form["cpu"])
        memory = float(request.form["memory"])
        process = float(request.form["process"])
        file_mod = float(request.form["file_mod"])
        encryption = float(request.form["encryption"])
        network = float(request.form["network"])

        result = model.predict([[
            cpu,
            memory,
            process,
            file_mod,
            encryption,
            network
        ]])

        if result[0] == 0:
            prediction = "Safe System"
        else:
            prediction = "⚠️ Ransomware Detected"

    return render_template(
        "monitor.html",
        prediction=prediction
    )

# Reports Page
@app.route("/reports")
def reports():
    return render_template("reports.html")

# Admin Page
@app.route("/admin")
def admin():
    return render_template("admin.html")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)