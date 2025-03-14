import csv
import datetime
from simple_term_menu import TerminalMenu
import sys
from termcolor import colored, cprint

accounts = []
current_user = {}


class Account:
    len_account = 0

    def __init__(self, account_id=0, first_name=None, last_name=None, password=None, balance_checking=0,
                 balance_savings=0, active=True):
        global accounts
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.balance_checking = balance_checking
        self.balance_savings = balance_savings
        self.active = active
        with open('bank.csv', mode='r', newline='', encoding="utf-8") as read_file:
            reader = csv.DictReader(read_file)
            for row in reader:
                accounts.append(row)
        Account.len_account = len(accounts)

    def create(self):
        if self.account_id == 0 and self.len_account == 0:
            self.account_id = 1001
        else:
            self.account_id = int(accounts[-1]["account_id"]) + 1
        list_of_values = {
            "account_id": self.account_id, "first_name": self.first_name, "last_name": self.last_name,
            "password": self.password, "balance_checking": float(self.balance_checking),
            "balance_savings": float(self.balance_savings), "active": self.active}

        with open('bank.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings",
                          "active"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(list_of_values)
        return list_of_values

    #The naming is weird, I have no clue what this is supposed to do by the name
    def user_input(self):
        list_of_input = ["first_name", "last_name", "password", "balance_checking", "balance_savings"]
        account = self.__dict__
        for val in list_of_input:
            for key in account:
                if not key == "account_id":
                    if val == key:
                        account[key] = input(f"Enter {key}: ")

    def login(self, user_name, password_user):
        global current_user
        global accounts
        for account in accounts:
            if account["account_id"] == user_name and account["password"] == password_user:
                current_user = account
                return current_user
        else:
            print("try agin")
            return False

    def logout(self):
        global current_user
        current_user = None
        return current_user

    def transaction_detail(self):
        global current_user
        global accounts
        with open("transactions.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['account_id'] == current_user['account_id']:
                    print(row)

    def transaction_one_detail(self,type):
        global current_user
        global accounts
        with open("transactions.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['account_id'] == current_user['account_id'] and row['type'] == type:
                    print(row)


class Withdraw(Account):
    rows = []

    def __init__(self, account):
        global accounts
        with open('transactions.csv', mode='r', newline='') as read_file:
            reader = csv.DictReader(read_file)
            for row in reader:
                #self.rows is not a great description of what you are putting there, accounts would probably make more sense
                self.rows.append(row)

    def overdraft(self):
        global current_user
        with open('transactions.csv', mode='r', newline='') as read_file:
            reader = csv.DictReader(read_file)
            rows = []
            for row in reader:
                if row['account_id'] == current_user['account_id'] and row['overdraft'] == True:
                    rows.append(row)

        if len(rows) > 1:
            return True

    def withdraw_money(self, amount):
        global accounts
        overdraft = False
        #if this is only available after you log in, it's kind of overkill to have a second login validator, a user should not
        #be able to access this without being logged in first, in the case of your application
        if not self.login(current_user['account_id'], current_user['password']):
            return "Please log in first"
        # if not current user active, just return, this way there's less indentation, and its easier to read
        # if not current_user['active']:
        #     return
        if current_user['active'] == "True":
            if amount > 0:
                if amount > 100:
                    #You probably want either to do elifs or to return out of this function, 
                    #there is logic here which is mutually exlusive, and all of which could run
                    print("You can only withdraw 100$")
                #It may have been good to do an elif, since both of these could happen at the same time
                if amount > 100 and float(current_user["balance_checking"]) < 0:
                    print("Customer cannot withdraw more than $100 if account balance is negative")
                current_user["balance_checking"] = float(current_user['balance_checking']) - amount
                if float(current_user["balance_checking"]) < 0:
                    overdraft = True
                    current_user["balance_checking"] = float(current_user['balance_checking']) - 35
                else:
                    overdraft = False
                if self.overdraft():
                    current_user['active'] = False

        list_of_do = {
            "account_id": current_user['account_id'], "amount": amount, "type": 'Withdraw_from_checking',
            "overdraft": overdraft, "Date": datetime.datetime.now()}
        #This could have been a "save CSV function, which could have been used in many places and saved you code
        #there is a principle called DRY (Do not reapeat yourself) which is a good buzz word in job interviews.
        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft", "Date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(list_of_do)
            for account in accounts:
                if account["account_id"] == current_user['account_id']:
                    account["balance_checking"] = float(current_user['balance_checking'])

        with open('bank.csv', 'w', newline='') as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings",
                          "active"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerows(accounts)

        return f"Withdrawal successful. New balance: {current_user['balance_checking']}"
    #You probably could have dynamically removed money, or added money to bank accounts with having one function for withdraw
    #and one function for deposit, but just giving them an account, or account type parameter
    def withdraw_from_savings(self, amount):
        global accounts
        overdraft = True
        if not self.login(current_user['account_id'], current_user['password']):
            return "Please log in first"
        if current_user['active'] == "True":
            if amount > 0:
                if amount > 100:
                    print("You can only withdraw 100$")
                if amount > 100 and float(current_user["balance_savings"]) < 0:
                    print("Customer cannot withdraw more than $100 if account balance is negative")
                current_user["balance_savings"] = float(current_user['balance_savings']) - amount
                if float(current_user["balance_savings"]) < 0:
                    overdraft = True
                else:
                    overdraft = False
                if self.overdraft():
                    current_user['active'] = False

        list_of_do = {
            "account_id": current_user['account_id'], "amount": amount, "type": 'Withdraw_from_savings',
            "overdraft": overdraft, "Date":datetime.datetime.now()}

        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft","Date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(list_of_do)
            for account in accounts:
                if account["account_id"] == current_user['account_id']:
                    account["balance_savings"] = float(current_user['balance_savings'])

        with open('bank.csv', 'w', newline='') as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings",
                          "active"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(accounts)
        return f"Withdrawal successful. New balance: {current_user['balance_savings']}"


class Deposit(Account):
    rows = []

    def __init__(self, account):
        global accounts
        with open('transactions.csv', mode='r', newline='') as read_file:
            reader = csv.DictReader(read_file)
            for row in reader:
                self.rows.append(row)

    def overdraft(self):
        global current_user
        with open('transactions.csv', mode='r', newline='') as read_file:
            reader = csv.DictReader(read_file)
            rows = []
            for row in reader:
                if row['account_id'] == current_user['account_id'] and row['overdraft'] == "True":
                    rows.append(row)

        if len(rows) > 1:
            return True

    def deposit_money(self, amount):
        global accounts
        overdraft = True
        #See note in withdraw
        if not self.login(current_user['account_id'], current_user['password']):
            return "Please log in first"
        if amount > 0:
            current_user["balance_checking"] = float(current_user['balance_checking']) + amount
        if self.overdraft():
            if float(current_user['balance_checking']) >= 0:
                current_user['active'] = True

        list_of_do = {
            "account_id": current_user['account_id'], "amount": amount, "type": 'deposit_in_checking',
            "overdraft": overdraft,"Date":datetime.datetime.now()}
        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft","Date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(list_of_do)
            for account in accounts:
                if account["account_id"] == current_user['account_id']:
                    account["balance_checking"] = float(current_user['balance_checking'])

        with open('bank.csv', 'w', newline='') as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings",
                          "active"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(accounts)
        return f"Deposit successful. New balance: {current_user['balance_checking']}"

    def deposit_in_saving(self, amount):
        global accounts
        overdraft = True
        if not self.login(current_user['account_id'], current_user['password']):
            return "Please log in first"
        if amount > 0:
            current_user["balance_savings"] = float(current_user['balance_savings']) + amount
        if self.overdraft():
            if float(current_user['balance_savings']) >= 0:
                current_user['active'] = True
        list_of_do = {
            "account_id": current_user['account_id'], "amount": amount, "type": 'deposit_in_savings',
            "overdraft": overdraft,"Date":datetime.datetime.now()}
        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft","Date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(list_of_do)
            for account in accounts:
                if account["account_id"] == current_user['account_id']:
                    account["balance_savings"] = float(current_user['balance_savings'])
        with open('bank.csv', 'w', newline='') as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings",
                          "active"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerows(accounts)

        return f"Deposit successful. New balance: {current_user['balance_savings']}"


#
class Transfer(Account):
    rows = []

    def __init__(self, account):
        global accounts
        with open('transactions.csv', mode='r', newline='') as read_file:
            reader = csv.DictReader(read_file)
            for row in reader:
                self.rows.append(row)
    #Same idea here, you can just an account, and user parameter, and pull from the user.accounts dyanmically
    def transfer_to_saving(self, amount):
        global accounts
        overdraft = False
        withdraw = Withdraw(account=current_user)
        deposit = Deposit(account=current_user)
        withdraw.withdraw_money(amount)
        deposit.deposit_in_saving(amount)

        list_of_do = {
            "account_id": current_user['account_id'], "amount": amount, "type": 'transfer_to_saving',
            "overdraft": overdraft,"Date":datetime.datetime.now()}

        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(list_of_do)
            for account in accounts:
                if account["account_id"] == current_user['account_id']:
                    account["balance_savings"] = float(current_user['balance_savings'])
        with open('bank.csv', 'w', newline='') as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings",
                          "active"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerows(accounts)
        return f"Transfer successful from balance_checking. New balance: {current_user['balance_savings']}"

    def transfer_to_checking(self, amount):
        global accounts
        overdraft = False
        withdraw = Withdraw(account=current_user)
        deposit = Deposit(account=current_user)
        withdraw.withdraw_from_savings(amount)
        deposit.deposit_money(amount)

        list_of_do = {
            "account_id": current_user['account_id'], "amount": amount, "type": 'transfer_to_saving',
            "overdraft": overdraft,"Date":datetime.datetime.now()}

        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft","Date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(list_of_do)
            for account in accounts:
                if account["account_id"] == current_user['account_id']:
                    account["balance_checking"] = float(current_user['balance_checking'])
        with open('bank.csv', 'w', newline='') as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings",
                          "active"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            writer.writerows(accounts)
        return f"Transfer successful form balance_savings. New balance: {current_user['balance_checking']}"

    def transfer_to_another_account(self, amount, account_id):
        global accounts
        ather_account = {}
        overdraft = False
        # withdraw = Withdraw(account=current_user)
        # withdraw.withdraw_money(amount)
        if amount > 0:
            current_user["balance_checking"] = float(current_user['balance_checking']) - amount
        if account_id:
            for account in accounts:
                if account['account_id'] == account_id:
                    ather_account = account
            if amount > 0:
                ather_account["balance_checking"] = float(ather_account['balance_checking']) + amount
        else:
            return "there is no account"

        list_of_do = [{
            "account_id": current_user['account_id'], "amount": amount, "type": 'transfer_to_another_account',
            "overdraft": overdraft,"Date":datetime.datetime.now()}, {
            "account_id": ather_account['account_id'], "amount": amount, "type": 'balance_checking',
            "overdraft": overdraft,"Date":datetime.datetime.now()}]

        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft","Date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerows(list_of_do)
            for account in accounts:
                if account["account_id"] == current_user['account_id']:
                    account["balance_checking"] = float(current_user['balance_checking'])
        with open('bank.csv', 'w', newline='') as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings",
                          "active"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(accounts)
            # print(list_of_values)
        return f"Transfer successful. New balance: {current_user['balance_checking']}"

w = colored("Welcome! Select an option:", "red")
def main_menu():

    options = ["Log in", "Create an Account", "Exit"]
    menu = TerminalMenu(options, title=w)

    while True:
        choice = menu.show()
        if choice == 0:
            login_menu()
        elif choice == 1:
            create_account_menu()
        elif choice == 2:
            print("Exiting...")
            break

def login_menu():
    customer_id = input("Enter your id: ")
    customer_password = input("Enter your password: ")

    if customer_id and customer_password:
        user = Account()
        if user.login(user_name=customer_id, password_user=customer_password):
            operation_menu(user)


def create_account_menu():
    user1 = Account()
    user1.user_input()
    user1.create()

def operation_menu(user):
    operations = ["Withdraw", "Deposit", "Transfer", "Log out", "Get Transactions"]
    menu = TerminalMenu(operations, title="Select an operation:")

    while True:
        operation_choice = menu.show()
        
        if operation_choice == 0:  
            withdrawal_menu(user)
        elif operation_choice == 1:  
            deposit_menu(user)
        elif operation_choice == 2:  
            transfer_menu(user)
        elif operation_choice == 3:  
            user.logout()
            break
        elif operation_choice == 4:  
            get_transactions_menu(user)

def withdrawal_menu(user):
    withdrawal_options = ["Checking Account", "Saving Account", "Back"]
    menu = TerminalMenu(withdrawal_options, title="Select account type:")

    choice = menu.show()
    if choice == 0:
        amount = float(input("How much do you want to withdraw? "))
        after_login = Withdraw(account=current_user)
        print(after_login.withdraw_money(amount=amount))
    elif choice == 1:
        amount = float(input("How much do you want to withdraw? "))
        after_login = Withdraw(account=current_user)
        print(after_login.withdraw_from_savings(amount=amount))

def deposit_menu(user):
    deposit_options = ["Checking Account", "Saving Account", "Back"]
    menu = TerminalMenu(deposit_options, title="Select account type:")

    choice = menu.show()
    if choice == 0:
        amount = float(input("How much do you want to deposit? "))
        after_login = Deposit(account=current_user)
        print(after_login.deposit_money(amount=amount))
    elif choice == 1: 
        amount = float(input("How much do you want to deposit? "))
        after_login = Deposit(account=current_user)
        print(after_login.deposit_in_saving(amount=amount))


def transfer_menu(user):
    withdrawal_options = ["transfer to another account", "transfer to checking","transfer to saving", "Back"]
    menu = TerminalMenu(withdrawal_options, title="Select account type:")
    choice = menu.show()
    if choice == 0:
        after_login = Transfer(account=current_user)
        amount = float(input("How much do you want to transfer? "))
        account_id = input("Enter the account id to transfer to: ")
        print(after_login.transfer_to_another_account(amount=amount, account_id=account_id))
    elif choice == 1: 
        after_login = Transfer(account=current_user)
        amount = float(input("How much do you want to transfer? "))
        print(after_login.transfer_to_checking(amount=amount))
    elif choice == 2:
        after_login = Transfer(account=current_user)
        amount = float(input("How much do you want to transfer? "))
        print(after_login.transfer_to_saving(amount=amount))


def get_transactions_menu(user):
    transaction_options = ["All Transactions", "Specific Transaction", "Back"]
    menu = TerminalMenu(transaction_options, title="Select transaction type:")

    choice = menu.show()
    if choice == 0: 
        user.transaction_detail()
    elif choice == 1: 
        type_transaction = input("Enter your transaction type: ")
        user.transaction_one_detail(type_transaction)

if __name__ == "__main__":
    main_menu()
