import sqlite3
import pandas as pd
from datetime import datetime

DATABASE_NAME = "data/database.db"

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            department TEXT,
            employee_id TEXT UNIQUE,
            role TEXT DEFAULT 'Employee',
            embedding BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    # Try to add columns if they don't exist (for migration)
    try:
        cursor.execute("ALTER TABLE Users ADD COLUMN age INTEGER")
    except: pass
    try:
        cursor.execute("ALTER TABLE Users ADD COLUMN department TEXT")
    except: pass
    try:
        cursor.execute("ALTER TABLE Users ADD COLUMN employee_id TEXT")
    except: pass
    
    # Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            check_in TIMESTAMP,
            check_out TIMESTAMP,
            duration REAL,
            category TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    ''')
    
    # Usage logs for rules (e.g., half-day tracking)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UsageLogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect(DATABASE_NAME)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
