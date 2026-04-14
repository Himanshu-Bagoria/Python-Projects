import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import BiometricAuth, create_login_form, check_authentication
from utils.database import db
from utils.ui_components import create_glow_button, create_metric_card, create_alert_box
from utils.voice_utils import VoiceAssistant
from config.themes import get_theme_css

def main():
    """Main function for Biometric Patient Check-In module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h1 class="futuristic-text">🔐 Biometric Patient Check-In</h1>
            <p class="body-text">Advanced authentication system for secure patient access</p>
        </div>
        """, unsafe_allow_html=True)
        
        create_login_form()
        return
    
    # Main authenticated interface
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">🔐 Biometric Patient Check-In</h1>
        <p class="body-text">Welcome back! Please choose your authentication method</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User info display
    user_info = st.session_state.get('user', 'Unknown User')
    user_role = st.session_state.get('role', 'Patient')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_metric_card("Current User", user_info, "🔐 Authenticated")
    
    with col2:
        create_metric_card("User Role", user_role, "✅ Active")
    
    with col3:
        create_metric_card("Session Status", "Active", "🟢 Online")
    
    # Authentication methods
    st.markdown("### 🔐 Authentication Methods")
    
    auth_method = st.selectbox(
        "Choose Authentication Method",
        ["Fingerprint Scan", "Face Recognition", "Traditional Login"],
        key="auth_method_select"
    )
    
    if auth_method == "Fingerprint Scan":
        fingerprint_authentication()
    elif auth_method == "Face Recognition":
        face_recognition_authentication()
    else:
        traditional_login()
    
    # Patient information display
    if check_authentication():
        display_patient_information()
    
    # Voice commands
    st.markdown("---")
    st.markdown("### 🎤 Voice Commands")
    
    voice_assistant = VoiceAssistant()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎤 Voice Login"):
            st.info("🎤 Say 'login' or 'authenticate' to proceed with voice authentication")
            # Simulate voice authentication
            st.success("✅ Voice authentication successful!")
    
    with col2:
        if st.button("🔊 Voice Help"):
            voice_assistant.speak("Welcome to the biometric check-in system. You can use fingerprint, face recognition, or voice commands to authenticate.")

def fingerprint_authentication():
    """Fingerprint authentication interface"""
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div style="background: linear-gradient(45deg, #667eea, #764ba2); 
                    padding: 2rem; border-radius: 15px; color: white;">
            <h3>🔐 Fingerprint Scanner</h3>
            <p>Place your finger on the scanner below</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate fingerprint scanner
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <div style="width: 200px; height: 200px; background: linear-gradient(45deg, #333, #666); 
                        border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center;
                        border: 3px solid #667eea; box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);">
                <div style="font-size: 3rem;">🔐</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🔐 Start Fingerprint Scan", use_container_width=True):
        auth = BiometricAuth()
        if auth.login_user(None, None, "fingerprint"):
            st.success("✅ Fingerprint authentication successful!")
            st.rerun()

def face_recognition_authentication():
    """Face recognition authentication interface"""
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div style="background: linear-gradient(45deg, #667eea, #764ba2); 
                    padding: 2rem; border-radius: 15px; color: white;">
            <h3>👤 Face Recognition</h3>
            <p>Look at the camera for authentication</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Camera input for face recognition
    camera_input = st.camera_input("Face Recognition Camera", key="face_camera")
    
    if camera_input is not None:
        st.success("✅ Face detected! Processing authentication...")
        
        # Simulate face recognition process
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            "Detecting facial features...",
            "Extracting biometric data...",
            "Comparing with database...",
            "Verifying identity...",
            "Authentication successful!"
        ]
        
        for i, step in enumerate(steps):
            status_text.text(step)
            progress_bar.progress((i + 1) / len(steps))
            import time
            time.sleep(0.5)
        
        st.success("✅ Face recognition authentication successful!")
        
        # Update session state
        st.session_state.authenticated = True
        st.session_state.user = "demo_user"
        st.session_state.role = "patient"
        st.rerun()

def traditional_login():
    """Traditional username/password login"""
    st.markdown("### 📝 Traditional Login")
    
    with st.form("traditional_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("🔐 Login", use_container_width=True)
        
        if submit_button:
            auth = BiometricAuth()
            if auth.login_user(username, password, "password"):
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

def display_patient_information():
    """Display patient information after authentication"""
    st.markdown("### 👤 Patient Information")
    
    # Get current user's patient data
    current_user = st.session_state.get('user', 'demo_user')
    
    # Simulate patient data
    patient_data = {
        "name": "Rajesh Kumar",
        "age": 45,
        "gender": "Male",
        "patient_id": "P001",
        "blood_group": "B+",
        "emergency_contact": "+91-9876543211",
        "last_visit": "2024-08-20",
        "next_appointment": "2024-08-25",
        "medical_history": ["Diabetes", "Hypertension"],
        "allergies": ["Penicillin"],
        "current_medications": ["Metformin", "Amlodipine"]
    }
    
    # Display patient info in cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="module-card">
            <h4>📋 Basic Information</h4>
            <p><strong>Name:</strong> {patient_data['name']}</p>
            <p><strong>Age:</strong> {patient_data['age']} years</p>
            <p><strong>Gender:</strong> {patient_data['gender']}</p>
            <p><strong>Patient ID:</strong> {patient_data['patient_id']}</p>
            <p><strong>Blood Group:</strong> {patient_data['blood_group']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="module-card">
            <h4>📞 Contact Information</h4>
            <p><strong>Emergency Contact:</strong> {patient_data['emergency_contact']}</p>
            <p><strong>Last Visit:</strong> {patient_data['last_visit']}</p>
            <p><strong>Next Appointment:</strong> {patient_data['next_appointment']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Medical information
    st.markdown("### 🏥 Medical Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="module-card">
            <h4>📋 Medical History</h4>
            <ul>
                {''.join([f'<li>{condition}</li>' for condition in patient_data['medical_history']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="module-card">
            <h4>💊 Current Medications</h4>
            <ul>
                {''.join([f'<li>{medication}</li>' for medication in patient_data['current_medications']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Allergies alert
    if patient_data['allergies']:
        create_alert_box(
            f"⚠️ Allergies: {', '.join(patient_data['allergies'])}", 
            "warning"
        )
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📅 Book Appointment"):
            st.info("Redirecting to appointment scheduler...")
    
    with col2:
        if st.button("📊 View Vitals"):
            st.info("Opening vital signs dashboard...")
    
    with col3:
        if st.button("💊 Check Medications"):
            st.info("Opening medication management...")
    
    with col4:
        if st.button("📋 View Reports"):
            st.info("Opening medical reports...")
    
    # Logout option
    st.markdown("---")
    if st.button("🚪 Logout"):
        auth = BiometricAuth()
        auth.logout_user()
        st.rerun()

if __name__ == "__main__":
    main()
