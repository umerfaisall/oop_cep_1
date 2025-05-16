import json
import json

class LoadData:
    def loadData(self):
        with open('data/people.json', 'r') as f:
            data = json.load(f)
            return data

    def loadCars(self):
        with open('data/cars.json', 'r') as f:
            data = json.load(f)
            return data

    def update_user_rented_car(self, username, rented_car_id):
        with open('data/people.json', 'r') as f:
            users = json.load(f)

        for user in users:
            if user['Username'] == username:
                user['RentedCarID']=rented_car_id
                break

        with open('data/people.json', 'w') as f:
            json.dump(users, f, indent=4)

    def update_car_availability(self, car_id, availability):
        with open('data/cars.json', 'r') as f:
            cars = json.load(f)

        for car in cars:
            if car['carID']==car_id:
                car['Available'] = availability
                break

        with open('data/cars.json', 'w') as f:
            json.dump(cars, f, indent=4)
