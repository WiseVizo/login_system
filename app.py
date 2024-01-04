from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('users.db')
    return db

# Close the database connection at the end of the request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Route for the home page (login form)
@app.route('/')
def login_form():
    return render_template('login.html')

# Route to handle login attempts
@app.route('/login', methods=['POST'])
def login():
    db = get_db()
    cursor = db.cursor()

    username = request.form['username']
    password = request.form['password']
    
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    
    if user:
        # session['logged_in'] = True
        return 'Logged in successfully!'
    else:
        return 'Invalid credentials. Please try again.'


# Route to render the registration form
@app.route('/register-form')
def register_form():
    return render_template('register.html')

# Route to handle user registration
@app.route('/register', methods=['POST'])
def register_user():
    db = get_db()
    cursor = db.cursor()

    username = request.form['username']
    password = request.form['password']
    
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    db.commit()
    
    return 'User registered successfully!'

if __name__ == '__main__':
    app.run(debug=True)
