import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import uuid
import qrcode
import io
from utils.database import db
from utils.auth import auth_manager, login_required
from utils.ui_components import UIComponents

@login_required
def telemedicine_platform():
    """Advanced Telemedicine Platform"""
    st.title("🎥 Smart Telemedicine Platform")
    
    # Initialize session state
    if 'telehealth_sessions' not in st.session_state:
        st.session_state['telehealth_sessions'] = []
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Schedule", 
        "🎥 Video Call", 
        "📋 History",
        "💊 E-Prescriptions"
    ])
    
    with tab1:
        schedule_consultation()
    
    with tab2:
        video_consultation_interface()
    
    with tab3:
        consultation_history()
    
    with tab4:
        e_prescription_management()

def schedule_consultation():
    """Schedule telemedicine consultation"""
    st.header("📅 Schedule Video Consultation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Patient selection
        patients_df = db.get_patients()
        if not patients_df.empty:
            patient_options = [f"{row['patient_id']} - {row['first_name']} {row['last_name']}" 
                             for _, row in patients_df.iterrows()]
            selected_patient = st.selectbox("Select Patient", patient_options)
        
        # Doctor selection
        doctors_df = db.get_doctors()
        if not doctors_df.empty:
            doctor_options = [f"{row['doctor_id']} - Dr. {row['first_name']} {row['last_name']}" 
                            for _, row in doctors_df.iterrows()]
            selected_doctor = st.selectbox("Select Doctor", doctor_options)
        
        # Basic details
        consultation_type = st.selectbox("Type", [
            "General Consultation", "Follow-up", "Mental Health", "Prescription Renewal"
        ])
        
        consultation_date = st.date_input("Date", min_value=datetime.now().date())
        consultation_time = st.selectbox("Time", [
            "09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"
        ])
        
        reason = st.text_area("Reason", placeholder="Describe reason for consultation...")
        
        if st.button("📅 Schedule", type="primary"):
            consultation_id = schedule_session(selected_patient, selected_doctor, 
                                             consultation_date, consultation_time, 
                                             consultation_type, reason)
            if consultation_id:
                st.success("✅ Consultation scheduled!")
                generate_meeting_qr(consultation_id)
    
    with col2:
        st.subheader("📋 Upcoming")
        display_upcoming_consultations()

def schedule_session(patient, doctor, date, time, consultation_type, reason):
    """Create consultation session"""
    consultation_id = str(uuid.uuid4())
    
    session_data = {
        'id': consultation_id,
        'patient': patient.split(' - ')[1] if patient else 'Unknown',
        'doctor': doctor.split(' - ')[1] if doctor else 'Unknown',
        'date': date.isoformat(),
        'time': time,
        'type': consultation_type,
        'reason': reason,
        'status': 'scheduled',
        'meeting_link': f"https://hospital-video.com/room/{consultation_id[:12]}",
        'meeting_id': consultation_id[:12]
    }
    
    st.session_state['telehealth_sessions'].append(session_data)
    return consultation_id

def generate_meeting_qr(consultation_id):
    """Generate QR code for meeting"""
    session = next((s for s in st.session_state['telehealth_sessions'] 
                   if s['id'] == consultation_id), None)
    
    if session:
        meeting_info = {
            'type': 'telemedicine',
            'meeting_id': session['meeting_id'],
            'meeting_link': session['meeting_link']
        }
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(json.dumps(meeting_info))
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert PIL Image to bytes for Streamlit display
        img_buffer = io.BytesIO()
        qr_img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        
        st.image(img_buffer, caption="Meeting QR Code", width=200)

def display_upcoming_consultations():
    """Show upcoming consultations"""
    upcoming = [s for s in st.session_state['telehealth_sessions'] if s['status'] == 'scheduled']
    
    if upcoming:
        for session in upcoming[:3]:
            st.write(f"**{session['type']}**")
            st.caption(f"{session['doctor']} - {session['date']} {session['time']}")
            if st.button("Join", key=f"join_{session['id'][:8]}"):
                st.session_state['active_consultation'] = session['id']
                st.rerun()
            st.divider()
    else:
        st.info("No upcoming consultations")

def video_consultation_interface():
    """Video consultation interface"""
    st.header("🎥 Video Consultation")
    
    if 'active_consultation' not in st.session_state:
        st.info("No active consultation. Schedule or join one first.")
        return
    
    consultation_id = st.session_state['active_consultation']
    session = next((s for s in st.session_state['telehealth_sessions'] 
                   if s['id'] == consultation_id), None)
    
    if not session:
        st.error("Consultation not found.")
        return
    
    # Consultation header
    st.success(f"🎥 Active: {session['type']}")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**Meeting ID:** {session['meeting_id']}")
    with col2:
        if st.button("📞 End", type="primary"):
            end_consultation(consultation_id)
            st.rerun()
    
    # Video simulation
    col_video1, col_video2 = st.columns(2)
    
    with col_video1:
        st.subheader("👨‍⚕️ Doctor")
        st.info("🎥 Doctor's video feed")
        st.button("🎤 Mute", key="doc_mute")
    
    with col_video2:
        st.subheader("👤 Patient")
        st.info("🎥 Patient's video feed")
        st.button("🎤 Mute", key="pat_mute")
    
    # Chat
    st.subheader("💬 Chat")
    
    # Sample messages
    st.markdown("**Dr. Johnson:** How are you feeling today?")
    st.markdown("**You:** I've been having headaches.")
    
    chat_input = st.text_input("Type message...")
    if st.button("Send") and chat_input:
        st.success(f"Message sent: {chat_input}")
    
    # Tools
    st.subheader("🛠️ Tools")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Vitals"):
            show_vitals_popup()
    with col2:
        if st.button("💊 Prescribe"):
            show_prescription_popup()
    with col3:
        if st.button("📄 Documents"):
            st.info("Document sharing interface")
    with col4:
        if st.button("📝 Notes"):
            st.info("Consultation notes interface")

def show_vitals_popup():
    """Show vitals input"""
    with st.popover("📊 Vital Signs"):
        temperature = st.number_input("Temperature (°F)", 95.0, 110.0, 98.6)
        blood_pressure = st.text_input("Blood Pressure", "120/80")
        heart_rate = st.number_input("Heart Rate", 40, 200, 70)
        
        if st.button("Record"):
            st.success("Vitals recorded!")

def show_prescription_popup():
    """Show prescription interface"""
    with st.popover("💊 Create Prescription"):
        medication = st.selectbox("Medication", [
            "Lisinopril 10mg", "Metformin 500mg", "Ibuprofen 200mg"
        ])
        dosage = st.text_input("Instructions", "Take once daily")
        duration = st.selectbox("Duration", ["7 days", "14 days", "30 days"])
        
        if st.button("Create"):
            st.success("Prescription created!")

def end_consultation(consultation_id):
    """End consultation"""
    for session in st.session_state['telehealth_sessions']:
        if session['id'] == consultation_id:
            session['status'] = 'completed'
            session['end_time'] = datetime.now().isoformat()
    
    if 'active_consultation' in st.session_state:
        del st.session_state['active_consultation']

def consultation_history():
    """Display consultation history"""
    st.header("📋 Consultation History")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        date_filter = st.date_input("From Date", 
                                   value=datetime.now().date() - timedelta(days=30))
    with col2:
        status_filter = st.selectbox("Status", ["All", "Completed", "Scheduled"])
    
    # History
    history = st.session_state['telehealth_sessions']
    
    if history:
        for session in history:
            if status_filter == "All" or session['status'] == status_filter.lower():
                with st.expander(f"{session['type']} - {session['date']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Doctor:** {session['doctor']}")
                        st.write(f"**Date:** {session['date']} {session['time']}")
                        st.write(f"**Status:** {session['status'].title()}")
                    
                    with col2:
                        if st.button("📄 Notes", key=f"notes_{session['id'][:8]}"):
                            st.info("Consultation notes would appear here")
                        if st.button("💊 Prescriptions", key=f"rx_{session['id'][:8]}"):
                            st.info("Prescriptions would appear here")
    else:
        st.info("No consultation history found.")

def e_prescription_management():
    """E-prescription management"""
    st.header("💊 E-Prescriptions")
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        UIComponents.render_metric_card("Active", "12", "+3", "success", "💊")
    with col2:
        UIComponents.render_metric_card("Refills Due", "3", "This week", "warning", "🔄")
    with col3:
        UIComponents.render_metric_card("Total Issued", "45", "All time", "info", "📱")
    with col4:
        UIComponents.render_metric_card("Pharmacies", "8", "Connected", "success", "🏪")
    
    # Prescription tabs
    tab_active, tab_create = st.tabs(["💊 Active", "➕ Create"])
    
    with tab_active:
        display_active_prescriptions()
    
    with tab_create:
        create_prescription_interface()

def display_active_prescriptions():
    """Display active prescriptions"""
    prescriptions = [
        {"medication": "Lisinopril 10mg", "dosage": "Once daily", "remaining": "15 days"},
        {"medication": "Metformin 500mg", "dosage": "Twice daily", "remaining": "5 days"}
    ]
    
    for i, rx in enumerate(prescriptions):
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{rx['medication']}**")
            st.caption(rx['dosage'])
        
        with col2:
            st.write(f"Remaining: {rx['remaining']}")
        
        with col3:
            if st.button("🔄 Refill", key=f"refill_{i}"):
                st.success("Refill requested!")

def create_prescription_interface():
    """Create prescription interface"""
    if auth_manager.get_current_user_role() != 'doctor':
        st.warning("Only doctors can create prescriptions.")
        return
    
    with st.form("create_prescription"):
        patient_id = st.text_input("Patient ID")
        medication = st.selectbox("Medication", [
            "Lisinopril 10mg", "Metformin 500mg", "Ibuprofen 200mg"
        ])
        dosage = st.text_input("Instructions")
        duration = st.selectbox("Duration", ["7 days", "14 days", "30 days"])
        
        if st.form_submit_button("💊 Create"):
            st.success("✅ Prescription created!")