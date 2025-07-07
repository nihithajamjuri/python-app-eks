import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = 'finance.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('Income', 'Expense')),
            username TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_user_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    password_hash = generate_password_hash(password)
    try:
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_user_exists(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def authenticate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user[2], password):
        return user
    return None

def insert_transaction(date, category, amount, type_, username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO transactions (date, category, amount, type, username) VALUES (?, ?, ?, ?, ?)",
        (date, category, amount, type_, username)
    )
    conn.commit()
    conn.close()

def fetch_user_transactions(username, from_date=None, to_date=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    query = "SELECT date, category, amount, type FROM transactions WHERE username = ?"
    params = [username]

    if from_date:
        query += " AND date >= ?"
        params.append(from_date)
    if to_date:
        query += " AND date <= ?"
        params.append(to_date)

    query += " ORDER BY date DESC"

    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    print(rows)
    return rows


def get_totals(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE username = ? AND type = 'Income'", (username,))
    income = c.fetchone()[0]

    c.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE username = ? AND type = 'Expense'", (username,))
    expense = c.fetchone()[0]

    conn.close()
    return income, expense

def get_expense_summary_by_category(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT category, SUM(amount) 
        FROM transactions 
        WHERE username = ? AND type = 'Expense' 
        GROUP BY category
    ''', (username,))
    rows = c.fetchall()
    print(rows)
    conn.close()
    return rows
