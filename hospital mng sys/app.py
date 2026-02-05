import streamlit as st
import os
import sys
from PIL import Image
import base64
from streamlit_option_menu import option_menu

# Add modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules
from modules.biometric_checkin import biometric_checkin
from modules.symptom_analyzer import symptom_analyzer
from modules.appointment_scheduler import appointment_scheduler
from modules.health_dashboard import health_dashboard
from modules.digital_prescription import digital_prescription
from modules.diagnosis_history import diagnosis_history
from modules.mental_wellness import mental_wellness
from modules.lab_report import lab_report
from modules.navigation_system import navigation_system
from modules.emergency_alert import emergency_alert
from modules.health_education import health_education
from modules.insurance_billing import insurance_billing
from modules.doctor_recommendation import doctor_recommendation
from modules.ward_monitoring import ward_monitoring
from modules.admin_dashboard import admin_dashboard
from modules.doctor_management import doctor_management
from modules.popup_catalogs import popup_catalogs
from modules.medical_records import medical_records
from modules.user_profile import user_profile_management
# New advanced modules
from modules.id_card_generator import id_card_generator
from modules.waiting_room_management import waiting_room_management
from modules.pre_entry_forms import pre_entry_forms
from modules.enhanced_ai_symptom_analyzer import enhanced_symptom_analyzer
from modules.telemedicine_platform import telemedicine_platform
from modules.advanced_analytics_dashboard import advanced_analytics_dashboard
from utils.theme_manager import set_theme, get_theme_css
from utils.auth import auth_manager

# Page configuration
st.set_page_config(
    page_title="Smart Hospital System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom theme CSS
st.markdown(get_theme_css(), unsafe_allow_html=True)

# Add decorative floating shapes
floating_shapes = '''
<div class="floating-shape"></div>
<div class="floating-shape"></div>
<div class="floating-shape"></div>
<div class="floating-shape"></div>
'''
st.markdown(floating_shapes, unsafe_allow_html=True)

# Session state initialization
if 'language' not in st.session_state:
    st.session_state['language'] = 'English'
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_theme' not in st.session_state:
    st.session_state['current_theme'] = 'light'
if 'notifications' not in st.session_state:
    st.session_state['notifications'] = []
if 'alerts' not in st.session_state:
    st.session_state['alerts'] = []
if 'notification_counter' not in st.session_state:
    st.session_state['notification_counter'] = 0

# Function to load and display logo
def display_logo():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""<div class='logo-container'>
                <h1 class='main-title'>Smart Hospital System</h1>
                <div class='pulse-effect'></div>
            </div>""", 
            unsafe_allow_html=True
        )

# Function to create a sidebar menu
def create_sidebar_menu():
    with st.sidebar:
        st.markdown("<div class='sidebar-header'>Navigation Panel</div>", unsafe_allow_html=True)
        
        # Theme toggle
        theme_col1, theme_col2 = st.columns([3, 1])
        with theme_col1:
            st.markdown("<div class='theme-label'>Theme</div>", unsafe_allow_html=True)
        with theme_col2:
            if st.button("🌓" if st.session_state['current_theme'] == 'light' else "🌞", key="theme_toggle"):
                st.session_state['current_theme'] = 'dark' if st.session_state['current_theme'] == 'light' else 'light'
                set_theme(st.session_state['current_theme'])
                st.experimental_rerun()
        
        # Language toggle
        lang_col1, lang_col2 = st.columns([3, 1])
        with lang_col1:
            st.markdown("<div class='lang-label'>Language</div>", unsafe_allow_html=True)
        with lang_col2:
            if st.button("🇮🇳" if st.session_state['language'] == 'English' else "🇬🇧", key="lang_toggle"):
                st.session_state['language'] = 'Hindi' if st.session_state['language'] == 'English' else 'English'
                st.experimental_rerun()
        
        # Main navigation menu
        selected = option_menu(
            menu_title=None,
            options=[
                "Biometric Check-In", "AI Symptom Analyzer", "Appointment Scheduler",
                "Health Dashboard", "Digital Prescription", "Medical Records",
                "Diagnosis History", "Mental Wellness", "Lab Reports", "Navigation System",
                "Emergency Alert", "Health Education", "Insurance & Billing",
                "Doctor Recommendation", "Ward Monitoring", "Doctor Management",
                "Services Catalog", "My Profile", "Admin Dashboard",
                "ID Card Generator", "Waiting Room", "Pre-Entry Forms", 
                "Telemedicine", "Analytics Dashboard"
            ],
            icons=[
                "fingerprint", "brain", "calendar-check", "heart-pulse", "prescription",
                "clipboard-data", "clipboard-data", "emoji-smile", "file-medical", "map", "exclamation-triangle",
                "book", "cash-coin", "person-badge", "hospital", "person-plus",
                "grid-3x3-gap", "person-circle", "gear",
                "credit-card", "clock", "clipboard-check", "camera-video", "graph-up"
            ],
            menu_icon="hospital",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "var(--accent-color)", "font-size": "18px"},
                "nav-link": {
                    "color": "var(--text-color)",
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "var(--hover-bg)"
                },
                "nav-link-selected": {"background-color": "var(--accent-color)", "color": "var(--selected-text)"},
            }
        )
        
        # User profile section
        auth_manager.show_user_profile()
        
        # Handle profile editor display
        if st.session_state.get('show_profile_editor', False):
            auth_manager.show_profile_editor()
        
        return selected

# Main function
def main():
    # Display logo
    display_logo()
    
    # Create sidebar menu and get selected option
    selected = create_sidebar_menu()
    
    # Display selected module
    if selected == "Biometric Check-In":
        biometric_checkin()
    elif selected == "AI Symptom Analyzer":
        enhanced_symptom_analyzer()
    elif selected == "Appointment Scheduler":
        appointment_scheduler()
    elif selected == "Health Dashboard":
        health_dashboard()
    elif selected == "Digital Prescription":
        digital_prescription()
    elif selected == "Medical Records":
        medical_records()
    elif selected == "Diagnosis History":
        diagnosis_history()
    elif selected == "Mental Wellness":
        mental_wellness()
    elif selected == "Lab Reports":
        lab_report()
    elif selected == "Navigation System":
        navigation_system()
    elif selected == "Emergency Alert":
        emergency_alert()
    elif selected == "Health Education":
        health_education()
    elif selected == "Insurance & Billing":
        insurance_billing()
    elif selected == "Doctor Recommendation":
        doctor_recommendation()
    elif selected == "Ward Monitoring":
        ward_monitoring()
    elif selected == "Doctor Management":
        doctor_management()
    elif selected == "Services Catalog":
        popup_catalogs()
    elif selected == "My Profile":
        user_profile_management()
    elif selected == "Admin Dashboard":
        admin_dashboard()
    elif selected == "ID Card Generator":
        id_card_generator()
    elif selected == "Waiting Room":
        waiting_room_management()
    elif selected == "Pre-Entry Forms":
        pre_entry_forms()
    elif selected == "Telemedicine":
        telemedicine_platform()
    elif selected == "Analytics Dashboard":
        advanced_analytics_dashboard()

if __name__ == "__main__":
    main()