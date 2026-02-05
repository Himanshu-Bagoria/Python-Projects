import streamlit as st
import time
from utils.database import db
import jwt
import datetime
from functools import wraps

class AuthManager:
    def __init__(self):
        self.secret_key = "hospital_management_secret_key_2025"
        self.algorithm = "HS256"
    
    def generate_token(self, user_data):
        """Generate JWT token for authenticated user"""
        payload = {
            'user_id': user_data['id'],
            'username': user_data['username'],
            'role': user_data['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def login_user(self, username, password):
        """Authenticate user and create session"""
        user = db.authenticate_user(username, password)
        if user:
            token = self.generate_token(user)
            st.session_state['authenticated'] = True
            st.session_state['user'] = user
            st.session_state['token'] = token
            st.session_state['login_time'] = time.time()
            
            # Log login action
            db.log_action(user['id'], 'login', 'users', user['id'])
            return True
        return False
    
    def logout_user(self):
        """Logout user and clear session"""
        if 'user' in st.session_state:
            # Log logout action
            db.log_action(st.session_state['user']['id'], 'logout', 'users', st.session_state['user']['id'])
        
        # Clear session
        for key in ['authenticated', 'user', 'token', 'login_time']:
            if key in st.session_state:
                del st.session_state[key]
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        if not st.session_state.get('authenticated', False):
            return False
        
        # Check token validity
        token = st.session_state.get('token')
        if not token:
            return False
        
        payload = self.verify_token(token)
        if not payload:
            self.logout_user()
            return False
        
        # Check session timeout (24 hours)
        login_time = st.session_state.get('login_time', 0)
        if time.time() - login_time > 86400:  # 24 hours
            self.logout_user()
            return False
        
        return True
    
    def get_current_user(self):
        """Get current authenticated user"""
        if self.is_authenticated():
            return st.session_state.get('user')
        return None
    
    def get_current_user_role(self):
        """Get current authenticated user's role"""
        user = self.get_current_user()
        if user:
            return user.get('role')
        return None
    
    def has_role(self, required_roles):
        """Check if current user has required role"""
        user = self.get_current_user()
        if not user:
            return False
        
        if isinstance(required_roles, str):
            required_roles = [required_roles]
        
        return user.get('role') in required_roles
    
    def require_auth(self, required_roles=None):
        """Decorator to require authentication for functions"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.is_authenticated():
                    self.show_login_form()
                    return
                
                if required_roles and not self.has_role(required_roles):
                    st.error("You don't have permission to access this page.")
                    return
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def show_login_form(self):
        """Display login form"""
        st.markdown("""
        <div class="info-box">
            <h2 style="color: var(--accent-color); text-align: center;">🏥 Hospital Management System</h2>
            <p style="text-align: center; color: var(--text-color);">Please login to continue</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("login_form"):
                st.markdown("### Login")
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    login_btn = st.form_submit_button("Login", use_container_width=True)
                with col_btn2:
                    register_btn = st.form_submit_button("Register", use_container_width=True)
                
                if login_btn:
                    if username and password:
                        if self.login_user(username, password):
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
                    else:
                        st.error("Please enter both username and password")
                
                if register_btn:
                    st.session_state['show_register'] = True
                    st.rerun()
            
            # Show registration form if requested
            if st.session_state.get('show_register', False):
                self.show_registration_form()
            
            # Demo credentials info
            with st.expander("Demo Credentials"):
                st.info("""
                **Admin Account:**
                - Username: admin
                - Password: admin123
                
                **Default Roles:**
                - admin: Full system access
                - doctor: Medical operations
                - nurse: Patient care operations
                - receptionist: Appointments and basic operations
                - patient: Personal health records
                """)
    
    def show_registration_form(self):
        """Display enhanced registration form with profile data"""
        st.markdown("---")
        st.markdown("### Register New User - Complete Profile Setup")
        
        with st.form("register_form"):
            # Basic account information
            st.subheader("📝 Account Information")
            col1, col2 = st.columns(2)
            
            with col1:
                reg_username = st.text_input("Username*", key="reg_username", help="Unique username for login")
                reg_email = st.text_input("Email*", key="reg_email", help="Valid email address")
                reg_phone = st.text_input("Phone Number", key="reg_phone", placeholder="+91 XXXXX XXXXX")
            
            with col2:
                reg_password = st.text_input("Password*", type="password", key="reg_password", help="Minimum 6 characters")
                reg_confirm_password = st.text_input("Confirm Password*", type="password", key="reg_confirm_password")
                reg_role = st.selectbox("Role*", ["patient", "doctor", "nurse", "receptionist"], key="reg_role")
            
            # Personal information
            st.subheader("👤 Personal Information")
            col3, col4, col5 = st.columns(3)
            
            with col3:
                first_name = st.text_input("First Name*", key="first_name")
                last_name = st.text_input("Last Name*", key="last_name")
                date_of_birth = st.date_input("Date of Birth", key="date_of_birth", help="Your birth date")
            
            with col4:
                gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"], key="gender")
                blood_group = st.selectbox("Blood Group", [
                    "Not Known", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"
                ], key="blood_group")
                preferred_language = st.selectbox("Preferred Language", ["English", "Hindi", "Other"], key="preferred_language")
            
            with col5:
                city = st.text_input("City", key="city")
                state = st.text_input("State", key="state")
                postal_code = st.text_input("Postal Code", key="postal_code")
            
            # Address information
            st.subheader("🏠 Address Information")
            address = st.text_area("Complete Address", key="address", placeholder="Street, Landmark, Area")
            
            # Emergency contact
            st.subheader("🆘 Emergency Contact")
            col6, col7, col8 = st.columns(3)
            
            with col6:
                emergency_contact_name = st.text_input("Emergency Contact Name", key="emergency_contact_name")
            with col7:
                emergency_contact_phone = st.text_input("Emergency Contact Phone", key="emergency_contact_phone")
            with col8:
                emergency_contact_relation = st.text_input("Relationship", key="emergency_contact_relation", placeholder="Father, Spouse, etc.")
            
            # Medical information (optional)
            st.subheader("⚕️ Medical Information (Optional)")
            col9, col10 = st.columns(2)
            
            with col9:
                medical_history = st.text_area("Medical History", key="medical_history", 
                                             placeholder="Previous surgeries, chronic conditions, etc.")
                allergies = st.text_area("Allergies", key="allergies", 
                                       placeholder="Drug allergies, food allergies, etc.")
            
            with col10:
                chronic_conditions = st.text_area("Chronic Conditions", key="chronic_conditions",
                                                placeholder="Diabetes, Hypertension, etc.")
                current_medications = st.text_area("Current Medications", key="current_medications",
                                                 placeholder="Regular medications you take")
            
            # Insurance information (optional)
            st.subheader("🏥 Insurance Information (Optional)")
            col11, col12, col13 = st.columns(3)
            
            with col11:
                insurance_provider = st.text_input("Insurance Provider", key="insurance_provider")
            with col12:
                insurance_policy_number = st.text_input("Policy Number", key="insurance_policy_number")
            with col13:
                insurance_expiry = st.date_input("Policy Expiry", key="insurance_expiry", value=None)
            
            # Terms and privacy
            st.markdown("---")
            terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy*")
            data_consent = st.checkbox("I consent to the storage and processing of my personal data for medical purposes*")
            
            # Form submission buttons
            col_reg1, col_reg2 = st.columns(2)
            with col_reg1:
                register_submit = st.form_submit_button("📝 Complete Registration", use_container_width=True, type="primary")
            with col_reg2:
                cancel_register = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if register_submit:
                # Validation
                if not all([reg_username, reg_email, reg_password, reg_confirm_password, first_name, last_name]):
                    st.error("⚠️ Please fill in all required fields marked with *")
                elif reg_password != reg_confirm_password:
                    st.error("⚠️ Passwords do not match")
                elif len(reg_password) < 6:
                    st.error("⚠️ Password must be at least 6 characters long")
                elif not terms_accepted or not data_consent:
                    st.error("⚠️ Please accept the terms and consent to data processing")
                else:
                    # Prepare profile data
                    profile_data = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'date_of_birth': date_of_birth,
                        'gender': gender,
                        'blood_group': blood_group,
                        'address': address,
                        'city': city,
                        'state': state,
                        'postal_code': postal_code,
                        'country': 'India',
                        'emergency_contact_name': emergency_contact_name,
                        'emergency_contact_phone': emergency_contact_phone,
                        'emergency_contact_relation': emergency_contact_relation,
                        'preferred_language': preferred_language,
                        'medical_history': medical_history,
                        'allergies': allergies,
                        'chronic_conditions': chronic_conditions,
                        'current_medications': current_medications,
                        'insurance_provider': insurance_provider,
                        'insurance_policy_number': insurance_policy_number,
                        'insurance_expiry': insurance_expiry
                    }
                    
                    # Create user with profile
                    user_id = db.create_user_with_profile(
                        reg_username, reg_password, reg_role, 
                        reg_email, reg_phone, profile_data
                    )
                    
                    if user_id:
                        st.success("✅ Registration successful! Your profile has been created with lifetime access.")
                        st.success("💾 All your data is securely stored and will be available whenever you log in.")
                        st.info(f"🆔 Your User ID: {user_id} - Please save this for your records")
                        
                        # Auto-login the user
                        user_data = {
                            'id': user_id,
                            'username': reg_username,
                            'role': reg_role,
                            'email': reg_email
                        }
                        
                        token = self.generate_token(user_data)
                        st.session_state['authenticated'] = True
                        st.session_state['user'] = user_data
                        st.session_state['token'] = token
                        st.session_state['login_time'] = time.time()
                        st.session_state['show_register'] = False
                        
                        st.balloons()
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("⚠️ Registration failed. Username or email may already exist.")
            
            if cancel_register:
                st.session_state['show_register'] = False
                st.rerun()
    
    def show_user_profile(self):
        """Display current user profile with edit capabilities"""
        user = self.get_current_user()
        if not user:
            return
        
        # Get complete user data including profile
        complete_user_data = db.get_complete_user_data(user['id'])
        
        with st.sidebar:
            st.markdown("---")
            if complete_user_data and complete_user_data.get('first_name'):
                st.markdown(f"**👤 {complete_user_data['first_name']} {complete_user_data.get('last_name', '')}**")
            else:
                st.markdown(f"**👤 {user['username']}**")
            st.markdown(f"**Role:** {user['role'].title()}")
            st.markdown(f"**Email:** {user.get('email', 'N/A')}")
            
            if st.button("👤 View/Edit Profile", use_container_width=True):
                st.session_state['show_profile_editor'] = True
            
            if st.button("🚪 Logout", use_container_width=True):
                self.logout_user()
                st.rerun()
    
    def show_profile_editor(self):
        """Display profile editor for current user"""
        user = self.get_current_user()
        if not user:
            return
        
        st.header("👤 My Profile - Lifetime Data Access")
        st.info("💾 Your data is permanently stored and will be available every time you log in.")
        
        # Get existing profile data
        profile_data = db.get_complete_user_data(user['id'])
        
        if not profile_data:
            st.warning("No profile found. Please complete your profile setup.")
            profile_data = {'id': user['id'], 'username': user['username'], 'email': user.get('email'), 'role': user['role']}
        
        with st.form("profile_editor"):
            # Display user info
            st.subheader("📋 Account Information")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.text_input("Username", value=profile_data.get('username', ''), disabled=True)
                st.text_input("User ID", value=str(profile_data.get('id', '')), disabled=True)
            with col2:
                st.text_input("Email", value=profile_data.get('email', ''), disabled=True)
                st.text_input("Role", value=profile_data.get('role', '').title(), disabled=True)
            with col3:
                st.text_input("Member Since", value=str(profile_data.get('created_at', ''))[:10] if profile_data.get('created_at') else '', disabled=True)
                st.text_input("Last Login", value=str(profile_data.get('last_login', ''))[:10] if profile_data.get('last_login') else '', disabled=True)
            
            # Editable profile information
            st.subheader("✏️ Personal Information")
            col4, col5, col6 = st.columns(3)
            
            with col4:
                first_name = st.text_input("First Name", value=profile_data.get('first_name', ''), key="edit_first_name")
                last_name = st.text_input("Last Name", value=profile_data.get('last_name', ''), key="edit_last_name")
                date_of_birth = st.date_input("Date of Birth", value=profile_data.get('date_of_birth'), key="edit_dob")
            
            with col5:
                gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"], 
                                    index=(["Male", "Female", "Other", "Prefer not to say"].index(profile_data.get('gender', 'Male')) 
                                          if profile_data.get('gender') in ["Male", "Female", "Other", "Prefer not to say"] else 0))
                blood_group = st.selectbox("Blood Group", ["Not Known", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                                         index=(["Not Known", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].index(profile_data.get('blood_group', 'Not Known'))
                                               if profile_data.get('blood_group') in ["Not Known", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"] else 0))
                preferred_language = st.selectbox("Preferred Language", ["English", "Hindi", "Other"],
                                                 index=(["English", "Hindi", "Other"].index(profile_data.get('preferred_language', 'English'))
                                                       if profile_data.get('preferred_language') in ["English", "Hindi", "Other"] else 0))
            
            with col6:
                city = st.text_input("City", value=profile_data.get('city', ''), key="edit_city")
                state = st.text_input("State", value=profile_data.get('state', ''), key="edit_state")
                postal_code = st.text_input("Postal Code", value=profile_data.get('postal_code', ''), key="edit_postal")
            
            # Address
            address = st.text_area("Complete Address", value=profile_data.get('address', ''), key="edit_address")
            
            # Emergency contact
            st.subheader("🆘 Emergency Contact")
            col7, col8, col9 = st.columns(3)
            
            with col7:
                emergency_name = st.text_input("Emergency Contact Name", value=profile_data.get('emergency_contact_name', ''), key="edit_emr_name")
            with col8:
                emergency_phone = st.text_input("Emergency Contact Phone", value=profile_data.get('emergency_contact_phone', ''), key="edit_emr_phone")
            with col9:
                emergency_relation = st.text_input("Relationship", value=profile_data.get('emergency_contact_relation', ''), key="edit_emr_relation")
            
            # Medical information
            st.subheader("⚕️ Medical Information")
            col10, col11 = st.columns(2)
            
            with col10:
                medical_history = st.text_area("Medical History", value=profile_data.get('medical_history', ''), key="edit_med_history")
                allergies = st.text_area("Allergies", value=profile_data.get('allergies', ''), key="edit_allergies")
            
            with col11:
                chronic_conditions = st.text_area("Chronic Conditions", value=profile_data.get('chronic_conditions', ''), key="edit_chronic")
                current_medications = st.text_area("Current Medications", value=profile_data.get('current_medications', ''), key="edit_medications")
            
            # Insurance information
            st.subheader("🏥 Insurance Information")
            col12, col13, col14 = st.columns(3)
            
            with col12:
                insurance_provider = st.text_input("Insurance Provider", value=profile_data.get('insurance_provider', ''), key="edit_insurance_provider")
            with col13:
                insurance_policy = st.text_input("Policy Number", value=profile_data.get('insurance_policy_number', ''), key="edit_policy_number")
            with col14:
                insurance_expiry = st.date_input("Policy Expiry", value=profile_data.get('insurance_expiry'), key="edit_insurance_expiry")
            
            # Bio section
            st.subheader("📝 About Me")
            bio = st.text_area("Personal Bio", value=profile_data.get('bio', ''), 
                             placeholder="Tell us a bit about yourself...", key="edit_bio")
            
            # Form buttons
            col_save, col_cancel = st.columns(2)
            
            with col_save:
                save_profile = st.form_submit_button("💾 Save Profile", use_container_width=True, type="primary")
            
            with col_cancel:
                cancel_edit = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if save_profile:
                # Prepare updated profile data
                updated_profile_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'date_of_birth': date_of_birth,
                    'gender': gender,
                    'blood_group': blood_group,
                    'address': address,
                    'city': city,
                    'state': state,
                    'postal_code': postal_code,
                    'country': 'India',
                    'emergency_contact_name': emergency_name,
                    'emergency_contact_phone': emergency_phone,
                    'emergency_contact_relation': emergency_relation,
                    'preferred_language': preferred_language,
                    'medical_history': medical_history,
                    'allergies': allergies,
                    'chronic_conditions': chronic_conditions,
                    'current_medications': current_medications,
                    'insurance_provider': insurance_provider,
                    'insurance_policy_number': insurance_policy,
                    'insurance_expiry': insurance_expiry,
                    'bio': bio
                }
                
                # Check if profile exists, create or update accordingly
                existing_profile = db.get_user_profile(user['id'])
                
                if existing_profile:
                    success = db.update_user_profile(user['id'], updated_profile_data)
                else:
                    success = db.create_user_profile(user['id'], updated_profile_data)
                
                if success:
                    st.success("✅ Profile updated successfully! Your data is permanently saved.")
                    st.success("💾 All changes have been stored and will be available in future sessions.")
                    st.session_state['show_profile_editor'] = False
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Failed to update profile. Please try again.")
            
            if cancel_edit:
                st.session_state['show_profile_editor'] = False
                st.rerun()
    
    def get_user_permissions(self, role):
        """Get permissions for a specific role"""
        permissions = {
            'admin': [
                'view_all_patients', 'edit_all_patients', 'delete_patients',
                'view_all_doctors', 'edit_all_doctors', 'delete_doctors',
                'view_all_appointments', 'edit_all_appointments', 'cancel_appointments',
                'view_billing', 'edit_billing', 'generate_reports',
                'manage_users', 'view_logs', 'system_settings',
                'create_prescriptions', 'edit_prescriptions', 'view_all_prescriptions',
                'manage_medicines', 'add_medicines', 'edit_medicines', 'delete_medicines',
                'create_medical_records', 'edit_medical_records', 'view_all_records',
                'biometric_checkin', 'view_appointments', 'create_appointments'
            ],
            'doctor': [
                'view_assigned_patients', 'edit_assigned_patients',
                'view_own_appointments', 'edit_own_appointments',
                'create_prescriptions', 'edit_prescriptions', 'view_prescriptions',
                'view_lab_results', 'order_lab_tests',
                'create_medical_records', 'edit_medical_records', 'view_medical_records',
                'view_medicines', 'search_medicines',
                'biometric_checkin', 'view_appointments', 'create_appointments'
            ],
            'nurse': [
                'view_assigned_patients', 'edit_patient_vitals',
                'view_ward_assignments', 'edit_ward_assignments',
                'view_medications', 'administer_medications',
                'view_lab_results', 'view_prescriptions', 'view_medicines',
                'biometric_checkin', 'view_appointments', 'create_appointments'
            ],
            'receptionist': [
                'view_appointments', 'create_appointments', 'edit_appointments',
                'view_patients', 'create_patients', 'edit_basic_patient_info',
                'view_billing', 'create_bills', 'view_prescriptions',
                'biometric_checkin'
            ],
            'patient': [
                'view_own_records', 'view_own_appointments', 'book_appointments',
                'view_own_prescriptions', 'view_own_lab_results',
                'update_own_profile', 'biometric_checkin'
            ]
        }
        
        return permissions.get(role, [])
    
    def has_permission(self, permission):
        """Check if current user has specific permission"""
        user = self.get_current_user()
        if not user:
            return False
        
        user_permissions = self.get_user_permissions(user['role'])
        return permission in user_permissions

# Global auth manager instance
auth_manager = AuthManager()

# Decorator functions for easy use
def require_auth(required_roles=None):
    """Decorator to require authentication"""
    return auth_manager.require_auth(required_roles)

def login_required(func):
    """Simple login required decorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not auth_manager.is_authenticated():
            auth_manager.show_login_form()
            return
        return func(*args, **kwargs)
    return wrapper