import streamlit as st
import sys
import os
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent / "modules"))
sys.path.append(str(Path(__file__).parent / "utils"))

# Import utility modules
try:
    from utils.ui_components import *
    from utils.auth import *
    from utils.database import *
    from utils.data_manager import data_manager
    from utils.token_manager import token_manager
    from config.themes import *
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Please ensure all required files are present.")

# Page configuration
st.set_page_config(
    page_title="🏥 Smart Hospital System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic design with blue background
def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Blue background for the entire app */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #4a90e2 100%);
        color: white;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        to { box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6); }
    }
    
    .module-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.95), rgba(230,230,230,0.95));
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        border: 2px solid transparent;
        color: #333333;
    }
    
    .module-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        border-color: #667eea;
    }
    
    .glow-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .glow-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 10px;
        border: 2px solid #667eea;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .home-button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        margin: 1rem 0;
        width: 100%;
    }
    
    .home-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
    }
    
    .futuristic-text {
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }
    
    .body-text {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 400;
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .floating {
        animation: floating 3s ease-in-out infinite;
    }
    
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .module-content {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        color: #333333;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def show_home_dashboard():
    """Display the home dashboard"""
    st.markdown("""
    <div class="main-header">
        <h1 class="futuristic-text" style="font-size: 3rem; margin: 0;">🏥 Smart Hospital System</h1>
        <p class="body-text" style="font-size: 1.2rem; margin: 0.5rem 0;">Advanced Healthcare Management Platform</p>
        <p class="body-text" style="font-size: 1rem; opacity: 0.8;">AI-Powered • Multilingual • Futuristic Design • Token Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Real-time statistics
    st.markdown("### 📊 Live System Statistics")
    
    # Get token statistics
    token_stats = token_manager.get_token_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎫 Active Tokens", token_stats['waiting'], f"↗️ +{token_stats['called']}")
    with col2:
        st.metric("🏥 Departments", len(token_stats['departments']), "Active")
    with col3:
        st.metric("📈 Completed Today", token_stats['completed'], "✓")
    with col4:
        st.metric("⚡ System Status", "Healthy", "🟢")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎫 Generate Token", use_container_width=True):
            st.session_state.current_module = "token_management"
            st.rerun()
    
    with col2:
        if st.button("🚨 Emergency Alert", use_container_width=True):
            st.session_state.current_module = "emergency_alert"
            st.rerun()
    
    with col3:
        if st.button("📅 Book Appointment", use_container_width=True):
            st.session_state.current_module = "appointment_scheduler"
            st.rerun()
    
    # System overview
    st.markdown("### 🏥 System Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="module-card pulse">
            <h3>🎫 Token Management</h3>
            <p>Smart queue management with priority-based token system</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="module-card floating">
            <h3>🤖 AI-Powered Diagnostics</h3>
            <p>Machine learning algorithms for symptom analysis and disease prediction</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="module-card pulse">
            <h3>📊 Real-Time Monitoring</h3>
            <p>Live vital signs tracking with intelligent alert systems</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Department status
    if token_stats['departments']:
        st.markdown("### 🏥 Department Status")
        dept_cols = st.columns(len(token_stats['departments']))
        
        for i, (dept, stats) in enumerate(token_stats['departments'].items()):
            with dept_cols[i]:
                waiting = stats['waiting']
                if waiting > 10:
                    color = "🔴"
                elif waiting > 5:
                    color = "🟡"
                else:
                    color = "🟢"
                
                st.markdown(f"""
                <div class="module-card">
                    <h4>{color} {dept}</h4>
                    <p>Waiting: {waiting}</p>
                    <p>Called: {stats['called']}</p>
                    <p>Completed: {stats['completed']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Feature highlights
    st.markdown("### ✨ Advanced Features")
    
    features = [
        ("🎫 Smart Tokens", "Priority-based queue management with real-time updates"),
        ("🤖 AI Diagnostics", "Machine learning for symptom analysis and disease prediction"),
        ("📊 Live Analytics", "Real-time statistics and performance monitoring"),
        ("🔒 Secure Access", "Biometric authentication and encrypted data transmission"),
        ("📱 Mobile Ready", "Optimized for all devices and screen sizes"),
        ("🌐 Multilingual", "Support for English and Hindi with voice integration")
    ]
    
    for i in range(0, len(features), 2):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="module-card">
                <h4>{features[i][0]}</h4>
                <p>{features[i][1]}</p>
            </div>
            """, unsafe_allow_html=True)
        if i + 1 < len(features):
            with col2:
                st.markdown(f"""
                <div class="module-card">
                    <h4>{features[i+1][0]}</h4>
                    <p>{features[i+1][1]}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Quick start guide
    st.markdown("### 🚀 Quick Start Guide")
    st.info("""
    **To get started:**
    1. **🎫 Generate Token** - Create a waiting token for any department
    2. **🔐 Biometric Check-In** - Secure patient authentication
    3. **📅 Book Appointment** - Schedule doctor appointments
    4. **🤖 AI Symptom Analysis** - Get AI-powered health insights
    5. **📊 Health Dashboard** - Monitor vital signs and health metrics
    6. **💊 Digital Prescriptions** - Manage medications digitally
    
    **Advanced Features:**
    - Real-time token management with priority queuing
    - Department-wise statistics and monitoring
    - AI-powered diagnostics and recommendations
    - Comprehensive data management and export
    """)

def show_module_content(module_name):
    """Display content for each module"""
    st.markdown(f"""
    <div class="module-content">
        <h1 class="futuristic-text" style="color: #667eea;">{module_name}</h1>
        <p class="body-text">Welcome to the {module_name} module. Add your data and view saved information.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Module-specific content
    if "Token Management" in module_name:
        st.markdown("### 🎫 Token Management System")
        
        # Token generation
        with st.expander("🎫 Generate New Token", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                patient_name = st.text_input("Patient Name")
                department = st.selectbox("Department", [
                    "Emergency", "Cardiology", "Neurology", "Orthopedics", 
                    "Dermatology", "Pediatrics", "General Medicine", "Surgery",
                    "Radiology", "Laboratory", "Pharmacy", "Reception"
                ])
            with col2:
                priority = st.selectbox("Priority", ["Emergency", "High", "Normal", "Low"])
                phone = st.text_input("Phone Number (Optional)")
            
            if st.button("🎫 Generate Token"):
                if patient_name and department:
                    token_data = token_manager.generate_token(patient_name, department, priority)
                    st.success(f"✅ Token generated successfully!")
                    st.info(f"""
                    **Token Details:**
                    - Token ID: {token_data['token_id']}
                    - Token Number: {token_data['token_number']}
                    - Department: {token_data['department']}
                    - Priority: {token_data['priority']}
                    - Estimated Wait: {token_data['estimated_wait_minutes']} minutes
                    """)
                    st.rerun()
                else:
                    st.error("Please enter patient name and select department")
        
        # Token display
        st.markdown("### 📋 Current Tokens")
        
        # Department filter
        dept_filter = st.selectbox("Filter by Department", ["All"] + [
            "Emergency", "Cardiology", "Neurology", "Orthopedics", 
            "Dermatology", "Pediatrics", "General Medicine", "Surgery",
            "Radiology", "Laboratory", "Pharmacy", "Reception"
        ])
        
        # Get tokens
        if dept_filter == "All":
            waiting_tokens = token_manager.get_waiting_tokens()
        else:
            waiting_tokens = token_manager.get_waiting_tokens(dept_filter)
        
        if waiting_tokens:
            # Display tokens in a table format
            for i, token in enumerate(waiting_tokens):
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                    with col1:
                        st.write(f"**{token['token_number']}** - {token['patient_name']}")
                        st.write(f"Dept: {token['department']} | ID: {token['token_id']}")
                    with col2:
                        if token['priority'] == "Emergency":
                            st.error(token['priority'])
                        elif token['priority'] == "High":
                            st.warning(token['priority'])
                        else:
                            st.info(token['priority'])
                    with col3:
                        st.write(f"{token['estimated_wait_minutes']} min")
                    with col4:
                        if st.button("📢 Call", key=f"call_{token['token_id']}"):
                            token_manager.call_token(token['token_id'])
                            st.success(f"Token {token['token_number']} called!")
                            st.rerun()
                    with col5:
                        if st.button("✅ Complete", key=f"complete_{token['token_id']}"):
                            token_manager.complete_token(token['token_id'])
                            st.success(f"Token {token['token_number']} completed!")
                            st.rerun()
        else:
            st.info("No waiting tokens found.")
        
        # Token statistics
        st.markdown("### 📊 Token Statistics")
        stats = token_manager.get_token_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Tokens", stats['total_tokens'])
        with col2:
            st.metric("Waiting", stats['waiting'])
        with col3:
            st.metric("Called", stats['called'])
        with col4:
            st.metric("Completed", stats['completed'])
        
        # Department-wise stats
        if stats['departments']:
            st.markdown("### 🏥 Department Statistics")
            for dept, dept_stats in stats['departments'].items():
                with st.container():
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.write(f"**{dept}**")
                    with col2:
                        st.write(f"Waiting: {dept_stats['waiting']}")
                    with col3:
                        st.write(f"Called: {dept_stats['called']}")
                    with col4:
                        st.write(f"Completed: {dept_stats['completed']}")
    
    elif "Biometric" in module_name:
        st.markdown("### 🔐 Authentication Methods")
        
        # Add new authentication record
        with st.expander("➕ Add New Authentication Record", expanded=True):
            patient_name = st.text_input("Patient Name")
            auth_method = st.selectbox("Authentication Method", ["Fingerprint Scan", "Face Recognition", "Traditional Login"])
            notes = st.text_area("Notes")
            
            if st.button("🔐 Save Authentication Record"):
                if patient_name:
                    auth_data = {
                        "patient_name": patient_name,
                        "auth_method": auth_method,
                        "notes": notes,
                        "status": "Authenticated"
                    }
                    data_manager.save_data("authentication", auth_data)
                    st.success("✅ Authentication record saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name")
        
        # View saved authentication records
        st.markdown("### 📋 Saved Authentication Records")
        auth_records = data_manager.load_data("authentication")
        if auth_records:
            for i, record in enumerate(auth_records):
                try:
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            patient_name = record.get('patient_name', 'Unknown Patient')
                            auth_method = record.get('auth_method', 'Unknown')
                            notes = record.get('notes', '')
                            timestamp = record.get('timestamp', '')[:10] if record.get('timestamp') else 'Unknown'
                            
                            st.write(f"**{patient_name}** - {auth_method}")
                            st.write(f"Notes: {notes}")
                            st.write(f"Date: {timestamp}")
                        with col2:
                            status = record.get('status', 'Unknown')
                            st.success(status)
                        with col3:
                            if st.button("🗑️", key=f"del_auth_{record.get('id', i)}"):
                                data_manager.delete_data("authentication", record.get('id', i))
                                st.rerun()
                except Exception as e:
                    st.error(f"Error displaying record: {e}")
        else:
            st.info("No authentication records found. Add your first record above.")
            
    elif "Symptom" in module_name:
        st.markdown("### 🤖 AI Symptom Analysis")
        
        # Add new symptom analysis
        with st.expander("➕ Add New Symptom Analysis", expanded=True):
            patient_name = st.text_input("Patient Name")
            symptoms = st.multiselect("Select Symptoms", ["Fever", "Headache", "Cough", "Fatigue", "Nausea", "Chest Pain", "Dizziness", "Shortness of Breath"])
            severity = st.select_slider("Symptom Severity", options=["Mild", "Moderate", "Severe"])
            diagnosis = st.text_input("AI Diagnosis")
            treatment = st.text_area("Recommended Treatment")
            
            if st.button("🔍 Save Symptom Analysis"):
                if patient_name and symptoms:
                    symptom_data = {
                        "patient_name": patient_name,
                        "symptoms": symptoms,
                        "severity": severity,
                        "diagnosis": diagnosis,
                        "treatment": treatment
                    }
                    data_manager.save_data("symptoms", symptom_data)
                    st.success("✅ Symptom analysis saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name and select symptoms")
        
        # View saved symptom analyses
        st.markdown("### 📋 Saved Symptom Analyses")
        symptom_records = data_manager.load_data("symptoms")
        if symptom_records:
            for record in symptom_records:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}** - {record['severity']}")
                        st.write(f"Symptoms: {', '.join(record['symptoms'])}")
                        if record['diagnosis']:
                            st.write(f"Diagnosis: {record['diagnosis']}")
                        if record['treatment']:
                            st.write(f"Treatment: {record['treatment']}")
                        st.write(f"Date: {record['timestamp'][:10]}")
                    with col2:
                        if st.button("🗑️", key=f"del_symptom_{record['id']}"):
                            data_manager.delete_data("symptoms", record['id'])
                            st.rerun()
        else:
            st.info("No symptom analyses found. Add your first analysis above.")
            
    elif "Appointment" in module_name:
        st.markdown("### 📅 Appointment Scheduling")
        
        # Add new appointment
        with st.expander("➕ Add New Appointment", expanded=True):
            patient_name = st.text_input("Patient Name")
            appointment_date = st.date_input("Appointment Date")
            appointment_time = st.time_input("Appointment Time")
            doctor = st.selectbox("Select Doctor", ["Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown", "Dr. Davis"])
            reason = st.text_area("Reason for Visit")
            
            if st.button("📅 Save Appointment"):
                if patient_name and appointment_date:
                    appointment_data = {
                        "patient_name": patient_name,
                        "date": appointment_date.isoformat(),
                        "time": appointment_time.strftime("%H:%M"),
                        "doctor": doctor,
                        "reason": reason,
                        "status": "Scheduled"
                    }
                    data_manager.save_data("appointments", appointment_data)
                    st.success("✅ Appointment saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name and select date")
        
        # View saved appointments
        st.markdown("### 📋 Saved Appointments")
        appointment_records = data_manager.load_data("appointments")
        if appointment_records:
            for record in appointment_records:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}** - {record['doctor']}")
                        st.write(f"Date: {record['date']} at {record['time']}")
                        if record['reason']:
                            st.write(f"Reason: {record['reason']}")
                    with col2:
                        st.info(record['status'])
                    with col3:
                        if st.button("🗑️", key=f"del_appt_{record['id']}"):
                            data_manager.delete_data("appointments", record['id'])
                            st.rerun()
        else:
            st.info("No appointments found. Add your first appointment above.")
            
    elif "Health Dashboard" in module_name:
        st.markdown("### 📊 Health Metrics")
        
        # Add new health metrics
        with st.expander("➕ Add New Health Metrics", expanded=True):
            patient_name = st.text_input("Patient Name")
            col1, col2, col3 = st.columns(3)
            with col1:
                heart_rate = st.number_input("Heart Rate (BPM)", min_value=40, max_value=200, value=75)
            with col2:
                blood_pressure_sys = st.number_input("Systolic BP", min_value=70, max_value=200, value=120)
                blood_pressure_dia = st.number_input("Diastolic BP", min_value=40, max_value=120, value=80)
            with col3:
                temperature = st.number_input("Temperature (°F)", min_value=95.0, max_value=105.0, value=98.6, step=0.1)
            
            notes = st.text_area("Notes")
            
            if st.button("📊 Save Health Metrics"):
                if patient_name:
                    health_data = {
                        "patient_name": patient_name,
                        "heart_rate": heart_rate,
                        "blood_pressure": f"{blood_pressure_sys}/{blood_pressure_dia}",
                        "temperature": temperature,
                        "notes": notes
                    }
                    data_manager.save_data("health_metrics", health_data)
                    st.success("✅ Health metrics saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name")
        
        # View saved health metrics
        st.markdown("### 📋 Saved Health Metrics")
        health_records = data_manager.load_data("health_metrics")
        if health_records:
            for record in health_records:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}**")
                        if record['notes']:
                            st.write(f"Notes: {record['notes']}")
                        st.write(f"Date: {record['timestamp'][:10]}")
                    with col2:
                        st.metric("Heart Rate", f"{record['heart_rate']} BPM")
                    with col3:
                        st.metric("Blood Pressure", record['blood_pressure'])
                    with col4:
                        st.metric("Temperature", f"{record['temperature']}°F")
                        if st.button("🗑️", key=f"del_health_{record['id']}"):
                            data_manager.delete_data("health_metrics", record['id'])
                            st.rerun()
        else:
            st.info("No health metrics found. Add your first metrics above.")
            
    elif "Prescription" in module_name:
        st.markdown("### 💊 Digital Prescriptions")
        
        # Add new prescription
        with st.expander("➕ Add New Prescription", expanded=True):
            patient_name = st.text_input("Patient Name")
            medicine_name = st.text_input("Medicine Name")
            dosage = st.text_input("Dosage")
            frequency = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "As needed"])
            duration = st.text_input("Duration")
            instructions = st.text_area("Special Instructions")
            
            if st.button("💊 Save Prescription"):
                if patient_name and medicine_name:
                    prescription_data = {
                        "patient_name": patient_name,
                        "medicine_name": medicine_name,
                        "dosage": dosage,
                        "frequency": frequency,
                        "duration": duration,
                        "instructions": instructions,
                        "status": "Active"
                    }
                    data_manager.save_data("prescriptions", prescription_data)
                    st.success("✅ Prescription saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name and medicine name")
        
        # View saved prescriptions
        st.markdown("### 📋 Saved Prescriptions")
        prescription_records = data_manager.load_data("prescriptions")
        if prescription_records:
            for record in prescription_records:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}** - {record['medicine_name']}")
                        st.write(f"Dosage: {record['dosage']} - {record['frequency']}")
                        st.write(f"Duration: {record['duration']}")
                        if record['instructions']:
                            st.write(f"Instructions: {record['instructions']}")
                        st.write(f"Date: {record['timestamp'][:10]}")
                    with col2:
                        st.success(record['status'])
                    with col3:
                        if st.button("🗑️", key=f"del_prescription_{record['id']}"):
                            data_manager.delete_data("prescriptions", record['id'])
                            st.rerun()
        else:
            st.info("No prescriptions found. Add your first prescription above.")
            
    elif "Diagnosis" in module_name:
        st.markdown("### 📈 Diagnosis History")
        
        # Add new diagnosis
        with st.expander("➕ Add New Diagnosis", expanded=True):
            patient_name = st.text_input("Patient Name")
            diagnosis = st.text_input("Diagnosis")
            doctor = st.text_input("Doctor Name")
            date_diagnosed = st.date_input("Date Diagnosed")
            symptoms = st.text_area("Symptoms")
            treatment_plan = st.text_area("Treatment Plan")
            
            if st.button("📈 Save Diagnosis"):
                if patient_name and diagnosis:
                    diagnosis_data = {
                        "patient_name": patient_name,
                        "diagnosis": diagnosis,
                        "doctor": doctor,
                        "date_diagnosed": date_diagnosed.isoformat(),
                        "symptoms": symptoms,
                        "treatment_plan": treatment_plan
                    }
                    data_manager.save_data("diagnoses", diagnosis_data)
                    st.success("✅ Diagnosis saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name and diagnosis")
        
        # View saved diagnoses
        st.markdown("### 📋 Saved Diagnoses")
        diagnosis_records = data_manager.load_data("diagnoses")
        if diagnosis_records:
            for record in diagnosis_records:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}** - {record['diagnosis']}")
                        st.write(f"Doctor: {record['doctor']}")
                        st.write(f"Date: {record['date_diagnosed']}")
                        if record['symptoms']:
                            st.write(f"Symptoms: {record['symptoms']}")
                        if record['treatment_plan']:
                            st.write(f"Treatment: {record['treatment_plan']}")
                    with col2:
                        if st.button("🗑️", key=f"del_diagnosis_{record['id']}"):
                            data_manager.delete_data("diagnoses", record['id'])
                            st.rerun()
        else:
            st.info("No diagnoses found. Add your first diagnosis above.")
        
    elif "Wellness" in module_name:
        st.markdown("### 🧠 Mental Wellness")
        
        # Add new mood entry
        with st.expander("➕ Add New Mood Entry", expanded=True):
            patient_name = st.text_input("Patient Name")
            mood = st.select_slider("How are you feeling today?", options=["😢 Sad", "😐 Okay", "😊 Happy", "🤩 Great"])
            energy_level = st.select_slider("Energy Level", options=["Very Low", "Low", "Medium", "High", "Very High"])
            sleep_hours = st.number_input("Hours of Sleep", min_value=0, max_value=24, value=8)
            notes = st.text_area("How are you feeling? Any concerns?")
            
            if st.button("💭 Save Mood Entry"):
                if patient_name:
                    mood_data = {
                        "patient_name": patient_name,
                        "mood": mood,
                        "energy_level": energy_level,
                        "sleep_hours": sleep_hours,
                        "notes": notes
                    }
                    data_manager.save_data("mood_tracker", mood_data)
                    st.success("✅ Mood entry saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name")
        
        # View saved mood entries
        st.markdown("### 📋 Mood History")
        mood_records = data_manager.load_data("mood_tracker")
        if mood_records:
            for record in mood_records:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}** - {record['mood']}")
                        st.write(f"Energy: {record['energy_level']} | Sleep: {record['sleep_hours']}h")
                        if record['notes']:
                            st.write(f"Notes: {record['notes']}")
                        st.write(f"Date: {record['timestamp'][:10]}")
                    with col2:
                        st.write(record['mood'])
                    with col3:
                        if st.button("🗑️", key=f"del_mood_{record['id']}"):
                            data_manager.delete_data("mood_tracker", record['id'])
                            st.rerun()
        else:
            st.info("No mood entries found. Add your first entry above.")
            
    elif "Lab" in module_name:
        st.markdown("### 🔬 Lab Reports")
        
        # Add new lab report
        with st.expander("➕ Add New Lab Report", expanded=True):
            patient_name = st.text_input("Patient Name")
            test_name = st.text_input("Test Name")
            test_date = st.date_input("Test Date")
            result = st.selectbox("Result", ["Normal", "Abnormal", "Critical", "Pending"])
            value = st.text_input("Test Value")
            reference_range = st.text_input("Reference Range")
            notes = st.text_area("Notes")
            
            if st.button("🔬 Save Lab Report"):
                if patient_name and test_name:
                    lab_data = {
                        "patient_name": patient_name,
                        "test_name": test_name,
                        "test_date": test_date.isoformat(),
                        "result": result,
                        "value": value,
                        "reference_range": reference_range,
                        "notes": notes
                    }
                    data_manager.save_data("lab_reports", lab_data)
                    st.success("✅ Lab report saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name and test name")
        
        # View saved lab reports
        st.markdown("### 📋 Saved Lab Reports")
        lab_records = data_manager.load_data("lab_reports")
        if lab_records:
            for record in lab_records:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}** - {record['test_name']}")
                        st.write(f"Date: {record['test_date']}")
                        st.write(f"Value: {record['value']} (Range: {record['reference_range']})")
                        if record['notes']:
                            st.write(f"Notes: {record['notes']}")
                    with col2:
                        if record['result'] == "Normal":
                            st.success(record['result'])
                        elif record['result'] == "Abnormal":
                            st.warning(record['result'])
                        elif record['result'] == "Critical":
                            st.error(record['result'])
                        else:
                            st.info(record['result'])
                    with col3:
                        if st.button("🗑️", key=f"del_lab_{record['id']}"):
                            data_manager.delete_data("lab_reports", record['id'])
                            st.rerun()
        else:
            st.info("No lab reports found. Add your first report above.")
            
    elif "Navigation" in module_name:
        st.markdown("### 🗺️ Hospital Navigation")
        
        # Add new navigation request
        with st.expander("➕ Add Navigation Request", expanded=True):
            patient_name = st.text_input("Patient Name")
            destination = st.selectbox("Where would you like to go?", ["Emergency Room", "Pharmacy", "Laboratory", "Radiology", "Cafeteria", "Reception", "Ward"])
            special_needs = st.multiselect("Special Needs", ["Wheelchair", "Elevator", "Assistance", "None"])
            notes = st.text_area("Additional Notes")
            
            if st.button("🗺️ Save Navigation Request"):
                if patient_name and destination:
                    nav_data = {
                        "patient_name": patient_name,
                        "destination": destination,
                        "special_needs": special_needs,
                        "notes": notes,
                        "status": "Route Calculated"
                    }
                    data_manager.save_data("navigation", nav_data)
                    st.success("✅ Navigation request saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name and select destination")
        
        # View saved navigation requests
        st.markdown("### 📋 Navigation History")
        nav_records = data_manager.load_data("navigation")
        if nav_records:
            for record in nav_records:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}** → {record['destination']}")
                        if record['special_needs']:
                            st.write(f"Special Needs: {', '.join(record['special_needs'])}")
                        if record['notes']:
                            st.write(f"Notes: {record['notes']}")
                        st.write(f"Date: {record['timestamp'][:10]}")
                    with col2:
                        st.info(record['status'])
                    with col3:
                        if st.button("🗑️", key=f"del_nav_{record['id']}"):
                            data_manager.delete_data("navigation", record['id'])
                            st.rerun()
        else:
            st.info("No navigation requests found. Add your first request above.")
            
    elif "Emergency" in module_name:
        st.markdown("### 🚨 Emergency Alert System")
        
        # Add new emergency alert
        with st.expander("➕ Add Emergency Alert", expanded=True):
            patient_name = st.text_input("Patient Name")
            emergency_type = st.selectbox("Emergency Type", ["Medical Emergency", "Fall", "Cardiac Arrest", "Respiratory Distress", "Other"])
            location = st.text_input("Location")
            severity = st.select_slider("Severity", options=["Low", "Medium", "High", "Critical"])
            description = st.text_area("Emergency Description")
            
            if st.button("🚨 Save Emergency Alert"):
                if patient_name and emergency_type:
                    emergency_data = {
                        "patient_name": patient_name,
                        "emergency_type": emergency_type,
                        "location": location,
                        "severity": severity,
                        "description": description,
                        "status": "Alert Sent"
                    }
                    data_manager.save_data("emergency_alerts", emergency_data)
                    st.success("✅ Emergency alert saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name and emergency type")
        
        # View saved emergency alerts
        st.markdown("### 📋 Emergency Alert History")
        emergency_records = data_manager.load_data("emergency_alerts")
        if emergency_records:
            for record in emergency_records:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}** - {record['emergency_type']}")
                        st.write(f"Location: {record['location']}")
                        if record['description']:
                            st.write(f"Description: {record['description']}")
                        st.write(f"Date: {record['timestamp'][:10]}")
                    with col2:
                        if record['severity'] == "Critical":
                            st.error(record['severity'])
                        elif record['severity'] == "High":
                            st.warning(record['severity'])
                        else:
                            st.info(record['severity'])
                    with col3:
                        if st.button("🗑️", key=f"del_emergency_{record['id']}"):
                            data_manager.delete_data("emergency_alerts", record['id'])
                            st.rerun()
        else:
            st.info("No emergency alerts found. Add your first alert above.")
            
    elif "Education" in module_name:
        st.markdown("### 📚 Health Education")
        
        # Add new education record
        with st.expander("➕ Add Education Record", expanded=True):
            patient_name = st.text_input("Patient Name")
            topic = st.selectbox("Educational Topic", ["Diabetes Management", "Heart Health", "Mental Wellness", "Nutrition", "Exercise", "Medication Safety", "Other"])
            material_type = st.selectbox("Material Type", ["Video", "Document", "Brochure", "Interactive Session", "Other"])
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=180, value=30)
            notes = st.text_area("Notes")
            
            if st.button("📖 Save Education Record"):
                if patient_name and topic:
                    education_data = {
                        "patient_name": patient_name,
                        "topic": topic,
                        "material_type": material_type,
                        "duration": duration,
                        "notes": notes
                    }
                    data_manager.save_data("education", education_data)
                    st.success("✅ Education record saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name and select topic")
        
        # View saved education records
        st.markdown("### 📋 Education History")
        education_records = data_manager.load_data("education")
        if education_records:
            for record in education_records:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}** - {record['topic']}")
                        st.write(f"Material: {record['material_type']} ({record['duration']} min)")
                        if record['notes']:
                            st.write(f"Notes: {record['notes']}")
                        st.write(f"Date: {record['timestamp'][:10]}")
                    with col2:
                        st.success("Completed")
                    with col3:
                        if st.button("🗑️", key=f"del_education_{record['id']}"):
                            data_manager.delete_data("education", record['id'])
                            st.rerun()
        else:
            st.info("No education records found. Add your first record above.")
            
    elif "Billing" in module_name:
        st.markdown("### 💳 Insurance & Billing")
        
        # Add new billing record
        with st.expander("➕ Add Billing Record", expanded=True):
            patient_name = st.text_input("Patient Name")
            service = st.text_input("Service/Procedure")
            amount = st.number_input("Amount ($)", min_value=0.0, value=100.0, step=10.0)
            insurance_coverage = st.slider("Insurance Coverage (%)", 0, 100, 80)
            payment_status = st.selectbox("Payment Status", ["Pending", "Paid", "Partial", "Overdue"])
            notes = st.text_area("Notes")
            
            if st.button("💳 Save Billing Record"):
                if patient_name and service:
                    patient_responsibility = amount * (1 - insurance_coverage / 100)
                    billing_data = {
                        "patient_name": patient_name,
                        "service": service,
                        "amount": amount,
                        "insurance_coverage": insurance_coverage,
                        "patient_responsibility": patient_responsibility,
                        "payment_status": payment_status,
                        "notes": notes
                    }
                    data_manager.save_data("billing", billing_data)
                    st.success("✅ Billing record saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name and service")
        
        # View saved billing records
        st.markdown("### 📋 Billing History")
        billing_records = data_manager.load_data("billing")
        if billing_records:
            for record in billing_records:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}** - {record['service']}")
                        st.write(f"Insurance: {record['insurance_coverage']}%")
                        if record['notes']:
                            st.write(f"Notes: {record['notes']}")
                        st.write(f"Date: {record['timestamp'][:10]}")
                    with col2:
                        st.write(f"Total: ${record['amount']:.2f}")
                    with col3:
                        st.write(f"Your Cost: ${record['patient_responsibility']:.2f}")
                    with col4:
                        if record['payment_status'] == "Paid":
                            st.success(record['payment_status'])
                        elif record['payment_status'] == "Pending":
                            st.info(record['payment_status'])
                        else:
                            st.warning(record['payment_status'])
                        if st.button("🗑️", key=f"del_billing_{record['id']}"):
                            data_manager.delete_data("billing", record['id'])
                            st.rerun()
        else:
            st.info("No billing records found. Add your first record above.")
            
    elif "Doctor" in module_name:
        st.markdown("### 👨‍⚕️ Doctor Recommendations")
        
        # Add new doctor recommendation
        with st.expander("➕ Add Doctor Recommendation", expanded=True):
            patient_name = st.text_input("Patient Name")
            specialty = st.selectbox("Medical Specialty", ["Cardiology", "Neurology", "Orthopedics", "Dermatology", "Pediatrics", "Oncology", "Psychiatry", "Other"])
            doctor_name = st.text_input("Doctor Name")
            hospital = st.text_input("Hospital/Clinic")
            rating = st.slider("Rating", 1, 5, 4)
            availability = st.selectbox("Availability", ["Available", "Limited", "Not Available"])
            notes = st.text_area("Notes")
            
            if st.button("👨‍⚕️ Save Doctor Recommendation"):
                if patient_name and doctor_name:
                    doctor_data = {
                        "patient_name": patient_name,
                        "specialty": specialty,
                        "doctor_name": doctor_name,
                        "hospital": hospital,
                        "rating": rating,
                        "availability": availability,
                        "notes": notes
                    }
                    data_manager.save_data("doctor_recommendations", doctor_data)
                    st.success("✅ Doctor recommendation saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name and doctor name")
        
        # View saved doctor recommendations
        st.markdown("### 📋 Doctor Recommendations")
        doctor_records = data_manager.load_data("doctor_recommendations")
        if doctor_records:
            for record in doctor_records:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}** - {record['doctor_name']}")
                        st.write(f"Specialty: {record['specialty']} | Hospital: {record['hospital']}")
                        st.write(f"Rating: {'⭐' * record['rating']}")
                        if record['notes']:
                            st.write(f"Notes: {record['notes']}")
                        st.write(f"Date: {record['timestamp'][:10]}")
                    with col2:
                        if record['availability'] == "Available":
                            st.success(record['availability'])
                        elif record['availability'] == "Limited":
                            st.warning(record['availability'])
                        else:
                            st.error(record['availability'])
                    with col3:
                        if st.button("🗑️", key=f"del_doctor_{record['id']}"):
                            data_manager.delete_data("doctor_recommendations", record['id'])
                            st.rerun()
        else:
            st.info("No doctor recommendations found. Add your first recommendation above.")
            
    elif "Ward" in module_name:
        st.markdown("### 🏥 Ward Monitoring")
        
        # Add new ward record
        with st.expander("➕ Add Ward Record", expanded=True):
            patient_name = st.text_input("Patient Name")
            room_number = st.text_input("Room Number")
            ward_type = st.selectbox("Ward Type", ["General", "ICU", "Emergency", "Surgery", "Maternity", "Pediatric"])
            admission_date = st.date_input("Admission Date")
            expected_discharge = st.date_input("Expected Discharge")
            status = st.selectbox("Status", ["Admitted", "Under Observation", "Recovering", "Ready for Discharge", "Discharged"])
            notes = st.text_area("Notes")
            
            if st.button("🏥 Save Ward Record"):
                if patient_name and room_number:
                    ward_data = {
                        "patient_name": patient_name,
                        "room_number": room_number,
                        "ward_type": ward_type,
                        "admission_date": admission_date.isoformat(),
                        "expected_discharge": expected_discharge.isoformat(),
                        "status": status,
                        "notes": notes
                    }
                    data_manager.save_data("ward_monitoring", ward_data)
                    st.success("✅ Ward record saved successfully!")
                    st.rerun()
                else:
                    st.error("Please enter patient name and room number")
        
        # View saved ward records
        st.markdown("### 📋 Ward Records")
        ward_records = data_manager.load_data("ward_monitoring")
        if ward_records:
            for record in ward_records:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{record['patient_name']}** - Room {record['room_number']}")
                        st.write(f"Ward: {record['ward_type']}")
                        st.write(f"Admission: {record['admission_date']} | Discharge: {record['expected_discharge']}")
                        if record['notes']:
                            st.write(f"Notes: {record['notes']}")
                    with col2:
                        if record['status'] == "Discharged":
                            st.success(record['status'])
                        elif record['status'] == "Ready for Discharge":
                            st.info(record['status'])
                        else:
                            st.warning(record['status'])
                    with col3:
                        if st.button("🗑️", key=f"del_ward_{record['id']}"):
                            data_manager.delete_data("ward_monitoring", record['id'])
                            st.rerun()
        else:
            st.info("No ward records found. Add your first record above.")
        
    elif "Admin" in module_name:
        st.markdown("### ⚙️ Admin Dashboard")
        
        # System statistics
        st.markdown("### 📊 System Statistics")
        
        # Count records from all data types
        data_types = [
            "authentication", "symptoms", "appointments", "health_metrics", 
            "prescriptions", "diagnoses", "mood_tracker", "lab_reports",
            "navigation", "emergency_alerts", "education", "billing",
            "doctor_recommendations", "ward_monitoring"
        ]
        
        # Get token statistics
        token_stats = token_manager.get_token_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_patients = 0
        total_records = 0
        
        for data_type in data_types:
            records = data_manager.load_data(data_type)
            total_records += len(records)
            # Count unique patients
            patients = set()
            for record in records:
                if 'patient_name' in record:
                    patients.add(record['patient_name'])
            total_patients += len(patients)
        
        with col1:
            st.metric("Total Records", total_records)
        with col2:
            st.metric("Active Tokens", token_stats['waiting'])
        with col3:
            st.metric("Departments", len(token_stats['departments']))
        with col4:
            st.metric("System Status", "Healthy")
        
        # Token management section
        st.markdown("### 🎫 Token Management")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Waiting", token_stats['waiting'], "⏳")
        with col2:
            st.metric("Called", token_stats['called'], "📢")
        with col3:
            st.metric("Completed", token_stats['completed'], "✅")
        with col4:
            st.metric("Total Today", token_stats['total_tokens'], "📊")
        
        # Department-wise token stats
        if token_stats['departments']:
            st.markdown("### 🏥 Department Token Statistics")
            for dept, stats in token_stats['departments'].items():
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        st.write(f"**{dept}**")
                    with col2:
                        st.write(f"Waiting: {stats['waiting']}")
                    with col3:
                        st.write(f"Called: {stats['called']}")
                    with col4:
                        st.write(f"Completed: {stats['completed']}")
                    with col5:
                        total_dept = stats['waiting'] + stats['called'] + stats['completed']
                        st.write(f"Total: {total_dept}")
        
        # Data management
        st.markdown("### 🗂️ Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear All Data"):
                if st.checkbox("I understand this will delete all saved data"):
                    data_manager.clear_all_data()
                    st.success("✅ All data cleared successfully!")
                    st.rerun()
        
        with col2:
            if st.button("🎫 Clear All Tokens"):
                if st.checkbox("I understand this will delete all tokens"):
                    token_manager._load_tokens = lambda: []
                    token_manager._save_token = lambda x: None
                    st.success("✅ All tokens cleared successfully!")
                    st.rerun()
        
        # Export data
        if st.button("📤 Export All Data"):
            import json
            all_data = {}
            for data_type in data_types:
                all_data[data_type] = data_manager.load_data(data_type)
            
            # Add token data
            all_data['tokens'] = token_manager._load_tokens()
            
            json_str = json.dumps(all_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Download Data",
                data=json_str,
                file_name="hospital_data_export.json",
                mime="application/json"
            )

def main():
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    if 'current_module' not in st.session_state:
        st.session_state.current_module = None
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    if 'language' not in st.session_state:
        st.session_state.language = 'English'
    
    # Sidebar for navigation and settings
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 class="futuristic-text" style="color: #667eea;">🏥 Smart Hospital</h2>
            <p class="body-text">Advanced Healthcare Management System</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Home button
        if st.button("🏠 Home Dashboard", key="home_button", use_container_width=True):
            st.session_state.current_module = None
            st.rerun()
        
        st.markdown("---")
        
        # Theme switcher
        st.markdown("### 🎨 Theme")
        theme = st.selectbox(
            "Choose Theme",
            ["Light", "Dark", "Futuristic"],
            index=0 if st.session_state.theme == 'light' else 1
        )
        st.session_state.theme = theme.lower()
        
        # Language switcher
        st.markdown("### 🌐 Language")
        language = st.selectbox(
            "Choose Language",
            ["English", "Hindi"],
            index=0 if st.session_state.language == 'English' else 1
        )
        st.session_state.language = language
        
        st.markdown("---")
        
        # Module navigation
        st.markdown("### 🚀 Modules")
        
        modules = [
            ("🔐 Biometric Check-In", "biometric_checkin"),
            ("🎫 Token Management", "token_management"),
            ("🤖 AI Symptom Analyzer", "symptom_analyzer"),
            ("📅 Smart Scheduler", "appointment_scheduler"),
            ("📊 Health Dashboard", "health_dashboard"),
            ("💊 Digital Prescription", "prescription_system"),
            ("📈 Diagnosis Tracker", "diagnosis_history"),
            ("🧠 Wellness Companion", "mental_wellness"),
            ("🔬 Lab Visualizer", "lab_visualizer"),
            ("🗺️ Navigation System", "navigation_system"),
            ("🚨 Emergency Alert", "emergency_alert"),
            ("📚 Education Hub", "health_education"),
            ("💳 Billing Assistant", "insurance_billing"),
            ("👨‍⚕️ Doctor Recommendation", "doctor_recommendation"),
            ("🏥 Ward Monitoring", "ward_monitoring"),
            ("⚙️ Admin Dashboard", "admin_dashboard")
        ]
        
        for module_name, module_id in modules:
            if st.button(module_name, key=module_id, use_container_width=True):
                st.session_state.current_module = module_id
                st.rerun()
        
        st.markdown("---")
        
        # System status
        st.markdown("### 📊 System Status")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Patients", "127", "↗️ +12")
        with col2:
            st.metric("Available Beds", "45", "↘️ -3")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🚨 Emergency Alert", use_container_width=True):
            st.session_state.current_module = "emergency_alert"
            st.rerun()
        if st.button("📞 Call Support", use_container_width=True):
            st.info("📞 Support: +1-800-HOSPITAL")
    
    # Main content area
    if st.session_state.current_module is None:
        # Welcome screen
        show_home_dashboard()
        
    else:
        # Show module content
        module_names = {
            "biometric_checkin": "🔐 Biometric Check-In",
            "token_management": "🎫 Token Management System",
            "symptom_analyzer": "🤖 AI Symptom Analyzer",
            "appointment_scheduler": "📅 Smart Appointment Scheduler",
            "health_dashboard": "📊 Health Dashboard",
            "prescription_system": "💊 Digital Prescription System",
            "diagnosis_history": "📈 Diagnosis History Tracker",
            "mental_wellness": "🧠 Mental Wellness Companion",
            "lab_visualizer": "🔬 Lab Report Visualizer",
            "navigation_system": "🗺️ Smart Navigation System",
            "emergency_alert": "🚨 Emergency Alert System",
            "health_education": "📚 Health Education Hub",
            "insurance_billing": "💳 Insurance & Billing Assistant",
            "doctor_recommendation": "👨‍⚕️ AI Doctor Recommendation",
            "ward_monitoring": "🏥 Smart Ward Monitoring",
            "admin_dashboard": "⚙️ Admin Dashboard"
        }
        
        module_name = module_names.get(st.session_state.current_module, st.session_state.current_module)
        show_module_content(module_name)

if __name__ == "__main__":
    main()
