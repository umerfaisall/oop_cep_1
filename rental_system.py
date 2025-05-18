from user import User
from car import Car
import json
import os
from datetime import datetime
from fileLoad import LoadData
from PaymentMethod import CreditCard
from PaymentMethod import CashPayment
class Rental_System:
    def __init__(self):
        self.users={}
        self.cars={}
        self.rental_history=[]
        
    def add_car(self, car:Car):
        self.cars[car.car_id]=car
        
    def add_user(self,user:User):
        self.users[user.username]=user
    
    def save_users_to_file(self, file_path="data/people.json"):
        data = []
        for user in self.users.values():
            data.append({
                "Username": user.username,
                "Email": user.email,
                "Password": user.password,
                "firstName": user.firstName,
                "LastName": user.lastName,
                "Balance": user.balance,
                "Role": user.role,
                "Address": user.address,
                "RentedCarID": user.rented_car_id
            })
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    def save_cars_to_file(self, file_path="data/cars.json"):
        data = []
        for car in self.cars.values():
            data.append({
                "carID": car.car_id,
                "Brand": car.brand,
                "Model": car.model,
                "SeatingCapacity": car.seatingCapacity,
                "Rental Price": car.rentalPricePerDay,
                "Available": car.isAvailable
            })
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    
    def reserve_car(self,username, car_id, start_date,end_date):
        if username not in self.users:
            return f'{username} not found!'
        user=self.users[username]
        car=self.cars.get(car_id)
        
        # Check if user exists
        if not user:
            raise ValueError(f"User '{username}' not found.")
    
        # Check if car exists
        if not car:
            raise ValueError(f"Car ID '{car_id}' not found.")
        
        if user.has_rented_a_car():                     # Ensure user doesn't already have an active rental
            raise Exception("User already has a rented car.")
        
        if not car.isAvailable:                        # Ensure the car is available for rental
            raise Exception(f"Car '{car.model}' is not available.")
        
        # Validate inputs
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise ValueError("Start and end dates must be datetime objects.")
        
        
        if start_date >= end_date:                    # Ensure the rental period is valid
            raise ValueError("End date must be after start date.")
        
         
        total_days = (end_date - start_date).days      # Calculate rental cost
        total_cost = total_days * car.rentalPricePerDay

        if user.balance < total_cost:                # Ensure user has enough balance
            raise Exception("Insufficient balance to reserve this car.")
        
        # Deduct balance
        user.balance -= total_cost
        
        #record rental
        rental_record = {
            "username": user.username,
            "email": user.email,
            "car_id": car.car_id,
            "brand": car.brand,
            "model": car.model,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "total_days": total_days,
            "total_cost": total_cost
        }
        self.rental_history.append(rental_record)
        
        
       # Mark the car as rented and update user record
        user.rent_a_car(car_id)  # Save car ID to user
        car.markRented()         # Set availability to False
        self.save_users_to_file()
        self.save_cars_to_file()

        LoadData().update_user_rented_car(username, car_id)
        LoadData().update_car_availability(car_id, False)
        print(f"Car '{car.model}' reserved successfully for Rs:{total_cost}")
        return True
        
    def add_balance(self, username, amount, payment_method=None):
        if username not in self.users:
            raise ValueError(f"User '{username}' not found.")
        
        user = self.users[username]

        if payment_method is None:
            print('1) Add Balance From a Credit Card')
            print('2) Add Balance Through Cash')
            choice = input("Enter choice (1 or 2): ").strip()
            if choice == '1':
                payment_method = 'Credit Card'
            elif choice == '2':
                payment_method = 'Cash'
            else:
                raise ValueError("Invalid selection.")

        try:
            if payment_method == 'Credit Card':
                card = CreditCard()
                card.collect_payment_details()
                card.process_payment(amount)
            elif payment_method == 'Cash':
                cash = CashPayment()
                cash.collect_payment_details()
                cash.process_payment(amount)
            else:
                raise ValueError("Invalid payment method.")
        except Exception as e:
            return f"Payment failed: {e}"

        user.balance += amount
        self.save_users_to_file()
        return f"Rs {amount} added successfully. New balance: Rs {user.balance:.2f}"  
    
    def return_car(self, username):
        if username not in self.users:                   # Check if user exists
            return f'{username} not found!'
        user = self.users[username]
        if not user.has_rented_a_car():                  # Check if user has an active rental
            return f'The user has not rented any car yet!'
        
        # Get the car ID and object
        car_id = user.rented_car_id
        car = self.cars.get(car_id)
        
        if car:
            car.markAvailable()                           # Mark car available if it exists
        user.return_car()                                 # Remove rental from user's record
        LoadData().update_user_rented_car(username, car_id)  # Update user data
        LoadData().update_car_availability(car_id, True)  # Update car availability
        self.save_users_to_file()
        self.save_cars_to_file()
        return f'{username} returned the car with Car ID: {car_id}'

    def save_rental_history(self, file_name='rental_history.json'):
        file_path = f"data/{file_name}"
        
        try:
            # Load existing history if file exists and is not empty
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, "r") as f:
                    existing_data = json.load(f)
            else:
                existing_data = []

            # Merge new records
            existing_data.extend(self.rental_history)

            # Write full list back to file
            with open(file_path, "w") as f:
                json.dump(existing_data, f, indent=4)

            # Clear in-memory history after saving
            self.rental_history.clear()
            print("Rental history saved to file.")

        except Exception as e:
            print(f"Error saving rental history: {e}")

        except Exception as e:
            print(f"Error saving rental history: {e}")
                       
    # def view_user_rental_history(self, username, file_name='rental_history.json'):
    #     if username not in self.users:
    #         return f"User '{username}' not found."

    #     file_path = f"data/{file_name}"

    #     try:
    #         # Load history from file
    #         if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    #             with open(file_path, "r") as f:
    #                 full_history = json.load(f)
    #         else:
    #             full_history = []
    #     except Exception as e:
    #         return  f"Error loading rental history: {e}"

    #     # Filter user's records
    #     user_history = [record for record in full_history if record["username"] == username]

    #     if not user_history:
    #         return f"No rental history found for user '{username}'."
    #     return user_history
    
    def __str__(self, username, file_name='rental_history.json'):
        if username not in self.users:
            return f"User '{username}' not found."

        file_path = f"data/{file_name}"

        try:
            # Load history from file
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, "r") as f:
                    full_history = json.load(f)
            else:
                full_history = []
        except Exception as e:
            return  f"Error loading rental history: {e}"

        # Filter user's records
        user_history = [record for record in full_history if record["username"] == username]

        if not user_history:
            return f"No rental history found for user '{username}'."
        return user_history