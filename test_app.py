import unittest
from app import app, get_db

class TestApp(unittest.TestCase):

    def setUp(self):
        # Set up a test client and a testing database
        app.testing = True
        self.app = app.test_client()
        with app.app_context():
            get_db()

    def tearDown(self):
        # Clean up any resources used in the tests
        pass

    def test_login(self):
        # Simulate a successful login
        response = self.app.post('/login', data=dict(
            username='vizo',  # replace with a valid username
            password='vizo',  # replace with a valid password
            email='cyacyan18@gmail.com'  # replace with a valid email
        ), follow_redirects=True)

        print(f"response-> {response}")
        print(f"data->{response.data}")

        # Check if the login was successful
        self.assertIn(b'Welcome', response.data) # checks if welcome msg was present in response data
        self.assertEqual(response.status_code, 200)

        # Simulate a failed login (invalid credentials)
        response = self.app.post('/login', data=dict(
            username='invalid_username',
            password='invalid_password',
            email='invalid_email@gmail.com'
        ), follow_redirects=True)

        # Check if the login failed
        self.assertIn(b'Invalid credentials', response.data)
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        # Simulate 1st step of successful registration
        response = self.app.post('/register', data=dict(
            username='vizo1',  # replace with a valid username
            password='vizo',  # replace with a valid password
            email='cyacyan18@gmail.com'  # replace with a valid email
        ), follow_redirects=True)

        print(f"data->{response.data}")

        self.assertIn(b'OTP Verification', response.data) # check if opt verification showed up
        self.assertEqual(response.status_code, 200)

        # After successful registration, get OTP from session
        with self.app as c:
            with c.session_transaction() as sess:
                otp = sess.get('otp')

        # Simulate submitting the OTP verification form
        response = self.app.post('/verify', data=dict(
            otp=otp
        ), follow_redirects=True)

    # Check if the response indicates successful verification
        self.assertIn(b'Registered successfully!', response.data)
        self.assertEqual(response.status_code, 200)

    # Attempt OTP verification with an incorrect OTP
        response = self.app.post('/verify', data=dict(
            otp='12345'  # Replace with an incorrect OTP
         ), follow_redirects=True)

    # Check if the application responds appropriately (e.g., displays an error message)
        self.assertIn(b'Invalid OTP', response.data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
