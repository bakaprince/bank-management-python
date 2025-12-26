from login_register import login, register
import basic_features as bf
import time

def home(acc_no):
    print("\n" + "." * 50)
    print(":                  BANK SYSTEM                   :")
    print("." * 50)
    print(": 1. Check Balance                               :")
    print(": 2. Withdraw                                    :")
    print(": 3. Deposit                                     :")
    print(": 4. Transfer Funds                              :")
    print(": 5. View Transaction History                    :")
    print(": 6. Loan Eligibility                            :")
    print(": 7. Report Wrongful Transaction                 :")
    print(": 8. Update Account Details                      :")
    print(": 9. KYC Status                                  :")
    print(": 10. Logout                                     :")
    print("." * 50)
    n = int(input("Enter choice (1-10): ").strip())

    if n == 1:
        bal = bf.check_balance(acc_no)
        print(f"Balance: {bal}")
    elif n == 2:
        bf.withdraw(acc_no, float(input("Enter amount to withdraw: ").strip()))
        print("Withdrawal successful.")
    elif n == 3:
        bf.deposit(acc_no, float(input("Enter amount to deposit: ").strip()))
        print("Deposit successful.")
    elif n == 4:
        bf.transfer_funds(acc_no)
        print("Transfer completed.")
    elif n == 5:
        history = bf.view_transaction_history(acc_no)
        for record in history:
            print(record)
    elif n == 6:
        eligibility = bf.check_loan_eligibility(acc_no)
        print(eligibility)
    elif n == 7:
        transaction_id = int(input("Enter Transaction ID to report: ").strip())
        reason = input("Enter reason for reporting: ").strip()
        report = bf.report_wrongful_transaction(acc_no, transaction_id, reason)
        if report: 
            print("Transaction reported successfully.")
        else:
            print("Failed to report transaction.") 
    elif n == 8:
        print("Update Account Details")
        print("Leave blank to skip a field")
        name = input("Enter new name (or leave blank): ").strip()
        phone = input("Enter new phone (or leave blank): ").strip()
        email = input("Enter new email (or leave blank): ").strip()
        address = input("Enter new address (or leave blank): ").strip()
        result = bf.update_account_details(acc_no, name if name else None, phone if phone else None, email if email else None, address if address else None)
        print(result)

    elif n == 9:
        status = bf.check_kyc_status(acc_no)
        print(f"KYC Status: {status}")
    elif n == 10:
        print("Logging out...")
        start_menu()
        return
    else:
        print("Invalid choice, please use only 1-10")
    print("Loading Options...Please wait..")
    time.sleep(1)
    control_menu(acc_no)


def control_menu(acc_no):
    print("\n" + "." * 50)
    print(":                  BANK SYSTEM                   :")
    print("." * 50)
    print(": 1. Go Back                                     :")
    print(": 2. Exit                                        :")
    print("." * 50)
    n = int(input("Enter choice (1-2): ").strip())
    if n == 1:
        home(acc_no)
    elif n == 2:
        print("Exiting... Goodbye!")
    else:
        print("Invalid choice....Use only 1 or 2",control_menu(acc_no))
        time.sleep(2)
        exit()


def start_menu():
    print("\n" + "." * 50)
    print(":                  BANK SYSTEM                   :")
    print("." * 50)
    print(": 1. Create Account                              :")
    print(": 2. Login                                       :")
    print("." * 50)
    n = int(input("Enter choice (1-2): ").strip())
    if n == 1:
        acc_no = register()
        time.sleep(1)
        if acc_no is not None:
            home(acc_no)
    else:
        acc_no = login()
        time.sleep(1)
        if acc_no is not None:
            home(acc_no)
        else:
            print("Returning to start menu...Please wait...")
            time.sleep(1)
            start_menu()

if __name__ == "__main__":
    start_menu()