from abc import ABC, abstractmethod
from datetime import datetime

# Custom Exception for Expired Card
class ExpiredCard(Exception):
    def __init__(self, message="Credit Card is expired."):
        super().__init__(message)

# Custom Exception for Insufficient Balance
class BalanceError(Exception):
    def __init__(self, message="Insufficient balance on the credit card."):
        super().__init__(message)

class PaymentMethod(ABC):
    @abstractmethod
    def collect_payment_details(self):
        pass

    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCard(PaymentMethod):
    def __init__(self):
        self.creditCardNo = None
        self.expiryDate = None
        self.cvv = None
        self.balance = None

    def collect_payment_details(self):
        self.creditCardNo = input('Enter Your Credit Card Number: ')
        
        # Taking expiry date in YYYY-MM-DD format and parsing it
        expiry_input = input("Enter Credit Card Expiry Date (YYYY-MM-DD): ")
        try:
            self.expiryDate = datetime.strptime(expiry_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please enter date as YYYY-MM-DD.")
            return

        self.cvv = input("Enter CVV: ")

        try:
            self.balance = float(input("Enter Credit Card Balance: "))
        except ValueError:
            print("Invalid balance. Please enter a numeric value.")
            return

    def process_payment(self, amount):
        try:
            if self.expiryDate < datetime.today().date():
                raise ExpiredCard()

            if self.balance < amount:
                raise BalanceError()

            self.balance -= amount
            print(f"Payment of {amount} successful. Remaining balance: {self.balance}")

        except ExpiredCard as ec:
            print(f"Payment failed: {ec}")
        except BalanceError as be:
            print(f"Payment failed: {be}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
class CashPayment(PaymentMethod):
    def collect_payment_details(self,user):
        try:
            self.balance = user.balance
        except ValueError as e:
            print("User Doesn't exist! ")
    def process_payment(self, amount):
        if self.balance <= amount:
            raise BalanceError
        self.balance -= amount

        