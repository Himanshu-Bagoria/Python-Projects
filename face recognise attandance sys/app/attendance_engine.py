from app.database import get_db_connection
from datetime import datetime, timedelta
import pandas as pd

def check_in(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if already checked in today and not checked out
    cursor.execute('''
        SELECT id FROM Attendance 
        WHERE user_id = ? AND check_out IS NULL 
        AND date(check_in) = date('now')
    ''', (user_id,))
    
    if cursor.fetchone():
        conn.close()
        return False, "Already checked in or not checked out from last session."
    
    # Insert new record
    cursor.execute('''
        INSERT INTO Attendance (user_id, check_in) 
        VALUES (?, ?)
    ''', (user_id, datetime.now()))
    
    conn.commit()
    conn.close()
    return True, "Check-in successful."

def check_out(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get active session
    cursor.execute('''
        SELECT id, check_in FROM Attendance 
        WHERE user_id = ? AND check_out IS NULL 
        ORDER BY check_in DESC LIMIT 1
    ''', (user_id,))
    
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "No active check-in found."
    
    attendance_id, check_in_time_str = row
    check_in_time = datetime.strptime(check_in_time_str, '%Y-%m-%d %H:%M:%S.%f')
    check_out_time = datetime.now()
    duration = (check_out_time - check_in_time).total_seconds() / 3600
    
    # Apply Rules
    category = "Full Day"
    if duration < 1:
        conn.close()
        return False, "Emergency Exit: Allowed only after 1 hour of entry."
    elif duration < 4:
        category = "Emergency"
    elif duration < 8:
        # Check half-day limit (5 per month)
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        cursor.execute('''
            SELECT COUNT(*) FROM Attendance 
            WHERE user_id = ? AND category = 'Half Day' 
            AND check_out >= ?
        ''', (user_id, month_start))
        
        half_day_count = cursor.fetchone()[0]
        if half_day_count >= 5:
            # Maybe restrict or just log? System auto-tracks usage.
            # We'll allow it but log it as exceeding or just let it be.
            # User requirement: "Half Day Exit: Allowed only 5 times per month (system auto‑tracks usage)."
            # Let's block it if it exceeds 5.
            conn.close()
            return False, f"Half Day Limit exceeded (5 per month). Current count: {half_day_count}"
        category = "Half Day"
    
    # Update attendance
    cursor.execute('''
        UPDATE Attendance 
        SET check_out = ?, duration = ?, category = ? 
        WHERE id = ?
    ''', (check_out_time, round(duration, 2), category, attendance_id))
    
    conn.commit()
    conn.close()
    return True, f"Check-out successful. Category: {category}. Duration: {round(duration, 2)} hrs."

def get_today_attendance():
    conn = get_db_connection()
    df = pd.read_sql_query('''
        SELECT u.name, a.check_in, a.check_out, a.duration, a.category 
        FROM Attendance a 
        JOIN Users u ON a.user_id = u.id 
        WHERE date(a.check_in) = date('now')
    ''', conn)
    conn.close()
    return df
