from gtts import gTTS
from tkinter import *
import tkinter.messagebox as messagebox
import sqlite3
import os
import pygame
from PIL import ImageTk,Image
import random


# Initialize SQLite database
def setup_database():
    conn = sqlite3.connect('airline_management.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number VARCHAR NOT NULL,
            origin VARCHAR NOT NULL,
            destination VARCHAR NOT NULL,
            departure_time VARCHAR NOT NULL,
            arrival_time VARCHAR NOT NULL
        )
    ''')
    
     # Create passengers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passengers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            passport_number TEXT UNIQUE NOT NULL,
            contact_info TEXT NOT NULL
        )
    ''')
    
    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_id INTEGER NOT NULL,
            flight_id INTEGER NOT NULL,
            seat_number TEXT,
            FOREIGN KEY(passenger_id) REFERENCES passengers(id),
            FOREIGN KEY(flight_id) REFERENCES flights(id)
        )
    ''')
    
    conn.commit()
    conn.close()

setup_database()
    
# Text-to-Speech function
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    audio_file = "flight_info.mp3"
    tts.save(audio_file)
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():  # Wait until the audio finishes playing
        continue
    
    pygame.mixer.quit()  # Properly quit the mixer
    os.remove(audio_file)  # Remove the audio file after playing

# Function to add a flight to the database

def add():
    flight_number = flight_number_entry.get()
    origin = origin_entry.get()
    destination = destination_entry.get()
    departure_time = departure_time_entry.get()
    arrival_time = arrival_time_entry.get()

    if flight_number and origin and destination and departure_time and arrival_time:
        conn = sqlite3.connect('airline_management.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO flights (flight_number, origin, destination, departure_time, arrival_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (flight_number, origin, destination, departure_time, arrival_time))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Flight added successfully!")
        
        # Text-to-Speech
        flight_info = f"Flight {flight_number} from {origin} to {destination} has been successfully added. Departure at {departure_time} and arrival at {arrival_time}."
        text_to_speech(flight_info)
        
        clear_entries()
    else:
        messagebox.showinfo("Alert", "Please fill in all fields.")

# Function to retrieve and announce flight information
def search():
    flight_number = flight_number_entry.get()

    if flight_number:
        conn = sqlite3.connect('airline_management.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT flight_number, origin, destination, departure_time, arrival_time
            FROM flights
            WHERE flight_number = ?
        ''', (flight_number,))
        
        result = cursor.fetchone()
        conn.close()

        if result:
            flight_info = f"Flight {result[0]} from {result[1]} to {result[2]} departs at {result[3]} and arrives at {result[4]}."
            text_to_speech(flight_info)
        else:
            messagebox.showinfo("Not Found", "No flight found with that flight number.")
    else:
        messagebox.showinfo("Alert", "Please enter a flight number to search.")

#  Function to update a flight
def update():
    flight_number = flight_number_entry.get()
    origin = origin_entry.get()
    destination = destination_entry.get()
    departure_time = departure_time_entry.get()
    arrival_time = arrival_time_entry.get()

    if flight_number and origin and destination and departure_time and arrival_time:
            conn = sqlite3.connect('airline_management.db')
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE flights 
                SET origin = ?, destination = ?, departure_time = ?, arrival_time = ? 
                WHERE flight_number = ?
            ''', (origin, destination, departure_time, arrival_time, flight_number))

            conn.commit()

            if cursor.rowcount > 0:  # Check if any rows were updated
                messagebox.showinfo("Success", f"Flight {flight_number} updated successfully.")
                
                flight_info = (f"Flight {flight_number} has been successfully updated. "
                               f"It will now depart from {origin} to {destination} at {departure_time} "
                               f"and arrive at {arrival_time}.")
                text_to_speech(flight_info)  # Assuming text_to_speech is defined elsewhere
                clear_entries()  # Assuming clear_entries is defined elsewhere
            else:
                messagebox.showinfo("Not Found", "No flight found with that flight number.")
    else:
        messagebox.showinfo("Alert", "Please fill in all fields.")


# Function to delete a flight
def delete():
    flight_number = flight_number_entry.get()

    if flight_number:
        conn = sqlite3.connect('airline_management.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM flights WHERE flight_number = ?
        ''', (flight_number,))
        
        conn.commit()
        conn.close()

        if cursor.xcount > 0:
            messagebox.showinfo("Success", f"Flight {flight_number} deleted successfully.")
            flight_info = f"Flight {flight_number} has been successfully deleted."
            text_to_speech(flight_info)
            clear_entries()
        else:
            messagebox.showinfo("Not Found", "No flight found with that flight number.")
    else:
        messagebox.showinfo("Alert", "Please enter a flight number to delete.")

# function to save passenger info
def save_passenger():
    # Get the input values from the entry fields
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()
    passport_number = passport_number_entry.get()
    contact_info = contact_info_entry.get()

    # Ensure all fields are filled
    if (name=="" or age=="" or gender=="" or passport_number=="" or contact_info==""):
        messagebox.showinfo("Alert", "Please fill in all the fields.")
        return

    # to connect to the database
    conn = sqlite3.connect('airline_management.db')
    cursor = conn.cursor()

    # to check if the passport number already exists
    cursor.execute('''
        SELECT COUNT(*) FROM passengers WHERE passport_number = ?
    ''', (passport_number,))
    exists = cursor.fetchone()[0]

    if exists:
        messagebox.showerror("Error", "A passenger with this passport number already exists.")
    else:
        cursor.execute('''
            INSERT INTO passengers (name, age, gender, passport_number, contact_info)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, age, gender, passport_number, contact_info))

        conn.commit()
        messagebox.showinfo("Success", f"Passenger {name} added successfully.")
        name_entry.delete(0, END)
        age_entry.delete(0, END)
        gender_entry.delete(0, END)
        contact_info_entry.delete(0, END)
    
    conn.close()
    
def generate_seat_number():
    seat_number = f"{random.randint(1, 150):03d}-"  # Generate seat number between 001 and 150
    seat_row = random.choice(['A', 'B', 'C', 'D'])  # Randomly select a row
    return seat_number + seat_row

def book_flight(passenger_id, flight_id):
    # Connect to the database
    conn = sqlite3.connect('airline_management.db')
    cursor = conn.cursor()

# Check if the passenger_id is already booked for the given flight_id
    cursor.execute('''
        SELECT COUNT(*) FROM bookings
        WHERE passenger_id = ? AND flight_id = ?
    ''', (passenger_id, flight_id))
    already_booked = cursor.fetchone()[0]

    if already_booked:
        messagebox.showwarning("Booking Error", "This passenger is already booked on this flight.")
    else:
        # Generate a random seat number only if booking is valid
        seat_number = generate_seat_number()
        
        # Insert the booking data into the bookings table
        cursor.execute('''
            INSERT INTO bookings (passenger_id, flight_id, seat_number)
            VALUES (?, ?, ?)
        ''', (passenger_id, flight_id, seat_number))

    # Commit the changes
    conn.commit()
    messagebox.showinfo("Success", f"Flight booked successfully! Seat number: {seat_number}")

    passport_number_entry.delete(0, END)
    passenger_id_entry.delete(0, END)
    flight_id_entry.delete(0, END)


    # Close the connection
    conn.close()
    
def submit_booking():
        try:
            passenger_id = passenger_id_entry.get()
            flight_id = flight_id_entry.get()
            book_flight(passenger_id, flight_id)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid numeric IDs.")


# Function to clear the input fields
def clear_entries():
    flight_number_entry.delete(0, END)
    origin_entry.delete(0, END)
    destination_entry.delete(0, END)
    departure_time_entry.delete(0, END)
    arrival_time_entry.delete(0, END)
    

# Initialize the Tkinter GUI
root = Tk()
root.title("Airline Management System")

left_frame = Frame(root, width=400, height=600, bg="lightblue")
left_frame.pack(side=LEFT, fill=BOTH, expand=True)

right_frame = Frame(root, width=400, height=600, bg="lightgray")
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)
 



# RIGHT SIDE



        
heading_label = Label(right_frame, text="ADMINISTRATOR'S PANEL", font=("Arial", 20, "bold"), bg="lightgray")
heading_label.place(x=100, y=15)

Label(right_frame, text="Flight Number", font=("Calibri", 12, "bold"), bg="lightgray").place(x=150, y=120)
Label(right_frame, text="Origin", font=("Calibri", 12, "bold"), bg="lightgray").place(x=150, y=170)
Label(right_frame, text="Destination", font=("Calibri", 12, "bold"), bg="lightgray").place(x=150, y=220)
Label(right_frame, text="Departure Time", font=("Calibri", 12, "bold"), bg="lightgray").place(x=150, y=270)
Label(right_frame, text="Arrival Time", font=("Calibri", 12, "bold"), bg="lightgray").place(x=150, y=320)

flight_number_entry = Entry(right_frame)
origin_entry = Entry(right_frame)
destination_entry = Entry(right_frame)
departure_time_entry = Entry(right_frame)
arrival_time_entry = Entry(right_frame)

flight_number_entry.place(x=280, y=125)
origin_entry.place(x=280, y=175)
destination_entry.place(x=280, y=225)
departure_time_entry.place(x=280, y=275)
arrival_time_entry.place(x=280, y=325)

# Add button for registering flight information
add_button = Button(right_frame, text="Add Flight", command=add)
add_button.place(x=180, y=380)

# Search button for getting flight information
search_button = Button(right_frame, text="Search Flight", command=search)
search_button.place(x=280, y=380)

# Update button for updating flight information
update_button = Button(right_frame, text="Update Flight", command=update)
update_button.place(x=180, y=430)
                   
# Delete button for deleting flight information
delete_button = Button(right_frame, text="Delete Flight", command=delete)
delete_button.place(x=280, y=430)



# LEFT SIDE





right_heading_label = Label(left_frame, text="Passenger Management", font=("Arial", 20, "bold"), bg="lightblue")
right_heading_label.place(x=170, y=100)

# put an image

path='image/user.png'
img=ImageTk.PhotoImage(Image.open(path))
limage=Label(left_frame, image=img, height=100, width=100, bg="lightblue")
limage.place(x=250, y=0)

# put passenger input fields
Label(left_frame, text="Passenger Name", font=("Calibri", 12, "bold"), bg="lightblue").place(x=190, y=167)
name_entry = Entry(left_frame)
name_entry.place(x=330, y=170)

Label(left_frame, text="Passenger Age", font=("Calibri", 12, "bold"), bg="lightblue").place(x=190, y=217)
age_entry = Entry(left_frame)
age_entry.place(x=330, y=220)

Label(left_frame, text="Passenger Gender", font=("Calibri", 12, "bold"), bg="lightblue").place(x=190, y=267)
gender_entry = Entry(left_frame)
gender_entry.place(x=330, y=270)

Label(left_frame, text="Passport Number", font=("Calibri", 12, "bold"), bg="lightblue").place(x=190, y=317)
passport_number_entry = Entry(left_frame)
passport_number_entry.place(x=330, y=320)

Label(left_frame, text="Contact Info", font=("Calibri", 12, "bold"), bg="lightblue").place(x=190, y=367)
contact_info_entry = Entry(left_frame)
contact_info_entry.place(x=330, y=370)

Label(left_frame, text="Passenger ID", font=("Calibri", 12, "bold"), bg="lightblue").place(x=190, y=457)
passenger_id_entry = Entry(left_frame)
passenger_id_entry.place(x=330, y=460)

Label(left_frame, text="flight ID", font=("Calibri", 12, "bold"), bg="lightblue").place(x=190, y=507)
flight_id_entry = Entry(left_frame)
flight_id_entry.place(x=330, y=510)

save_button = Button(left_frame, text="Save", command=save_passenger, bg="green", fg="white")
save_button.place(x=330, y=410)

book_button = Button(left_frame, text="Book flight", command=submit_booking, fg="green", bg="white")
book_button.place(x=330, y=550)


root.geometry("1200x720")
root.mainloop()
