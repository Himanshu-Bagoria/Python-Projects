import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication
from utils.database import db
from utils.ui_components import create_glow_button, create_metric_card, create_alert_box, display_qr_code
from utils.voice_utils import VoiceAssistant
from utils.image_utils import create_medicine_image_display, create_image_url_input
from config.themes import get_theme_css

class PrescriptionSystem:
    def __init__(self):
        self.medications = self.load_medications()
        self.pharmacy_inventory = self.load_pharmacy_inventory()
        
    def load_medications(self):
        """Load available medications"""
        return [
            {
                "id": "MED001",
                "name": "Metformin",
                "generic_name": "Metformin Hydrochloride",
                "category": "Antidiabetic",
                "dosage_forms": ["500mg", "1000mg"],
                "frequency": ["Once daily", "Twice daily"],
                "side_effects": ["Nausea", "Diarrhea", "Stomach upset"],
                "image_url": None,
                "hindi_name": "मेटफॉर्मिन",
                "hindi_description": "मधुमेह के लिए दवा"
            },
            {
                "id": "MED002",
                "name": "Amlodipine",
                "generic_name": "Amlodipine Besylate",
                "category": "Antihypertensive",
                "dosage_forms": ["5mg", "10mg"],
                "frequency": ["Once daily"],
                "side_effects": ["Dizziness", "Swelling", "Headache"],
                "image_url": None,
                "hindi_name": "एम्लोडिपाइन",
                "hindi_description": "उच्च रक्तचाप के लिए दवा"
            },
            {
                "id": "MED003",
                "name": "Paracetamol",
                "generic_name": "Acetaminophen",
                "category": "Analgesic",
                "dosage_forms": ["500mg", "650mg"],
                "frequency": ["As needed", "Every 4-6 hours"],
                "side_effects": ["Rare liver problems", "Allergic reactions"],
                "image_url": None,
                "hindi_name": "पैरासिटामोल",
                "hindi_description": "दर्द और बुखार के लिए दवा"
            },
            {
                "id": "MED004",
                "name": "Omeprazole",
                "generic_name": "Omeprazole",
                "category": "Proton Pump Inhibitor",
                "dosage_forms": ["20mg", "40mg"],
                "frequency": ["Once daily", "Twice daily"],
                "side_effects": ["Headache", "Nausea", "Abdominal pain"],
                "image_url": None,
                "hindi_name": "ओमेप्राजोल",
                "hindi_description": "एसिडिटी के लिए दवा"
            }
        ]
    
    def load_pharmacy_inventory(self):
        """Load pharmacy inventory"""
        return {
            "MED001": {"stock": 150, "price": 25.50, "expiry": "2025-12-31"},
            "MED002": {"stock": 200, "price": 45.00, "expiry": "2025-10-15"},
            "MED003": {"stock": 500, "price": 12.75, "expiry": "2026-03-20"},
            "MED004": {"stock": 300, "price": 35.25, "expiry": "2025-11-30"}
        }
    
    def create_prescription(self, patient_id, doctor_id, medications, diagnosis, notes=""):
        """Create a new prescription"""
        prescription_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "medications": medications,
            "diagnosis": diagnosis,
            "notes": notes,
            "status": "Active",
            "created_at": datetime.now().isoformat()
        }
        
        prescription_id = db.add_prescription(prescription_data)
        return prescription_id
    
    def generate_prescription_qr(self, prescription_id, prescription_data):
        """Generate QR code for prescription"""
        qr_data = {
            "prescription_id": prescription_id,
            "patient_id": prescription_data["patient_id"],
            "doctor_id": prescription_data["doctor_id"],
            "medications": prescription_data["medications"],
            "diagnosis": prescription_data["diagnosis"],
            "created_at": prescription_data["created_at"]
        }
        
        import json
        return json.dumps(qr_data)
    
    def check_medication_availability(self, medication_id, quantity):
        """Check if medication is available in pharmacy"""
        if medication_id in self.pharmacy_inventory:
            inventory = self.pharmacy_inventory[medication_id]
            return inventory["stock"] >= quantity
        return False
    
    def calculate_prescription_cost(self, medications):
        """Calculate total cost of prescription"""
        total_cost = 0
        for med in medications:
            if med["medication_id"] in self.pharmacy_inventory:
                price = self.pharmacy_inventory[med["medication_id"]]["price"]
                quantity = med.get("quantity", 1)
                total_cost += price * quantity
        return total_cost
    
    def get_medication_reminders(self, prescription_id):
        """Generate medication reminders"""
        prescription = db.get_prescription(prescription_id)
        if not prescription:
            return []
        
        reminders = []
        for medication in prescription["medications"]:
            frequency = medication.get("frequency", "Once daily")
            duration = medication.get("duration", "7 days")
            
            # Generate reminder schedule
            if "Twice daily" in frequency:
                reminders.append({
                    "medication": medication["name"],
                    "time": "09:00",
                    "message": f"Take {medication['name']} - Morning dose"
                })
                reminders.append({
                    "medication": medication["name"],
                    "time": "21:00",
                    "message": f"Take {medication['name']} - Evening dose"
                })
            else:
                reminders.append({
                    "medication": medication["name"],
                    "time": "09:00",
                    "message": f"Take {medication['name']}"
                })
        
        return reminders

def main():
    """Main function for Digital Prescription & QR Pharmacy module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the Prescription System")
        return
    
    # Initialize prescription system
    prescription_system = PrescriptionSystem()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">💊 Digital Prescription & QR Pharmacy</h1>
        <p class="body-text">AI-powered prescription management with QR code integration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Voice assistant
    voice_assistant = VoiceAssistant()
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Create Prescription")
        
        # Prescription creation form
        with st.form("prescription_form"):
            # Patient selection
            patient_id = st.session_state.get('user', 'demo_user')
            st.info(f"Patient: {patient_id}")
            
            # Doctor selection
            doctors = db.doctors
            doctor_options = [f"{doc['name']} - {doc['specialization']}" for doc in doctors]
            selected_doctor = st.selectbox("Select Doctor", doctor_options)
            doctor_id = doctors[doctor_options.index(selected_doctor)]["id"]
            
            # Diagnosis
            diagnosis = st.text_input("Diagnosis", placeholder="Enter diagnosis...")
            
            # Medication selection
            st.markdown("#### 💊 Medications")
            
            medications = []
            num_medications = st.number_input("Number of medications", min_value=1, max_value=10, value=1)
            
            for i in range(num_medications):
                st.markdown(f"**Medication {i+1}**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Medication selection
                    medication_options = [f"{med['name']} ({med['generic_name']})" for med in prescription_system.medications]
                    selected_med = st.selectbox(f"Medication {i+1}", medication_options, key=f"med_{i}")
                    
                    # Get selected medication
                    selected_medication = prescription_system.medications[medication_options.index(selected_med)]
                    
                    # Dosage form
                    dosage_form = st.selectbox("Dosage Form", selected_medication["dosage_forms"], key=f"dosage_{i}")
                    
                    # Frequency
                    frequency = st.selectbox("Frequency", selected_medication["frequency"], key=f"freq_{i}")
                
                with col2:
                    # Duration
                    duration = st.selectbox("Duration", ["7 days", "14 days", "30 days", "60 days", "90 days"], key=f"duration_{i}")
                    
                    # Quantity
                    quantity = st.number_input("Quantity", min_value=1, value=30, key=f"qty_{i}")
                    
                    # Instructions
                    instructions = st.text_area("Special Instructions", placeholder="Take with food, etc.", key=f"instructions_{i}")
                
                # Check availability
                if prescription_system.check_medication_availability(selected_medication["id"], quantity):
                    st.success(f"✅ {selected_medication['name']} available in pharmacy")
                else:
                    st.error(f"❌ {selected_medication['name']} not available in sufficient quantity")
                
                medications.append({
                    "medication_id": selected_medication["id"],
                    "name": selected_medication["name"],
                    "dosage": dosage_form,
                    "frequency": frequency,
                    "duration": duration,
                    "quantity": quantity,
                    "instructions": instructions
                })
            
            # Notes
            notes = st.text_area("Additional Notes", placeholder="Any additional instructions...")
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("💊 Create Prescription", use_container_width=True)
            
            if submit_button:
                if diagnosis and medications:
                    # Create prescription
                    prescription_id = prescription_system.create_prescription(
                        patient_id,
                        doctor_id,
                        medications,
                        diagnosis,
                        notes
                    )
                    
                    if prescription_id:
                        st.success("✅ Prescription created successfully!")
                        
                        # Generate QR code
                        prescription_data = {
                            "patient_id": patient_id,
                            "doctor_id": doctor_id,
                            "medications": medications,
                            "diagnosis": diagnosis,
                            "created_at": datetime.now().isoformat()
                        }
                        
                        qr_data = prescription_system.generate_prescription_qr(prescription_id, prescription_data)
                        display_qr_code(qr_data, "Prescription QR Code")
                        
                        # Calculate cost
                        total_cost = prescription_system.calculate_prescription_cost(medications)
                        st.info(f"💰 Total Cost: ₹{total_cost:.2f}")
                        
                        # Voice confirmation
                        voice_assistant.speak(f"Prescription created successfully. Total cost is {total_cost:.2f} rupees.")
                    else:
                        st.error("❌ Failed to create prescription. Please try again.")
                else:
                    st.error("❌ Please fill in all required fields.")
    
    with col2:
        st.markdown("### 📊 Prescription Stats")
        
        # Statistics
        total_prescriptions = len(db.prescriptions)
        active_prescriptions = len([p for p in db.prescriptions if p["status"] == "Active"])
        total_cost = sum([prescription_system.calculate_prescription_cost(p["medications"]) for p in db.prescriptions])
        
        create_metric_card("Total Prescriptions", total_prescriptions)
        create_metric_card("Active Prescriptions", active_prescriptions)
        create_metric_card("Total Cost", f"₹{total_cost:.2f}")
        
        # Pharmacy inventory
        st.markdown("### 🏥 Pharmacy Inventory")
        
        for med_id, inventory in prescription_system.pharmacy_inventory.items():
            medication = next((med for med in prescription_system.medications if med["id"] == med_id), None)
            if medication:
                stock_color = "green" if inventory["stock"] > 50 else "orange" if inventory["stock"] > 20 else "red"
                st.markdown(f"""
                <div class="module-card">
                    <h4>{medication['name']}</h4>
                    <p><strong>Stock:</strong> <span style="color: {stock_color};">{inventory['stock']} units</span></p>
                    <p><strong>Price:</strong> ₹{inventory['price']:.2f}</p>
                    <p><strong>Expiry:</strong> {inventory['expiry']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Voice commands
        st.markdown("### 🎤 Voice Commands")
        
        if st.button("🎤 Voice Prescription"):
            st.info("🎤 Say 'create prescription' to start voice prescription creation")
            # Simulate voice prescription
            st.success("✅ Voice prescription creation initiated!")
        
        if st.button("🔊 Check Inventory"):
            voice_assistant.speak("Checking pharmacy inventory status.")
    
    # Prescription history
    st.markdown("---")
    st.markdown("### 📋 Prescription History")
    
    patient_prescriptions = db.get_patient_prescriptions(patient_id)
    
    if patient_prescriptions:
        for prescription in patient_prescriptions:
            with st.expander(f"📋 Prescription {prescription['id']} - {prescription['date']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Diagnosis:** {prescription['diagnosis']}")
                    st.markdown(f"**Doctor:** {prescription['doctor_id']}")
                    st.markdown(f"**Status:** {prescription['status']}")
                    
                    if prescription.get('notes'):
                        st.markdown(f"**Notes:** {prescription['notes']}")
                
                with col2:
                    st.markdown("**Medications:**")
                    for med in prescription['medications']:
                        st.markdown(f"• {med['name']} {med['dosage']} - {med['frequency']}")
                    
                    # Generate QR code for this prescription
                    qr_data = prescription_system.generate_prescription_qr(prescription['id'], prescription)
                    display_qr_code(qr_data, f"QR Code - {prescription['id']}")
    else:
        st.info("No prescription history found.")
    
    # Medication reminders
    st.markdown("---")
    st.markdown("### ⏰ Medication Reminders")
    
    if patient_prescriptions:
        active_prescriptions = [p for p in patient_prescriptions if p["status"] == "Active"]
        
        if active_prescriptions:
            for prescription in active_prescriptions:
                reminders = prescription_system.get_medication_reminders(prescription['id'])
                
                st.markdown(f"**Reminders for Prescription {prescription['id']}:**")
                for reminder in reminders:
                    st.markdown(f"⏰ {reminder['time']} - {reminder['message']}")
        else:
            st.info("No active prescriptions for reminders.")
    else:
        st.info("No prescriptions found for reminders.")
    
    # Medicine image integration
    st.markdown("---")
    st.markdown("### 🖼️ Medicine Visualizations")
    
    st.markdown("#### Add Custom Medicine Images")
    
    for medication in prescription_system.medications[:3]:  # Show first 3 medications
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"**{medication['name']}**")
            st.write(f"Category: {medication['category']}")
            st.write(f"Generic: {medication['generic_name']}")
        
        with col2:
            image_url = create_image_url_input(
                f"Image URL for {medication['name']}",
                key=f"med_image_url_{medication['id']}"
            )
            
            if image_url:
                create_medicine_image_display(medication['name'], image_url)
            else:
                create_medicine_image_display(medication['name'])

def create_prescription_analytics():
    """Create prescription analytics dashboard"""
    st.markdown("### 📈 Prescription Analytics")
    
    # Get prescription data
    prescriptions_df = pd.DataFrame(db.prescriptions)
    
    if not prescriptions_df.empty:
        # Convert date column
        prescriptions_df['date'] = pd.to_datetime(prescriptions_df['date'])
        
        # Monthly prescription trend
        monthly_prescriptions = prescriptions_df.groupby(prescriptions_df['date'].dt.to_period('M')).size().reset_index(name='count')
        
        fig = px.line(monthly_prescriptions, x='date', y='count', title='Monthly Prescription Trend')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Most prescribed medications
        all_medications = []
        for prescription in db.prescriptions:
            for med in prescription['medications']:
                all_medications.append(med['name'])
        
        if all_medications:
            medication_counts = pd.Series(all_medications).value_counts()
            
            fig2 = px.bar(
                x=medication_counts.index,
                y=medication_counts.values,
                title="Most Prescribed Medications"
            )
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No prescription data available for analytics.")

if __name__ == "__main__":
    main()
