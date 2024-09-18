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

# Initialize the Tkinter GUI
root = Tk()
root.title("Airline Management System")

left_frame = Frame(root, width=400, height=600, bg="lightblue")
left_frame.pack(side=LEFT, fill=BOTH, expand=True)

# LEFT SIDE





right_heading_label = Label(left_frame, text="Passenger Management", font=("Arial", 20, "bold"), bg="lightblue")
right_heading_label.place(x=500, y=100)

path='image/user.png'
img=ImageTk.PhotoImage(Image.open(path))
limage=Label(left_frame, image=img, height=100, width=100, bg="lightblue")
limage.place(x=600, y=0)

# put passenger input fields
Label(left_frame, text="Passenger Name", font=("Calibri", 12, "bold"), bg="lightblue").place(x=530, y=187)
name_entry = Entry(left_frame)
name_entry.place(x=670, y=190)

Label(left_frame, text="Passenger Age", font=("Calibri", 12, "bold"), bg="lightblue").place(x=530, y=237)
age_entry = Entry(left_frame)
age_entry.place(x=670, y=240)

Label(left_frame, text="Passenger Gender", font=("Calibri", 12, "bold"), bg="lightblue").place(x=530, y=287)
gender_entry = Entry(left_frame)
gender_entry.place(x=670, y=290)

Label(left_frame, text="Passport Number", font=("Calibri", 12, "bold"), bg="lightblue").place(x=530, y=337)
passport_number_entry = Entry(left_frame)
passport_number_entry.place(x=670, y=340)

Label(left_frame, text="Contact Info", font=("Calibri", 12, "bold"), bg="lightblue").place(x=530, y=387)
contact_info_entry = Entry(left_frame)
contact_info_entry.place(x=670, y=390)

Label(left_frame, text="Passenger ID", font=("Calibri", 12, "bold"), bg="lightblue").place(x=530, y=477)
passenger_id_entry = Entry(left_frame)
passenger_id_entry.place(x=670, y=480)

Label(left_frame, text="flight ID", font=("Calibri", 12, "bold"), bg="lightblue").place(x=530, y=527)
flight_id_entry = Entry(left_frame)
flight_id_entry.place(x=670, y=530)

save_button = Button(left_frame, text="Save", command=save_passenger, bg="green", fg="white")
save_button.place(x=670, y=430)

book_button = Button(left_frame, text="Book flight", command=submit_booking, fg="green", bg="white")
book_button.place(x=670, y=570)


root.geometry("1200x720")
root.mainloop()
