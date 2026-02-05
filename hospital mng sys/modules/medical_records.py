import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
from utils.database import db
from utils.auth import auth_manager, login_required

@login_required
def medical_records():
    """Medical records management"""
    st.title("📋 Medical Records Management")
    
    tabs = st.tabs(["➕ Create Record", "📋 View Records", "🔍 Search Records", "📊 Records Analytics"])
    
    with tabs[0]:
        create_medical_record()
    with tabs[1]:
        view_medical_records()
    with tabs[2]:
        search_medical_records()
    with tabs[3]:
        records_analytics()

def create_medical_record():
    """Create new medical record"""
    st.header("➕ Create New Medical Record")
    
    user = auth_manager.get_current_user()
    if user['role'] not in ['admin', 'doctor']:
        st.error("🚫 Access Denied: Only administrators and doctors can create medical records.")
        return
    
    with st.form("create_record_form", clear_on_submit=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("👤 Patient Information")
            
            # Patient selection
            patients_df = db.get_patients()
            if not patients_df.empty:
                patient_options = [f"{row['patient_id']} - {row['first_name']} {row['last_name']}" 
                                 for _, row in patients_df.iterrows()]
                selected_patient = st.selectbox("Select Patient*", patient_options, key="medical_record_patient_select")
                patient_id = selected_patient.split(' - ')[0] if selected_patient else None
            else:
                st.warning("No patients found. Please add patients first.")
                patient_id = None
            
            # Doctor info (auto-filled)
            doctor_name = f"Dr. {user['username']}"
            st.text_input("Attending Doctor", value=doctor_name, disabled=True)
            doctor_id = f"DR{user['id']:03d}"
        
        with col2:
            st.subheader("📅 Record Details")
            record_date = st.date_input("Record Date*", value=date.today())
            record_type = st.selectbox("Record Type", [
                "Consultation", "Follow-up", "Emergency", "Surgery", 
                "Lab Results", "Imaging", "Discharge Summary", "Other"
            ], key="medical_record_type")
        
        # Medical Information
        st.subheader("🏥 Medical Information")
        
        col3, col4 = st.columns(2)
        
        with col3:
            # Chief complaint and symptoms
            chief_complaint = st.text_area("Chief Complaint*", 
                                         placeholder="Patient's main concern or reason for visit")
            
            symptoms = st.text_area("Symptoms", 
                                  placeholder="List of symptoms observed/reported")
            
            # Physical examination
            physical_examination = st.text_area("Physical Examination", 
                                               placeholder="Physical examination findings")
        
        with col4:
            # Diagnosis
            diagnosis = st.text_area("Diagnosis*", 
                                   placeholder="Primary and secondary diagnoses")
            
            # Treatment plan
            treatment = st.text_area("Treatment Plan", 
                                   placeholder="Prescribed treatment, procedures, etc.")
            
            # Follow-up
            follow_up_date = st.date_input("Follow-up Date", value=None)
            follow_up_instructions = st.text_area("Follow-up Instructions", 
                                                 placeholder="Instructions for next visit")
        
        # Vital Signs
        st.subheader("📊 Vital Signs")
        
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            temperature = st.number_input("Temperature (°F)", min_value=90.0, max_value=110.0, value=98.6, step=0.1)
            blood_pressure_systolic = st.number_input("BP Systolic (mmHg)", min_value=70, max_value=200, value=120)
        
        with col6:
            pulse_rate = st.number_input("Pulse Rate (bpm)", min_value=40, max_value=150, value=72)
            blood_pressure_diastolic = st.number_input("BP Diastolic (mmHg)", min_value=40, max_value=120, value=80)
        
        with col7:
            respiratory_rate = st.number_input("Respiratory Rate (breaths/min)", min_value=10, max_value=40, value=16)
            oxygen_saturation = st.number_input("Oxygen Saturation (%)", min_value=70, max_value=100, value=98)
        
        with col8:
            weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1)
            height = st.number_input("Height (cm)", min_value=30.0, max_value=250.0, value=170.0, step=0.1)
        
        # Medications and Lab Orders
        st.subheader("💊 Medications & Lab Orders")
        
        col9, col10 = st.columns(2)
        
        with col9:
            prescribed_medications = st.text_area("Prescribed Medications", 
                                                placeholder="List medications with dosage, frequency, duration")
            
        with col10:
            lab_orders = st.text_area("Lab Orders", 
                                    placeholder="Ordered laboratory tests")
        
        # Additional Notes
        st.subheader("📝 Additional Notes")
        
        notes = st.text_area("Doctor's Notes", 
                           placeholder="Additional observations, recommendations, or notes")
        
        # Submit button
        st.markdown("---")
        
        col_submit1, col_submit2 = st.columns([3, 1])
        with col_submit1:
            submitted = st.form_submit_button("📋 Create Medical Record", type="primary", use_container_width=True)
        
        if submitted:
            if not all([patient_id, chief_complaint, diagnosis]):
                st.error("❌ Please fill in all required fields marked with *")
            else:
                # Prepare vitals data
                vitals_data = {
                    'temperature': temperature,
                    'blood_pressure': f"{blood_pressure_systolic}/{blood_pressure_diastolic}",
                    'pulse_rate': pulse_rate,
                    'respiratory_rate': respiratory_rate,
                    'oxygen_saturation': oxygen_saturation,
                    'weight': weight,
                    'height': height,
                    'bmi': round(weight / ((height/100) ** 2), 2)
                }
                
                # Create record
                record_data = {
                    'patient_id': patient_id,
                    'doctor_id': doctor_id,
                    'record_date': record_date,
                    'record_type': record_type,
                    'chief_complaint': chief_complaint,
                    'symptoms': symptoms,
                    'physical_examination': physical_examination,
                    'diagnosis': diagnosis,
                    'treatment': treatment,
                    'prescribed_medications': prescribed_medications,
                    'lab_orders': lab_orders,
                    'vitals': json.dumps(vitals_data),
                    'follow_up_date': follow_up_date,
                    'follow_up_instructions': follow_up_instructions,
                    'notes': notes
                }
                
                record_id = create_medical_record_in_db(record_data)
                
                if record_id:
                    st.success(f"✅ Medical record created successfully!")
                    st.info(f"📋 Record ID: {record_id}")
                    
                    # Log the action
                    db.log_action(user['id'], 'create_medical_record', 'medical_records', record_id)
                else:
                    st.error("❌ Failed to create medical record. Please try again.")

def create_medical_record_in_db(record_data):
    """Create medical record in database"""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Generate record ID
        record_id = f"MR{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        try:
            cursor.execute('''
                INSERT INTO medical_records (
                    record_id, patient_id, doctor_id, record_date, diagnosis,
                    symptoms, treatment, prescriptions, lab_results, vitals,
                    follow_up_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record_id,
                record_data['patient_id'],
                record_data['doctor_id'],
                record_data['record_date'],
                record_data['diagnosis'],
                record_data.get('symptoms'),
                record_data.get('treatment'),
                record_data.get('prescribed_medications'),
                record_data.get('lab_orders'),
                record_data.get('vitals'),
                record_data.get('follow_up_date')
            ))
            
            conn.commit()
            return record_id
        except Exception as e:
            st.error(f"Database error: {str(e)}")
            return None

def view_medical_records():
    """View existing medical records"""
    st.header("📋 View Medical Records")
    
    user = auth_manager.get_current_user()
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if user['role'] == 'admin':
            view_type = st.selectbox("View Type", ["All Records", "By Patient", "By Doctor", "My Records"], key="records_view_type_admin")
        elif user['role'] == 'doctor':
            view_type = st.selectbox("View Type", ["My Records", "By Patient"], key="records_view_type_doctor")
        else:
            view_type = "My Records"
    
    with col2:
        if view_type == "By Patient":
            patients_df = db.get_patients()
            if not patients_df.empty:
                patient_options = ["All"] + [f"{row['patient_id']} - {row['first_name']} {row['last_name']}" 
                                           for _, row in patients_df.iterrows()]
                selected_patient = st.selectbox("Select Patient", patient_options, key="records_patient_filter")
                patient_filter = None if selected_patient == "All" else selected_patient.split(' - ')[0]
            else:
                patient_filter = None
        else:
            patient_filter = None
    
    with col3:
        date_from = st.date_input("From Date", value=None)
    
    # Get records from database (sample implementation)
    records_data = get_sample_medical_records()
    
    if not records_data.empty:
        st.subheader(f"📊 Found {len(records_data)} medical records")
        
        # Display records
        for idx, record in records_data.iterrows():
            with st.expander(f"📋 {record['Record ID']} - {record['Patient']} - {record['Date']}", expanded=False):
                
                col_a, col_b = st.columns([3, 1])
                
                with col_a:
                    st.markdown(f"**Record ID:** {record['Record ID']}")
                    st.markdown(f"**Patient:** {record['Patient']}")
                    st.markdown(f"**Doctor:** {record['Doctor']}")
                    st.markdown(f"**Date:** {record['Date']}")
                    st.markdown(f"**Type:** {record['Type']}")
                    st.markdown(f"**Diagnosis:** {record['Diagnosis']}")
                
                with col_b:
                    if st.button(f"👁️ View Full", key=f"view_{record['Record ID']}"):
                        show_full_medical_record(record)
                    
                    if user['role'] in ['admin', 'doctor']:
                        if st.button(f"✏️ Edit", key=f"edit_{record['Record ID']}"):
                            st.info("Edit functionality would be implemented here")
    else:
        st.info("📋 No medical records found matching your criteria.")

def search_medical_records():
    """Search medical records"""
    st.header("🔍 Search Medical Records")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search records...", 
                                   placeholder="Search by diagnosis, symptoms, patient name, or record ID")
    
    with col2:
        search_type = st.selectbox("Search In", [
            "All Fields", "Diagnosis", "Symptoms", "Patient Name", "Record ID"
        ], key="records_search_type")
    
    if search_term:
        # Sample search results
        st.subheader("🔍 Search Results")
        
        # This would be replaced with actual database search
        sample_results = get_sample_medical_records()
        
        if not sample_results.empty:
            # Filter based on search term (simplified)
            filtered_results = sample_results[
                sample_results['Diagnosis'].str.contains(search_term, case=False, na=False) |
                sample_results['Patient'].str.contains(search_term, case=False, na=False)
            ]
            
            if not filtered_results.empty:
                st.dataframe(filtered_results, use_container_width=True)
            else:
                st.info("No records found matching your search criteria.")
        else:
            st.info("No records available to search.")

def records_analytics():
    """Medical records analytics"""
    st.header("📊 Medical Records Analytics")
    
    user = auth_manager.get_current_user()
    if user['role'] not in ['admin', 'doctor']:
        st.error("🚫 Access Denied: Only administrators and doctors can view analytics.")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", "1,234", delta="+23 this week")
    
    with col2:
        st.metric("Active Patients", "456", delta="+12")
    
    with col3:
        st.metric("Average Records/Day", "15.2", delta="+2.1")
    
    with col4:
        st.metric("Follow-ups Pending", "89", delta="-5")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Most common diagnoses
        st.subheader("📊 Most Common Diagnoses")
        
        diagnoses_data = {
            'Diagnosis': ['Hypertension', 'Diabetes', 'Common Cold', 'Anxiety', 'Back Pain'],
            'Count': [45, 38, 32, 28, 25]
        }
        
        import plotly.express as px
        fig = px.bar(x=diagnoses_data['Count'], y=diagnoses_data['Diagnosis'], 
                    orientation='h', title="Top 5 Diagnoses")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Records by month
        st.subheader("📈 Records Trend")
        
        monthly_data = {
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Records': [234, 267, 289, 298, 312, 334]
        }
        
        fig = px.line(x=monthly_data['Month'], y=monthly_data['Records'], 
                     title="Monthly Records Created")
        st.plotly_chart(fig, use_container_width=True)

def show_full_medical_record(record):
    """Show full medical record details"""
    st.markdown("---")
    st.subheader(f"📋 Complete Medical Record - {record['Record ID']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Record ID:** {record['Record ID']}")
        st.markdown(f"**Patient:** {record['Patient']}")
        st.markdown(f"**Doctor:** {record['Doctor']}")
        st.markdown(f"**Date:** {record['Date']}")
        st.markdown(f"**Type:** {record['Type']}")
        st.markdown(f"**Diagnosis:** {record['Diagnosis']}")
        
        # Additional details would be shown here
        st.markdown("**Symptoms:** Fever, headache, body ache")
        st.markdown("**Treatment:** Rest, medication as prescribed")
        st.markdown("**Follow-up:** 1 week")
    
    with col2:
        st.markdown("**Actions:**")
        if st.button("🖨️ Print Record", key=f"print_record_{record['Record ID']}"):
            st.success("Record sent to printer!")
        
        if st.button("📧 Email to Patient", key=f"email_record_{record['Record ID']}"):
            st.success("Record emailed to patient!")
        
        if st.button("📋 Create Follow-up", key=f"followup_record_{record['Record ID']}"):
            st.success("Follow-up appointment created!")

def get_sample_medical_records():
    """Get sample medical records data"""
    return pd.DataFrame({
        'Record ID': ['MR20250825001', 'MR20250825002', 'MR20250825003', 'MR20250825004'],
        'Patient': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown'],
        'Doctor': ['Dr. Smith', 'Dr. Johnson', 'Dr. Brown', 'Dr. Davis'],
        'Date': ['2025-08-25', '2025-08-24', '2025-08-23', '2025-08-22'],
        'Type': ['Consultation', 'Follow-up', 'Emergency', 'Consultation'],
        'Diagnosis': ['Common Cold', 'Diabetes Follow-up', 'Chest Pain', 'Hypertension']
    })