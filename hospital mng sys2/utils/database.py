import streamlit as st
import json
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid

class HospitalDatabase:
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_directory()
        self.load_data()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def load_data(self):
        """Load all data from JSON files"""
        self.patients = self.load_json("patients.json", self.get_default_patients())
        self.doctors = self.load_json("doctors.json", self.get_default_doctors())
        self.appointments = self.load_json("appointments.json", self.get_default_appointments())
        self.prescriptions = self.load_json("prescriptions.json", self.get_default_prescriptions())
        self.lab_reports = self.load_json("lab_reports.json", self.get_default_lab_reports())
        self.vital_signs = self.load_json("vital_signs.json", self.get_default_vital_signs())
        self.emergency_alerts = self.load_json("emergency_alerts.json", [])
        self.ward_data = self.load_json("ward_data.json", self.get_default_ward_data())
    
    def load_json(self, filename, default_data):
        """Load JSON file or create with default data"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        else:
            self.save_json(filename, default_data)
            return default_data
    
    def save_json(self, filename, data):
        """Save data to JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_default_patients(self):
        """Get default patient data"""
        return [
            {
                "id": "P001",
                "name": "Rajesh Kumar",
                "age": 45,
                "gender": "Male",
                "phone": "+91-9876543210",
                "email": "rajesh.kumar@email.com",
                "blood_group": "B+",
                "emergency_contact": "+91-9876543211",
                "medical_history": ["Diabetes", "Hypertension"],
                "allergies": ["Penicillin"],
                "registration_date": "2024-01-15",
                "last_visit": "2024-08-20",
                "status": "Active"
            },
            {
                "id": "P002",
                "name": "Priya Sharma",
                "age": 32,
                "gender": "Female",
                "phone": "+91-9876543212",
                "email": "priya.sharma@email.com",
                "blood_group": "O+",
                "emergency_contact": "+91-9876543213",
                "medical_history": ["Asthma"],
                "allergies": ["Dust", "Pollen"],
                "registration_date": "2024-02-10",
                "last_visit": "2024-08-18",
                "status": "Active"
            },
            {
                "id": "P003",
                "name": "Amit Patel",
                "age": 28,
                "gender": "Male",
                "phone": "+91-9876543214",
                "email": "amit.patel@email.com",
                "blood_group": "A+",
                "emergency_contact": "+91-9876543215",
                "medical_history": [],
                "allergies": [],
                "registration_date": "2024-03-05",
                "last_visit": "2024-08-22",
                "status": "Active"
            }
        ]
    
    def get_default_doctors(self):
        """Get default doctor data"""
        return [
            {
                "id": "D001",
                "name": "Dr. Meera Singh",
                "specialization": "Cardiology",
                "experience": 15,
                "phone": "+91-9876543220",
                "email": "dr.meera.singh@hospital.com",
                "availability": ["Monday", "Wednesday", "Friday"],
                "rating": 4.8,
                "consultation_fee": 1500,
                "status": "Available"
            },
            {
                "id": "D002",
                "name": "Dr. Arjun Reddy",
                "specialization": "Neurology",
                "experience": 12,
                "phone": "+91-9876543221",
                "email": "dr.arjun.reddy@hospital.com",
                "availability": ["Tuesday", "Thursday", "Saturday"],
                "rating": 4.6,
                "consultation_fee": 1800,
                "status": "Available"
            },
            {
                "id": "D003",
                "name": "Dr. Kavita Gupta",
                "specialization": "Pediatrics",
                "experience": 8,
                "phone": "+91-9876543222",
                "email": "dr.kavita.gupta@hospital.com",
                "availability": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "rating": 4.9,
                "consultation_fee": 1200,
                "status": "Available"
            }
        ]
    
    def get_default_appointments(self):
        """Get default appointment data"""
        return [
            {
                "id": "A001",
                "patient_id": "P001",
                "doctor_id": "D001",
                "date": "2024-08-25",
                "time": "10:00",
                "type": "Consultation",
                "status": "Scheduled",
                "notes": "Follow-up for diabetes management"
            },
            {
                "id": "A002",
                "patient_id": "P002",
                "doctor_id": "D003",
                "date": "2024-08-26",
                "time": "14:30",
                "type": "Check-up",
                "status": "Scheduled",
                "notes": "Regular health check-up"
            }
        ]
    
    def get_default_prescriptions(self):
        """Get default prescription data"""
        return [
            {
                "id": "PR001",
                "patient_id": "P001",
                "doctor_id": "D001",
                "date": "2024-08-20",
                "medications": [
                    {
                        "name": "Metformin",
                        "dosage": "500mg",
                        "frequency": "Twice daily",
                        "duration": "30 days",
                        "instructions": "Take with food"
                    }
                ],
                "diagnosis": "Type 2 Diabetes",
                "notes": "Continue current medication, monitor blood sugar levels"
            }
        ]
    
    def get_default_lab_reports(self):
        """Get default lab report data"""
        return [
            {
                "id": "LR001",
                "patient_id": "P001",
                "date": "2024-08-20",
                "tests": [
                    {
                        "name": "Blood Glucose",
                        "value": "140",
                        "unit": "mg/dL",
                        "normal_range": "70-140",
                        "status": "High"
                    },
                    {
                        "name": "HbA1c",
                        "value": "7.2",
                        "unit": "%",
                        "normal_range": "4.0-5.6",
                        "status": "High"
                    }
                ],
                "status": "Completed"
            }
        ]
    
    def get_default_vital_signs(self):
        """Get default vital signs data"""
        return {
            "P001": {
                "heart_rate": 75,
                "blood_pressure": "120/80",
                "temperature": 37.0,
                "oxygen_saturation": 98,
                "respiratory_rate": 16,
                "last_updated": datetime.now().isoformat()
            },
            "P002": {
                "heart_rate": 68,
                "blood_pressure": "115/75",
                "temperature": 36.8,
                "oxygen_saturation": 99,
                "respiratory_rate": 14,
                "last_updated": datetime.now().isoformat()
            }
        }
    
    def get_default_ward_data(self):
        """Get default ward monitoring data"""
        return {
            "ward_101": {
                "bed_1": {"occupied": True, "patient_id": "P001", "temperature": 22.5, "noise_level": 45},
                "bed_2": {"occupied": False, "patient_id": None, "temperature": 23.0, "noise_level": 40},
                "bed_3": {"occupied": True, "patient_id": "P002", "temperature": 22.8, "noise_level": 50}
            },
            "ward_102": {
                "bed_1": {"occupied": False, "patient_id": None, "temperature": 22.3, "noise_level": 35},
                "bed_2": {"occupied": True, "patient_id": "P003", "temperature": 22.7, "noise_level": 42}
            }
        }
    
    # Patient operations
    def add_patient(self, patient_data):
        """Add new patient"""
        patient_data["id"] = f"P{str(len(self.patients) + 1).zfill(3)}"
        patient_data["registration_date"] = datetime.now().strftime("%Y-%m-%d")
        patient_data["status"] = "Active"
        self.patients.append(patient_data)
        self.save_json("patients.json", self.patients)
        return patient_data["id"]
    
    def get_patient(self, patient_id):
        """Get patient by ID"""
        for patient in self.patients:
            if patient["id"] == patient_id:
                return patient
        return None
    
    def update_patient(self, patient_id, updates):
        """Update patient information"""
        for patient in self.patients:
            if patient["id"] == patient_id:
                patient.update(updates)
                self.save_json("patients.json", self.patients)
                return True
        return False
    
    def search_patients(self, query):
        """Search patients by name or ID"""
        results = []
        query = query.lower()
        for patient in self.patients:
            if (query in patient["name"].lower() or 
                query in patient["id"].lower() or
                query in patient["phone"]):
                results.append(patient)
        return results
    
    # Doctor operations
    def get_doctors_by_specialization(self, specialization):
        """Get doctors by specialization"""
        return [doc for doc in self.doctors if doc["specialization"].lower() == specialization.lower()]
    
    def get_available_doctors(self, date):
        """Get available doctors for a specific date"""
        day = datetime.strptime(date, "%Y-%m-%d").strftime("%A")
        return [doc for doc in self.doctors if day in doc["availability"] and doc["status"] == "Available"]
    
    # Appointment operations
    def add_appointment(self, appointment_data):
        """Add new appointment"""
        appointment_data["id"] = f"A{str(len(self.appointments) + 1).zfill(3)}"
        appointment_data["status"] = "Scheduled"
        self.appointments.append(appointment_data)
        self.save_json("appointments.json", self.appointments)
        return appointment_data["id"]
    
    def get_patient_appointments(self, patient_id):
        """Get appointments for a patient"""
        return [apt for apt in self.appointments if apt["patient_id"] == patient_id]
    
    def update_appointment_status(self, appointment_id, status):
        """Update appointment status"""
        for appointment in self.appointments:
            if appointment["id"] == appointment_id:
                appointment["status"] = status
                self.save_json("appointments.json", self.appointments)
                return True
        return False
    
    # Prescription operations
    def add_prescription(self, prescription_data):
        """Add new prescription"""
        prescription_data["id"] = f"PR{str(len(self.prescriptions) + 1).zfill(3)}"
        prescription_data["date"] = datetime.now().strftime("%Y-%m-%d")
        self.prescriptions.append(prescription_data)
        self.save_json("prescriptions.json", self.prescriptions)
        return prescription_data["id"]
    
    def get_patient_prescriptions(self, patient_id):
        """Get prescriptions for a patient"""
        return [pres for pres in self.prescriptions if pres["patient_id"] == patient_id]
    
    # Lab report operations
    def add_lab_report(self, report_data):
        """Add new lab report"""
        report_data["id"] = f"LR{str(len(self.lab_reports) + 1).zfill(3)}"
        report_data["date"] = datetime.now().strftime("%Y-%m-%d")
        report_data["status"] = "Completed"
        self.lab_reports.append(report_data)
        self.save_json("lab_reports.json", self.lab_reports)
        return report_data["id"]
    
    def get_patient_lab_reports(self, patient_id):
        """Get lab reports for a patient"""
        return [report for report in self.lab_reports if report["patient_id"] == patient_id]
    
    # Vital signs operations
    def update_vital_signs(self, patient_id, vitals):
        """Update patient vital signs"""
        self.vital_signs[patient_id] = {
            **vitals,
            "last_updated": datetime.now().isoformat()
        }
        self.save_json("vital_signs.json", self.vital_signs)
    
    def get_vital_signs(self, patient_id):
        """Get patient vital signs"""
        return self.vital_signs.get(patient_id, {})
    
    # Emergency alert operations
    def add_emergency_alert(self, alert_data):
        """Add emergency alert"""
        alert_data["id"] = str(uuid.uuid4())
        alert_data["timestamp"] = datetime.now().isoformat()
        alert_data["status"] = "Active"
        self.emergency_alerts.append(alert_data)
        self.save_json("emergency_alerts.json", self.emergency_alerts)
        return alert_data["id"]
    
    def get_active_emergency_alerts(self):
        """Get active emergency alerts"""
        return [alert for alert in self.emergency_alerts if alert["status"] == "Active"]
    
    # Ward monitoring operations
    def update_ward_data(self, ward_id, bed_id, data):
        """Update ward monitoring data"""
        if ward_id not in self.ward_data:
            self.ward_data[ward_id] = {}
        self.ward_data[ward_id][bed_id] = data
        self.save_json("ward_data.json", self.ward_data)
    
    def get_ward_data(self, ward_id=None):
        """Get ward monitoring data"""
        if ward_id:
            return self.ward_data.get(ward_id, {})
        return self.ward_data
    
    # Analytics and reporting
    def get_statistics(self):
        """Get hospital statistics"""
        return {
            "total_patients": len(self.patients),
            "active_patients": len([p for p in self.patients if p["status"] == "Active"]),
            "total_doctors": len(self.doctors),
            "available_doctors": len([d for d in self.doctors if d["status"] == "Available"]),
            "total_appointments": len(self.appointments),
            "today_appointments": len([a for a in self.appointments if a["date"] == datetime.now().strftime("%Y-%m-%d")]),
            "active_emergencies": len(self.get_active_emergency_alerts()),
            "occupied_beds": sum(1 for ward in self.ward_data.values() 
                               for bed in ward.values() if bed.get("occupied", False))
        }
    
    def export_patient_data(self, patient_id):
        """Export patient data for reporting"""
        patient = self.get_patient(patient_id)
        if not patient:
            return None
        
        patient_data = {
            "patient": patient,
            "appointments": self.get_patient_appointments(patient_id),
            "prescriptions": self.get_patient_prescriptions(patient_id),
            "lab_reports": self.get_patient_lab_reports(patient_id),
            "vital_signs": self.get_vital_signs(patient_id)
        }
        
        return patient_data

# Global database instance
db = HospitalDatabase()
