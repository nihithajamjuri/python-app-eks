from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import (
    init_db, 
    create_user_table,
    register_user, 
    authenticate_user, 
    insert_transaction,
    fetch_user_transactions, 
    get_totals, 
    get_expense_summary_by_category,
    check_user_exists
)
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this in production

# Initialize DB and user table
init_db()
create_user_table()

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']

    if not check_user_exists(username):
        session.pop('user', None)
        return redirect(url_for('login'))

    income, expense = get_totals(username)
    balance = income - expense
    return render_template('index.html', income=income, expense=expense, balance=balance)

@app.route('/add', methods=['POST'])
def add_transaction():
    if 'user' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))

    try:
        date = request.form['date']
        category = request.form['category']
        amount = float(request.form['amount'])
        raw_type = request.form['type'].strip().lower()
        if raw_type == 'income':
            type_ = 'Income'
        elif raw_type == 'expense':
            type_ = 'Expense'
        else:
            flash("Transaction type must be Income or Expense.", "danger")
            return redirect(url_for('index'))

        username = session['user']

        if not date or not category:
            flash("Date and category are required.", "danger")
            return redirect(url_for('index'))

        if amount <= 0:
            flash("Amount must be positive.", "danger")
            return redirect(url_for('index'))

        if type_ not in ('Income', 'Expense'):
            flash("Transaction type must be Income or Expense.", "danger")
            return redirect(url_for('index'))

        insert_transaction(date, category, amount, type_, username)
        flash("Transaction added successfully.", "success")
        print(f"Received date: {date}, category: {category}, amount: {amount}, type: {type_}, username: {username}")

        return redirect(url_for('index'))

    except ValueError:
        flash("Amount must be a valid number.", "danger")
        return redirect(url_for('index'))
    except Exception as e:
        print("Error in add_transaction:", e)
        flash("An error occurred while adding the transaction.", "danger")
        return redirect(url_for('index'))

@app.route('/reports', methods=['GET', 'POST'])
def reports():
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')

    transactions = fetch_user_transactions(username, from_date, to_date)
    print(transactions)
    return render_template('reports.html', transactions=transactions, from_date=from_date, to_date=to_date)

@app.route('/chart')
def show_chart():
    if 'user' not in session:
        return redirect(url_for('login'))

    username = session['user']

    try:
        data = get_expense_summary_by_category(username)
        if not data:
            flash("No data found to generate the chart.", "warning")
            return redirect(url_for('index'))

        categories = [row[0] for row in data if row[0]]
        amounts = [float(row[1]) for row in data if row[1] is not None]

        fig = go.Figure(data=[go.Pie(labels=categories, values=amounts, hole=0.4)])
        fig.update_layout(title_text="Expenses by Category")
        chart_html = pio.to_html(fig, full_html=False)

        return render_template('chart.html', chart_html=chart_html)

    except Exception as e:
        print("Error generating chart:", e)
        flash("An error occurred while generating the chart.", "danger")
        return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            flash("Signup successful. Please login.", "success")
            return redirect(url_for('login'))
        else:
            flash("Username already exists.", "danger")
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            session['user'] = user[1]
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password.", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
