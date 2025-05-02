import tkinter as tk
import mysql.connector

def login(main_cn, main_cr):
    account_no = entry_account_no.get()
    password = entry_password.get()
    login_mode = var.get()
    # SQL query to check if the user ID and password match for the given login mode
    query = """
    SELECT COUNT(*) FROM bankinfo
    WHERE account_no = %s AND password = %s AND login_mode = %s
    """
    values = (account_no, password, login_mode)
    main_cr.execute(query, values)
    result = main_cr.fetchone()[0]
    if result == 1:
        # Login successful
        print("Login successful!")
        window.destroy()
        return login_mode, account_no
    else:
        # Login failed
        print("Login failed. Please check your credentials.")
        return None, None

def run_login(main_cn, main_cr):
    global window, entry_account_no, entry_password, var
    window = tk.Tk()
    window.title("Login Form")
    window.geometry("1000x300")
    window.configure(bg='White')

    l = tk.Label(window, text='Welcome to Gareeb Bank', font=('Algerian', 32), bg='White', fg='Black')
    l.grid(row=2, column=2)

    # Create labels and entry fields
    label_account_no = tk.Label(window, text="Account No:")
    label_account_no.grid(row=4, column=1)
    entry_account_no = tk.Entry(window)
    entry_account_no.grid(row=4, column=2)

    label_password = tk.Label(window, text="Password:")
    label_password.grid(row=5, column=1)
    entry_password = tk.Entry(window, show="*")
    entry_password.grid(row=5, column=2)

    # Create dropdown menu for login mode
    label_login_mode = tk.Label(window, text="Login Mode:")
    label_login_mode.grid(row=10, column=1)
    var = tk.StringVar()
    dropdown_login_mode = tk.OptionMenu(window, var, "Employee", "User")
    dropdown_login_mode.grid(row=10, column=2)

    # Create login button
    button_login = tk.Button(window, text="Login", command=lambda: [set_login_details(main_cn, main_cr)])
    button_login.grid(row=12, column=2)

    window.mainloop()

def set_login_details(main_cn, main_cr):
    global login_mode, account_no
    login_mode, account_no = login(main_cn, main_cr)
    if login_mode:
        window.quit()

def get_login_details():
    global login_mode, account_no
    return login_mode, account_no

login_mode = None
account_no = None
