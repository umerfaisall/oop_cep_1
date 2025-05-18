import json

class LoadData:
    def loadData(self):
        # Load and return user data from people.json
        with open('data/people.json', 'r') as f:
            data = json.load(f)
            return data

    def loadCars(self):
        # Load and return car data from cars.json
        with open('data/cars.json', 'r') as f:
            data = json.load(f)
            return data

    def update_user_rented_car(self, username, rented_car_id):
        # Open people.json and load existing users
        with open('data/people.json', 'r') as f:
            users = json.load(f)

        # Find the user and update their rented car ID
        for user in users:
            if user['Username'] == username:
                user['RentedCarID'] = rented_car_id
                break

        # Save the updated list of users back to the JSON file
        with open('data/people.json', 'w') as f:
            json.dump(users, f, indent=4)

    def update_car_availability(self, car_id, availability):
        # Open cars.json and load existing cars
        with open('data/cars.json', 'r') as f:
            cars = json.load(f)

        # Find the car and update its availability status
        for car in cars:
            if car['carID'] == car_id:
                car['Available'] = availability
                break

        # Save the updated list of cars back to the JSON file
        with open('data/cars.json', 'w') as f:
            json.dump(cars, f, indent=4)