import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication
from utils.database import db
from utils.ui_components import create_glow_button, create_metric_card, create_alert_box, display_qr_code
from utils.voice_utils import VoiceAssistant, create_voice_input_widget
from config.themes import get_theme_css

class AppointmentScheduler:
    def __init__(self):
        self.doctors = self.load_doctors()
        self.specializations = self.get_specializations()
        self.time_slots = self.generate_time_slots()
        
    def load_doctors(self):
        """Load available doctors"""
        return [
            {
                "id": "D001",
                "name": "Dr. Meera Singh",
                "specialization": "Cardiology",
                "experience": 15,
                "rating": 4.8,
                "consultation_fee": 1500,
                "availability": ["Monday", "Wednesday", "Friday"],
                "time_slots": ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
            },
            {
                "id": "D002",
                "name": "Dr. Arjun Reddy",
                "specialization": "Neurology",
                "experience": 12,
                "rating": 4.6,
                "consultation_fee": 1800,
                "availability": ["Tuesday", "Thursday", "Saturday"],
                "time_slots": ["09:00", "10:30", "12:00", "14:30", "16:00"]
            },
            {
                "id": "D003",
                "name": "Dr. Kavita Gupta",
                "specialization": "Pediatrics",
                "experience": 8,
                "rating": 4.9,
                "consultation_fee": 1200,
                "availability": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "time_slots": ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"]
            }
        ]
    
    def get_specializations(self):
        """Get available specializations"""
        return list(set([doc["specialization"] for doc in self.doctors]))
    
    def generate_time_slots(self):
        """Generate available time slots"""
        slots = []
        start_time = datetime.strptime("09:00", "%H:%M")
        end_time = datetime.strptime("17:00", "%H:%M")
        
        current_time = start_time
        while current_time <= end_time:
            slots.append(current_time.strftime("%H:%M"))
            current_time += timedelta(minutes=30)
        
        return slots
    
    def get_available_doctors(self, specialization=None, date=None):
        """Get available doctors for given criteria"""
        available_doctors = []
        
        for doctor in self.doctors:
            if specialization and doctor["specialization"] != specialization:
                continue
            
            if date:
                day_name = date.strftime("%A")
                if day_name not in doctor["availability"]:
                    continue
            
            available_doctors.append(doctor)
        
        return available_doctors
    
    def get_available_slots(self, doctor_id, date):
        """Get available time slots for a doctor on a specific date"""
        doctor = next((doc for doc in self.doctors if doc["id"] == doctor_id), None)
        if not doctor:
            return []
        
        # Get existing appointments for this doctor and date
        existing_appointments = db.get_appointments_by_doctor_date(doctor_id, date.strftime("%Y-%m-%d"))
        booked_slots = [apt["time"] for apt in existing_appointments]
        
        # Filter out booked slots
        available_slots = [slot for slot in doctor["time_slots"] if slot not in booked_slots]
        
        return available_slots
    
    def predict_optimal_slots(self, doctor_id, date, urgency="normal"):
        """Predict optimal time slots based on urgency and availability"""
        available_slots = self.get_available_slots(doctor_id, date)
        
        if not available_slots:
            return []
        
        # Simple optimization: prioritize morning slots for urgent cases
        if urgency == "urgent":
            # Prefer morning slots (09:00-12:00)
            morning_slots = [slot for slot in available_slots if "09:" in slot or "10:" in slot or "11:" in slot]
            if morning_slots:
                return morning_slots[:3]  # Return top 3 morning slots
        
        # For normal cases, return all available slots
        return available_slots
    
    def book_appointment(self, patient_id, doctor_id, date, time, appointment_type="Consultation"):
        """Book an appointment"""
        appointment_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "date": date.strftime("%Y-%m-%d"),
            "time": time,
            "type": appointment_type,
            "status": "Scheduled"
        }
        
        appointment_id = db.add_appointment(appointment_data)
        return appointment_id

def main():
    """Main function for Smart Appointment Scheduler module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the Appointment Scheduler")
        return
    
    # Initialize scheduler
    scheduler = AppointmentScheduler()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">📅 Smart Appointment Scheduler</h1>
        <p class="body-text">AI-powered appointment booking with optimal time slot prediction</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Voice assistant
    voice_assistant = VoiceAssistant()
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Book Appointment")
        
        # Appointment booking form
        with st.form("appointment_form"):
            # Specialization selection
            specialization = st.selectbox(
                "Select Specialization",
                ["All"] + scheduler.specializations,
                key="specialization_select"
            )
            
            # Date selection
            min_date = datetime.now().date()
            max_date = min_date + timedelta(days=30)
            
            selected_date = st.date_input(
                "Select Date",
                min_value=min_date,
                max_value=max_date,
                value=min_date + timedelta(days=1)
            )
            
            # Urgency level
            urgency = st.selectbox(
                "Urgency Level",
                ["normal", "urgent", "emergency"],
                key="urgency_select"
            )
            
            # Get available doctors
            available_doctors = scheduler.get_available_doctors(
                specialization if specialization != "All" else None,
                selected_date
            )
            
            if available_doctors:
                # Doctor selection
                doctor_options = [f"{doc['name']} - {doc['specialization']} (₹{doc['consultation_fee']})" for doc in available_doctors]
                selected_doctor_option = st.selectbox("Select Doctor", doctor_options)
                
                # Get selected doctor
                selected_doctor = available_doctors[doctor_options.index(selected_doctor_option)]
                
                # Get optimal time slots
                optimal_slots = scheduler.predict_optimal_slots(
                    selected_doctor["id"], 
                    selected_date, 
                    urgency
                )
                
                if optimal_slots:
                    # Time slot selection
                    selected_time = st.selectbox("Select Time Slot", optimal_slots)
                    
                    # Appointment type
                    appointment_type = st.selectbox(
                        "Appointment Type",
                        ["Consultation", "Follow-up", "Emergency", "Check-up"]
                    )
                    
                    # Additional notes
                    notes = st.text_area("Additional Notes (Optional)")
                    
                    # Submit button
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        submit_button = st.form_submit_button("📅 Book Appointment", use_container_width=True)
                    
                    if submit_button:
                        # Book appointment
                        patient_id = st.session_state.get('user', 'demo_user')
                        appointment_id = scheduler.book_appointment(
                            patient_id,
                            selected_doctor["id"],
                            selected_date,
                            selected_time,
                            appointment_type
                        )
                        
                        if appointment_id:
                            st.success("✅ Appointment booked successfully!")
                            
                            # Generate QR code for appointment
                            qr_data = f"Appointment: {appointment_id}\nDoctor: {selected_doctor['name']}\nDate: {selected_date}\nTime: {selected_time}"
                            display_qr_code(qr_data, "Appointment QR Code")
                            
                            # Voice confirmation
                            voice_assistant.speak(f"Appointment confirmed with {selected_doctor['name']} on {selected_date} at {selected_time}")
                        else:
                            st.error("❌ Failed to book appointment. Please try again.")
                else:
                    st.warning("⚠️ No available time slots for the selected doctor on this date.")
            else:
                st.warning("⚠️ No doctors available for the selected criteria.")
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        
        # Get statistics
        total_appointments = len(db.appointments)
        today_appointments = len([apt for apt in db.appointments if apt["date"] == datetime.now().strftime("%Y-%m-%d")])
        available_doctors_count = len([doc for doc in scheduler.doctors if doc["availability"]])
        
        create_metric_card("Total Appointments", total_appointments)
        create_metric_card("Today's Appointments", today_appointments)
        create_metric_card("Available Doctors", available_doctors_count)
        
        # Voice commands
        st.markdown("### 🎤 Voice Commands")
        
        if st.button("🎤 Voice Booking"):
            st.info("🎤 Say 'book appointment' to start voice booking process")
            # Simulate voice booking
            st.success("✅ Voice booking initiated!")
        
        if st.button("🔊 Check Availability"):
            voice_assistant.speak("Checking doctor availability for your preferred date and time.")

def create_calendar_view():
    """Create interactive calendar view"""
    st.markdown("### 📅 Calendar View")
    
    # Get current month
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    
    # Create calendar
    cal = calendar.monthcalendar(year, month)
    
    # Display calendar
    st.markdown(f"**{calendar.month_name[month]} {year}**")
    
    # Create calendar grid
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    # Header
    cols = st.columns(7)
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"**{day}**")
    
    # Calendar days
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day != 0:
                    # Check if day has appointments
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    appointments = [apt for apt in db.appointments if apt["date"] == date_str]
                    
                    if appointments:
                        st.markdown(f"<div style='background: #667eea; color: white; padding: 5px; border-radius: 5px; text-align: center;'>{day}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='padding: 5px; text-align: center;'>{day}</div>", unsafe_allow_html=True)

def create_appointment_analytics():
    """Create appointment analytics dashboard"""
    st.markdown("### 📈 Appointment Analytics")
    
    # Get appointment data
    appointments_df = pd.DataFrame(db.appointments)
    
    if not appointments_df.empty:
        # Convert date column
        appointments_df['date'] = pd.to_datetime(appointments_df['date'])
        
        # Daily appointments trend
        daily_appointments = appointments_df.groupby('date').size().reset_index(name='count')
        
        fig = px.line(daily_appointments, x='date', y='count', title='Daily Appointment Trend')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Doctor-wise appointments
        doctor_appointments = appointments_df.groupby('doctor_id').size().reset_index(name='count')
        
        fig2 = px.bar(doctor_appointments, x='doctor_id', y='count', title='Appointments by Doctor')
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No appointment data available for analytics.")

def create_voice_booking_interface():
    """Create voice-controlled booking interface"""
    st.markdown("### 🎤 Voice-Controlled Booking")
    
    voice_assistant = VoiceAssistant()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Voice Commands")
        
        commands = [
            "Book appointment with cardiologist",
            "Schedule follow-up next week",
            "Check doctor availability",
            "Cancel my appointment",
            "Reschedule for tomorrow"
        ]
        
        for command in commands:
            st.write(f"• {command}")
    
    with col2:
        st.markdown("#### Voice Input")
        
        if st.button("🎤 Start Voice Recognition"):
            st.info("🎤 Listening for voice commands...")
            
            # Simulate voice processing
            import time
            time.sleep(2)
            
            st.success("✅ Voice command recognized: 'Book appointment with cardiologist'")
            
            # Auto-fill form based on voice command
            st.session_state.specialization_select = "Cardiology"
            st.session_state.urgency_select = "normal"
            st.rerun()

if __name__ == "__main__":
    main()
