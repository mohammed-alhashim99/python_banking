import csv
import datetime

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

    def transaction_one_detail(self):
        global current_user
        global accounts
        with open("transactions.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['account_id'] == current_user['account_id'] and row['type'] == current_user[""]:
                    print(row)


class Withdraw(Account):
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
                if row['account_id'] == current_user['account_id'] and row['overdraft'] == True:
                    rows.append(row)

        if len(rows) > 1:
            return True

    def withdraw_money(self, amount):
        global accounts
        overdraft = False
        if not self.login(current_user['account_id'], current_user['password']):
            return "Please log in first"
        if current_user['active'] == "True":
            if amount > 0:
                if amount > 100:
                    print("You can only withdraw 100$")
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
            "overdraft": overdraft}
        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft"]
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
            "overdraft": overdraft}

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
        if not self.login(current_user['account_id'], current_user['password']):
            return "Please log in first"
        if amount > 0:
            current_user["balance_checking"] = float(current_user['balance_checking']) + amount
        if self.overdraft():
            if float(current_user['balance_checking']) >= 0:
                current_user['active'] = True

        list_of_do = {
            "account_id": current_user['account_id'], "amount": amount, "type": 'deposit_in_checking',
            "overdraft": overdraft}
        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft"]
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
            "overdraft": overdraft}
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

    def transfer_to_saving(self, amount):
        global accounts
        overdraft = False
        withdraw = Withdraw(account=current_user)
        deposit = Deposit(account=current_user)
        withdraw.withdraw_money(amount)
        deposit.deposit_in_saving(amount)

        list_of_do = {
            "account_id": current_user['account_id'], "amount": amount, "type": 'transfer_to_saving',
            "overdraft": overdraft}

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
        return True

    def transfer_to_checking(self, amount):
        global accounts
        overdraft = False
        withdraw = Withdraw(account=current_user)
        deposit = Deposit(account=current_user)
        withdraw.withdraw_from_savings(amount)
        deposit.deposit_money(amount)

        list_of_do = {
            "account_id": current_user['account_id'], "amount": amount, "type": 'transfer_to_saving',
            "overdraft": overdraft}

        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft"]
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
        return True

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
            "overdraft": overdraft}, {
            "account_id": ather_account['account_id'], "amount": amount, "type": 'balance_checking',
            "overdraft": overdraft}]

        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft"]
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
        return True


crete_or_login = int(input("Enter 1 for log in or 2 for crete an account :"))
if crete_or_login == 1:

    customer_id = input("Enter your id:")
    customer_password = input("Enter your password:")

    if customer_id and customer_password:
        user = Account()
        if user.login(user_name=customer_id, password_user=customer_password):
            operation = int(
                input("Enter 1 for withdrawal or 2 for deposit or 3 for Transfer 4 log out  5 get transactions:"))
            if operation == 1:

                withdrawal = int(input("Enter 1 for checking account or 2 for saving account :"))

                if withdrawal == 1:
                    after_login = Withdraw(account=current_user)
                    amount = float(input("how mach do you want:"))
                    after_login.withdraw_money(amount=amount)
                if withdrawal == 2:
                    after_login = Withdraw(account=current_user)
                    amount = float(input("how mach do you want:"))
                    after_login.withdraw_from_savings(amount=amount)

            if operation == 2:

                deposit = int(input("Enter 1 for checking account or 2 for saving account :"))

                if deposit == 1:
                    after_login = Deposit(account=current_user)
                    amount = float(input("how mach do you want:"))
                    after_login.deposit_money(amount=amount)

                if deposit == 2:
                    after_login = Deposit(account=current_user)
                    amount = float(input("how mach do you want:"))
                    after_login.deposit_in_saving(amount=amount)

            if operation == 3:
                after_login = Transfer(account=current_user)
                amount = float(input("how mach do you want:"))
                account_id = input("Enter the id:")
                after_login.transfer_to_another_account(amount=amount, account_id=account_id)

            if operation == 4:
                user.logout()

            if operation == 5:

                operation_transaction = int(input("Enter 1 for all transactions or 2 for specific transaction :"))

                if operation_transaction == 1:
                    user.transaction_detail()

                if operation_transaction == 2:
                    type_transaction = input("Enter your type of transaction:")
                    print(type(type_transaction))
                    user.transaction_one_detail(type_transaction)

if crete_or_login == 2:
    user1 = Account()
    user1.user_input()
    user1.create()
