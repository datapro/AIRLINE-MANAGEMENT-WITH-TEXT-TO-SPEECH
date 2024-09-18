import sqlite3

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
