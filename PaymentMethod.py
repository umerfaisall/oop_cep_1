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

# Abstract base class for payment methods
class PaymentMethod(ABC):
    @abstractmethod
    def collect_payment_details(self):
        pass

    @abstractmethod
    def process_payment(self, amount):
        pass

# Concrete implementation for Credit Card payment
class CreditCard(PaymentMethod):
    def __init__(self):
        self.creditCardNo = None
        self.expiryDate = None
        self.cvv = None
        self.balance = None

    def collect_payment_details(self):
        # Collect credit card number from user
        self.creditCardNo = input('Enter Your Credit Card Number: ')

        # Collect and parse expiry date
        expiry_input = input("Enter Credit Card Expiry Date (YYYY-MM-DD): ")
        try:
            self.expiryDate = datetime.strptime(expiry_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please enter date as YYYY-MM-DD.")
            return

        # Collect CVV
        self.cvv = input("Enter CVV: ")

        # Collect balance and ensure it's a valid float
        try:
            self.balance = float(input("Enter Credit Card Balance: "))
        except ValueError:
            print("Invalid balance. Please enter a numeric value.")
            return

    def process_payment(self, amount):
        try:
            # Check if the card is expired
            if self.expiryDate < datetime.today().date():
                raise ExpiredCard()

            # Check if there is sufficient balance
            if self.balance < amount:
                raise BalanceError()

            # Deduct the amount from balance
            self.balance -= amount
            print(f"Payment of {amount} successful. Remaining balance: {self.balance}")

        except ExpiredCard as ec:
            print(f"Payment failed: {ec}")
        except BalanceError as be:
            print(f"Payment failed: {be}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Concrete implementation for Cash Payment
class CashPayment(PaymentMethod):
    def collect_payment_details(self, amount):
        try:
            # For cash payment, we just set the balance directly
            self.balance = amount
        except ValueError as e:
            print("User Doesn't exist! ")

    def process_payment(self, amount):
        # Raise error if balance is not sufficient
        if self.balance <= amount:
            raise BalanceError
        self.balance -= amount
