from flask import Flask, render_template, request, g, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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
        session['logged_in'] = True  # Set session after successful login
        session['username'] = username  # Store username in session
        return redirect(url_for('index'))  # Redirect to index page after login also it takes function name not the route name
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

@app.route('/index')
def index():
    # Code to render index.html
    return render_template('index.html')

# Route to handle logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)  # Clear username from session if needed
    return redirect(url_for('login_form'))  # Redirect to login form after logout

if __name__ == '__main__':
    app.run(debug=True)
