import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import time

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication
from utils.database import db
from utils.ui_components import create_vital_signs_chart, create_metric_card, create_alert_box
from utils.voice_utils import VoiceAssistant
from config.themes import get_theme_css

class HealthDashboard:
    def __init__(self):
        self.vital_signs = {}
        self.alerts = []
        self.update_interval = 5  # seconds
        
    def generate_real_time_vitals(self, patient_id):
        """Generate realistic real-time vital signs"""
        # Base values for different vital signs
        base_values = {
            "heart_rate": 75,
            "blood_pressure_systolic": 120,
            "blood_pressure_diastolic": 80,
            "temperature": 37.0,
            "oxygen_saturation": 98,
            "respiratory_rate": 16,
            "blood_glucose": 100,
            "weight": 70
        }
        
        # Add realistic variations
        current_vitals = {}
        for vital, base_value in base_values.items():
            if vital == "blood_pressure_systolic":
                variation = np.random.normal(0, 5)
                current_vitals[vital] = max(90, min(140, base_value + variation))
            elif vital == "blood_pressure_diastolic":
                variation = np.random.normal(0, 3)
                current_vitals[vital] = max(60, min(90, base_value + variation))
            elif vital == "heart_rate":
                variation = np.random.normal(0, 8)
                current_vitals[vital] = max(60, min(100, base_value + variation))
            elif vital == "temperature":
                variation = np.random.normal(0, 0.3)
                current_vitals[vital] = max(36.0, min(37.5, base_value + variation))
            elif vital == "oxygen_saturation":
                variation = np.random.normal(0, 1)
                current_vitals[vital] = max(95, min(100, base_value + variation))
            elif vital == "respiratory_rate":
                variation = np.random.normal(0, 2)
                current_vitals[vital] = max(12, min(20, base_value + variation))
            elif vital == "blood_glucose":
                variation = np.random.normal(0, 10)
                current_vitals[vital] = max(70, min(140, base_value + variation))
            else:
                current_vitals[vital] = base_value
        
        # Add timestamp
        current_vitals["timestamp"] = datetime.now()
        
        return current_vitals
    
    def check_vital_alerts(self, vitals):
        """Check for abnormal vital signs and generate alerts"""
        alerts = []
        
        # Heart rate alerts
        if vitals["heart_rate"] > 100:
            alerts.append({
                "type": "warning",
                "message": f"⚠️ High heart rate: {vitals['heart_rate']} BPM",
                "severity": "moderate"
            })
        elif vitals["heart_rate"] < 60:
            alerts.append({
                "type": "warning",
                "message": f"⚠️ Low heart rate: {vitals['heart_rate']} BPM",
                "severity": "moderate"
            })
        
        # Blood pressure alerts
        if vitals["blood_pressure_systolic"] > 140:
            alerts.append({
                "type": "error",
                "message": f"🚨 High blood pressure: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']}",
                "severity": "high"
            })
        elif vitals["blood_pressure_systolic"] < 90:
            alerts.append({
                "type": "error",
                "message": f"🚨 Low blood pressure: {vitals['blood_pressure_systolic']}/{vitals['blood_pressure_diastolic']}",
                "severity": "high"
            })
        
        # Temperature alerts
        if vitals["temperature"] > 37.5:
            alerts.append({
                "type": "warning",
                "message": f"🌡️ Elevated temperature: {vitals['temperature']:.1f}°C",
                "severity": "moderate"
            })
        
        # Oxygen saturation alerts
        if vitals["oxygen_saturation"] < 95:
            alerts.append({
                "type": "error",
                "message": f"🫁 Low oxygen saturation: {vitals['oxygen_saturation']}%",
                "severity": "high"
            })
        
        # Blood glucose alerts
        if vitals["blood_glucose"] > 140:
            alerts.append({
                "type": "warning",
                "message": f"🍬 High blood glucose: {vitals['blood_glucose']} mg/dL",
                "severity": "moderate"
            })
        elif vitals["blood_glucose"] < 70:
            alerts.append({
                "type": "error",
                "message": f"🍬 Low blood glucose: {vitals['blood_glucose']} mg/dL",
                "severity": "high"
            })
        
        return alerts
    
    def get_vital_trends(self, patient_id, hours=24):
        """Get vital signs trends over time"""
        # Generate historical data
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        timestamps = pd.date_range(start=start_time, end=end_time, freq='5min')
        trends = {}
        
        for vital in ["heart_rate", "temperature", "oxygen_saturation", "blood_glucose"]:
            # Generate realistic trend data
            base_value = {
                "heart_rate": 75,
                "temperature": 37.0,
                "oxygen_saturation": 98,
                "blood_glucose": 100
            }[vital]
            
            # Add some trend and noise
            trend = np.linspace(0, np.random.normal(0, 5), len(timestamps))
            noise = np.random.normal(0, 2, len(timestamps))
            values = base_value + trend + noise
            
            trends[vital] = pd.Series(values, index=timestamps)
        
        return trends

def main():
    """Main function for Real-Time Health Dashboard module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the Health Dashboard")
        return
    
    # Initialize dashboard
    dashboard = HealthDashboard()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">📊 Real-Time Health Dashboard</h1>
        <p class="body-text">Live monitoring of vital signs and health metrics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Voice assistant
    voice_assistant = VoiceAssistant()
    
    # Get patient ID
    patient_id = st.session_state.get('user', 'demo_user')
    
    # Main dashboard layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💓 Live Vital Signs")
        
        # Generate current vitals
        current_vitals = dashboard.generate_real_time_vitals(patient_id)
        
        # Display vital signs in cards
        vital_cols = st.columns(4)
        
        with vital_cols[0]:
            create_metric_card(
                "Heart Rate",
                f"{current_vitals['heart_rate']:.0f} BPM",
                "💓"
            )
        
        with vital_cols[1]:
            create_metric_card(
                "Blood Pressure",
                f"{current_vitals['blood_pressure_systolic']:.0f}/{current_vitals['blood_pressure_diastolic']:.0f}",
                "🩸"
            )
        
        with vital_cols[2]:
            create_metric_card(
                "Temperature",
                f"{current_vitals['temperature']:.1f}°C",
                "🌡️"
            )
        
        with vital_cols[3]:
            create_metric_card(
                "Oxygen Saturation",
                f"{current_vitals['oxygen_saturation']:.0f}%",
                "🫁"
            )
        
        # Additional vitals
        vital_cols2 = st.columns(4)
        
        with vital_cols2[0]:
            create_metric_card(
                "Respiratory Rate",
                f"{current_vitals['respiratory_rate']:.0f} /min",
                "🫁"
            )
        
        with vital_cols2[1]:
            create_metric_card(
                "Blood Glucose",
                f"{current_vitals['blood_glucose']:.0f} mg/dL",
                "🍬"
            )
        
        with vital_cols2[2]:
            create_metric_card(
                "Weight",
                f"{current_vitals['weight']:.1f} kg",
                "⚖️"
            )
        
        with vital_cols2[3]:
            create_metric_card(
                "Last Updated",
                current_vitals['timestamp'].strftime("%H:%M:%S"),
                "🕐"
            )
        
        # Real-time charts
        st.markdown("### 📈 Vital Signs Trends")
        
        # Create tabs for different chart views
        tab1, tab2, tab3 = st.tabs(["Live Monitoring", "24-Hour Trends", "Alerts"])
        
        with tab1:
            # Live monitoring chart
            fig = create_vital_signs_chart()
            st.plotly_chart(fig, use_container_width=True)
            
            # Auto-refresh button
            if st.button("🔄 Refresh Data"):
                st.rerun()
        
        with tab2:
            # 24-hour trends
            trends = dashboard.get_vital_trends(patient_id, hours=24)
            
            # Heart rate trend
            fig_hr = px.line(
                x=trends["heart_rate"].index,
                y=trends["heart_rate"].values,
                title="Heart Rate Trend (24 Hours)",
                labels={"x": "Time", "y": "Heart Rate (BPM)"}
            )
            fig_hr.update_layout(height=300)
            st.plotly_chart(fig_hr, use_container_width=True)
            
            # Temperature trend
            fig_temp = px.line(
                x=trends["temperature"].index,
                y=trends["temperature"].values,
                title="Temperature Trend (24 Hours)",
                labels={"x": "Time", "y": "Temperature (°C)"}
            )
            fig_temp.update_layout(height=300)
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with tab3:
            # Alerts section
            alerts = dashboard.check_vital_alerts(current_vitals)
            
            if alerts:
                st.markdown("### 🚨 Health Alerts")
                for alert in alerts:
                    create_alert_box(alert["message"], alert["type"])
            else:
                st.success("✅ All vital signs are within normal range")
    
    with col2:
        st.markdown("### 📊 Health Summary")
        
        # Health status
        health_score = calculate_health_score(current_vitals)
        create_metric_card("Health Score", f"{health_score:.0f}%", "🏥")
        
        # Risk assessment
        risk_level = assess_health_risk(current_vitals)
        create_metric_card("Risk Level", risk_level, "⚠️" if risk_level != "Low" else "✅")
        
        # Next check-up
        next_checkup = datetime.now() + timedelta(days=7)
        create_metric_card("Next Check-up", next_checkup.strftime("%b %d"), "📅")
        
        # Voice commands
        st.markdown("### 🎤 Voice Commands")
        
        if st.button("🎤 Read Vitals"):
            vitals_summary = f"Heart rate {current_vitals['heart_rate']:.0f} beats per minute. Blood pressure {current_vitals['blood_pressure_systolic']:.0f} over {current_vitals['blood_pressure_diastolic']:.0f}. Temperature {current_vitals['temperature']:.1f} degrees Celsius."
            voice_assistant.speak(vitals_summary)
        
        if st.button("🔊 Check Alerts"):
            if alerts:
                alert_message = f"You have {len(alerts)} health alerts. Please review them immediately."
            else:
                alert_message = "No health alerts at this time. All vital signs are normal."
            voice_assistant.speak(alert_message)
    
    # Patient information panel
    st.markdown("---")
    st.markdown("### 👤 Patient Information")
    
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
        st.info("📋 Demo patient data - Rajesh Kumar, 45 years, Blood Group B+")
    
    # Export options
    st.markdown("---")
    st.markdown("### 📤 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Report"):
            st.success("✅ Health report exported successfully!")
    
    with col2:
        if st.button("📈 Export Trends"):
            st.success("✅ Vital signs trends exported successfully!")
    
    with col3:
        if st.button("📋 Share with Doctor"):
            st.success("✅ Health data shared with your doctor!")

def calculate_health_score(vitals):
    """Calculate overall health score based on vital signs"""
    score = 100
    
    # Heart rate scoring
    if 60 <= vitals["heart_rate"] <= 100:
        score += 0
    else:
        score -= 20
    
    # Blood pressure scoring
    if 90 <= vitals["blood_pressure_systolic"] <= 140 and 60 <= vitals["blood_pressure_diastolic"] <= 90:
        score += 0
    else:
        score -= 25
    
    # Temperature scoring
    if 36.0 <= vitals["temperature"] <= 37.5:
        score += 0
    else:
        score -= 15
    
    # Oxygen saturation scoring
    if vitals["oxygen_saturation"] >= 95:
        score += 0
    else:
        score -= 30
    
    # Blood glucose scoring
    if 70 <= vitals["blood_glucose"] <= 140:
        score += 0
    else:
        score -= 20
    
    return max(0, min(100, score))

def assess_health_risk(vitals):
    """Assess overall health risk level"""
    risk_score = 0
    
    # High risk factors
    if vitals["oxygen_saturation"] < 95:
        risk_score += 3
    if vitals["blood_pressure_systolic"] > 140 or vitals["blood_pressure_systolic"] < 90:
        risk_score += 2
    if vitals["heart_rate"] > 100 or vitals["heart_rate"] < 60:
        risk_score += 2
    if vitals["blood_glucose"] > 140 or vitals["blood_glucose"] < 70:
        risk_score += 2
    
    # Medium risk factors
    if vitals["temperature"] > 37.5:
        risk_score += 1
    
    if risk_score >= 5:
        return "High"
    elif risk_score >= 2:
        return "Medium"
    else:
        return "Low"

if __name__ == "__main__":
    main()
