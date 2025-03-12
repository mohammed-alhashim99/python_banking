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