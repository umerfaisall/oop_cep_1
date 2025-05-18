import streamlit as st
from auth import Auth
from user import User
from admin import Admin
from car import Car
from rental_system import Rental_System
from fileLoad import LoadData
from datetime import datetime
import pandas as pd


class CarRentalApp:
    def __init__(self):
        # Initialize backend systems
        self.auth = Auth()
        self.rental_system = Rental_System()
        
        # Load cars from JSON
        self._load_cars()
        
        # Initialize session state
        self._init_session_state()

    def _load_cars(self):
        """Load cars from JSON data"""
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
            self.rental_system.add_car(car_obj)

    def _init_session_state(self):
        """Initialize session state variables"""
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        if "user" not in st.session_state:
            st.session_state.user = None
        if "role" not in st.session_state:
            st.session_state.role = None
    
    def refresh_user_data(self):
        """Refresh user data from database to keep the session state updated"""
        if st.session_state.logged_in and st.session_state.user:
            username = st.session_state.user["Username"]
            fresh_data = [u for u in LoadData().loadData() if u["Username"] == username]
            if fresh_data:
                st.session_state.user = fresh_data[0]
                return True
        return False
    
    def show_login(self):
        """Display login form"""
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if self.auth.signIN(username, password):
                user_data = [u for u in LoadData().loadData() if u["Username"] == username][0]
                st.session_state.user = user_data
                st.session_state.role = user_data["Role"]
                st.session_state.logged_in = True
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid username or password.")
    
    def show_signup(self):
        """Display signup form"""
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
            if self.auth.signUP(username, email, password, fname, lname, balance, role, address):
                st.success("Sign up successful. Please log in.")
            else:
                st.error("Sign up failed. Try a different username or email.")
    
    def show_customer_dashboard(self):
        """Display customer dashboard"""
        # Refresh user data to ensure we have the latest information
        self.refresh_user_data()
        
        user_data = st.session_state.user
        user = User(
            username=user_data['Username'],
            email=user_data['Email'],
            password=user_data['Password'],
            firstname=user_data.get('firstName') or user_data.get('FirstName'),
            lastname=user_data.get('LastName'),
            balance=user_data['Balance'],
            role=user_data['Role'],
            address=user_data['Address'],
            rentedcarid=user_data.get('RentedCarID')
        )
        self.rental_system.add_user(user)

        st.subheader("Customer Dashboard")
        
        # Display current user info at the top of the dashboard
        st.write(f"**Welcome, {user.firstName}!**")
        st.write(f"**Current Balance:** Rs {user.balance}")
        st.write(f"**Rented Car ID:** {user.rented_car_id if user.rented_car_id else 'None'}")
        
        # Bullet-point style menu for customer actions
        option = st.sidebar.radio("Customer Actions", [
            "View Available Cars", 
            "Rent a Car", 
            "Return a Car", 
            "View Rental History", 
            "Add Balance", 
            "Logout"
        ])

        if option == "View Available Cars":
            self._handle_view_available_cars()
        elif option == "Rent a Car":
            self._handle_rent_car(user)
        elif option == "Return a Car":
            self._handle_return_car(user)
        elif option == "View Rental History":
            self._handle_view_rental_history(user)
        elif option == "Add Balance":
            self._handle_add_balance(user)
        elif option == "Logout":
            self._handle_logout()
    
    def _handle_view_available_cars(self):
        """Show available cars"""
        st.subheader("Available Cars")
        available_cars = []
        for car in self.rental_system.cars.values():
            if car.isAvailable:
                available_cars.append([car.car_id, car.brand, car.model, car.seatingCapacity, car.rentalPricePerDay])
        
        if available_cars:
            df = pd.DataFrame(available_cars, columns=["Car ID", "Brand", "Model", "Seating Capacity", "Price per day (Rs)"])
            st.dataframe(df)
        else:
            st.warning("No available cars currently.")
    
    def _handle_rent_car(self, user):
        """Handle car rental process"""
        # Check if user already has a rented car
        if user.rented_car_id:
            st.warning(f"You already have rented car ID: {user.rented_car_id}. Please return it before renting another.")
        else:
            available_car_ids = [car.car_id for car in self.rental_system.cars.values() if car.isAvailable]
            if not available_car_ids:
                st.warning("No cars available for rent.")
            else:
                car_id = st.selectbox("Select Car ID to rent", available_car_ids)
                start = st.date_input("Start Date")
                end = st.date_input("End Date")

                if st.button("Reserve Car"):
                    try:
                        start_date = datetime.strptime(str(start), "%Y-%m-%d")
                        end_date = datetime.strptime(str(end), "%Y-%m-%d")
                        self.rental_system.reserve_car(user.username, car_id, start_date, end_date)
                        self.rental_system.save_rental_history()
                        st.success("Car reserved successfully.")
                        # Refresh user data to update UI
                        self.refresh_user_data()
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
    
    def _handle_return_car(self, user):
        """Handle car return process"""
        if user.rented_car_id:
            if st.button("Return Car"):
                try:
                    msg = self.rental_system.return_car(user.username)
                    st.success(msg)
                    # Refresh user data to update UI
                    self.refresh_user_data()
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
        else:
            st.warning("You have no rented car to return.")
    
    def _handle_view_rental_history(self, user):
        """Show rental history for a user"""
        history = self.rental_system.__str__(user.username)
        if isinstance(history, str):
            st.error(history)
        elif not history:
            st.info("No rental history found.")
        else:
            st.subheader("Your Rental History")
            df_history = pd.DataFrame(history)
            st.dataframe(df_history)
    
    def _handle_add_balance(self, user):
        """Handle adding balance to user account"""
        amount = st.number_input("Enter amount to add", min_value=1.0, step=100.0)
        payment_method = st.selectbox("Select payment method", ["Credit Card", "Cash"])
        
        # Payment details collection UI based on selected method
        if payment_method == "Credit Card":
            st.subheader("Credit Card Details")
            card_number = st.text_input("Card Number", max_chars=16)
            card_holder = st.text_input("Card Holder Name")
            expiry = st.text_input("Expiry Date (MM/YY)")
            cvv = st.text_input("CVV", max_chars=3, type="password")
            payment_details_valid = card_number and card_holder and expiry and cvv
        else:  # Cash
            st.subheader("Cash Payment")
            receipt_number = st.text_input("Receipt Number")
            payment_details_valid = receipt_number
        
        if st.button("Add Balance"):
            if not payment_details_valid:
                st.error("Please fill all payment details")
            else:
                try:
                    # Create a custom version of add_balance that doesn't require console input
                    if payment_method == "Credit Card":
                        # Mock the CreditCard behavior without requiring console input
                        user_obj = self.rental_system.users[user.username]
                        user_obj.balance += amount
                        self.rental_system.save_users_to_file()
                        msg = f"Rs {amount} added successfully via Credit Card. New balance: Rs {user_obj.balance:.2f}"
                    else:  # Cash
                        # Mock the CashPayment behavior without requiring console input
                        user_obj = self.rental_system.users[user.username]
                        user_obj.balance += amount
                        self.rental_system.save_users_to_file()
                        msg = f"Rs {amount} added successfully via Cash. New balance: Rs {user_obj.balance:.2f}"
                    
                    st.success(msg)
                    # Refresh user data to update UI
                    self.refresh_user_data()
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
    
    def _handle_logout(self):
        """Handle user logout"""
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None
        st.success("Logged out.")
        st.rerun()
    
    def show_admin_dashboard(self):
        """Display admin dashboard"""
        # Refresh admin data to ensure we have the latest information
        self.refresh_user_data()
        
        admin_data = st.session_state.user
        admin = Admin(
            username=admin_data['Username'],
            email=admin_data['Email'],
            password=admin_data['Password'],
            firstname=admin_data.get('FirstName'),
            lastname=admin_data.get('LastName'),
            balance=admin_data['Balance'],
            role=admin_data['Role'],
            address=admin_data['Address'],
            rentedcarid=admin_data.get('RentedCarID')
        )

        st.subheader("Admin Dashboard")
        st.write(f"**Welcome, {admin.firstName}!**")
        
        # Bullet-point style menu for admin actions
        option = st.sidebar.radio("Admin Actions", [
            "Add Car", 
            "Remove Car", 
            "View Reserved Cars", 
            "View Rental History", 
            "Logout"
        ])

        if option == "Add Car":
            self._handle_add_car(admin)
        elif option == "Remove Car":
            self._handle_remove_car(admin)
        elif option == "View Reserved Cars":
            self._handle_view_reserved_cars(admin)
        elif option == "View Rental History":
            self._handle_admin_rental_history(admin)
        elif option == "Logout":
            self._handle_logout()
    
    def _handle_add_car(self, admin):
        """Handle adding a new car"""
        car_id = st.text_input("Car ID")
        brand = st.text_input("Brand")
        model = st.text_input("Model")
        SeatingCapacity = st.number_input("Seating Capacity", step=1)
        price = st.number_input("Price per day (Rs)", min_value=0.0)

        if st.button("Add Car"):
            try:
                admin.add_car_to_system(car_id, brand, model, SeatingCapacity, price, True)
                st.success("Car added successfully.")
                st.rerun()
            except Exception as e:
                st.error(str(e))
    
    def _handle_remove_car(self, admin):
        """Handle removing a car"""
        car_ids = [car.car_id for car in self.rental_system.cars.values()]
        if not car_ids:
            st.warning("No cars in the system.")
        else:
            car_id = st.selectbox("Car ID to remove", car_ids)
            if st.button("Remove"):
                try:
                    admin.remove_car_from_system(car_id)
                    st.success("Car removed.")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
    
    def _handle_view_reserved_cars(self, admin):
        """Show reserved cars"""
        reserved = admin.print_reserved_cars()
        if not reserved:
            st.info("No cars are currently reserved.")
        else:
            st.subheader("Reserved Cars")
            df_reserved = pd.DataFrame(reserved)
            st.dataframe(df_reserved)
    
    def _handle_admin_rental_history(self, admin):
        """Show rental history for admin"""
        history = admin.print_rental_history()
        if not history:
            st.info("No rental history found.")
        else:
            st.subheader("Rental History")
            df_history = pd.DataFrame(history)
            st.dataframe(df_history)
    
    def run(self):
        """Main method to run the application"""
        st.title("🚗 Car Rental System")
        if not st.session_state.logged_in:
            page = st.sidebar.radio("Navigate", ["Login", "Sign Up"])
            if page == "Login":
                self.show_login()
            else:
                self.show_signup()
        else:
            if st.session_state.role.lower() == "admin":
                self.show_admin_dashboard()
            else:
                self.show_customer_dashboard()


# Instantiate and run the app
if __name__ == "__main__":
    app = CarRentalApp()
    app.run()