import matplotlib.pyplot as plt
import mysql.connector as mysql
from banklogin import run_login, get_login_details

cn = mysql.connect(host='Localhost', user='root', passwd='lps123', database='GareebBank')
cr = cn.cursor()

def user_interface(account_no):
    while True:
        print('Welcome User', account_no)
        ch = int(input('''Enter 1 To Check Current Balance
Enter 2 To Transfer Money
Enter 3 To Check KYC Status 
Enter 0 To Exit
Your Choice='''))

        try:
            if ch == 1:
                q = "SELECT current_balance FROM user_info WHERE account_no = %s"
                cr.execute(q, (account_no,))
                b = cr.fetchone()
                print('₹', b[0])

            elif ch == 2:
                c = int(input("Enter Receiver's Account No.: "))
                p = int(input('Enter Amount To Be Transferred: '))
                q1 = "UPDATE user_info SET current_balance = current_balance + %s WHERE account_no = %s"
                q2 = "UPDATE user_info SET current_balance = current_balance - %s WHERE account_no = %s"
                cr.execute(q1, (p, c))
                cr.execute(q2, (p, account_no))
                print('amount transferred successfull')
                cn.commit()

            elif ch == 3:
                q1 = "SELECT KYC_status FROM user_info WHERE account_no = %s"
                cr.execute(q1, (account_no,))
                b = cr.fetchone()
                print('Your KYC Status is', b[0])
            elif ch == 0:
                print("Exiting User Interface")
                break

            else:
                print("Invalid choice. Please enter a number between 0 and 3.")
        
        except:
            cn.close()

def emp_interface():
    while True:
        print('Welcome Employee')
        ch = int(input('''Enter 1 To Insert New User
Enter 2 Update Info
Enter 3 Delete A User
Enter 4 Display All Records
Enter 5 Search A Record
Enter 6 View KYC Status Graph
Enter 0 To Exit
Your Choice='''))

        try:
            if ch == 1:
                account_no = int(input('Enter account_no: '))
                name = input('Enter Name: ')
                phoneno = input('Enter PhoneNo: ')
                current_balance = float(input('Enter current_balance: '))
                kyc_status = input('Enter kyc_status: ')
                password=input('Enter New Password')
                q = "INSERT INTO user_info (account_no, Name, PhoneNo, current_balance, KYC_status) VALUES (%s, %s, %s, %s, %s)"
                q2= "INSERT INTO bankinfo(account_no,password,login_mode) VALUES (%s, %s, %s)"
                values1=(account_no,password,'User')
                values = (account_no, name, phoneno, current_balance, kyc_status)
                cr.execute(q, values)
                cr.execute(q2,values1)
                cn.commit()
                print('Task Completed Successfully')

            elif ch == 2:
                w = input('Enter the field to update: ')
                n = input('Enter the new value: ')
                account_no = input('Enter the account number to update: ')
                q = "UPDATE user_info SET {} = '{}' WHERE account_no = {};".format(w, n, account_no)
                cr.execute(q)
                cn.commit()
                print('Task Completed Successfully')

            elif ch == 3:
                account_no = int(input('Enter the account number to delete: '))
                q = "DELETE FROM user_info WHERE account_no = {};".format(account_no)
                cr.execute(q)
                cn.commit()
                print('Task Completed Successfully')

            elif ch == 4:
                q = "SELECT * FROM user_info"
                cr.execute(q)
                a = cr.fetchall()
                for record in a:
                    print(record)

            elif ch == 5:
                account_no = int(input('Enter account number to search for: '))
                q = "SELECT * FROM user_info WHERE account_no = {};".format(account_no)
                cr.execute(q)
                b = cr.fetchall()
                print(b)

            elif ch == 6:
                plot_kyc_status_graph()

            elif ch == 0:
                print("Exiting Employee Interface")
                break

            else:
                print("Invalid choice. Please enter a number between 0 and 6.")
        
        except :
            cn.close()

def plot_kyc_status_graph():
    q = "SELECT KYC_status, COUNT(*) FROM user_info GROUP BY KYC_status"
    cr.execute(q)
    result = cr.fetchall()

    statuses = [row[0] for row in result]
    counts = [row[1] for row in result]

    plt.figure(figsize=(10, 5))
    plt.bar(statuses, counts, color=['green', 'red'])
    plt.title('KYC Status Distribution')
    plt.xlabel('KYC Status')
    plt.ylabel('Number of Users')
    plt.grid(True)
    plt.show()

def menu():
    if __name__ == "__main__":
        run_login(cn, cr)
        login_mode, account_no = get_login_details()

        if login_mode == "Employee":
            emp_interface()
        elif login_mode == "User":
            user_interface(account_no)
menu()

