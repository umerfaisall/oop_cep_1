import json

class Car:
    def  __init__(self, car_id, brand, model, seatingCapacity, rentalpricePerDay, isAvailable):
        # Initialize the Car object with all required attributes
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.seatingCapacity = seatingCapacity
        self.rentalPricePerDay = rentalpricePerDay
        self.isAvailable = isAvailable

    def markRented(self):
        # Mark the car as rented (not available)
        self.isAvailable = False

    def markAvailable(self):
        # Mark the car as available for rent
        self.isAvailable = True

    def to_dict(self):
        # Convert the Car object to a dictionary format suitable for JSON serialization
        return {
            'carID': self.car_id,
            'Brand' : self.brand,
            'Model' : self.model,
            'SeatingCapacity': self.seatingCapacity,
            'Rental Price': self.rentalPricePerDay,
            'Available': self.isAvailable
        }

    def save_to_json(self, fileName):
        try:
            # Try to open and load existing data from the JSON file
            with open('data/' + fileName, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            # If the file does not exist, start with an empty list
            data = []

        # Append the current car data to the list
        data.append(self.to_dict())

        # Save the updated data back to the JSON file
        with open('data/' + fileName, 'w') as f:
            json.dump(data, f, indent=4)
