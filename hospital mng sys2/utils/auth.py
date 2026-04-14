import streamlit as st
import cv2
import numpy as np
import hashlib
import json
import os
from datetime import datetime, timedelta
import base64
from PIL import Image
import io

class BiometricAuth:
    def __init__(self):
        self.users_file = "data/users.json"
        self.load_users()
    
    def load_users(self):
        """Load user data from JSON file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {
                "admin": {
                    "password": hashlib.sha256("admin123".encode()).hexdigest(),
                    "role": "admin",
                    "fingerprint": "admin_fingerprint_hash",
                    "face_data": "admin_face_hash",
                    "last_login": None
                }
            }
            self.save_users()
    
    def save_users(self):
        """Save user data to JSON file"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, username, password):
        """Verify user password"""
        if username in self.users:
            return self.users[username]["password"] == self.hash_password(password)
        return False
    
    def simulate_fingerprint_scan(self):
        """Simulate fingerprint scanning"""
        st.markdown("### 🔐 Fingerprint Authentication")
        
        # Simulate fingerprint scanning process
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            "Initializing scanner...",
            "Place finger on sensor...",
            "Scanning fingerprint...",
            "Processing biometric data...",
            "Verifying identity...",
            "Authentication complete!"
        ]
        
        for i, step in enumerate(steps):
            status_text.text(step)
            progress_bar.progress((i + 1) / len(steps))
            st.empty()
            import time
            time.sleep(0.5)
        
        # Simulate successful authentication
        return True
    
    def simulate_face_recognition(self):
        """Simulate face recognition"""
        st.markdown("### 👤 Face Recognition")
        
        # Create a simple face detection simulation
        camera_input = st.camera_input("Look at the camera for face recognition")
        
        if camera_input is not None:
            # Convert to OpenCV format
            image = Image.open(camera_input)
            image_array = np.array(image)
            
            # Simulate face detection
            st.success("✅ Face detected! Processing...")
            
            # Simulate recognition process
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
                st.empty()
                import time
                time.sleep(0.3)
            
            return True
        
        return False
    
    def login_user(self, username, password=None, auth_method="password"):
        """Login user with various authentication methods"""
        if auth_method == "password":
            if self.verify_password(username, password):
                st.session_state.user = username
                st.session_state.role = self.users[username]["role"]
                st.session_state.authenticated = True
                self.users[username]["last_login"] = datetime.now().isoformat()
                self.save_users()
                return True
            else:
                st.error("❌ Invalid username or password")
                return False
        
        elif auth_method == "fingerprint":
            if self.simulate_fingerprint_scan():
                # For demo, assume successful authentication
                st.session_state.user = "demo_user"
                st.session_state.role = "patient"
                st.session_state.authenticated = True
                return True
            return False
        
        elif auth_method == "face":
            if self.simulate_face_recognition():
                # For demo, assume successful authentication
                st.session_state.user = "demo_user"
                st.session_state.role = "patient"
                st.session_state.authenticated = True
                return True
            return False
    
    def logout_user(self):
        """Logout current user"""
        if 'user' in st.session_state:
            del st.session_state.user
        if 'role' in st.session_state:
            del st.session_state.role
        if 'authenticated' in st.session_state:
            del st.session_state.authenticated
        st.success("✅ Logged out successfully")
    
    def require_auth(self, required_role=None):
        """Decorator to require authentication"""
        if not st.session_state.get('authenticated', False):
            st.error("🔒 Please log in to access this feature")
            st.stop()
        
        if required_role and st.session_state.get('role') != required_role:
            st.error(f"🚫 Access denied. Required role: {required_role}")
            st.stop()
    
    def get_current_user(self):
        """Get current authenticated user"""
        return st.session_state.get('user')
    
    def get_current_role(self):
        """Get current user role"""
        return st.session_state.get('role')

def create_login_form():
    """Create login form with multiple authentication methods"""
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">🔐 Smart Hospital Login</h1>
        <p class="body-text">Choose your preferred authentication method</p>
    </div>
    """, unsafe_allow_html=True)
    
    auth = BiometricAuth()
    
    # Authentication method selection
    auth_method = st.selectbox(
        "Select Authentication Method",
        ["Password", "Fingerprint", "Face Recognition"],
        key="auth_method"
    )
    
    if auth_method == "Password":
        with st.form("login_form"):
            username = st.text_input("Username", key="username")
            password = st.text_input("Password", type="password", key="password")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("🔐 Login", use_container_width=True)
            
            if submit_button:
                if auth.login_user(username, password, "password"):
                    st.success("✅ Login successful!")
                    st.rerun()
    
    elif auth_method == "Fingerprint":
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <div style="background: linear-gradient(45deg, #667eea, #764ba2); 
                        padding: 2rem; border-radius: 15px; color: white;">
                <h3>🔐 Fingerprint Scanner</h3>
                <p>Place your finger on the scanner below</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔐 Start Fingerprint Scan", use_container_width=True):
            if auth.login_user(None, None, "fingerprint"):
                st.success("✅ Fingerprint authentication successful!")
                st.rerun()
    
    elif auth_method == "Face Recognition":
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <div style="background: linear-gradient(45deg, #667eea, #764ba2); 
                        padding: 2rem; border-radius: 15px; color: white;">
                <h3>👤 Face Recognition</h3>
                <p>Look at the camera for authentication</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("👤 Start Face Recognition", use_container_width=True):
            if auth.login_user(None, None, "face"):
                st.success("✅ Face recognition successful!")
                st.rerun()
    
    # Demo credentials
    st.markdown("---")
    st.markdown("### 🧪 Demo Credentials")
    st.info("""
    **For testing purposes:**
    - Username: `admin`
    - Password: `admin123`
    - Role: Administrator
    """)

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_user_info():
    """Get current user information"""
    if check_authentication():
        return {
            "username": st.session_state.get('user'),
            "role": st.session_state.get('role'),
            "authenticated": True
        }
    return None
