from fileLoad import LoadData
from user import User
class Auth:
    def signIN(self,username,password):
        try:
            data = LoadData()
            users = data.loadData()
            for user in users:
                if user['Username'] == username and user['Password'] == password:
                    return True
            return False
        except FileNotFoundError:
            print(" Error: Data file not found.")
        except KeyError as e:
            print(f" Error: Missing expected field in data - {e}")
        except Exception as e:
            print(f" An unexpected error occurred: {e}")
    def signUP(self, username, email, password, firstName, lastName, balance=None, role=None, address=None):
        try:
            data = LoadData()
            users = data.loadData()
            for user in users:
                if user['Username'] == username :
                    print("Username already occupied!")
                    return False
                if user['Email'] == email:
                    print('Email already registered')
                    return False
            user = User(username,email,password,firstName,lastName,balance,role,address)
            user.save_to_JSON('people.json')
            return True
        except FileNotFoundError:
            print("File Not Found")
            return False
        except KeyError as e:
            print(f"Error: Missing expected field in user data - {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred during sign-up: {e}")
            return False
