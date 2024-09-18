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



# Function to show the admin frame (right)
#def show_right_frame():
 #   login_frame.pack_forget()
  #  right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

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
        
       # clear_entries()
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
             #   clear_entries()  # Assuming clear_entries is defined elsewhere
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
            #clear_entries()
        else:
            messagebox.showinfo("Not Found", "No flight found with that flight number.")
    else:
        messagebox.showinfo("Alert", "Please enter a flight number to delete.")


# Initialize the Tkinter GUI
root = Tk()
root.title("Airline Management System")


right_frame = Frame(root, width=400, height=600, bg="lightgray")
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)



# RIGHT SIDE



        
heading_label = Label(right_frame, text="ADMINISTRATOR'S PANEL", font=("Arial", 20, "bold"), bg="lightgray")
heading_label.place(x=500, y=50)

Label(right_frame, text="Flight Number", font=("Calibri", 12, "bold"), bg="lightgray").place(x=550, y=150)
Label(right_frame, text="Origin", font=("Calibri", 12, "bold"), bg="lightgray").place(x=550, y=200)
Label(right_frame, text="Destination", font=("Calibri", 12, "bold"), bg="lightgray").place(x=550, y=250)
Label(right_frame, text="Departure Time", font=("Calibri", 12, "bold"), bg="lightgray").place(x=550, y=300)
Label(right_frame, text="Arrival Time", font=("Calibri", 12, "bold"), bg="lightgray").place(x=550, y=350)

flight_number_entry = Entry(right_frame)
origin_entry = Entry(right_frame)
destination_entry = Entry(right_frame)
departure_time_entry = Entry(right_frame)
arrival_time_entry = Entry(right_frame)

flight_number_entry.place(x=680, y=155)
origin_entry.place(x=680, y=205)
destination_entry.place(x=680, y=255)
departure_time_entry.place(x=680, y=305)
arrival_time_entry.place(x=680, y=355)

# Add button for registering flight information
add_button = Button(right_frame, text="Add Flight", command=add)
add_button.place(x=580, y=410)

# Search button for getting flight information
search_button = Button(right_frame, text="Search Flight", command=search)
search_button.place(x=680, y=410)

# Update button for updating flight information
update_button = Button(right_frame, text="Update Flight", command=update)
update_button.place(x=580, y=460)
                   
# Delete button for deleting flight information
delete_button = Button(right_frame, text="Delete Flight", command=delete)
delete_button.place(x=680, y=460)




root.geometry("1200x720")
root.mainloop()
