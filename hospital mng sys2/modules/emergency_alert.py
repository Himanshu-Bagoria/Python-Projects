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
from utils.ui_components import create_glow_button, create_metric_card, create_alert_box
from utils.voice_utils import VoiceAssistant
from config.themes import get_theme_css

class EmergencyAlertSystem:
    def __init__(self):
        self.emergency_types = [
            "Medical Emergency",
            "Cardiac Arrest",
            "Respiratory Distress",
            "Severe Bleeding",
            "Unconsciousness",
            "Severe Pain",
            "Fall",
            "Allergic Reaction",
            "Seizure",
            "Other"
        ]
        self.response_teams = self.load_response_teams()
        
    def load_response_teams(self):
        """Load emergency response teams"""
        return [
            {
                "id": "ERT001",
                "name": "Emergency Response Team 1",
                "specialization": "General Emergency",
                "status": "Available",
                "response_time": "2-3 minutes",
                "contact": "+91-9876543201"
            },
            {
                "id": "ERT002",
                "name": "Cardiac Emergency Team",
                "specialization": "Cardiac Emergencies",
                "status": "Available",
                "response_time": "1-2 minutes",
                "contact": "+91-9876543202"
            },
            {
                "id": "ERT003",
                "name": "Trauma Response Team",
                "specialization": "Trauma & Bleeding",
                "status": "Available",
                "response_time": "2-4 minutes",
                "contact": "+91-9876543203"
            }
        ]
    
    def create_emergency_alert(self, patient_id, emergency_type, location, description=""):
        """Create emergency alert"""
        alert_data = {
            "patient_id": patient_id,
            "emergency_type": emergency_type,
            "location": location,
            "description": description,
            "severity": self.assess_emergency_severity(emergency_type),
            "status": "Active",
            "created_at": datetime.now().isoformat()
        }
        
        alert_id = db.add_emergency_alert(alert_data)
        return alert_id
    
    def assess_emergency_severity(self, emergency_type):
        """Assess emergency severity level"""
        high_severity = ["Cardiac Arrest", "Respiratory Distress", "Severe Bleeding", "Unconsciousness"]
        medium_severity = ["Severe Pain", "Allergic Reaction", "Seizure"]
        
        if emergency_type in high_severity:
            return "Critical"
        elif emergency_type in medium_severity:
            return "High"
        else:
            return "Medium"
    
    def get_nearest_response_team(self, emergency_type, location):
        """Get nearest available response team"""
        # Simple logic to match team based on emergency type
        if "Cardiac" in emergency_type:
            return next((team for team in self.response_teams if "Cardiac" in team["specialization"]), self.response_teams[0])
        elif "Bleeding" in emergency_type or "Trauma" in emergency_type:
            return next((team for team in self.response_teams if "Trauma" in team["specialization"]), self.response_teams[0])
        else:
            return self.response_teams[0]
    
    def get_patient_location(self, patient_id):
        """Get patient's current location"""
        # Simulate patient location tracking
        locations = [
            "Room 101, Ward A",
            "Room 205, Ward B", 
            "Emergency Department",
            "ICU Room 3",
            "Outpatient Clinic"
        ]
        return np.random.choice(locations)
    
    def get_patient_vitals(self, patient_id):
        """Get patient's current vital signs"""
        # Simulate real-time vital signs
        return {
            "heart_rate": np.random.randint(60, 120),
            "blood_pressure": f"{np.random.randint(90, 160)}/{np.random.randint(60, 100)}",
            "oxygen_saturation": np.random.randint(85, 100),
            "temperature": round(np.random.uniform(36.0, 39.0), 1),
            "respiratory_rate": np.random.randint(12, 25)
        }

def main():
    """Main function for Emergency Alert System module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the Emergency Alert System")
        return
    
    # Initialize emergency system
    emergency_system = EmergencyAlertSystem()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">🚨 Emergency Alert System</h1>
        <p class="body-text">One-tap SOS and real-time emergency response coordination</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Voice assistant
    voice_assistant = VoiceAssistant()
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🚨 Emergency Alert Panel")
        
        # Emergency status
        active_alerts = db.get_active_emergency_alerts()
        
        if active_alerts:
            st.markdown("#### ⚠️ Active Emergency Alerts")
            for alert in active_alerts:
                create_alert_box(
                    f"🚨 {alert['emergency_type']} - {alert['location']} - {alert['status']}",
                    "error"
                )
        
        # Emergency alert creation
        st.markdown("#### 🆘 Create Emergency Alert")
        
        with st.form("emergency_alert_form"):
            # Emergency type selection
            emergency_type = st.selectbox(
                "Emergency Type",
                emergency_system.emergency_types,
                key="emergency_type_select"
            )
            
            # Location
            patient_id = st.session_state.get('user', 'demo_user')
            current_location = emergency_system.get_patient_location(patient_id)
            
            location = st.text_input(
                "Location",
                value=current_location,
                key="emergency_location"
            )
            
            # Description
            description = st.text_area(
                "Additional Description (Optional)",
                placeholder="Describe the emergency situation...",
                key="emergency_description"
            )
            
            # Severity assessment
            severity = emergency_system.assess_emergency_severity(emergency_type)
            
            # Display severity
            severity_color = {
                "Critical": "red",
                "High": "orange", 
                "Medium": "yellow"
            }.get(severity, "blue")
            
            st.markdown(f"""
            <div style="background: {severity_color}; color: white; padding: 1rem; border-radius: 10px; text-align: center;">
                <h4>Emergency Severity: {severity}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("🚨 SEND EMERGENCY ALERT", use_container_width=True)
            
            if submit_button:
                # Create emergency alert
                alert_id = emergency_system.create_emergency_alert(
                    patient_id,
                    emergency_type,
                    location,
                    description
                )
                
                if alert_id:
                    st.success("✅ Emergency alert sent successfully!")
                    
                    # Get response team
                    response_team = emergency_system.get_nearest_response_team(emergency_type, location)
                    
                    # Display response information
                    st.markdown(f"""
                    <div class="module-card">
                        <h4>🚑 Emergency Response Initiated</h4>
                        <p><strong>Response Team:</strong> {response_team['name']}</p>
                        <p><strong>Response Time:</strong> {response_team['response_time']}</p>
                        <p><strong>Contact:</strong> {response_team['contact']}</p>
                        <p><strong>Alert ID:</strong> {alert_id}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Voice alert
                    voice_assistant.speak(f"Emergency alert sent. {response_team['name']} is responding. Estimated arrival time {response_team['response_time']}.")
                else:
                    st.error("❌ Failed to send emergency alert. Please try again.")
        
        # Quick SOS buttons
        st.markdown("#### ⚡ Quick SOS Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🫀 Cardiac Emergency", use_container_width=True):
                st.error("🚨 CARDIAC EMERGENCY ALERT SENT!")
                voice_assistant.speak("Cardiac emergency alert sent. Cardiac team responding immediately.")
        
        with col2:
            if st.button("🫁 Respiratory Emergency", use_container_width=True):
                st.error("🚨 RESPIRATORY EMERGENCY ALERT SENT!")
                voice_assistant.speak("Respiratory emergency alert sent. Medical team responding immediately.")
        
        with col3:
            if st.button("🩸 Bleeding Emergency", use_container_width=True):
                st.error("🚨 BLEEDING EMERGENCY ALERT SENT!")
                voice_assistant.speak("Bleeding emergency alert sent. Trauma team responding immediately.")
    
    with col2:
        st.markdown("### 📊 Emergency Status")
        
        # Emergency statistics
        total_alerts = len(db.emergency_alerts)
        active_alerts_count = len(active_alerts)
        resolved_alerts = total_alerts - active_alerts_count
        
        create_metric_card("Total Alerts", total_alerts)
        create_metric_card("Active Alerts", active_alerts_count, "🚨")
        create_metric_card("Resolved Alerts", resolved_alerts, "✅")
        
        # Response team status
        st.markdown("### 🚑 Response Teams")
        
        for team in emergency_system.response_teams:
            status_color = "green" if team["status"] == "Available" else "red"
            st.markdown(f"""
            <div class="module-card">
                <h4>{team['name']}</h4>
                <p><strong>Status:</strong> <span style="color: {status_color};">{team['status']}</span></p>
                <p><strong>Response Time:</strong> {team['response_time']}</p>
                <p><strong>Contact:</strong> {team['contact']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Voice commands
        st.markdown("### 🎤 Voice Commands")
        
        if st.button("🎤 Voice Emergency"):
            st.info("🎤 Say 'emergency' or 'help' to activate voice emergency alert")
            # Simulate voice emergency
            st.success("✅ Voice emergency alert activated!")
        
        if st.button("🔊 Check Status"):
            voice_assistant.speak(f"Emergency system status: {active_alerts_count} active alerts, {len(emergency_system.response_teams)} response teams available.")
    
    # Patient information for emergency
    st.markdown("---")
    st.markdown("### 👤 Emergency Patient Information")
    
    # Get patient data
    patient = db.get_patient(patient_id) if patient_id != 'demo_user' else None
    
    if patient:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="module-card">
                <h4>📋 Basic Info</h4>
                <p><strong>Name:</strong> {patient['name']}</p>
                <p><strong>Age:</strong> {patient['age']} years</p>
                <p><strong>Blood Group:</strong> {patient['blood_group']}</p>
                <p><strong>Emergency Contact:</strong> {patient['emergency_contact']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="module-card">
                <h4>🏥 Medical History</h4>
                <ul>
                    {''.join([f'<li>{condition}</li>' for condition in patient['medical_history']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="module-card">
                <h4>⚠️ Allergies</h4>
                <ul>
                    {''.join([f'<li>{allergy}</li>' for allergy in patient['allergies']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Demo patient data
        st.info("📋 Demo patient data - Rajesh Kumar, 45 years, Blood Group B+, Emergency Contact: +91-9876543211")
    
    # Current vital signs
    st.markdown("### 💓 Current Vital Signs")
    
    vitals = emergency_system.get_patient_vitals(patient_id)
    
    vital_cols = st.columns(5)
    
    with vital_cols[0]:
        create_metric_card("Heart Rate", f"{vitals['heart_rate']} BPM", "💓")
    
    with vital_cols[1]:
        create_metric_card("Blood Pressure", vitals['blood_pressure'], "🩸")
    
    with vital_cols[2]:
        create_metric_card("Oxygen Saturation", f"{vitals['oxygen_saturation']}%", "🫁")
    
    with vital_cols[3]:
        create_metric_card("Temperature", f"{vitals['temperature']}°C", "🌡️")
    
    with vital_cols[4]:
        create_metric_card("Respiratory Rate", f"{vitals['respiratory_rate']} /min", "🫁")
    
    # Emergency protocols
    st.markdown("---")
    st.markdown("### 📋 Emergency Protocols")
    
    protocols = [
        {
            "name": "Cardiac Arrest Protocol",
            "steps": ["Call for help", "Start CPR", "Use AED if available", "Monitor vital signs"]
        },
        {
            "name": "Respiratory Distress Protocol", 
            "steps": ["Assess airway", "Provide oxygen", "Monitor breathing", "Prepare for intubation if needed"]
        },
        {
            "name": "Severe Bleeding Protocol",
            "steps": ["Apply direct pressure", "Elevate if possible", "Use tourniquet if severe", "Monitor for shock"]
        }
    ]
    
    for protocol in protocols:
        with st.expander(f"📋 {protocol['name']}"):
            for i, step in enumerate(protocol['steps'], 1):
                st.write(f"{i}. {step}")

def create_emergency_analytics():
    """Create emergency analytics dashboard"""
    st.markdown("### 📈 Emergency Analytics")
    
    # Get emergency data
    emergency_data = db.emergency_alerts
    
    if emergency_data:
        # Convert to DataFrame
        df = pd.DataFrame(emergency_data)
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Emergency types distribution
        emergency_types = df['emergency_type'].value_counts()
        
        fig = px.pie(
            values=emergency_types.values,
            names=emergency_types.index,
            title="Emergency Types Distribution"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Daily emergency trend
        daily_emergencies = df.groupby(df['created_at'].dt.date).size().reset_index(name='count')
        
        fig2 = px.line(
            daily_emergencies,
            x='created_at',
            y='count',
            title="Daily Emergency Alerts Trend"
        )
        fig2.update_layout(height=300)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No emergency data available for analytics.")

if __name__ == "__main__":
    main()
