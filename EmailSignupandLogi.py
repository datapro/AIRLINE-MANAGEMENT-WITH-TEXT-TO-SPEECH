import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess  

# Database setup
def setup_database():
    conn = sqlite3.connect('airline_manage.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            position TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to handle signup logic
def signup():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    position = entry_position.get()
    password = entry_password.get()

    if first_name == "" or last_name == "" or email == "" or position == "" or password == "":
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    conn = sqlite3.connect('airline_manage.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, position, password) 
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, position, password))

        conn.commit()
        messagebox.showinfo("Success", "User registered successfully")
        clear_fields()
        root.destroy()
        show_login_page()  # Open the login page after successful signup
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already exists")
    finally:
        conn.close()

# Function to clear input fields after signup
def clear_fields():
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_password.delete(0, tk.END)

# Function to show the login page
def show_login_page():
    login_window = tk.Tk()
    login_window.title("Login Page")
    login_window.geometry("400x300")

    # Labels and entry fields for login
    tk.Label(login_window, text="First Name").pack(pady=5)
    login_first_name = tk.Entry(login_window)
    login_first_name.pack(pady=5)

    tk.Label(login_window, text="Position (Flight Attendant/Admin)").pack(pady=5)
    login_position = tk.Entry(login_window)
    login_position.pack(pady=5)

    tk.Label(login_window, text="Password").pack(pady=5)
    login_password = tk.Entry(login_window, show='*')
    login_password.pack(pady=5)

    def login():
        first_name = login_first_name.get()
        position = login_position.get()
        password = login_password.get()

        if first_name == "" or position == "" or password == "":
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        conn = sqlite3.connect('airline_manage.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users WHERE first_name = ? AND position = ? AND password = ?
        ''', (first_name, position, password))

        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Success", "Login successful")
            login_window.destroy()  
            if position.lower() == "admin":
                open_admin_page()  
            elif position.lower() == "flight attendant":
                open_flight_attendant_page()  
            else:
                messagebox.showerror("Error", "Invalid position. Please choose Admin or Flight Attendant.")
        else:
            messagebox.showerror("Error", "Invalid credentials")

    # Login button
    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack(pady=20)

    login_window.mainloop()

# Function to open admin.py page
def open_admin_page():
    # This will open admin.py as a separate process.
    subprocess.Popen(["python", "admin.py"])  

# Function to open flight.py page
def open_flight_attendant_page():
    # This will open flight.py as a separate process.
    subprocess.Popen(["python", "flight.py"])  

# Main application setup (Signup Page)
def main_app():
    global entry_first_name, entry_last_name, entry_email, entry_position, entry_password, root

    root = tk.Tk()
    root.title("Airline Management Signup")
    root.geometry("400x400")

    # Labels and entry fields
    tk.Label(root, text="First Name").pack(pady=5)
    entry_first_name = tk.Entry(root)
    entry_first_name.pack(pady=5)

    tk.Label(root, text="Last Name").pack(pady=5)
    entry_last_name = tk.Entry(root)
    entry_last_name.pack(pady=5)

    tk.Label(root, text="Email").pack(pady=5)
    entry_email = tk.Entry(root)
    entry_email.pack(pady=5)

    tk.Label(root, text="Position (Flight Attendant/Admin)").pack(pady=5)
    entry_position = tk.Entry(root)
    entry_position.pack(pady=5)

    tk.Label(root, text="Password").pack(pady=5)
    entry_password = tk.Entry(root, show='*')
    entry_password.pack(pady=5)

    # Signup button
    signup_button = tk.Button(root, text="Sign Up", command=signup)
    signup_button.pack(pady=20)

    root.mainloop()

# Initialize the database and start the application
if __name__ == "__main__":
    setup_database()
    main_app()