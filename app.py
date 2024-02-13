# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# MySQL database setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abhi992744",
    database="wecaredb"
)
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
''')

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS help_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    disease_name VARCHAR(255) NOT NULL,
    symptoms TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# Create patients table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    disease_name VARCHAR(255) NOT NULL,
    symptomps TEXT NOT NULL,
    hospital_name VARCHAR(255) NOT NULL,
    doc_name VARCHAR(255) NOT NULL,
    expenditure FLOAT NOT NULL,
    email VARCHAR(255) NOT NULL,
    remarks TEXT,
    rating int,
    FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

conn.commit()
conn.close()

# Route for the home page (index page)
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Retrieve user details from the session
    username = session['username']

    return render_template('index.html', username=username)

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle user registration
        username = request.form['username']
        password = request.form['password']

        # Save user data to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abhi992744",
            database="wecaredb"
        )
        cursor = conn.cursor()
        
        # Check if the username is already taken
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('register.html', message='Username already taken. Please choose another.')

        # Insert user data
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))

        conn.commit()

        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        user_id = cursor.fetchone()[0]

        session['username'] = username
        session['user_id'] = user_id

        # Redirect to the login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle user login
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abhi992744",
            database="wecaredb"
            )
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['username'] = username  # Store username in session
            return redirect(url_for('index'))
        else:
            # Display an error message
            return render_template('login.html', message='Invalid username or password. Please try again.')
            
    return render_template('login.html')


# Route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



#get user id
def get_user_id(username):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abhi992744",
        database="wecaredb"
    )
    cursor = conn.cursor()

    # Get user ID based on the username
    cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
    user_id = cursor.fetchone()[0]

    conn.close()
    return user_id


if __name__ == '__main__':
    app.run(debug=True)
