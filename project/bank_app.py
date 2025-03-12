import csv
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
        with open("bank.csv", mode='r', newline='') as read_file:
            reader = csv.DictReader(read_file)
            for row in reader:
                accounts.append(row)
            # print('account class called', Account.accounts)
        Account.len_account = len(accounts)
        # print(Account.len_account)

    def create(self):
        if self.account_id == 0 and self.len_account == 0:
            self.account_id = 1001
        else:
            self.account_id = int(accounts[-1]["account_id"]) + 1
        list_of_values = {
            "account_id": self.account_id, "first_name": self.first_name, "last_name": self.last_name,
            "password": self.password, "balance_checking": float(self.balance_checking),
            "balance_savings": float(self.balance_savings), "active": self.active}

        with open('./bank.csv', 'a', newline='') as csvfile:
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
        for account in accounts:
            if account['account_id'] == user_name and account['password'] == password_user:
                current_user = account
                # print('before save', current_user)
                return True
            else:
                print("try agin")


class Withdraw(Account):
    rows = []

    # global current_user
    # print('current user w', current_user)
    def __init__(self, account):
        global accounts
        print('accounts: ', accounts)
        with open('./transactions.csv', mode='r', newline='') as read_file:
            reader = csv.DictReader(read_file)
            for row in reader:
                self.rows.append(row)
        # print(account)
        # print('checking', account['balance_checking'])
        # print('account_id', account['account_id'])
        # print('password from withdraw', account['password'])
        # print('savings', account['balance_savings'])
        # print('account active', account['active'])

    def overdraft(self):
        global current_user
        with open('./transactions.csv', mode='r', newline='') as read_file:
            reader = csv.DictReader(read_file)
            rows = []
            for row in reader:
                print(row)
                if row['account_id'] == current_user['account_id'] and row['overdraft'] == "True":
                    # print(row)
                    rows.append(row)

        if len(rows) > 1:
            return True

    def withdraw_money(self, amount):
        global accounts
        overdraft = True
        if not self.login(current_user['account_id'], current_user['password']):
            return "Please log in first"
        if current_user['active'] == "True":
            if amount > 0:
                current_user["balance_checking"] = float(current_user['balance_checking']) - amount
                print(current_user["balance_checking"])
                print(type(current_user["balance_checking"]))
                for account in accounts:
                    if account['account_id'] == current_user['account_id']:
                        account = current_user
                        print('updated account', account)
                if float(current_user["balance_checking"]) < 0:
                    overdraft = True
                else:
                    overdraft = False
                if self.overdraft():
                    current_user['active'] = False

        list_of_do = {
            "account_id": current_user['account_id'], "amount": amount, "type": 'balance_checking',
            "overdraft": overdraft}
        # print(f"the list: {list_of_do}")
        with open('./transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(list_of_do)
        # print(self.balance_checking)
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

        return f"Withdrawal successful. New balance: {current_user['balance_checking']}"

    def withdraw_from_savings(self, amount):
        global accounts
        overdraft = True
        if not self.login(current_user['account_id'], current_user['password']):
            return "Please log in first"
        if current_user['active'] == "True":
            if amount > 0:
                current_user["balance_savings"] = float(current_user['balance_savings']) - amount
                # for account in accounts:
                #     if account['account_id'] == current_user['account_id']:
                #         account = current_user
                #         print('updated account', account)
                if float(current_user["balance_savings"]) < 0:
                    overdraft = True
                else:
                    overdraft = False
                if self.overdraft():
                    current_user['active'] = False

        list_of_do = {
            "account_id": current_user['account_id'], "amount": amount, "type": 'balance_savings',
            "overdraft": overdraft}
        # print(f"the list: {list_of_do}")
        with open('./transactions.csv', 'a', newline='') as csvfile:
            fieldnames = ["account_id", "amount", "type", "overdraft"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow(list_of_do)
        # print(self.balance_checking)
        list_of_values = {
            "account_id": current_user['account_id'], "first_name": current_user['first_name'],
            "last_name": current_user['last_name'],
            "password": current_user['password'], "balance_checking": float(current_user['balance_checking']),
            "balance_savings": float(current_user['balance_savings']), "active": current_user['active']}

        with open('./bank.csv', 'w', newline='') as csvfile:
            fieldnames = ["account_id", "first_name", "last_name", "password", "balance_checking", "balance_savings",
                          "active"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(list_of_values)

        return f"Withdrawal successful. New balance: {current_user['balance_savings']}"


#
#
# class Deposit(Account):
#     pass
#
#
# class Transfer(Account):
#     pass
#
#
# class Protection(Account):
#     pass

op = int(input("Enter 1 log in or 2 crete :"))
if op == 1:
    user_id = input("Enter your id:")
    user_passeord = input("Enter your password:")
    if user_id and user_passeord:
        user = Account(account_id=user_id, password=user_passeord)
        user.login(user_name=user_id, password_user=user_passeord)
        # print('logged in', current_user)
        withdrawal = int(input("Enter 1 ch or 2 sav :"))
        if withdrawal == 1:
            after_login = Withdraw(account=current_user)
            amount = float(input("how mach you want:"))
            after_login.withdraw_money(amount=amount)
        if withdrawal == 2:
            after_login = Withdraw(account=current_user)
            amount = float(input("how mach you want:"))
            after_login.withdraw_from_savings(amount=amount)
if op == 2:
    user1 = Account()
    user1.user_input()
    user1.create()
