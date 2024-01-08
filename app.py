from flask import Flask, render_template, request, g, session, redirect, url_for
from flask_bcrypt import Bcrypt
import sqlite3
from flask_mail import Mail, Message
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
bcrypt = Bcrypt(app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # Use SSL/TLS
app.config['MAIL_USERNAME'] = 'mecoc1011@gmail.com' # use ur gmail
app.config['MAIL_PASSWORD'] = 'idef tvaq vkvx troh'  # App password generated for Gmail. search for app passwords in security section of gmail 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('users.db')
    return db


# Function to send an email
def send_email(subject, sender, recipients, body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = body
    mail.send(msg)

# Function to generate a random 6-digit OTP
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    return otp

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

@app.route('/login', methods=['POST'])
def login():
    db = get_db()
    cursor = db.cursor()

    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    cursor.execute('SELECT * FROM users WHERE username = ? AND email = ?', (username, email))

    user = cursor.fetchone()
    
    if user:
        stored_hashed_password = user[2]  # Fetch the stored hashed password from the database
        if bcrypt.check_password_hash(stored_hashed_password, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
    
    return 'Invalid credentials. Please try again.'


# Route to render the registration form
@app.route('/register-form')
def register_form():
    return render_template('register.html')

# Route to handle user registration
@app.route('/register', methods=['POST'])
def register_user():
    # db = get_db()
    # cursor = db.cursor()

    username = request.form['username']
    password = request.form['password']
    email = request.form['email']  
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    # print(f"from register:{password} -> {hashed_password}")
    print(f"register, user->{username} email-> {email}")
    session['username'] = username
    session["email"] = email
    session["hashed_password"] = hashed_password
    

     # Generate OTP
    otp = generate_otp()

    # Save OTP in session
    session['otp'] = otp

    # Send OTP to the user's email
    subject = "Verification Code for Vizo's page"
    body = f'Your verification code is: {otp}'
    

    
    sender = 'mecoc1011@gmail.com'
    recipients = [email]  # Replace with the recipient's email address

    
    send_email(subject, sender, recipients, body)
    
    return redirect(url_for('verify'))




# Route for OTP verification
@app.route('/verify', methods=['GET', 'POST'])
def verify():


    if request.method == 'POST':

        db = get_db()
        cursor = db.cursor()

        entered_otp = request.form.get('otp')
        stored_otp = session.get('otp')

        # Check if the entered OTP is '0000' (replace with actual OTP validation logic)
        if entered_otp == stored_otp:
            username = session.get('username')
            email = session.get('email')
            hashed_password = session.get('hashed_password')
            print(f"user->{username} email-> {email}")
            # Insert into the database
            cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, hashed_password, email))

            db.commit()

            return 'Registered successfully!'  # Redirect or render success page
        else:
            return 'Invalid OTP. Please try again.'

    return render_template('verify.html')

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
    