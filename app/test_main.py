import unittest
from main import app
import sqlite3
import uuid

DB_NAME = 'finance.db'

class MainAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.username = f'testuser_{uuid.uuid4().hex[:6]}'
        self.password = 'testpass123'
        self._reset_test_db()

    def _reset_test_db(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("DELETE FROM transactions")
        c.execute("DELETE FROM users")
        conn.commit()
        conn.close()

    def test_signup_and_login(self):
        # Signup
        response = self.client.post('/signup', data={
            'username': self.username,
            'password': self.password
        }, follow_redirects=True)
        self.assertIn(b'Signup successful', response.data)

        # Login
        response = self.client.post('/login', data={
            'username': self.username,
            'password': self.password
        }, follow_redirects=True)
        self.assertIn(b'Login successful', response.data)

    def test_add_transaction(self):
        self.test_signup_and_login()  # login as a new user

        response = self.client.post('/add', data={
            'date': '2025-01-01',
            'category': 'Salary',
            'amount': '1000',
            'type': 'Income'
        }, follow_redirects=True)
        self.assertIn(b'Transaction added successfully', response.data)

    def test_chart(self):
        self.test_signup_and_login()

        # Add an expense transaction (needed for chart)
        response = self.client.post('/add', data={
            'date': '2025-01-01',
            'category': 'Food',
            'amount': '50',
            'type': 'Expense'
        }, follow_redirects=True)
        self.assertIn(b'Transaction added successfully', response.data)

        # Now test the chart route
        response = self.client.get('/chart', follow_redirects=True)
        self.assertIn(b'Expenses by Category', response.data)


    def test_logout(self):
        self.test_signup_and_login()

        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Logged out successfully', response.data)


if __name__ == '__main__':
    unittest.main()
