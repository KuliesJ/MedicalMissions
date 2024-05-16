from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create_account', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surename = request.form['surename']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        birthdate = request.form['birthdate']
        country = request.form['country']

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (Name, Surename, Birthdate, Country, Email, Password, Approved) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, surename, birthdate, country, email, password, 0))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template("register.html")


@app.route('/login_account', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            # User found, perform login logic
            return redirect(url_for('index'))
        else:
            # User not found or password incorrect, handle accordingly
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
