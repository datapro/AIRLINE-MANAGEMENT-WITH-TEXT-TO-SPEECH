from gtts import gTTS
from tkinter import *
import tkinter.messagebox as messagebox  # Correcting import
import sqlite3
import os
import pygame

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

def add_flight():
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
        flight_info = f"Flight {flight_number} from {origin} to {destination} has been added. Departure at {departure_time} and arrival at {arrival_time}."
        text_to_speech(flight_info)
        
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

def clear_entries():
    flight_number_entry.delete(0, END)
    origin_entry.delete(0, END)
    destination_entry.delete(0, END)
    departure_time_entry.delete(0, END)
    arrival_time_entry.delete(0, END)

root = Tk()  # Changed tk.Tk() to Tk()
root.title("Airline Management System")

Label(root, text="Flight Number").grid(row=0, column=0)
Label(root, text="Origin").grid(row=1, column=0)
Label(root, text="Destination").grid(row=2, column=0)
Label(root, text="Departure Time").grid(row=3, column=0)
Label(root, text="Arrival Time").grid(row=4, column=0)

flight_number_entry = Entry(root)
origin_entry = Entry(root)
destination_entry = Entry(root)
departure_time_entry = Entry(root)
arrival_time_entry = Entry(root)

flight_number_entry.grid(row=0, column=1)
origin_entry.grid(row=1, column=1)
destination_entry.grid(row=2, column=1)
departure_time_entry.grid(row=3, column=1)
arrival_time_entry.grid(row=4, column=1)

add_button = Button(root, text="Add Flight", command=add_flight)
add_button.grid(row=5, column=0, columnspan=2)

root.mainloop()
