from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'app.OsJoMeMi'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create_account', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        birthdate = request.form['birthdate']
        country = request.form['country']

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE Email = ?", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            return render_template("register.html", error="Email already registered")
        cursor.execute("INSERT INTO users (Name, Surname, Birthdate, Country, Email, Password, Approved) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, surname, birthdate, country, email, hashed_password, 0))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route('/goals_and_services')
def goalsServices():
    return render_template("goals_services.html")

@app.route('/next_mission')
def nextMission():
    return render_template("next_mission.html")

@app.route('/donations')
def donations():
    return render_template("donations.html")

@app.route('/contact_us')
def contactUs():
    return render_template("contact_us.html")

@app.route('/photo_videos')
def photoVideos():
    return render_template("photo_videos.html")

def getMissions():
    conn = sqlite3.connect('database.db')  # Connect to the database
    cursor = conn.cursor()
    
    # Execute the query to fetch all missions
    cursor.execute("SELECT id, Name, Date_to_begin, Date_to_end, Itinerary, Cost, mission_cost_description, Contact FROM missions")
    
    # Fetch all rows from the executed query
    missions = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return missions

@app.route('/terms_and_conditions')
def termsAndConditions():
    return render_template('terms.html')

@app.route('/about_peru')
def aboutPeru():
    return render_template('about_peru.html')

@app.route('/previous_missions')
def previousMissions():
    listMissions = getMissions()
    return render_template('previous_missions.html', missions=listMissions)

@app.route('/login_account', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE Email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[7]):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Elimina el ID del usuario de la sesión
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
