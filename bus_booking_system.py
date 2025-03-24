import mysql.connector
import requests

# API to calculate GST (mock API for demonstration)
def calculate_gst(total_fare):
    gst_rate = 0.18  # 18% GST
    gst_amount = total_fare * gst_rate
    return gst_amount

class Booking:
    def __init__(self, name, seat_no, source, destination, email, total_fare):
        self.name = name
        self.seat_no = seat_no
        self.source = source
        self.destination = destination
        self.email = email
        self.total_fare = total_fare
        self.gst_amount = calculate_gst(total_fare)
        self.total_bill = total_fare + self.gst_amount

    def __str__(self):
        return (f"Seat No: {self.seat_no}, Name: {self.name}, Source: {self.source}, "
                f"Destination: {self.destination}, Email: {self.email}, Total Fare: {self.total_fare}, "
                f"GST Amount: {self.gst_amount}, Total Bill: {self.total_bill}")

class BusBookingSystem:
    def __init__(self):
        self.bookings = []
        self.conn = self.connect_to_db()
        self.create_table()

    def connect_to_db(self):
        try:
            # Connect to MySQL server (without specifying the database)
            conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Replace with your MySQL username
                password="12345"
            "  # Replace with your MySQL password
            )
            cursor = conn.cursor()

            # Check if the database exists
            cursor.execute("SHOW DATABASES LIKE 'bus_booking_db'")
            result = cursor.fetchone()

            # If the database doesn't exist, create it
            if not result:
                cursor.execute("CREATE DATABASE bus_booking_db")
                print("Database 'bus_booking_db' created successfully.")

            # Connect to the specific database
            conn.database = "bus_booking_db"
            return conn

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            exit(1)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                seat_no INT PRIMARY KEY,
                name VARCHAR(255),
                source VARCHAR(255),
                destination VARCHAR(255),
                email VARCHAR(255),
                total_fare DECIMAL(10, 2),
                gst_amount DECIMAL(10, 2),
                total_bill DECIMAL(10, 2)
            )
        ''')
        self.conn.commit()

    def book_seat(self):
        name = input("Enter name: ")
        seat_no = int(input("Enter seat number: "))
        source = input("Enter Source: ")
        destination = input("Enter Destination: ")
        email = input("Enter Email: ")
        total_fare = float(input("Enter Total Fare: "))

        new_booking = Booking(name, seat_no, source, destination, email, total_fare)
        self.bookings.append(new_booking)
        self.save_booking_to_db(new_booking)
        print("Seat booked successfully.")

    def save_booking_to_db(self, booking):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO bookings (seat_no, name, source, destination, email, total_fare, gst_amount, total_bill)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (booking.seat_no, booking.name, booking.source, booking.destination, booking.email, booking.total_fare, booking.gst_amount, booking.total_bill))
        self.conn.commit()

    def view_reservations(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM bookings')
        bookings = cursor.fetchall()

        if not bookings:
            print("No reservations made yet.")
            return

        print("All reservations:")
        print("Seat No.\tName\t\tSource\t\tDestination\tEmail\t\tTotal Fare\tGST Amount\tTotal Bill")
        
        for booking in bookings:
            print("------------------------------------------------------------------------------------------------------------------")
            print(f"{booking[0]}\t\t{booking[1]}\t\t{booking[2]}\t\t{booking[3]}\t\t{booking[4]}\t\t{booking[5]}\t\t{booking[6]}\t\t{booking[7]}")

    def edit_reservation(self):
        seat_to_edit = int(input("Enter seat number to edit: "))

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM bookings WHERE seat_no = %s', (seat_to_edit,))
        booking = cursor.fetchone()

        if booking:
            name = input("Enter new name: ")
            source = input("Enter new source: ")
            destination = input("Enter new destination: ")
            email = input("Enter new email: ")
            total_fare = float(input("Enter new total fare: "))
            gst_amount = calculate_gst(total_fare)
            total_bill = total_fare + gst_amount

            cursor.execute('''
                UPDATE bookings
                SET name = %s, source = %s, destination = %s, email = %s, total_fare = %s, gst_amount = %s, total_bill = %s
                WHERE seat_no = %s
            ''', (name, source, destination, email, total_fare, gst_amount, total_bill, seat_to_edit))
            self.conn.commit()
            print("Reservation edited successfully.")
        else:
            print("Reservation not found.")

    def print_ticket(self):
        seat_to_print = int(input("Enter seat number to print ticket: "))

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM bookings WHERE seat_no = %s', (seat_to_print,))
        booking = cursor.fetchone()

        if booking:
            print(f"Ticket for Seat No. {booking[0]}")
            print(f"Passenger Name: {booking[1]}")
            print(f"Passenger Source: {booking[2]}")
            print(f"Passenger Destination: {booking[3]}")
            print(f"Passenger Email: {booking[4]}")
            print(f"Total Fare: {booking[5]}")
            print(f"GST Amount: {booking[6]}")
            print(f"Total Bill: {booking[7]}")
        else:
            print("Reservation not found.")

    def close_connection(self):
        self.conn.close()

def main():
    system = BusBookingSystem()
    choice = 0

    while choice != 5:
        print("\nMini Bus Booking System")
        print("1. Book a seat")
        print("2. View reservations")
        print("3. Edit a reservation")
        print("4. Print a ticket")
        print("5. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            system.book_seat()
        elif choice == 2:
            system.view_reservations()
        elif choice == 3:
            system.edit_reservation()
        elif choice == 4:
            system.print_ticket()
        elif choice == 5:
            system.close_connection()
            print("Exiting...")
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()