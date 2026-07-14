
import json
import random
import string
from pathlib import Path


class Bank:
    database = "data.json"
    data = []

    # ---- load data from disk when the class is first imported ----
    try:
        if Path(database).exists():
            with open(database) as fs:
                content = fs.read().strip()
                data = json.loads(content) if content else []
        else:
            # create an empty database file instead of just printing a message
            with open(database, "w") as fs:
                fs.write(json.dumps([]))
            data = []
    except Exception as err:
        print(f"An exception occurred while loading the database: {err}")
        data = []

    # internal helpers
    
    @staticmethod
    def _update():
        with open(Bank.database, "w") as fs:
            fs.write(json.dumps(Bank.data, indent=2))

    @classmethod
    def _account_number_exists(cls, acc_no):
        return any(rec["accountNo"] == acc_no for rec in Bank.data)

    @classmethod
    def _generate_account_number(cls):
        while True:
            alpha = random.choices(string.ascii_letters, k=3)
            num = random.choices(string.digits, k=3)
            spchar = random.choices("$#@%^&", k=1)
            id_chars = alpha + num + spchar
            random.shuffle(id_chars)
            acc_no = "".join(id_chars)
            if not cls._account_number_exists(acc_no):
                return acc_no

    @staticmethod
    def _find_account(acc_no, pin):
        matches = [
            rec for rec in Bank.data
            if rec["accountNo"] == acc_no and rec["pin"] == pin
        ]
        return matches[0] if matches else None

    # ------------------------------------------------------------------ #
    # public operations
    # ------------------------------------------------------------------ #
    def create_account(self, name, age, email, pin):
        """Create a new account. Returns (success, message, info_dict|None)."""
        try:
            age = int(age)
            pin = int(pin)
        except (TypeError, ValueError):
            return False, "Age and PIN must be numbers.", None

        if not name or not name.strip():
            return False, "Name cannot be empty.", None

        if age < 18:
            return False, "You must be 18 or older to create an account.", None

        if len(str(pin)) != 4:
            return False, "PIN must be exactly 4 digits.", None

        info = {
            "name": name.strip(),
            "age": age,
            "email": email.strip(),
            "pin": pin,
            "accountNo": Bank._generate_account_number(),
            "balance": 0,
        }

        Bank.data.append(info)
        Bank._update()
        return True, "Account created successfully!", info

    def deposit(self, acc_no, pin, amount):
        """Deposit money. Returns (success, message, new_balance|None)."""
        try:
            pin = int(pin)
            amount = int(amount)
        except (TypeError, ValueError):
            return False, "PIN and amount must be numbers.", None

        account = Bank._find_account(acc_no, pin)
        if account is None:
            return False, "No account found with that account number and PIN.", None

        if amount <= 0 or amount > 10000:
            return False, "You can only deposit an amount between 1 and 10,000.", None

        account["balance"] += amount
        Bank._update()
        return True, "Amount deposited successfully.", account["balance"]

    def withdraw(self, acc_no, pin, amount):
        """Withdraw money. Returns (success, message, new_balance|None)."""
        try:
            pin = int(pin)
            amount = int(amount)
        except (TypeError, ValueError):
            return False, "PIN and amount must be numbers.", None

        account = Bank._find_account(acc_no, pin)
        if account is None:
            return False, "No account found with that account number and PIN.", None

        if amount <= 0:
            return False, "Withdrawal amount must be greater than 0.", None

        if account["balance"] < amount:
            return False, "Insufficient balance.", None

        account["balance"] -= amount
        Bank._update()
        return True, "Amount withdrawn successfully.", account["balance"]

    def get_details(self, acc_no, pin):
        """Fetch account details. Returns (success, message, info_dict|None)."""
        try:
            pin = int(pin)
        except (TypeError, ValueError):
            return False, "PIN must be a number.", None

        account = Bank._find_account(acc_no, pin)
        if account is None:
            return False, "No account found with that account number and PIN.", None

        return True, "Account found.", dict(account)

    def update_details(self, acc_no, pin, name=None, email=None, new_pin=None):
        """
        Update name / email / pin. Pass None (or empty string) for any
        field you don't want to change. Age, accountNo, and balance can't
        be changed. Returns (success, message, updated_info|None).
        """
        try:
            pin = int(pin)
        except (TypeError, ValueError):
            return False, "PIN must be a number.", None

        account = Bank._find_account(acc_no, pin)
        if account is None:
            return False, "No account found with that account number and PIN.", None

        if name:
            account["name"] = name.strip()
        if email:
            account["email"] = email.strip()
        if new_pin:
            try:
                new_pin = int(new_pin)
            except ValueError:
                return False, "New PIN must be numeric.", None
            if len(str(new_pin)) != 4:
                return False, "New PIN must be exactly 4 digits.", None
            account["pin"] = new_pin

        Bank._update()
        return True, "Details updated successfully.", dict(account)

    def delete_account(self, acc_no, pin, confirm=False):
        """Delete an account. Caller must pass confirm=True to actually delete."""
        try:
            pin = int(pin)
        except (TypeError, ValueError):
            return False, "PIN must be a number.", None

        account = Bank._find_account(acc_no, pin)
        if account is None:
            return False, "No account found with that account number and PIN.", None

        if not confirm:
            return False, "Deletion not confirmed.", None

        Bank.data.remove(account)
        Bank._update()
        return True, "Account deleted successfully.", None