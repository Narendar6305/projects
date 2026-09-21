import random
from datetime import datetime

# Database to store all accounts
accounts = {}

def create_account():
    print("\n  CREATE BANK ACCOUNT  ")
    name = input("Enter your full name: ").strip()
    phone = input("Enter your phone number: ").strip()

    # Simple validation for phone number
    if not phone.isdigit() or len(phone) < 10:
        print("Invalid phone number, Please try again.")
        return

    pin = input("Create a 4-digit PIN: ").strip()
    if not pin.isdigit() or len(pin) != 4:
        print("PIN must be exactly 4 digits, Please try again.")
        return

    # Generate a unique 12-digit account number
    while True:
        acc_number = random.randint(100000000000, 999999999999)
        if acc_number not in accounts:
            break

    # Initialize account data
    accounts[acc_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "history": []
    }

    print("\n Account created successfully!")
    print(f" Your Account Number is: {acc_number}")
    print("Please keep your Account Number and PIN secure.")

def login():
    print("\n LOGIN ")
    try:
        acc_number = int(input("Enter Account Number: "))
    except ValueError:
        print("Invalid input, Account number must be numeric.")
        return None

    pin = input("Enter PIN: ").strip()

    if acc_number in accounts and accounts[acc_number]["pin"] == pin:
        print(f"\n Login successful! Welcome, {accounts[acc_number]['name']}.")
        return acc_number
    else:
        print(" Invalid Account Number or PIN.")
        return None

def check_balance(acc_number):
    balance = accounts[acc_number]["balance"]
    print(f"\n Current Account Balance: ${balance:.2f}")

def deposit(acc_number):
    print("\n  DEPOSIT MONEY  ")
    try:
        amount = float(input("Enter amount to deposit: "))
    except ValueError:
        print(" Invalid amount.")
        return

    if amount <= 0:
        print(" Deposit amount must be greater than zero.")
        return

    accounts[acc_number]["balance"] += amount
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = f"[{timestamp}] Deposited: +${amount:.2f}"
    accounts[acc_number]["history"].append(record)

    print(f" Successfully deposited {amount:.2f}.")
    check_balance(acc_number)

def withdraw(acc_number):
    print("\n  WITHDRAW MONEY  ")
    try:
        amount = float(input("Enter amount to withdraw: "))
    except ValueError:
        print(" Invalid amount")
        return

    if amount <= 0:
        print(" Withdrawal amount must be greater than zero")
        return

    if amount > accounts[acc_number]["balance"]:
        print(" Insufficient balance!")
        return

    accounts[acc_number]["balance"] -= amount
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = f"[{timestamp}] Withdrew: -${amount:.2f}"
    accounts[acc_number]["history"].append(record)

    print(f" Successfully withdrew ${amount:.2f}.")
    check_balance(acc_number)

def transfer(acc_number):
    print("\n TRANSFER MONEY ")
    try:
        receiver_acc = int(input("Enter receiver's Account Number: "))
    except ValueError:
        print(" Invalid account number format.")
        return

    if receiver_acc not in accounts:
        print(" Receiver account does not exist.")
        return

    if receiver_acc == acc_number:
        print(" You cannot transfer money to your own account")
        return

    try:
        amount = float(input("Enter amount to transfer: "))
    except ValueError:
        print(" Invalid amount")
        return

    if amount <= 0:
        print(" Transfer amount must be greater than zero")
        return

    if amount > accounts[acc_number]["balance"]:
        print(" Insufficient balance for this transfer")
        return

    # Deduct from sender
    accounts[acc_number]["balance"] -= amount
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sender_record = f"[{timestamp}] Transferred {amount:.2f} to Account {receiver_acc}"
    accounts[acc_number]["history"].append(sender_record)

    # Add to receiver
    accounts[receiver_acc]["balance"] += amount
    receiver_record = f"[{timestamp}] Received {amount:.2f} from Account {acc_number}"
    accounts[receiver_acc]["history"].append(receiver_record)

    print(f" Successfully transferred {amount:.2f} to Account {receiver_acc}.")
    check_balance(acc_number)

def view_history(acc_number):
    print("\n TRANSACTION HISTORY ")
    history = accounts[acc_number]["history"]
    if not history:
        print("No transactions found.")
    else:
        for index, record in enumerate(history, 1):
            print(f"{index}. {record}")

def change_pin(acc_number):
    print("\n CHANGE PIN ")
    old_pin = input("Enter current PIN: ").strip()

    if accounts[acc_number]["pin"] != old_pin:
        print(" Incorrect current PIN.")
        return

    new_pin = input("Enter new 4-digit PIN: ").strip()
    if not new_pin.isdigit() or len(new_pin) != 4:
        print(" PIN must be exactly 4 digits")
        return

    confirm_pin = input("Confirm new 4-digit PIN: ").strip()
    if new_pin != confirm_pin:
        print(" PINs do not match. Try again")
        return

    accounts[acc_number]["pin"] = new_pin
    print(" PIN changed successfully!")

def account_menu(acc_number):
    while True:
        print("    ACCOUNT MENU    ")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            check_balance(acc_number)
        elif choice == '2':
            deposit(acc_number)
        elif choice == '3':
            withdraw(acc_number)
        elif choice == '4':
            transfer(acc_number)
        elif choice == '5':
            view_history(acc_number)
        elif choice == '6':
            change_pin(acc_number)
        elif choice == '7':
            print("\n Logging out... Returning to Main Menu.")
            break
        else:
            print(" Invalid choice Please select between 1 and 7.")

def main():
    while True:
        print("   BANKING SYSTEM   ")
        print("1. Create Bank Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            create_account()
        elif choice == '2':
            acc_number = login()
            if acc_number is not None:
                account_menu(acc_number)
        elif choice == '3':
            print("\nThank you for using the Banking System ")
            break
        else:
            print(" Invalid choice. Please choose 1, 2, or 3.")

# Program entry point
if __name__ == "__main__":
    main()