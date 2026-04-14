from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import qrcode
import os

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

        if user:
            flash("Email already exists!")
            return redirect("/register")

        db.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",(name,email,password))
        db.commit()

        flash("Registration Successful!")
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email=? AND password=?", (email,password)).fetchone()

        if user:
            session["user"] = user[1]
            return redirect("/dashboard")
        else:
            flash("Invalid credentials")

    return render_template("login.html")

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    message = ""
    qr_file = ""

    if request.method == "POST":
        source = request.form["source"]
        destination = request.form["destination"]

        # Smart Pricing
        if source == destination:
            price = 20
        elif source == "Nagpur" and destination == "Pune":
            price = 150
        else:
            price = 100

        db = get_db()
        db.execute("INSERT INTO bookings (user, source, destination, price) VALUES (?,?,?,?)",
                   (session["user"], source, destination, price))
        db.commit()

        # QR Code
        data = f"{session['user']} | {source} → {destination} | ₹{price}"
        img = qrcode.make(data)

        if not os.path.exists("static/qr"):
            os.makedirs("static/qr")

        qr_file = f"{session['user']}.png"
        img.save(f"static/qr/{qr_file}")

        message = "Pass Booked Successfully!"

    db = get_db()
    bookings = db.execute("SELECT * FROM bookings WHERE user=?", (session["user"],)).fetchall()

    return render_template("dashboard.html", user=session["user"], bookings=bookings, message=message, qr=qr_file)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)