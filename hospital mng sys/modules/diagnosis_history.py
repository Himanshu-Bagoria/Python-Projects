import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.database import db
from utils.auth import auth_manager, login_required

@login_required
def diagnosis_history():
    """Diagnosis history management"""
    st.title("📋 Medical Records & Diagnosis History")
    
    tabs = st.tabs(["📝 Add Record", "📊 View History", "🔍 Search Records"])
    
    with tabs[0]:
        add_medical_record()
    with tabs[1]:
        view_medical_history()
    with tabs[2]:
        search_medical_records()

def add_medical_record():
    """Add new medical record"""
    if not auth_manager.has_permission('create_medical_records'):
        st.error("You don't have permission to add medical records.")
        return
    
    st.header("Add Medical Record")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Patient selection
        patients_df = db.get_patients()
        selected_patient = None
        if not patients_df.empty:
            patient_options = [f"{row['patient_id']} - {row['first_name']} {row['last_name']}" 
                             for _, row in patients_df.iterrows()]
            selected_patient = st.selectbox("Select Patient", patient_options)
        else:
            st.warning("No patients found. Please add patients first.")
            return
        
        # Record date
        record_date = st.date_input("Record Date", value=date.today())
        
        # Chief complaint
        chief_complaint = st.text_area("Chief Complaint", placeholder="Patient's main concern...")
    
    with col2:
        # Appointment reference
        appointment_id = st.text_input("Appointment ID (Optional)")
        
        # Vital signs
        st.subheader("Vital Signs")
        temperature = st.number_input("Temperature (°F)", value=98.6)
        blood_pressure = st.text_input("Blood Pressure", placeholder="120/80")
        heart_rate = st.number_input("Heart Rate (bpm)", value=70)
        respiratory_rate = st.number_input("Respiratory Rate", value=16)
    
    # Physical examination
    st.subheader("Physical Examination")
    physical_exam = st.text_area("Physical Examination Findings", height=100)
    
    # Diagnosis
    st.subheader("Diagnosis")
    primary_diagnosis = st.text_area("Primary Diagnosis")
    secondary_diagnosis = st.text_area("Secondary Diagnosis (Optional)")
    
    # Treatment plan
    st.subheader("Treatment Plan")
    treatment_plan = st.text_area("Treatment Plan", height=100)
    
    # Follow-up
    follow_up_required = st.checkbox("Follow-up Required")
    if follow_up_required:
        follow_up_date = st.date_input("Follow-up Date")
        follow_up_notes = st.text_area("Follow-up Instructions")
    
    if st.button("Save Medical Record", type="primary"):
        if not selected_patient:
            st.error("Please select a patient first.")
            return
            
        record_data = {
            'patient_id': selected_patient.split(' - ')[0] if selected_patient else None,
            'record_date': record_date,
            'chief_complaint': chief_complaint,
            'vitals': f"T:{temperature}°F, BP:{blood_pressure}, HR:{heart_rate}, RR:{respiratory_rate}",
            'physical_exam': physical_exam,
            'primary_diagnosis': primary_diagnosis,
            'secondary_diagnosis': secondary_diagnosis,
            'treatment_plan': treatment_plan
        }
        
        if record_data['patient_id'] and primary_diagnosis:
            st.success("Medical record saved successfully!")
        else:
            st.error("Please fill in required fields.")

def view_medical_history():
    """View patient medical history"""
    st.header("Medical History")
    
    # Patient selection
    patients_df = db.get_patients()
    if not patients_df.empty:
        patient_options = [f"{row['patient_id']} - {row['first_name']} {row['last_name']}" 
                         for _, row in patients_df.iterrows()]
        selected_patient = st.selectbox("Select Patient", patient_options, key="history_patient")
        
        if selected_patient:
            patient_id = selected_patient.split(' - ')[0]
            
            # Sample medical records
            records = pd.DataFrame({
                'Date': ['2025-08-25', '2025-08-20', '2025-08-15'],
                'Chief Complaint': ['Headache', 'Chest pain', 'Fever'],
                'Diagnosis': ['Tension headache', 'Anxiety', 'Viral fever'],
                'Doctor': ['Dr. Smith', 'Dr. Johnson', 'Dr. Brown'],
                'Treatment': ['Rest, OTC pain relief', 'Counseling', 'Symptomatic treatment']
            })
            
            st.subheader(f"Medical History for {selected_patient}")
            
            for idx, record in records.iterrows():
                with st.expander(f"{record['Date']} - {record['Chief Complaint']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Diagnosis:** {record['Diagnosis']}")
                        st.write(f"**Doctor:** {record['Doctor']}")
                    with col2:
                        st.write(f"**Treatment:** {record['Treatment']}")

def search_medical_records():
    """Search medical records"""
    st.header("Search Medical Records")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_type = st.selectbox("Search by", ["Diagnosis", "Date Range", "Doctor"])
    
    with col2:
        if search_type == "Diagnosis":
            search_term = st.text_input("Enter diagnosis keyword")
        elif search_type == "Date Range":
            start_date = st.date_input("Start Date")
        else:
            search_term = st.text_input("Enter doctor name")
    
    with col3:
        if search_type == "Date Range":
            end_date = st.date_input("End Date")
    
    if st.button("Search"):
        st.info("Search results would be displayed here.")