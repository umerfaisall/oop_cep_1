from user import User
from car import Car
import json

class Admin(User):
    def __init__(self, username, email, password, firstname, lastname, balance, role, address,rentedcarid):
        # Initialize parent User class
        super().__init__(username, email, password, firstname, lastname, balance, role, address,rentedcarid)
        self.balance = None  # Keeping balance as it may be used later

    def add_car_to_system(self, car_id, brand, model, seating_capacity, rental_price_per_day, is_available):
        try:
            # Try to open and load existing cars from JSON file
            with open('data/cars.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            # If file doesn't exist, start with an empty list
            data = []

        # Check if the car already exists
        for car in data:
            if car.get('carID') == car_id:
                raise ValueError("Car already exists!")

        # Create a new car entry
        new_car = {
            'carID': car_id,
            'Brand': brand,
            'Model': model,
            'SeatingCapacity': seating_capacity,
            'Rental Price': rental_price_per_day,
            'Available': is_available
        }
        
        # Add the new car and save back to the file
        data.append(new_car)
        with open('data/cars.json', 'w') as f:
            json.dump(data, f, indent=4)
        print(f'Car {car_id} added successfully!')

    def remove_car_from_system(self, car_id):
        try:
            # Load existing car data
            with open('data/cars.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print("File not found!")
            return

        # Check and remove car if it exists
        car_exists = False
        for car in data:
            if car.get('carID') == car_id:
                car_exists = True
                data.remove(car)
                break

        # If car wasn't found, notify and return
        if not car_exists:
            print(f"Car with ID {car_id} doesn't exist!")
            return

        # Write updated data back to the file
        with open('data/cars.json', 'w') as f:
            json.dump(data, f, indent=4)

        print(f'Car {car_id} removed successfully!')

    def print_reserved_cars(self):
        try:
            # Load car data and filter for reserved (not available) cars
            with open('data/cars.json', 'r') as f:
                data = json.load(f)
                reserved_cars = [car for car in data if not car.get('Available')]  # Checking the correct field name 'Available'
                return reserved_cars
        except FileNotFoundError:
            print("File not found!")

    def print_rental_history(self):
        try:
            # Load rental history data
            with open('data/rental_history.json','r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            print("File Not Found!!")
