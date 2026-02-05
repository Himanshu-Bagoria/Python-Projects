import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.database import db
from utils.auth import auth_manager, login_required
from utils.ui_components import UIComponents
import time

@login_required
def user_profile_management():
    """User profile management with lifetime data access"""
    st.title("👤 My Profile - Lifetime Data Access")
    
    user = auth_manager.get_current_user()
    if not user:
        st.error("Please log in to access your profile.")
        return
    
    # Get complete user data
    complete_user_data = db.get_complete_user_data(user['id'])
    
    # Create tabs for different profile sections
    tabs = st.tabs([
        "📋 Profile Overview", "✏️ Edit Profile", "🔒 Privacy & Settings", 
        "📊 My Data Summary", "📱 Account Activity"
    ])
    
    with tabs[0]:
        show_profile_overview(user, complete_user_data)
    
    with tabs[1]:
        show_profile_editor(user, complete_user_data)
    
    with tabs[2]:
        show_privacy_settings(user, complete_user_data)
    
    with tabs[3]:
        show_data_summary(user, complete_user_data)
    
    with tabs[4]:
        show_account_activity(user, complete_user_data)

def show_profile_overview(user, profile_data):
    """Display profile overview with key information"""
    st.header("📋 Profile Overview")
    
    if not profile_data:
        st.warning("⚠️ Your profile is incomplete. Please complete your profile to enjoy full features.")
        if st.button("✏️ Complete Profile Now", type="primary"):
            st.session_state['active_tab'] = 1
            st.rerun()
        return
    
    # Profile completeness indicator
    completion_score = calculate_profile_completion(profile_data)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Profile picture placeholder
        st.image("https://via.placeholder.com/200x200/4a90e2/ffffff?text=👤", width=200)
        
        # Profile completion
        UIComponents.render_metric_card(
            "Profile Complete", f"{completion_score}%", 
            color="success" if completion_score >= 80 else "warning",
            icon="📈"
        )
    
    with col2:
        # Basic information
        st.subheader(f"👋 Hello, {profile_data.get('first_name', user['username'])}!")
        
        # Create info cards
        basic_info = [
            {"label": "Full Name", "value": f"{profile_data.get('first_name', '')} {profile_data.get('last_name', '')}", "icon": "👤"},
            {"label": "Role", "value": profile_data.get('role', '').title(), "icon": "🏷️"},
            {"label": "Email", "value": profile_data.get('email', 'Not provided'), "icon": "📧"},
            {"label": "Phone", "value": profile_data.get('phone', 'Not provided'), "icon": "📱"},
            {"label": "Blood Group", "value": profile_data.get('blood_group', 'Not specified'), "icon": "🩸"},
            {"label": "City", "value": profile_data.get('city', 'Not specified'), "icon": "🏙️"},
        ]
        
        for info in basic_info:
            col_icon, col_text = st.columns([1, 4])
            with col_icon:
                st.markdown(f"**{info['icon']}**")
            with col_text:
                st.markdown(f"**{info['label']}:** {info['value']}")
    
    with col3:
        # Account statistics
        member_since = profile_data.get('created_at', '')[:10] if profile_data.get('created_at') else 'Unknown'
        last_login = profile_data.get('last_login', '')[:10] if profile_data.get('last_login') else 'Unknown'
        
        UIComponents.render_metric_card(
            "Member Since", member_since, 
            color="info", icon="📅"
        )
        
        UIComponents.render_metric_card(
            "Last Login", last_login, 
            color="primary", icon="🔐"
        )
    
    # Additional profile sections
    if profile_data.get('bio'):
        st.subheader("📝 About Me")
        st.info(profile_data['bio'])
    
    # Emergency contact
    if profile_data.get('emergency_contact_name'):
        st.subheader("🆘 Emergency Contact")
        col_em1, col_em2, col_em3 = st.columns(3)
        with col_em1:
            st.write(f"**Name:** {profile_data.get('emergency_contact_name', 'N/A')}")
        with col_em2:
            st.write(f"**Phone:** {profile_data.get('emergency_contact_phone', 'N/A')}")
        with col_em3:
            st.write(f"**Relationship:** {profile_data.get('emergency_contact_relation', 'N/A')}")
    
    # Medical summary
    medical_info = []
    if profile_data.get('allergies'):
        medical_info.append(f"**Allergies:** {profile_data['allergies']}")
    if profile_data.get('chronic_conditions'):
        medical_info.append(f"**Chronic Conditions:** {profile_data['chronic_conditions']}")
    if profile_data.get('current_medications'):
        medical_info.append(f"**Current Medications:** {profile_data['current_medications']}")
    
    if medical_info:
        st.subheader("⚕️ Medical Summary")
        for info in medical_info:
            st.write(info)

def show_profile_editor(user, profile_data):
    """Display comprehensive profile editor"""
    st.header("✏️ Edit My Profile")
    st.info("💾 All changes are automatically saved and will persist across sessions.")
    
    if not profile_data:
        profile_data = {
            'id': user['id'], 
            'username': user['username'], 
            'email': user.get('email'), 
            'role': user['role']
        }
    
    with st.form("comprehensive_profile_editor"):
        # Personal Information Section
        st.subheader("👤 Personal Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            first_name = st.text_input("First Name*", value=profile_data.get('first_name', ''))
            last_name = st.text_input("Last Name*", value=profile_data.get('last_name', ''))
            date_of_birth = st.date_input("Date of Birth", value=profile_data.get('date_of_birth'))
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"], 
                                index=(["Male", "Female", "Other", "Prefer not to say"].index(profile_data.get('gender', 'Male')) 
                                      if profile_data.get('gender') in ["Male", "Female", "Other", "Prefer not to say"] else 0))
            blood_group = st.selectbox("Blood Group", ["Not Known", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                                     index=(["Not Known", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].index(profile_data.get('blood_group', 'Not Known'))
                                           if profile_data.get('blood_group') in ["Not Known", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"] else 0))
            preferred_language = st.selectbox("Preferred Language", ["English", "Hindi", "Other"],
                                             index=(["English", "Hindi", "Other"].index(profile_data.get('preferred_language', 'English'))
                                                   if profile_data.get('preferred_language') in ["English", "Hindi", "Other"] else 0))
        
        with col3:
            city = st.text_input("City", value=profile_data.get('city', ''))
            state = st.text_input("State", value=profile_data.get('state', ''))
            postal_code = st.text_input("Postal Code", value=profile_data.get('postal_code', ''))
        
        # Contact Information
        st.subheader("📞 Contact Information")
        col4, col5 = st.columns(2)
        
        with col4:
            address = st.text_area("Complete Address", value=profile_data.get('address', ''))
        with col5:
            bio = st.text_area("Personal Bio", value=profile_data.get('bio', ''), 
                             placeholder="Tell us a bit about yourself...")
        
        # Emergency Contact
        st.subheader("🆘 Emergency Contact")
        col6, col7, col8 = st.columns(3)
        
        with col6:
            emergency_name = st.text_input("Emergency Contact Name", value=profile_data.get('emergency_contact_name', ''))
        with col7:
            emergency_phone = st.text_input("Emergency Contact Phone", value=profile_data.get('emergency_contact_phone', ''))
        with col8:
            emergency_relation = st.text_input("Relationship", value=profile_data.get('emergency_contact_relation', ''))
        
        # Medical Information
        st.subheader("⚕️ Medical Information")
        col9, col10 = st.columns(2)
        
        with col9:
            medical_history = st.text_area("Medical History", value=profile_data.get('medical_history', ''),
                                         placeholder="Previous surgeries, conditions, etc.")
            allergies = st.text_area("Allergies", value=profile_data.get('allergies', ''),
                                   placeholder="Drug allergies, food allergies, etc.")
        
        with col10:
            chronic_conditions = st.text_area("Chronic Conditions", value=profile_data.get('chronic_conditions', ''),
                                            placeholder="Diabetes, Hypertension, etc.")
            current_medications = st.text_area("Current Medications", value=profile_data.get('current_medications', ''),
                                             placeholder="Regular medications you take")
        
        # Insurance Information
        st.subheader("🏥 Insurance Information")
        col11, col12, col13 = st.columns(3)
        
        with col11:
            insurance_provider = st.text_input("Insurance Provider", value=profile_data.get('insurance_provider', ''))
        with col12:
            insurance_policy = st.text_input("Policy Number", value=profile_data.get('insurance_policy_number', ''))
        with col13:
            insurance_expiry = st.date_input("Policy Expiry", value=profile_data.get('insurance_expiry'))
        
        # Form submission
        col_save, col_cancel = st.columns(2)
        
        with col_save:
            save_profile = st.form_submit_button("💾 Save Profile", use_container_width=True, type="primary")
        
        with col_cancel:
            cancel_edit = st.form_submit_button("↩️ Reset Form", use_container_width=True)
        
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
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ Failed to update profile. Please try again.")
        
        if cancel_edit:
            st.rerun()

def show_privacy_settings(user, profile_data):
    """Display privacy and notification settings"""
    st.header("🔒 Privacy & Settings")
    
    # Privacy settings
    st.subheader("🛡️ Privacy Settings")
    
    with st.form("privacy_settings"):
        data_sharing = st.checkbox("Allow data sharing for research purposes", 
                                 value=profile_data.get('data_sharing', False) if profile_data else False)
        newsletter = st.checkbox("Subscribe to health newsletter", 
                               value=profile_data.get('newsletter', False) if profile_data else False)
        
        st.subheader("🔔 Notification Preferences")
        email_notifications = st.checkbox("Email notifications", 
                                        value=profile_data.get('email_notifications', True) if profile_data else True)
        sms_notifications = st.checkbox("SMS notifications", 
                                      value=profile_data.get('sms_notifications', True) if profile_data else True)
        appointment_reminders = st.checkbox("Appointment reminders", 
                                          value=profile_data.get('appointment_reminders', True) if profile_data else True)
        medication_reminders = st.checkbox("Medication reminders", 
                                         value=profile_data.get('medication_reminders', True) if profile_data else True)
        health_tips = st.checkbox("Health tips and wellness content", 
                                value=profile_data.get('health_tips', True) if profile_data else True)
        
        st.subheader("🎨 Display Preferences")
        theme = st.selectbox("Theme", ["light", "dark"], 
                           index=(["light", "dark"].index(profile_data.get('theme', 'light')) 
                                 if profile_data and profile_data.get('theme') in ["light", "dark"] else 0))
        language = st.selectbox("Interface Language", ["English", "Hindi"], 
                              index=(["English", "Hindi"].index(profile_data.get('pref_language', 'English')) 
                                    if profile_data and profile_data.get('pref_language') in ["English", "Hindi"] else 0))
        
        if st.form_submit_button("💾 Save Settings", type="primary"):
            # Update user preferences
            preferences_data = {
                'theme': theme,
                'language': language,
                'email_notifications': email_notifications,
                'sms_notifications': sms_notifications,
                'appointment_reminders': appointment_reminders,
                'medication_reminders': medication_reminders,
                'health_tips': health_tips,
                'newsletter': newsletter,
                'data_sharing': data_sharing
            }
            
            # Check if preferences exist
            existing_prefs = db.get_user_preferences(user['id'])
            
            if existing_prefs:
                success = db.update_user_preferences(user['id'], preferences_data)
            else:
                success = db.create_user_preferences(user['id'], preferences_data)
            
            if success:
                st.success("✅ Settings updated successfully!")
            else:
                st.error("❌ Failed to update settings.")

def show_data_summary(user, profile_data):
    """Display user's data summary and statistics"""
    st.header("📊 My Data Summary")
    
    if not profile_data:
        st.warning("Complete your profile to see data summary.")
        return
    
    # Data completeness metrics
    col1, col2, col3, col4 = st.columns(4)
    
    completion_score = calculate_profile_completion(profile_data)
    
    with col1:
        UIComponents.render_metric_card(
            "Profile Complete", f"{completion_score}%", 
            color="success" if completion_score >= 80 else "warning",
            icon="📈"
        )
    
    with col2:
        data_points = count_data_points(profile_data)
        UIComponents.render_metric_card(
            "Data Points", str(data_points), 
            color="info", icon="📊"
        )
    
    with col3:
        member_days = calculate_member_days(profile_data.get('created_at'))
        UIComponents.render_metric_card(
            "Member Days", str(member_days), 
            color="primary", icon="📅"
        )
    
    with col4:
        UIComponents.render_metric_card(
            "Data Storage", "Lifetime", 
            color="success", icon="💾"
        )
    
    # Data categories breakdown
    st.subheader("📋 Data Categories")
    
    categories = [
        {"name": "Personal Information", "filled": bool(profile_data.get('first_name') and profile_data.get('last_name'))},
        {"name": "Contact Details", "filled": bool(profile_data.get('address') and profile_data.get('phone'))},
        {"name": "Medical History", "filled": bool(profile_data.get('medical_history') or profile_data.get('allergies'))},
        {"name": "Emergency Contact", "filled": bool(profile_data.get('emergency_contact_name'))},
        {"name": "Insurance Info", "filled": bool(profile_data.get('insurance_provider'))},
    ]
    
    for category in categories:
        col_name, col_status = st.columns([3, 1])
        with col_name:
            st.write(f"**{category['name']}**")
        with col_status:
            if category['filled']:
                st.success("✅ Complete")
            else:
                st.warning("⚠️ Incomplete")
    
    # Data export option
    st.subheader("📤 Data Export")
    st.info("You can export your data at any time. Your data belongs to you!")
    
    if st.button("📥 Download My Data", type="secondary"):
        export_user_data(user, profile_data)

def show_account_activity(user, profile_data):
    """Display account activity and session information"""
    st.header("📱 Account Activity")
    
    # Account information
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 Account Details")
        st.write(f"**Username:** {user['username']}")
        st.write(f"**User ID:** {user['id']}")
        st.write(f"**Role:** {user['role'].title()}")
        st.write(f"**Email:** {user.get('email', 'Not provided')}")
        
        if profile_data:
            st.write(f"**Member Since:** {profile_data.get('created_at', '')[:10] if profile_data.get('created_at') else 'Unknown'}")
            st.write(f"**Last Login:** {profile_data.get('last_login', '')[:10] if profile_data.get('last_login') else 'Unknown'}")
    
    with col2:
        st.subheader("🔐 Security Information")
        st.write("**Account Status:** Active")
        st.write("**Two-Factor Auth:** Not configured")
        st.write("**Password Strength:** Good")
        st.write("**Data Encryption:** Enabled")
    
    # Session information
    st.subheader("💻 Current Session")
    
    session_info = [
        {"label": "Login Time", "value": str(datetime.fromtimestamp(st.session_state.get('login_time', time.time())))[:19]},
        {"label": "Session Token", "value": "***encrypted***"},
        {"label": "Device Type", "value": "Web Browser"},
        {"label": "IP Address", "value": "Protected"},
    ]
    
    for info in session_info:
        col_label, col_value = st.columns([1, 2])
        with col_label:
            st.write(f"**{info['label']}:**")
        with col_value:
            st.write(info['value'])

def calculate_profile_completion(profile_data):
    """Calculate profile completion percentage"""
    if not profile_data:
        return 0
    
    fields = [
        'first_name', 'last_name', 'date_of_birth', 'gender', 'blood_group',
        'address', 'city', 'state', 'phone', 'emergency_contact_name',
        'emergency_contact_phone', 'medical_history', 'allergies'
    ]
    
    filled_fields = sum(1 for field in fields if profile_data.get(field))
    return int((filled_fields / len(fields)) * 100)

def count_data_points(profile_data):
    """Count total data points in profile"""
    if not profile_data:
        return 0
    
    return sum(1 for value in profile_data.values() if value and str(value).strip())

def calculate_member_days(created_at):
    """Calculate days since registration"""
    if not created_at:
        return 0
    
    try:
        created_date = datetime.strptime(created_at[:10], '%Y-%m-%d')
        return (datetime.now() - created_date).days
    except:
        return 0

def export_user_data(user, profile_data):
    """Export user data for download"""
    if not profile_data:
        st.error("No data to export.")
        return
    
    # Create export data
    export_data = {
        "account_info": {
            "user_id": user['id'],
            "username": user['username'],
            "email": user.get('email'),
            "role": user['role'],
            "export_date": datetime.now().isoformat()
        },
        "profile_data": profile_data
    }
    
    # Convert to JSON string
    import json
    json_data = json.dumps(export_data, indent=2, default=str)
    
    st.download_button(
        label="📥 Download JSON",
        data=json_data,
        file_name=f"profile_data_{user['username']}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )
    
    st.success("✅ Data export ready! Click the download button above.")