import sqlite3
import pandas as pd
import hashlib
import datetime
from contextlib import contextmanager
import json
import os

class HospitalDatabase:
    def __init__(self, db_path="data/hospital.db"):
        self.db_path = db_path
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database with all required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table for authentication
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'patient',
                    email TEXT UNIQUE,
                    phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # User profiles table for detailed personal information
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    date_of_birth DATE,
                    gender TEXT,
                    blood_group TEXT,
                    address TEXT,
                    city TEXT,
                    state TEXT,
                    postal_code TEXT,
                    country TEXT DEFAULT 'India',
                    emergency_contact_name TEXT,
                    emergency_contact_phone TEXT,
                    emergency_contact_relation TEXT,
                    profile_picture TEXT,
                    bio TEXT,
                    medical_history TEXT,
                    allergies TEXT,
                    chronic_conditions TEXT,
                    current_medications TEXT,
                    insurance_provider TEXT,
                    insurance_policy_number TEXT,
                    insurance_expiry DATE,
                    preferred_language TEXT DEFAULT 'English',
                    notification_preferences TEXT,
                    privacy_settings TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # User sessions table for tracking active sessions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # User preferences table for app settings
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    theme TEXT DEFAULT 'light',
                    language TEXT DEFAULT 'English',
                    timezone TEXT DEFAULT 'Asia/Kolkata',
                    date_format TEXT DEFAULT 'DD/MM/YYYY',
                    time_format TEXT DEFAULT '24',
                    email_notifications BOOLEAN DEFAULT 1,
                    sms_notifications BOOLEAN DEFAULT 1,
                    push_notifications BOOLEAN DEFAULT 1,
                    appointment_reminders BOOLEAN DEFAULT 1,
                    medication_reminders BOOLEAN DEFAULT 1,
                    health_tips BOOLEAN DEFAULT 1,
                    newsletter BOOLEAN DEFAULT 0,
                    data_sharing BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # Patients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    patient_id TEXT UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    date_of_birth DATE,
                    gender TEXT,
                    blood_group TEXT,
                    address TEXT,
                    emergency_contact TEXT,
                    medical_history TEXT,
                    allergies TEXT,
                    insurance_info TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Doctors table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS doctors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    doctor_id TEXT UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    specialization TEXT NOT NULL,
                    qualification TEXT,
                    experience_years INTEGER,
                    department TEXT,
                    consultation_fee REAL,
                    available_days TEXT,
                    available_hours TEXT,
                    rating REAL DEFAULT 0.0,
                    total_reviews INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Appointments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    appointment_id TEXT UNIQUE NOT NULL,
                    patient_id TEXT NOT NULL,
                    doctor_id TEXT NOT NULL,
                    appointment_date DATE NOT NULL,
                    appointment_time TIME NOT NULL,
                    status TEXT DEFAULT 'scheduled',
                    type TEXT DEFAULT 'consultation',
                    reason TEXT,
                    notes TEXT,
                    fee REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
            ''')
            
            # Medical records table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS medical_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_id TEXT UNIQUE NOT NULL,
                    patient_id TEXT NOT NULL,
                    doctor_id TEXT NOT NULL,
                    appointment_id TEXT,
                    diagnosis TEXT,
                    symptoms TEXT,
                    treatment TEXT,
                    prescriptions TEXT,
                    lab_results TEXT,
                    vitals TEXT,
                    record_date DATE NOT NULL,
                    follow_up_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
                    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
                )
            ''')
            
            # Prescriptions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prescriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prescription_id TEXT UNIQUE NOT NULL,
                    patient_id TEXT NOT NULL,
                    doctor_id TEXT NOT NULL,
                    record_id TEXT,
                    medications TEXT NOT NULL,
                    dosage TEXT,
                    frequency TEXT,
                    duration TEXT,
                    instructions TEXT,
                    issued_date DATE NOT NULL,
                    expiry_date DATE,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
                    FOREIGN KEY (record_id) REFERENCES medical_records(record_id)
                )
            ''')
            
            # Lab tests table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS lab_tests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_id TEXT UNIQUE NOT NULL,
                    patient_id TEXT NOT NULL,
                    doctor_id TEXT NOT NULL,
                    test_name TEXT NOT NULL,
                    test_type TEXT,
                    ordered_date DATE NOT NULL,
                    scheduled_date DATE,
                    completed_date DATE,
                    results TEXT,
                    status TEXT DEFAULT 'ordered',
                    lab_technician TEXT,
                    normal_range TEXT,
                    remarks TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
                )
            ''')
            
            # Billing table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS billing (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bill_id TEXT UNIQUE NOT NULL,
                    patient_id TEXT NOT NULL,
                    appointment_id TEXT,
                    service_type TEXT NOT NULL,
                    description TEXT,
                    amount REAL NOT NULL,
                    tax_amount REAL DEFAULT 0.0,
                    total_amount REAL NOT NULL,
                    payment_status TEXT DEFAULT 'pending',
                    payment_method TEXT,
                    insurance_coverage REAL DEFAULT 0.0,
                    bill_date DATE NOT NULL,
                    due_date DATE,
                    paid_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
                )
            ''')
            
            # Ward management table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS wards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ward_id TEXT UNIQUE NOT NULL,
                    ward_name TEXT NOT NULL,
                    ward_type TEXT NOT NULL,
                    total_beds INTEGER NOT NULL,
                    occupied_beds INTEGER DEFAULT 0,
                    department TEXT,
                    floor_number INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Bed assignments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bed_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assignment_id TEXT UNIQUE NOT NULL,
                    ward_id TEXT NOT NULL,
                    bed_number INTEGER NOT NULL,
                    patient_id TEXT,
                    admission_date DATE,
                    discharge_date DATE,
                    status TEXT DEFAULT 'available',
                    daily_rate REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ward_id) REFERENCES wards(ward_id),
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
            ''')
            
            # System logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    table_name TEXT,
                    record_id TEXT,
                    old_values TEXT,
                    new_values TEXT,
                    ip_address TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Medicines/Medications table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS medicines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    medicine_id TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    generic_name TEXT,
                    brand_name TEXT,
                    category TEXT NOT NULL,
                    type TEXT NOT NULL,
                    strength TEXT,
                    unit TEXT,
                    manufacturer TEXT,
                    description TEXT,
                    indications TEXT,
                    contraindications TEXT,
                    side_effects TEXT,
                    dosage_form TEXT,
                    route_of_administration TEXT,
                    storage_conditions TEXT,
                    shelf_life TEXT,
                    price REAL,
                    stock_quantity INTEGER DEFAULT 0,
                    minimum_stock INTEGER DEFAULT 10,
                    prescription_required BOOLEAN DEFAULT 1,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            
            # Create default admin user if not exists
            self.create_default_admin()
            
            # Create sample medicines if not exists
            self.create_default_medicines()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_default_admin(self):
        """Create default admin user"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if admin exists
            cursor.execute("SELECT id FROM users WHERE username = 'admin'")
            if not cursor.fetchone():
                admin_password = self.hash_password("admin123")
                cursor.execute('''
                    INSERT INTO users (username, password_hash, role, email)
                    VALUES (?, ?, ?, ?)
                ''', ("admin", admin_password, "admin", "admin@hospital.com"))
                conn.commit()
    
    def authenticate_user(self, username, password):
        """Authenticate user and return user data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                SELECT id, username, role, email FROM users 
                WHERE username = ? AND password_hash = ? AND is_active = 1
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            if user:
                # Update last login
                cursor.execute('''
                    UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
                ''', (user['id'],))
                conn.commit()
                
                return dict(user)
            return None
    
    def create_user(self, username, password, role, email=None, phone=None):
        """Create new user"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            
            try:
                cursor.execute('''
                    INSERT INTO users (username, password_hash, role, email, phone)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, password_hash, role, email, phone))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None
    
    def get_patients(self, limit=None):
        """Get all patients"""
        with self.get_connection() as conn:
            query = "SELECT * FROM patients ORDER BY created_at DESC"
            if limit:
                query += f" LIMIT {limit}"
            return pd.read_sql_query(query, conn)
    
    def get_doctors(self, department=None):
        """Get all doctors, optionally filtered by department"""
        with self.get_connection() as conn:
            if department:
                query = "SELECT * FROM doctors WHERE department = ? ORDER BY last_name"
                return pd.read_sql_query(query, conn, params=[department])
            else:
                query = "SELECT * FROM doctors ORDER BY last_name"
                return pd.read_sql_query(query, conn)
    
    def get_appointments(self, patient_id=None, doctor_id=None, date=None):
        """Get appointments with optional filters"""
        with self.get_connection() as conn:
            query = "SELECT * FROM appointments WHERE 1=1"
            params = []
            
            if patient_id:
                query += " AND patient_id = ?"
                params.append(patient_id)
            if doctor_id:
                query += " AND doctor_id = ?"
                params.append(doctor_id)
            if date:
                query += " AND appointment_date = ?"
                params.append(date)
            
            query += " ORDER BY appointment_date DESC, appointment_time DESC"
            return pd.read_sql_query(query, conn, params=params)
    
    def create_appointment(self, appointment_data):
        """Create new appointment"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Generate appointment ID
            appointment_id = f"APT{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            cursor.execute('''
                INSERT INTO appointments 
                (appointment_id, patient_id, doctor_id, appointment_date, appointment_time, 
                 reason, type, fee, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                appointment_id,
                appointment_data.get('patient_id'),
                appointment_data.get('doctor_id'),
                appointment_data.get('appointment_date'),
                appointment_data.get('appointment_time'),
                appointment_data.get('reason'),
                appointment_data.get('type', 'consultation'),
                appointment_data.get('fee'),
                'scheduled'
            ))
            
            conn.commit()
            return appointment_id
    
    def log_action(self, user_id, action, table_name=None, record_id=None, old_values=None, new_values=None):
        """Log user actions for audit trail"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO system_logs 
                (user_id, action, table_name, record_id, old_values, new_values)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id, action, table_name, record_id,
                json.dumps(old_values) if old_values else None,
                json.dumps(new_values) if new_values else None
            ))
            
            conn.commit()
    
    def get_dashboard_stats(self):
        """Get statistics for dashboard"""
        with self.get_connection() as conn:
            stats = {}
            
            # Total patients
            stats['total_patients'] = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
            
            # Total doctors
            stats['total_doctors'] = conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
            
            # Today's appointments
            today = datetime.date.today()
            stats['todays_appointments'] = conn.execute(
                "SELECT COUNT(*) FROM appointments WHERE appointment_date = ?", 
                (today,)
            ).fetchone()[0]
            
            # Pending appointments
            stats['pending_appointments'] = conn.execute(
                "SELECT COUNT(*) FROM appointments WHERE status = 'scheduled'"
            ).fetchone()[0]
            
            # Revenue this month
            current_month = datetime.date.today().strftime('%Y-%m')
            stats['monthly_revenue'] = conn.execute(
                "SELECT COALESCE(SUM(total_amount), 0) FROM billing WHERE strftime('%Y-%m', bill_date) = ?",
                (current_month,)
            ).fetchone()[0]
            
            return stats
    
    def create_default_medicines(self):
        """Create default medicines if not exists"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if medicines exist
            cursor.execute("SELECT COUNT(*) FROM medicines")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Add common medicines
                medicines = [
                    {
                        'medicine_id': 'MED001',
                        'name': 'Paracetamol',
                        'generic_name': 'Acetaminophen',
                        'brand_name': 'Tylenol',
                        'category': 'Analgesic',
                        'type': 'Tablet',
                        'strength': '500mg',
                        'unit': 'mg',
                        'manufacturer': 'Generic Pharma',
                        'description': 'Pain reliever and fever reducer',
                        'indications': 'Fever, headache, body pain, cold symptoms',
                        'contraindications': 'Liver disease, alcohol dependency',
                        'side_effects': 'Nausea, allergic reactions (rare)',
                        'dosage_form': 'Tablet',
                        'route_of_administration': 'Oral',
                        'storage_conditions': 'Store at room temperature',
                        'shelf_life': '3 years',
                        'price': 2.50,
                        'stock_quantity': 1000,
                        'minimum_stock': 100
                    },
                    {
                        'medicine_id': 'MED002',
                        'name': 'Ibuprofen',
                        'generic_name': 'Ibuprofen',
                        'brand_name': 'Advil',
                        'category': 'NSAID',
                        'type': 'Tablet',
                        'strength': '400mg',
                        'unit': 'mg',
                        'manufacturer': 'Generic Pharma',
                        'description': 'Anti-inflammatory and pain reliever',
                        'indications': 'Pain, inflammation, fever',
                        'contraindications': 'Stomach ulcers, kidney disease',
                        'side_effects': 'Stomach upset, dizziness',
                        'dosage_form': 'Tablet',
                        'route_of_administration': 'Oral',
                        'storage_conditions': 'Store at room temperature',
                        'shelf_life': '3 years',
                        'price': 3.00,
                        'stock_quantity': 800,
                        'minimum_stock': 80
                    },
                    {
                        'medicine_id': 'MED003',
                        'name': 'Amoxicillin',
                        'generic_name': 'Amoxicillin',
                        'brand_name': 'Amoxil',
                        'category': 'Antibiotic',
                        'type': 'Capsule',
                        'strength': '250mg',
                        'unit': 'mg',
                        'manufacturer': 'Generic Pharma',
                        'description': 'Broad-spectrum antibiotic',
                        'indications': 'Bacterial infections',
                        'contraindications': 'Penicillin allergy',
                        'side_effects': 'Nausea, diarrhea, allergic reactions',
                        'dosage_form': 'Capsule',
                        'route_of_administration': 'Oral',
                        'storage_conditions': 'Store in cool, dry place',
                        'shelf_life': '2 years',
                        'price': 5.50,
                        'stock_quantity': 500,
                        'minimum_stock': 50,
                        'prescription_required': 1
                    },
                    {
                        'medicine_id': 'MED004',
                        'name': 'Cetirizine',
                        'generic_name': 'Cetirizine',
                        'brand_name': 'Zyrtec',
                        'category': 'Antihistamine',
                        'type': 'Tablet',
                        'strength': '10mg',
                        'unit': 'mg',
                        'manufacturer': 'Generic Pharma',
                        'description': 'Antihistamine for allergies',
                        'indications': 'Allergic rhinitis, urticaria',
                        'contraindications': 'Severe kidney disease',
                        'side_effects': 'Drowsiness, dry mouth',
                        'dosage_form': 'Tablet',
                        'route_of_administration': 'Oral',
                        'storage_conditions': 'Store at room temperature',
                        'shelf_life': '3 years',
                        'price': 4.00,
                        'stock_quantity': 600,
                        'minimum_stock': 60
                    },
                    {
                        'medicine_id': 'MED005',
                        'name': 'Metformin',
                        'generic_name': 'Metformin',
                        'brand_name': 'Glucophage',
                        'category': 'Antidiabetic',
                        'type': 'Tablet',
                        'strength': '500mg',
                        'unit': 'mg',
                        'manufacturer': 'Generic Pharma',
                        'description': 'Diabetes medication',
                        'indications': 'Type 2 diabetes mellitus',
                        'contraindications': 'Kidney disease, severe heart failure',
                        'side_effects': 'Nausea, diarrhea, metallic taste',
                        'dosage_form': 'Tablet',
                        'route_of_administration': 'Oral',
                        'storage_conditions': 'Store at room temperature',
                        'shelf_life': '3 years',
                        'price': 6.00,
                        'stock_quantity': 400,
                        'minimum_stock': 40,
                        'prescription_required': 1
                    }
                ]
                
                for med in medicines:
                    cursor.execute('''
                        INSERT INTO medicines (
                            medicine_id, name, generic_name, brand_name, category, type,
                            strength, unit, manufacturer, description, indications,
                            contraindications, side_effects, dosage_form, route_of_administration,
                            storage_conditions, shelf_life, price, stock_quantity, minimum_stock,
                            prescription_required
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        med['medicine_id'], med['name'], med['generic_name'], med['brand_name'],
                        med['category'], med['type'], med['strength'], med['unit'],
                        med['manufacturer'], med['description'], med['indications'],
                        med['contraindications'], med['side_effects'], med['dosage_form'],
                        med['route_of_administration'], med['storage_conditions'],
                        med['shelf_life'], med['price'], med['stock_quantity'],
                        med['minimum_stock'], med.get('prescription_required', 0)
                    ))
                
                conn.commit()
    
    def get_medicines(self, search_term=None, category=None, limit=None):
        """Get medicines with optional search and filter"""
        with self.get_connection() as conn:
            query = "SELECT * FROM medicines WHERE status = 'active'"
            params = []
            
            if search_term:
                query += " AND (name LIKE ? OR generic_name LIKE ? OR brand_name LIKE ? OR indications LIKE ?)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern, search_pattern, search_pattern])
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            query += " ORDER BY name"
            
            if limit:
                query += f" LIMIT {limit}"
            
            return pd.read_sql_query(query, conn, params=params)
    
    def add_medicine(self, medicine_data):
        """Add new medicine to database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Generate medicine ID if not provided
            if not medicine_data.get('medicine_id'):
                medicine_data['medicine_id'] = f"MED{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            try:
                cursor.execute('''
                    INSERT INTO medicines (
                        medicine_id, name, generic_name, brand_name, category, type,
                        strength, unit, manufacturer, description, indications,
                        contraindications, side_effects, dosage_form, route_of_administration,
                        storage_conditions, shelf_life, price, stock_quantity, minimum_stock,
                        prescription_required
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    medicine_data['medicine_id'], medicine_data['name'],
                    medicine_data.get('generic_name'), medicine_data.get('brand_name'),
                    medicine_data['category'], medicine_data['type'],
                    medicine_data.get('strength'), medicine_data.get('unit'),
                    medicine_data.get('manufacturer'), medicine_data.get('description'),
                    medicine_data.get('indications'), medicine_data.get('contraindications'),
                    medicine_data.get('side_effects'), medicine_data.get('dosage_form'),
                    medicine_data.get('route_of_administration'), medicine_data.get('storage_conditions'),
                    medicine_data.get('shelf_life'), medicine_data.get('price', 0),
                    medicine_data.get('stock_quantity', 0), medicine_data.get('minimum_stock', 10),
                    medicine_data.get('prescription_required', 0)
                ))
                
                conn.commit()
                return medicine_data['medicine_id']
            except sqlite3.IntegrityError:
                return None
    
    def update_medicine(self, medicine_id, medicine_data):
        """Update existing medicine"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE medicines SET
                    name = ?, generic_name = ?, brand_name = ?, category = ?, type = ?,
                    strength = ?, unit = ?, manufacturer = ?, description = ?, indications = ?,
                    contraindications = ?, side_effects = ?, dosage_form = ?, route_of_administration = ?,
                    storage_conditions = ?, shelf_life = ?, price = ?, stock_quantity = ?,
                    minimum_stock = ?, prescription_required = ?, updated_at = CURRENT_TIMESTAMP
                WHERE medicine_id = ?
            ''', (
                medicine_data['name'], medicine_data.get('generic_name'),
                medicine_data.get('brand_name'), medicine_data['category'],
                medicine_data['type'], medicine_data.get('strength'),
                medicine_data.get('unit'), medicine_data.get('manufacturer'),
                medicine_data.get('description'), medicine_data.get('indications'),
                medicine_data.get('contraindications'), medicine_data.get('side_effects'),
                medicine_data.get('dosage_form'), medicine_data.get('route_of_administration'),
                medicine_data.get('storage_conditions'), medicine_data.get('shelf_life'),
                medicine_data.get('price', 0), medicine_data.get('stock_quantity', 0),
                medicine_data.get('minimum_stock', 10), medicine_data.get('prescription_required', 0),
                medicine_id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_medicine(self, medicine_id):
        """Soft delete medicine (set status to inactive)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE medicines SET status = 'inactive', updated_at = CURRENT_TIMESTAMP
                WHERE medicine_id = ?
            ''', (medicine_id,))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def get_medicine_categories(self):
        """Get all unique medicine categories"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM medicines WHERE status = 'active' ORDER BY category")
            return [row[0] for row in cursor.fetchall()]
    
    def create_prescription(self, prescription_data):
        """Create new prescription"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Generate prescription ID
            prescription_id = f"RX{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            cursor.execute('''
                INSERT INTO prescriptions (
                    prescription_id, patient_id, doctor_id, record_id, medications,
                    dosage, frequency, duration, instructions, issued_date, expiry_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                prescription_id,
                prescription_data['patient_id'],
                prescription_data['doctor_id'],
                prescription_data.get('record_id'),
                json.dumps(prescription_data['medications']),
                prescription_data.get('dosage'),
                prescription_data.get('frequency'),
                prescription_data.get('duration'),
                prescription_data.get('instructions'),
                prescription_data['issued_date'],
                prescription_data.get('expiry_date')
            ))
            
            conn.commit()
            return prescription_id
    
    def get_prescriptions(self, patient_id=None, doctor_id=None, limit=None):
        """Get prescriptions with optional filters"""
        with self.get_connection() as conn:
            query = "SELECT * FROM prescriptions WHERE 1=1"
            params = []
            
            if patient_id:
                query += " AND patient_id = ?"
                params.append(patient_id)
            if doctor_id:
                query += " AND doctor_id = ?"
                params.append(doctor_id)
            
            query += " ORDER BY issued_date DESC"
            
            if limit:
                query += f" LIMIT {limit}"
            
            return pd.read_sql_query(query, conn, params=params)
    
    # ===== USER PROFILE MANAGEMENT FUNCTIONS =====
    
    def create_user_profile(self, user_id, profile_data):
        """Create user profile with personal information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO user_profiles (
                        user_id, first_name, last_name, date_of_birth, gender, blood_group,
                        address, city, state, postal_code, country, emergency_contact_name,
                        emergency_contact_phone, emergency_contact_relation, profile_picture,
                        bio, medical_history, allergies, chronic_conditions, current_medications,
                        insurance_provider, insurance_policy_number, insurance_expiry,
                        preferred_language, notification_preferences, privacy_settings
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    profile_data.get('first_name'),
                    profile_data.get('last_name'),
                    profile_data.get('date_of_birth'),
                    profile_data.get('gender'),
                    profile_data.get('blood_group'),
                    profile_data.get('address'),
                    profile_data.get('city'),
                    profile_data.get('state'),
                    profile_data.get('postal_code'),
                    profile_data.get('country', 'India'),
                    profile_data.get('emergency_contact_name'),
                    profile_data.get('emergency_contact_phone'),
                    profile_data.get('emergency_contact_relation'),
                    profile_data.get('profile_picture'),
                    profile_data.get('bio'),
                    profile_data.get('medical_history'),
                    profile_data.get('allergies'),
                    profile_data.get('chronic_conditions'),
                    profile_data.get('current_medications'),
                    profile_data.get('insurance_provider'),
                    profile_data.get('insurance_policy_number'),
                    profile_data.get('insurance_expiry'),
                    profile_data.get('preferred_language', 'English'),
                    json.dumps(profile_data.get('notification_preferences', {})),
                    json.dumps(profile_data.get('privacy_settings', {}))
                ))
                
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
    
    def get_user_profile(self, user_id):
        """Get user profile by user ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT up.*, u.username, u.email, u.phone, u.role, u.created_at as user_created_at
                FROM user_profiles up
                JOIN users u ON up.user_id = u.id
                WHERE up.user_id = ?
            ''', (user_id,))
            
            profile = cursor.fetchone()
            if profile:
                profile_dict = dict(profile)
                # Parse JSON fields
                if profile_dict.get('notification_preferences'):
                    profile_dict['notification_preferences'] = json.loads(profile_dict['notification_preferences'])
                if profile_dict.get('privacy_settings'):
                    profile_dict['privacy_settings'] = json.loads(profile_dict['privacy_settings'])
                return profile_dict
            return None
    
    def update_user_profile(self, user_id, profile_data):
        """Update user profile information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE user_profiles SET
                    first_name = ?, last_name = ?, date_of_birth = ?, gender = ?, blood_group = ?,
                    address = ?, city = ?, state = ?, postal_code = ?, country = ?,
                    emergency_contact_name = ?, emergency_contact_phone = ?, emergency_contact_relation = ?,
                    profile_picture = ?, bio = ?, medical_history = ?, allergies = ?,
                    chronic_conditions = ?, current_medications = ?, insurance_provider = ?,
                    insurance_policy_number = ?, insurance_expiry = ?, preferred_language = ?,
                    notification_preferences = ?, privacy_settings = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (
                profile_data.get('first_name'),
                profile_data.get('last_name'),
                profile_data.get('date_of_birth'),
                profile_data.get('gender'),
                profile_data.get('blood_group'),
                profile_data.get('address'),
                profile_data.get('city'),
                profile_data.get('state'),
                profile_data.get('postal_code'),
                profile_data.get('country', 'India'),
                profile_data.get('emergency_contact_name'),
                profile_data.get('emergency_contact_phone'),
                profile_data.get('emergency_contact_relation'),
                profile_data.get('profile_picture'),
                profile_data.get('bio'),
                profile_data.get('medical_history'),
                profile_data.get('allergies'),
                profile_data.get('chronic_conditions'),
                profile_data.get('current_medications'),
                profile_data.get('insurance_provider'),
                profile_data.get('insurance_policy_number'),
                profile_data.get('insurance_expiry'),
                profile_data.get('preferred_language', 'English'),
                json.dumps(profile_data.get('notification_preferences', {})),
                json.dumps(profile_data.get('privacy_settings', {})),
                user_id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def create_user_with_profile(self, username, password, role, email=None, phone=None, profile_data=None):
        """Create user with profile and preferences in one transaction"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            
            try:
                # Create user
                cursor.execute('''
                    INSERT INTO users (username, password_hash, role, email, phone)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, password_hash, role, email, phone))
                
                user_id = cursor.lastrowid
                
                # Create profile if data provided
                if profile_data:
                    cursor.execute('''
                        INSERT INTO user_profiles (
                            user_id, first_name, last_name, date_of_birth, gender, blood_group,
                            address, city, state, postal_code, country, emergency_contact_name,
                            emergency_contact_phone, emergency_contact_relation, preferred_language
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        user_id,
                        profile_data.get('first_name'),
                        profile_data.get('last_name'),
                        profile_data.get('date_of_birth'),
                        profile_data.get('gender'),
                        profile_data.get('blood_group'),
                        profile_data.get('address'),
                        profile_data.get('city'),
                        profile_data.get('state'),
                        profile_data.get('postal_code'),
                        profile_data.get('country', 'India'),
                        profile_data.get('emergency_contact_name'),
                        profile_data.get('emergency_contact_phone'),
                        profile_data.get('emergency_contact_relation'),
                        profile_data.get('preferred_language', 'English')
                    ))
                
                # Create default preferences
                cursor.execute('''
                    INSERT INTO user_preferences (user_id) VALUES (?)
                ''', (user_id,))
                
                conn.commit()
                return user_id
                
            except sqlite3.IntegrityError:
                conn.rollback()
                return None
    
    def get_complete_user_data(self, user_id):
        """Get complete user data including profile and preferences"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get user, profile, and preferences in one query
            cursor.execute('''
                SELECT 
                    u.id, u.username, u.email, u.phone, u.role, u.created_at, u.last_login,
                    up.first_name, up.last_name, up.date_of_birth, up.gender, up.blood_group,
                    up.address, up.city, up.state, up.postal_code, up.country,
                    up.emergency_contact_name, up.emergency_contact_phone, up.emergency_contact_relation,
                    up.profile_picture, up.bio, up.medical_history, up.allergies, up.chronic_conditions,
                    up.current_medications, up.insurance_provider, up.insurance_policy_number,
                    up.insurance_expiry, up.preferred_language,
                    pr.theme, pr.language as pref_language, pr.timezone, pr.date_format, pr.time_format,
                    pr.email_notifications, pr.sms_notifications, pr.push_notifications,
                    pr.appointment_reminders, pr.medication_reminders, pr.health_tips,
                    pr.newsletter, pr.data_sharing
                FROM users u
                LEFT JOIN user_profiles up ON u.id = up.user_id
                LEFT JOIN user_preferences pr ON u.id = pr.user_id
                WHERE u.id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            if result:
                return dict(result)
            return None
    
    def get_user_preferences(self, user_id):
        """Get user preferences"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_preferences WHERE user_id = ?', (user_id,))
            
            preferences = cursor.fetchone()
            return dict(preferences) if preferences else None
    
    def update_user_preferences(self, user_id, preferences_data):
        """Update user preferences"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE user_preferences SET
                    theme = ?, language = ?, timezone = ?, date_format = ?, time_format = ?,
                    email_notifications = ?, sms_notifications = ?, push_notifications = ?,
                    appointment_reminders = ?, medication_reminders = ?, health_tips = ?,
                    newsletter = ?, data_sharing = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (
                preferences_data.get('theme'),
                preferences_data.get('language'),
                preferences_data.get('timezone'),
                preferences_data.get('date_format'),
                preferences_data.get('time_format'),
                preferences_data.get('email_notifications'),
                preferences_data.get('sms_notifications'),
                preferences_data.get('push_notifications'),
                preferences_data.get('appointment_reminders'),
                preferences_data.get('medication_reminders'),
                preferences_data.get('health_tips'),
                preferences_data.get('newsletter'),
                preferences_data.get('data_sharing'),
                user_id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def create_user_preferences(self, user_id, preferences_data=None):
        """Create user preferences with default values"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if preferences_data is None:
                preferences_data = {}
            
            try:
                cursor.execute('''
                    INSERT INTO user_preferences (
                        user_id, theme, language, timezone, date_format, time_format,
                        email_notifications, sms_notifications, push_notifications,
                        appointment_reminders, medication_reminders, health_tips,
                        newsletter, data_sharing
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    preferences_data.get('theme', 'light'),
                    preferences_data.get('language', 'English'),
                    preferences_data.get('timezone', 'Asia/Kolkata'),
                    preferences_data.get('date_format', 'DD/MM/YYYY'),
                    preferences_data.get('time_format', '24'),
                    preferences_data.get('email_notifications', True),
                    preferences_data.get('sms_notifications', True),
                    preferences_data.get('push_notifications', True),
                    preferences_data.get('appointment_reminders', True),
                    preferences_data.get('medication_reminders', True),
                    preferences_data.get('health_tips', True),
                    preferences_data.get('newsletter', False),
                    preferences_data.get('data_sharing', False)
                ))
                
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

# Global database instance
db = HospitalDatabase()
