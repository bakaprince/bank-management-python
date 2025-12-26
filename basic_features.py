import mysql.connector as mysql
from datetime import datetime, timedelta
import datetime as dt
cn = mysql.connect(host="localhost", user="root", password="bakaprince", database="bank_management_cse")
cr = cn.cursor()


def deposit(account_no, amount):
    query = "INSERT INTO transactions (account_no, type, amount) VALUES (%s, %s, %s)"
    values = (account_no, "deposit", amount)
    cr.execute(query, values)
    cr.execute("UPDATE accounts SET balance = balance + %s WHERE account_no = %s", (amount, account_no))
    cn.commit()


def withdraw(account_no, amount):
    bal = check_balance(account_no)
    if amount > bal:
        raise ValueError("Insufficient Balance")
    query = "INSERT INTO transactions (account_no, type, amount) VALUES (%s, %s, %s)"
    values = (account_no, "withdraw", amount)
    cr.execute(query, values)
    cr.execute("UPDATE accounts SET balance = balance - %s WHERE account_no = %s", (amount, account_no))
    cn.commit()

def check_balance(account_no):
    cr.execute("SELECT balance FROM accounts WHERE account_no = %s", (account_no,))
    row = cr.fetchone()
    if row is None:
        raise ValueError(f"Account {account_no} not found")
    return float(row[0])

def transfer_funds(from_account):
    to_account=int(input("Enter recipient account number: ").strip())
    amount=float(input("Enter amount to transfer: ").strip())
    bal = check_balance(from_account)
    if amount > bal:
        raise ValueError("Insufficient Balance")
    query = "INSERT INTO transactions (account_no, type, amount) VALUES (%s, %s, %s)"
    values = (from_account, "transfer_out", amount)
    cr.execute(query, values)
    cr.execute("UPDATE accounts SET balance = balance - %s WHERE account_no = %s", (amount, from_account))
    query = "INSERT INTO transactions (account_no, type, amount) VALUES (%s, %s, %s)"
    values = (to_account, "transfer_in", amount)
    cr.execute(query, values)
    cr.execute("UPDATE accounts SET balance = balance + %s WHERE account_no = %s", (amount, to_account))
    cn.commit()


def view_transaction_history(account_no=None, limit=100):
    if account_no is None:
        cr.execute("SELECT id, account_no, type, amount, date FROM transactions ORDER BY date DESC LIMIT %s", (limit,))
    else:
        cr.execute("SELECT id, account_no, type, amount, date FROM transactions WHERE account_no = %s ORDER BY date DESC LIMIT %s", (account_no, limit))
    return cr.fetchall()


def check_loan_eligibility(account_no):
    query = "SELECT balance, created_at FROM accounts WHERE account_no = %s"
    cr.execute(query, (account_no,))
    row = cr.fetchone()
    if not row:
        return "Account does not exist."
    balance, created_at = row
    account_age_days = (dt.datetime.now() - created_at).days
    if account_age_days < 180:
        return "Loan Rejected: Account must be at least 180 days old."

    if balance < 5000:
        return "Loan Rejected: Minimum balance required is 5000."
    query = """SELECT date FROM transactions WHERE account_no = %s ORDER BY date DESC LIMIT 1"""
    cr.execute(query, (account_no,))
    tx = cr.fetchone()
    if not tx:
        return "Loan Rejected: At least one transaction must exist."
    last_tx_date = tx[0]
    days_since_last_tx = (dt.datetime.now() - last_tx_date).days
    if days_since_last_tx < 30:
        return "Loan Rejected: Last transaction must be at least 30 days old."
    return "Loan Approved: Eligible for loan."


def report_wrongful_transaction(transaction_id, account_no, reason):
    query = "SELECT id, flag FROM transactions WHERE id = %s AND account_no = %s"
    cr.execute(query, (transaction_id, account_no))
    row = cr.fetchone()
    if not row:
        return "Invalid transaction for this account."
    tid, flag = row
    if flag != "OK":
        return "This transaction has already been reported."
    query = "UPDATE transactions SET flag = 'Flagged', type = %s WHERE id = %s"
    cr.execute(query, (reason[:15], transaction_id))
    return "Wrongful transaction reported successfully."

def update_account_details(account_no, name=None, phone=None, email=None, address=None):
    if name:
        query = "UPDATE accounts SET name = %s WHERE account_no = %s"
        cr.execute(query, (name, account_no))

    if phone:
        query = "UPDATE accounts SET phone = %s WHERE account_no = %s"
        cr.execute(query, (phone, account_no))

    if email:
        query = "UPDATE accounts SET email = %s WHERE account_no = %s"
        cr.execute(query, (email, account_no))
    if address:
        query = "UPDATE kyc SET address = %s WHERE account_no = %s"
        cr.execute(query, (address, account_no))
    cn.commit()
    return "Account details updated successfully."

def check_kyc_status(account_no):
    query = "SELECT status FROM kyc WHERE account_no = %s"
    cr.execute(query, (account_no,))
    row = cr.fetchone()
    if row is None:
        return "No KYC record found for this account."
    return row[0]