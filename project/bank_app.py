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
            "account_id": current_user['account_id'], "amount": amount, "type": 'balance_checking',
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
                current_user["balance_savings"] = float(current_user['balance_savings']) - amount
                if float(current_user["balance_savings"]) < 0:
                    overdraft = True
                else:
                    overdraft = False
                if self.overdraft():
                    current_user['active'] = False

        list_of_do = {
            "account_id": current_user['account_id'], "amount": amount, "type": 'balance_savings',
            "overdraft": overdraft}

        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(list_of_do)
        list_of_values = {
            "account_id": current_user['account_id'], "first_name": current_user['first_name'],
            "last_name": current_user['last_name'],
            "password": current_user['password'], "balance_checking": float(current_user['balance_checking']),
            "balance_savings": float(current_user['balance_savings']), "active": current_user['active']}

        with open('bank.csv', 'w', newline='') as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings",
                          "active"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(list_of_values)

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
            "account_id": current_user['account_id'], "amount": amount, "type": 'balance_checking',
            "overdraft": overdraft}
        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(list_of_do)
        list_of_values = {
            "account_id": current_user['account_id'], "first_name": current_user['first_name'],
            "last_name": current_user['last_name'],
            "password": current_user['password'], "balance_checking": float(current_user['balance_checking']),
            "balance_savings": float(current_user['balance_savings']), "active": current_user['active']}

        with open('bank.csv', 'w', newline='') as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings",
                          "active"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(list_of_values)

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
            "account_id": current_user['account_id'], "amount": amount, "type": 'balance_savings',
            "overdraft": overdraft}

        with open('transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(list_of_do)
        list_of_values = {
            "account_id": current_user['account_id'], "first_name": current_user['first_name'],
            "last_name": current_user['last_name'],
            "password": current_user['password'], "balance_checking": float(current_user['balance_checking']),
            "balance_savings": float(current_user['balance_savings']), "active": current_user['active']}

        with open('bank.csv', 'w', newline='') as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings",
                          "active"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(list_of_values)

        return f"Deposit successful. New balance: {current_user['balance_savings']}"


