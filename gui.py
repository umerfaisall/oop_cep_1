
# import streamlit as st
# from auth import Auth
# from user import User
# from admin import Admin
# from car import Car
# from rental_system import Rental_System
# from fileLoad import LoadData
# from datetime import datetime
# import pandas as pd
# # Initialize backend
# auth = Auth()
# rental_system = Rental_System()

# # Load cars from JSON once
# car_data = LoadData().loadCars()
# for car in car_data:
#     car_obj = Car(
#         car_id=car["carID"],
#         brand=car["Brand"],
#         model=car["Model"],
#         seatingCapacity=car["SeatingCapacity"],
#         rentalpricePerDay=car["Rental Price"],
#         isAvailable=car["Available"]
#     )
#     rental_system.add_car(car_obj)

# # Session state
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "user" not in st.session_state:
#     st.session_state.user = None
# if "role" not in st.session_state:
#     st.session_state.role = None

# def show_login():
#     st.subheader("Login")
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         if auth.signIN(username, password):
#             user_data = [u for u in LoadData().loadData() if u["Username"] == username][0]
#             st.session_state.user = user_data
#             st.session_state.role = user_data["Role"]
#             st.session_state.logged_in = True
#             st.success("Login successful.")
#             st.rerun()
#         else:
#             st.error("Invalid username or password.")

# def show_signup():
#     st.subheader("Sign Up")
#     role = st.selectbox("Role", ["customer", "admin"])
#     username = st.text_input("Username")
#     email = st.text_input("Email")
#     password = st.text_input("Password", type="password")
#     fname = st.text_input("First Name")
#     lname = st.text_input("Last Name")
#     address = st.text_input("Address")
#     balance = None
#     if role == "customer":
#         balance = st.number_input("Initial Balance", min_value=0.0)

#     if st.button("Register"):
#         if auth.signUP(username, email, password, fname, lname, balance, role, address):
#             st.success("Sign up successful. Please log in.")
#         else:
#             st.error("Sign up failed. Try a different username or email.")

# def show_customer_dashboard():
#     user_data = st.session_state.user
#     user = User(
#         username=user_data['Username'],
#         email=user_data['Email'],
#         password=user_data['Password'],
#         firstname=user_data['firstName'],
#         lastname=user_data['LastName'],
#         balance=user_data['Balance'],
#         role=user_data['Role'],
#         address=user_data['Address'],
#         rentedcarid=user_data.get('RentedCarID')
#     )
#     rental_system.add_user(user)

#     st.subheader("Customer Dashboard")
#     option = st.selectbox("Choose an action", [
#         "View Available Cars", "Rent a Car", "Return a Car", "View Rental History", "Check Balance", "Logout"
#     ])

#     if option == "View Available Cars":
#         st.subheader("Available Cars")
#         available_cars = []
#         for car in rental_system.cars.values():
#             if car.isAvailable:
#                 available_cars.append([car.car_id, car.brand, car.model, car.rentalPricePerDay])
        
#         if available_cars:
#             df = pd.DataFrame(available_cars, columns=["Car ID", "Brand", "Model", "Price per day (Rs)"])
#             st.dataframe(df)
#         else:
#             st.warning("No available cars currently.")

#     elif option == "Rent a Car":
#         car_id = st.selectbox("Select Car ID to rent", [car.car_id for car in rental_system.cars.values() if car.isAvailable])
#         start = st.date_input("Start Date")
#         end = st.date_input("End Date")

#         if st.button("Reserve Car"):
#             try:
#                 start_date = datetime.strptime(str(start), "%Y-%m-%d")
#                 end_date = datetime.strptime(str(end), "%Y-%m-%d")
#                 rental_system.reserve_car(user.username, car_id, start_date, end_date)
#                 rental_system.save_rental_history()
#                 st.success("Car reserved successfully.")
#             except Exception as e:
#                 st.error(str(e))

#     elif option == "Return a Car":
#         if user.rented_car_id:
#             msg = rental_system.return_car(user.username)
#             st.info(msg)
#         else:
#             st.warning("You have no rented car to return.")

#     elif option == "View Rental History":
#         history = rental_system.view_user_rental_history(user.username)
#         if isinstance(history, str):
#             st.error(history)
#         else:
#             df_history = pd.DataFrame(history)
            
#             # Display the DataFrame
#             st.dataframe(df_history)
#     elif option == "Check Balance":
#         st.info(f"Your current balance: Rs {user.balance}")

#     elif option == "Logout":
#         st.session_state.logged_in = False
#         st.session_state.user = None
#         st.session_state.role = None
#         st.success("Logged out.")
#         st.rerun()

# def show_admin_dashboard():
#     admin_data = st.session_state.user
#     admin = Admin(
#         username=admin_data['Username'],
#         email=admin_data['Email'],
#         password=admin_data['Password'],
#         firstname=admin_data['FirstName'],
#         lastname=admin_data['LastName'],
#         balance=admin_data['Balance'],
#         role=admin_data['Role'],
#         address=admin_data['Address'],
#         rentedcarid=admin_data.get('RentedCarID')
#     )

#     st.subheader("Admin Dashboard")
#     option = st.selectbox("Choose an action", [
#         "Add Car", "Remove Car", "View Reserved Cars", "View Rental History", "Logout"
#     ])

#     if option == "Add Car":
#         car_id = st.text_input("Car ID")
#         brand = st.text_input("Brand")
#         model = st.text_input("Model")
#         SeatingCapacity = st.number_input("Seating Capacity", step=1)
#         price = st.number_input("Price per day (Rs)", min_value=0.0)

#         if st.button("Add Car"):
#             try:
#                 admin.add_car_to_system(car_id, brand, model, SeatingCapacity, price, True)
#                 st.success("Car added successfully.")
#             except Exception as e:
#                 st.error(str(e))

#     elif option == "Remove Car":
#         car_id = st.selectbox("Car ID to remove", [car.car_id for car in rental_system.cars.values()])
#         if st.button("Remove"):
#             admin.remove_car_from_system(car_id)
#             st.success("Car removed.")

#     elif option == "View Reserved Cars":
#         reserved = admin.print_reserved_cars()
#         st.json(reserved)

#     elif option == "View Rental History":
#         history = admin.print_rental_history()
    
#     # Convert the history (which is a list of dictionaries) to a Pandas DataFrame
#         df_history = pd.DataFrame(history)
    
#     # Display the DataFrame
#         st.dataframe(df_history)
#     elif option == "Logout":
#         st.session_state.logged_in = False
#         st.session_state.user = None
#         st.session_state.role = None
#         st.success("Logged out.")
#         st.experimental_rerun()

# def run_app():
#     st.title("🚗 Car Rental System")
#     if not st.session_state.logged_in:
#         page = st.sidebar.radio("Navigate", ["Login", "Sign Up"])
#         if page == "Login":
#             show_login()
#         else:
#             show_signup()
#     else:
#         if st.session_state.role.lower() == "admin":
#             show_admin_dashboard()
#         else:
#             show_customer_dashboard()

# if __name__ == "__main__":
#     run_app()
import streamlit as st
from auth import Auth
from user import User
from admin import Admin
from car import Car
from rental_system import Rental_System
from fileLoad import LoadData
from datetime import datetime
import pandas as pd

# Initialize backend
auth = Auth()
rental_system = Rental_System()

# Load cars from JSON once
car_data = LoadData().loadCars()
for car in car_data:
    car_obj = Car(
        car_id=car["carID"],
        brand=car["Brand"],
        model=car["Model"],
        seatingCapacity=car["SeatingCapacity"],
        rentalpricePerDay=car["Rental Price"],
        isAvailable=car["Available"]
    )
    rental_system.add_car(car_obj)

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None

def show_login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if auth.signIN(username, password):
            user_data = [u for u in LoadData().loadData() if u["Username"] == username][0]
            st.session_state.user = user_data
            st.session_state.role = user_data["Role"]
            st.session_state.logged_in = True
            st.success("Login successful.")
            st.rerun()
        else:
            st.error("Invalid username or password.")

def show_signup():
    st.subheader("Sign Up")
    role = st.selectbox("Role", ["customer", "admin"])
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    address = st.text_input("Address")
    balance = None
    if role == "customer":
        balance = st.number_input("Initial Balance", min_value=0.0)

    if st.button("Register"):
        if auth.signUP(username, email, password, fname, lname, balance, role, address):
            st.success("Sign up successful. Please log in.")
        else:
            st.error("Sign up failed. Try a different username or email.")

def show_customer_dashboard():
    user_data = st.session_state.user
    user = User(
        username=user_data['Username'],
        email=user_data['Email'],
        password=user_data['Password'],
        firstname=user_data['firstName'],
        lastname=user_data['LastName'],
        balance=user_data['Balance'],
        role=user_data['Role'],
        address=user_data['Address'],
        rentedcarid=user_data.get('RentedCarID')
    )
    rental_system.add_user(user)

    st.subheader("Customer Dashboard")
    
    # Bullet-point style menu for customer actions
    option = st.sidebar.radio("Customer Actions", [
        "View Available Cars", 
        "Rent a Car", 
        "Return a Car", 
        "View Rental History", 
        "Check Balance", 
        "Logout"
    ])

    if option == "View Available Cars":
        st.subheader("Available Cars")
        available_cars = []
        for car in rental_system.cars.values():
            if car.isAvailable:
                available_cars.append([car.car_id, car.brand, car.model, car.rentalPricePerDay])
        
        if available_cars:
            df = pd.DataFrame(available_cars, columns=["Car ID", "Brand", "Model", "Price per day (Rs)"])
            st.dataframe(df)
        else:
            st.warning("No available cars currently.")

    elif option == "Rent a Car":
        car_id = st.selectbox("Select Car ID to rent", [car.car_id for car in rental_system.cars.values() if car.isAvailable])
        start = st.date_input("Start Date")
        end = st.date_input("End Date")

        if st.button("Reserve Car"):
            try:
                start_date = datetime.strptime(str(start), "%Y-%m-%d")
                end_date = datetime.strptime(str(end), "%Y-%m-%d")
                rental_system.reserve_car(user.username, car_id, start_date, end_date)
                rental_system.save_rental_history()
                st.success("Car reserved successfully.")
            except Exception as e:
                st.error(str(e))

    elif option == "Return a Car":
        if user.rented_car_id:
            msg = rental_system.return_car(user.username)
            st.info(msg)
        else:
            st.warning("You have no rented car to return.")

    elif option == "View Rental History":
        history = rental_system.view_user_rental_history(user.username)
        if isinstance(history, str):
            st.error(history)
        else:
            df_history = pd.DataFrame(history)
            st.dataframe(df_history)
            
    elif option == "Check Balance":
        st.info(f"Your current balance: Rs {user.balance}")

    elif option == "Logout":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.success("Logged out.")
        st.rerun()

def show_admin_dashboard():
    admin_data = st.session_state.user
    admin = Admin(
        username=admin_data['Username'],
        email=admin_data['Email'],
        password=admin_data['Password'],
        firstname=admin_data['FirstName'],
        lastname=admin_data['LastName'],
        balance=admin_data['Balance'],
        role=admin_data['Role'],
        address=admin_data['Address'],
        rentedcarid=admin_data.get('RentedCarID')
    )

    st.subheader("Admin Dashboard")
    
    # Bullet-point style menu for admin actions
    option = st.sidebar.radio("Admin Actions", [
        "Add Car", 
        "Remove Car", 
        "View Reserved Cars", 
        "View Rental History", 
        "Logout"
    ])

    if option == "Add Car":
        car_id = st.text_input("Car ID")
        brand = st.text_input("Brand")
        model = st.text_input("Model")
        SeatingCapacity = st.number_input("Seating Capacity", step=1)
        price = st.number_input("Price per day (Rs)", min_value=0.0)

        if st.button("Add Car"):
            try:
                admin.add_car_to_system(car_id, brand, model, SeatingCapacity, price, True)
                st.success("Car added successfully.")
            except Exception as e:
                st.error(str(e))

    elif option == "Remove Car":
        car_id = st.selectbox("Car ID to remove", [car.car_id for car in rental_system.cars.values()])
        if st.button("Remove"):
            admin.remove_car_from_system(car_id)
            st.success("Car removed.")

    elif option == "View Reserved Cars":
        reserved = admin.print_reserved_cars()
        df_reserved = pd.DataFrame(reserved)
        st.dataframe(df_reserved)
        

    elif option == "View Rental History":
        history = admin.print_rental_history()
        df_history = pd.DataFrame(history)
        st.dataframe(df_history)
        
    elif option == "Logout":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.success("Logged out.")
        st.rerun()

def run_app():
    st.title("🚗 Car Rental System")
    if not st.session_state.logged_in:
        page = st.sidebar.radio("Navigate", ["Login", "Sign Up"])
        if page == "Login":
            show_login()
        else:
            show_signup()
    else:
        if st.session_state.role.lower() == "admin":
            show_admin_dashboard()
        else:
            show_customer_dashboard()

if __name__ == "__main__":
    run_app()
