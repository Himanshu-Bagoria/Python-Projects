#!/usr/bin/env python3
"""
Demo Data Setup Script for Smart Hospital Management System
This script creates comprehensive demo data for testing and demonstration
"""

import sqlite3
import pandas as pd
import json
import hashlib
from datetime import datetime, date, timedelta
import random
import uuid
import os

# Add utils to path
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.database import db

def create_demo_patients():
    """Create demo patient data"""
    print("Creating demo patients...")
    
    demo_patients = [
        {
            'patient_id': 'PT001',
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1985-03-15',
            'gender': 'Male',
            'blood_group': 'A+',
            'address': '123 Main Street, Downtown',
            'emergency_contact': '+1-555-0101',
            'medical_history': 'Hypertension, Family history of diabetes',
            'allergies': 'Penicillin',
            'insurance_info': 'Blue Cross Blue Shield - Policy #BC123456'
        },
        {
            'patient_id': 'PT002',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': '1990-07-22',
            'gender': 'Female',
            'blood_group': 'B+',
            'address': '456 Oak Avenue, Midtown',
            'emergency_contact': '+1-555-0102',
            'medical_history': 'Asthma, Previous appendectomy',
            'allergies': 'Shellfish, Pollen',
            'insurance_info': 'Aetna Health - Policy #AH789012'
        },
        {
            'patient_id': 'PT003',
            'first_name': 'Robert',
            'last_name': 'Johnson',
            'date_of_birth': '1975-11-08',
            'gender': 'Male',
            'blood_group': 'O-',
            'address': '789 Pine Street, Uptown',
            'emergency_contact': '+1-555-0103',
            'medical_history': 'Type 2 Diabetes, High cholesterol',
            'allergies': 'None known',
            'insurance_info': 'United Healthcare - Policy #UH345678'
        },
        {
            'patient_id': 'PT004',
            'first_name': 'Emily',
            'last_name': 'Davis',
            'date_of_birth': '1988-05-12',
            'gender': 'Female',
            'blood_group': 'AB+',
            'address': '321 Elm Drive, Suburban',
            'emergency_contact': '+1-555-0104',
            'medical_history': 'Migraine headaches, Thyroid disorder',
            'allergies': 'Latex, Aspirin',
            'insurance_info': 'Cigna Health - Policy #CG901234'
        },
        {
            'patient_id': 'PT005',
            'first_name': 'Michael',
            'last_name': 'Brown',
            'date_of_birth': '1965-09-30',
            'gender': 'Male',
            'blood_group': 'A-',
            'address': '654 Maple Lane, Riverside',
            'emergency_contact': '+1-555-0105',
            'medical_history': 'Heart disease, Previous bypass surgery',
            'allergies': 'Sulfa drugs',
            'insurance_info': 'Medicare - Policy #MC567890'
        }
    ]
    
    # Insert demo patients
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        for patient in demo_patients:
            cursor.execute('''
                INSERT OR REPLACE INTO patients (
                    patient_id, first_name, last_name, date_of_birth, gender,
                    blood_group, address, emergency_contact, medical_history,
                    allergies, insurance_info
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient['patient_id'], patient['first_name'], patient['last_name'],
                patient['date_of_birth'], patient['gender'], patient['blood_group'],
                patient['address'], patient['emergency_contact'], patient['medical_history'],
                patient['allergies'], patient['insurance_info']
            ))
        
        conn.commit()
    
    print(f"✅ Created {len(demo_patients)} demo patients")

def create_demo_doctors():
    """Create demo doctor data"""
    print("Creating demo doctors...")
    
    demo_doctors = [
        {
            'doctor_id': 'DR001',
            'first_name': 'James',
            'last_name': 'Wilson',
            'specialization': 'Cardiology',
            'qualification': 'MD, FACC',
            'experience_years': 15,
            'department': 'Cardiology',
            'consultation_fee': 200.0,
            'available_days': 'Monday,Tuesday,Wednesday,Thursday,Friday',
            'available_hours': '09:00-17:00',
            'rating': 4.8,
            'total_reviews': 156
        },
        {
            'doctor_id': 'DR002',
            'first_name': 'Sarah',
            'last_name': 'Connor',
            'specialization': 'Neurology',
            'qualification': 'MD, PhD',
            'experience_years': 12,
            'department': 'Neurology',
            'consultation_fee': 250.0,
            'available_days': 'Monday,Wednesday,Friday',
            'available_hours': '10:00-16:00',
            'rating': 4.9,
            'total_reviews': 98
        },
        {
            'doctor_id': 'DR003',
            'first_name': 'David',
            'last_name': 'Martinez',
            'specialization': 'Orthopedics',
            'qualification': 'MD, MS Orthopedics',
            'experience_years': 18,
            'department': 'Orthopedics',
            'consultation_fee': 180.0,
            'available_days': 'Tuesday,Thursday,Saturday',
            'available_hours': '08:00-14:00',
            'rating': 4.7,
            'total_reviews': 203
        },
        {
            'doctor_id': 'DR004',
            'first_name': 'Lisa',
            'last_name': 'Anderson',
            'specialization': 'Pediatrics',
            'qualification': 'MD, MPH',
            'experience_years': 10,
            'department': 'Pediatrics',
            'consultation_fee': 150.0,
            'available_days': 'Monday,Tuesday,Wednesday,Thursday,Friday',
            'available_hours': '09:00-17:00',
            'rating': 4.9,
            'total_reviews': 145
        },
        {
            'doctor_id': 'DR005',
            'first_name': 'Richard',
            'last_name': 'Thompson',
            'specialization': 'Emergency Medicine',
            'qualification': 'MD, FACEP',
            'experience_years': 8,
            'department': 'Emergency',
            'consultation_fee': 300.0,
            'available_days': 'All Days',
            'available_hours': '24/7',
            'rating': 4.6,
            'total_reviews': 87
        }
    ]
    
    # Insert demo doctors
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        for doctor in demo_doctors:
            cursor.execute('''
                INSERT OR REPLACE INTO doctors (
                    doctor_id, first_name, last_name, specialization, qualification,
                    experience_years, department, consultation_fee, available_days,
                    available_hours, rating, total_reviews
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                doctor['doctor_id'], doctor['first_name'], doctor['last_name'],
                doctor['specialization'], doctor['qualification'], doctor['experience_years'],
                doctor['department'], doctor['consultation_fee'], doctor['available_days'],
                doctor['available_hours'], doctor['rating'], doctor['total_reviews']
            ))
        
        conn.commit()
    
    print(f"✅ Created {len(demo_doctors)} demo doctors")

def create_demo_appointments():
    """Create demo appointment data"""
    print("Creating demo appointments...")
    
    # Generate appointments for the next 30 days
    appointments = []
    base_date = date.today()
    
    for i in range(30):
        appointment_date = base_date + timedelta(days=i)
        
        # Skip weekends for some doctors
        if appointment_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
            continue
        
        # Create 3-5 appointments per day
        num_appointments = random.randint(3, 5)
        
        for j in range(num_appointments):
            appointment_time = f"{8 + j * 2}:00"  # 8:00, 10:00, 12:00, etc.
            
            appointment = {
                'appointment_id': f"APT{appointment_date.strftime('%Y%m%d')}{j+1:02d}",
                'patient_id': random.choice(['PT001', 'PT002', 'PT003', 'PT004', 'PT005']),
                'doctor_id': random.choice(['DR001', 'DR002', 'DR003', 'DR004', 'DR005']),
                'appointment_date': appointment_date.isoformat(),
                'appointment_time': appointment_time,
                'status': random.choice(['scheduled', 'completed', 'cancelled']),
                'type': random.choice(['consultation', 'follow-up', 'emergency', 'checkup']),
                'reason': random.choice([
                    'Regular checkup', 'Follow-up visit', 'Chest pain', 'Headache',
                    'Joint pain', 'Fever', 'Blood pressure check', 'Medication review'
                ]),
                'fee': random.choice([150.0, 180.0, 200.0, 250.0, 300.0])
            }
            appointments.append(appointment)
    
    # Insert demo appointments
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        for apt in appointments:
            cursor.execute('''
                INSERT OR REPLACE INTO appointments (
                    appointment_id, patient_id, doctor_id, appointment_date,
                    appointment_time, status, type, reason, fee
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                apt['appointment_id'], apt['patient_id'], apt['doctor_id'],
                apt['appointment_date'], apt['appointment_time'], apt['status'],
                apt['type'], apt['reason'], apt['fee']
            ))
        
        conn.commit()
    
    print(f"✅ Created {len(appointments)} demo appointments")

def create_demo_medical_records():
    """Create demo medical records"""
    print("Creating demo medical records...")
    
    medical_records = [
        {
            'record_id': 'MR001',
            'patient_id': 'PT001',
            'doctor_id': 'DR001',
            'appointment_id': 'APT2024011501',
            'diagnosis': 'Essential Hypertension',
            'symptoms': 'Elevated blood pressure, occasional headaches',
            'treatment': 'Lifestyle modifications, antihypertensive medication',
            'prescriptions': json.dumps([
                {'medication': 'Lisinopril', 'dosage': '10mg', 'frequency': 'Once daily'},
                {'medication': 'Amlodipine', 'dosage': '5mg', 'frequency': 'Once daily'}
            ]),
            'lab_results': 'BP: 150/95, Cholesterol: 220 mg/dL',
            'vitals': json.dumps({
                'temperature': 98.6,
                'blood_pressure': '150/95',
                'heart_rate': 78,
                'respiratory_rate': 16
            }),
            'record_date': '2024-01-15',
            'follow_up_date': '2024-02-15'
        },
        {
            'record_id': 'MR002',
            'patient_id': 'PT002',
            'doctor_id': 'DR004',
            'appointment_id': 'APT2024011502',
            'diagnosis': 'Asthma exacerbation',
            'symptoms': 'Shortness of breath, wheezing, chest tightness',
            'treatment': 'Bronchodilator, corticosteroids',
            'prescriptions': json.dumps([
                {'medication': 'Albuterol inhaler', 'dosage': '90mcg', 'frequency': 'As needed'},
                {'medication': 'Prednisone', 'dosage': '20mg', 'frequency': 'Once daily for 5 days'}
            ]),
            'lab_results': 'Peak flow: 320 L/min',
            'vitals': json.dumps({
                'temperature': 98.4,
                'blood_pressure': '125/80',
                'heart_rate': 92,
                'respiratory_rate': 22,
                'oxygen_saturation': 96
            }),
            'record_date': '2024-01-15',
            'follow_up_date': '2024-01-29'
        }
    ]
    
    # Insert demo medical records
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        for record in medical_records:
            cursor.execute('''
                INSERT OR REPLACE INTO medical_records (
                    record_id, patient_id, doctor_id, appointment_id, diagnosis,
                    symptoms, treatment, prescriptions, lab_results, vitals,
                    record_date, follow_up_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record['record_id'], record['patient_id'], record['doctor_id'],
                record['appointment_id'], record['diagnosis'], record['symptoms'],
                record['treatment'], record['prescriptions'], record['lab_results'],
                record['vitals'], record['record_date'], record['follow_up_date']
            ))
        
        conn.commit()
    
    print(f"✅ Created {len(medical_records)} demo medical records")

def create_demo_prescriptions():
    """Create demo prescriptions"""
    print("Creating demo prescriptions...")
    
    prescriptions = [
        {
            'prescription_id': 'RX001',
            'patient_id': 'PT001',
            'doctor_id': 'DR001',
            'record_id': 'MR001',
            'medications': json.dumps([
                {
                    'name': 'Lisinopril',
                    'strength': '10mg',
                    'quantity': 30,
                    'instructions': 'Take once daily with food'
                },
                {
                    'name': 'Amlodipine',
                    'strength': '5mg',
                    'quantity': 30,
                    'instructions': 'Take once daily in the morning'
                }
            ]),
            'dosage': 'As prescribed',
            'frequency': 'Daily',
            'duration': '30 days',
            'instructions': 'Monitor blood pressure regularly. Contact doctor if BP > 160/100',
            'issued_date': '2024-01-15',
            'expiry_date': '2024-07-15',
            'status': 'active'
        },
        {
            'prescription_id': 'RX002',
            'patient_id': 'PT002',
            'doctor_id': 'DR004',
            'record_id': 'MR002',
            'medications': json.dumps([
                {
                    'name': 'Albuterol inhaler',
                    'strength': '90mcg',
                    'quantity': 1,
                    'instructions': 'Use as rescue inhaler for acute symptoms'
                },
                {
                    'name': 'Prednisone',
                    'strength': '20mg',
                    'quantity': 5,
                    'instructions': 'Take one tablet daily for 5 days with food'
                }
            ]),
            'dosage': 'As prescribed',
            'frequency': 'As needed / Daily',
            'duration': '5 days for Prednisone, ongoing for inhaler',
            'instructions': 'Use inhaler for acute breathing difficulty. Complete course of Prednisone.',
            'issued_date': '2024-01-15',
            'expiry_date': '2024-07-15',
            'status': 'active'
        }
    ]
    
    # Insert demo prescriptions
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        for prescription in prescriptions:
            cursor.execute('''
                INSERT OR REPLACE INTO prescriptions (
                    prescription_id, patient_id, doctor_id, record_id, medications,
                    dosage, frequency, duration, instructions, issued_date,
                    expiry_date, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                prescription['prescription_id'], prescription['patient_id'],
                prescription['doctor_id'], prescription['record_id'],
                prescription['medications'], prescription['dosage'],
                prescription['frequency'], prescription['duration'],
                prescription['instructions'], prescription['issued_date'],
                prescription['expiry_date'], prescription['status']
            ))
        
        conn.commit()
    
    print(f"✅ Created {len(prescriptions)} demo prescriptions")

def create_demo_lab_tests():
    """Create demo lab tests"""
    print("Creating demo lab tests...")
    
    lab_tests = [
        {
            'test_id': 'LAB001',
            'patient_id': 'PT001',
            'doctor_id': 'DR001',
            'test_name': 'Complete Blood Count',
            'test_type': 'Hematology',
            'ordered_date': '2024-01-15',
            'scheduled_date': '2024-01-16',
            'completed_date': '2024-01-16',
            'results': json.dumps({
                'WBC': '7.2 K/uL',
                'RBC': '4.5 M/uL',
                'Hemoglobin': '14.2 g/dL',
                'Hematocrit': '42.1%',
                'Platelets': '285 K/uL'
            }),
            'status': 'completed',
            'lab_technician': 'Sarah Lab Tech',
            'normal_range': 'All values within normal limits',
            'remarks': 'Normal complete blood count'
        },
        {
            'test_id': 'LAB002',
            'patient_id': 'PT001',
            'doctor_id': 'DR001',
            'test_name': 'Lipid Panel',
            'test_type': 'Chemistry',
            'ordered_date': '2024-01-15',
            'scheduled_date': '2024-01-16',
            'completed_date': '2024-01-16',
            'results': json.dumps({
                'Total_Cholesterol': '220 mg/dL',
                'LDL': '145 mg/dL',
                'HDL': '45 mg/dL',
                'Triglycerides': '180 mg/dL'
            }),
            'status': 'completed',
            'lab_technician': 'Mike Lab Tech',
            'normal_range': 'Total Cholesterol: <200 mg/dL, LDL: <100 mg/dL',
            'remarks': 'Elevated cholesterol and LDL. Recommend dietary changes.'
        }
    ]
    
    # Insert demo lab tests
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        for test in lab_tests:
            cursor.execute('''
                INSERT OR REPLACE INTO lab_tests (
                    test_id, patient_id, doctor_id, test_name, test_type,
                    ordered_date, scheduled_date, completed_date, results,
                    status, lab_technician, normal_range, remarks
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                test['test_id'], test['patient_id'], test['doctor_id'],
                test['test_name'], test['test_type'], test['ordered_date'],
                test['scheduled_date'], test['completed_date'], test['results'],
                test['status'], test['lab_technician'], test['normal_range'],
                test['remarks']
            ))
        
        conn.commit()
    
    print(f"✅ Created {len(lab_tests)} demo lab tests")

def create_demo_billing():
    """Create demo billing records"""
    print("Creating demo billing records...")
    
    billing_records = [
        {
            'bill_id': 'BILL001',
            'patient_id': 'PT001',
            'appointment_id': 'APT2024011501',
            'service_type': 'Consultation',
            'description': 'Cardiology consultation with Dr. Wilson',
            'amount': 200.0,
            'tax_amount': 20.0,
            'total_amount': 220.0,
            'payment_status': 'paid',
            'payment_method': 'Credit Card',
            'insurance_coverage': 150.0,
            'bill_date': '2024-01-15',
            'due_date': '2024-01-30',
            'paid_date': '2024-01-16'
        },
        {
            'bill_id': 'BILL002',
            'patient_id': 'PT002',
            'appointment_id': 'APT2024011502',
            'service_type': 'Consultation + Medication',
            'description': 'Pediatric consultation and prescribed medications',
            'amount': 180.0,
            'tax_amount': 18.0,
            'total_amount': 198.0,
            'payment_status': 'pending',
            'payment_method': None,
            'insurance_coverage': 120.0,
            'bill_date': '2024-01-15',
            'due_date': '2024-01-30',
            'paid_date': None
        }
    ]
    
    # Insert demo billing records
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        for bill in billing_records:
            cursor.execute('''
                INSERT OR REPLACE INTO billing (
                    bill_id, patient_id, appointment_id, service_type, description,
                    amount, tax_amount, total_amount, payment_status, payment_method,
                    insurance_coverage, bill_date, due_date, paid_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                bill['bill_id'], bill['patient_id'], bill['appointment_id'],
                bill['service_type'], bill['description'], bill['amount'],
                bill['tax_amount'], bill['total_amount'], bill['payment_status'],
                bill['payment_method'], bill['insurance_coverage'],
                bill['bill_date'], bill['due_date'], bill['paid_date']
            ))
        
        conn.commit()
    
    print(f"✅ Created {len(billing_records)} demo billing records")

def main():
    """Main function to setup all demo data"""
    print("🏥 Setting up demo data for Smart Hospital Management System...")
    print("=" * 60)
    
    try:
        # Create all demo data
        create_demo_patients()
        create_demo_doctors()
        create_demo_appointments()
        create_demo_medical_records()
        create_demo_prescriptions()
        create_demo_lab_tests()
        create_demo_billing()
        
        print("=" * 60)
        print("✅ Demo data setup completed successfully!")
        print("\n📊 Summary:")
        print("- 5 Demo patients created")
        print("- 5 Demo doctors created")
        print("- Multiple appointments scheduled")
        print("- Medical records with prescriptions")
        print("- Lab tests and billing records")
        print("\n🚀 You can now run the application with: streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Error setting up demo data: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()