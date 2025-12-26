import mysql.connector as mysql
import random
import time
from datetime import datetime

cn = mysql.connect(host="localhost", user="root", password="bakaprince", database="bank_management_cse")
cr = cn.cursor()


def login():
    try:
        acc = input("Account number: ").strip()
        pin = input("PIN: ").strip()
        cr.execute("SELECT account_no FROM accounts WHERE account_no = %s AND pin = %s", (acc, pin))
        row = cr.fetchone()
        if row:
            print("Login successful,Please wait...")
            return int(row[0])
        print("Login failed: invalid credentials")
        return None
    except Exception as e:
        print("Error during login:", e)
        return None


def generate_account_number():
    while True:
        acc_no=random.randint(10000000,99999999)
        query="select * from accounts where account_no=%s"
        values=(acc_no,)
        cr.execute(query,values)
        data=cr.fetchall()
        if len(data)==0:
            return acc_no


def register():
    name = input("Enter your name: ").strip()
    while True:
        dob = input("Enter your date of birth (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(dob, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format! Please strictly follow YYYY-MM-DD format (e.g., 1990-05-15)")
    phone = input("Enter your phone number: ").strip()
    email = input("Enter your email address: ").strip()
    acc_type = input("Enter account type (Savings/Current): ").strip()
    pin = input("Set a 4-6 digit PIN: ").strip()
    acc_no = generate_account_number()
    query = "INSERT INTO accounts (account_no, name, dob, phone, email, account_type, pin) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    values = (acc_no, name, dob, phone, email, acc_type, pin)
    cr.execute(query, values)
    cn.commit()
    print(f"Account created. Your account number is: {acc_no}")
    print("Redirecting to main menu...Please wait...")
    time.sleep(3)
    return acc_no
    