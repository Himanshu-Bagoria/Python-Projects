import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import json
import os
from PIL import Image
import base64
from utils.database import db
from utils.auth import auth_manager, login_required

@login_required
def doctor_management():
    """Advanced doctor management module - Admin only"""
    st.title("👨‍⚕️ Doctor Management System")
    
    # Check if user is admin
    user = auth_manager.get_current_user()
    if user['role'] != 'admin':
        st.error("🚫 Access Denied: Only administrators can manage doctors.")
        st.info("Contact your system administrator for access.")
        return
    
    # Welcome message for admin
    st.markdown(f"""
    <div class="success-box">
        <h3>Welcome, Dr. Administrator!</h3>
        <p>You have exclusive access to manage all doctor profiles in the hospital system.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "➕ Add New Doctor", "📋 Manage Doctors", "📊 Doctor Analytics", 
        "🏥 Specializations", "⚙️ Settings"
    ])
    
    with tab1:
        add_new_doctor()
    
    with tab2:
        manage_existing_doctors()
    
    with tab3:
        doctor_analytics()
    
    with tab4:
        manage_specializations()
    
    with tab5:
        doctor_settings()

def add_new_doctor():
    """Add new doctor form with comprehensive details"""
    st.header("➕ Add New Doctor")
    
    with st.form("add_doctor_form", clear_on_submit=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("👤 Personal Information")
            
            # Basic Info
            col_a, col_b = st.columns(2)
            with col_a:
                first_name = st.text_input("First Name*", placeholder="Enter first name")
                last_name = st.text_input("Last Name*", placeholder="Enter last name")
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                
            with col_b:
                date_of_birth = st.date_input("Date of Birth", max_value=date.today())
                phone = st.text_input("Phone Number*", placeholder="+1-234-567-8900")
                email = st.text_input("Email Address*", placeholder="doctor@hospital.com")
            
            # Address
            st.subheader("📍 Address Information")
            address = st.text_area("Complete Address", placeholder="Street, City, State, ZIP")
            
            col_c, col_d = st.columns(2)
            with col_c:
                emergency_contact = st.text_input("Emergency Contact", placeholder="Emergency contact number")
            with col_d:
                blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        
        with col2:
            st.subheader("📸 Doctor Photo")
            
            # Photo upload
            uploaded_photo = st.file_uploader(
                "Upload Doctor Photo", 
                type=['png', 'jpg', 'jpeg'],
                help="Upload a professional photo (Max 5MB)"
            )
            
            if uploaded_photo:
                image = Image.open(uploaded_photo)
                st.image(image, caption="Doctor Photo", width=200)
            else:
                st.info("📷 Upload a professional photo")
        
        # Professional Information
        st.subheader("🎓 Professional Details")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            medical_license = st.text_input("Medical License Number*", placeholder="MD123456789")
            specialization = st.selectbox("Primary Specialization*", [
                "General Medicine", "Cardiology", "Neurology", "Orthopedics",
                "Pediatrics", "Gynecology", "Dermatology", "ENT", "Ophthalmology",
                "Psychiatry", "Oncology", "Radiology", "Anesthesiology", "Surgery",
                "Emergency Medicine", "Internal Medicine", "Family Medicine"
            ])
            
        with col2:
            sub_specialization = st.text_input("Sub-specialization", placeholder="Optional")
            experience_years = st.number_input("Years of Experience*", min_value=0, max_value=50, value=5)
            
        with col3:
            department = st.selectbox("Department*", [
                "General Medicine", "Cardiology", "Neurology", "Orthopedics",
                "Pediatrics", "Gynecology", "Dermatology", "ENT", "Ophthalmology",
                "Emergency", "Surgery", "ICU", "OPD"
            ])
            position = st.selectbox("Position", [
                "Junior Doctor", "Senior Doctor", "Consultant", "HOD", "Chief Medical Officer"
            ])
        
        # Education & Qualifications
        st.subheader("🎓 Education & Qualifications")
        
        col1, col2 = st.columns(2)
        with col1:
            medical_degree = st.text_input("Medical Degree*", placeholder="MBBS, MD, etc.")
            university = st.text_input("University/Medical School", placeholder="Medical school name")
            graduation_year = st.number_input("Graduation Year", min_value=1980, max_value=2030, value=2015)
            
        with col2:
            additional_qualifications = st.text_area("Additional Qualifications", 
                                                   placeholder="MS, DNB, Fellowship, etc.")
            certifications = st.text_area("Certifications", 
                                        placeholder="Board certifications, etc.")
            languages = st.text_input("Languages Spoken", placeholder="English, Spanish, Hindi")
        
        # Schedule & Availability
        st.subheader("📅 Schedule & Availability")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            consultation_fee = st.number_input("Consultation Fee (₹)*", min_value=100, value=500)
            follow_up_fee = st.number_input("Follow-up Fee (₹)", min_value=100, value=300)
            
        with col2:
            working_days = st.multiselect("Working Days", [
                "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
            ], default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
            
        with col3:
            start_time = st.time_input("Start Time", value=time(9, 0))
            end_time = st.time_input("End Time", value=time(17, 0))
        
        # Additional Information
        st.subheader("ℹ️ Additional Information")
        
        col1, col2 = st.columns(2)
        with col1:
            achievements = st.text_area("Achievements & Awards", 
                                      placeholder="Notable achievements, awards, publications")
            research_interests = st.text_area("Research Interests", 
                                            placeholder="Areas of research interest")
            
        with col2:
            bio = st.text_area("Professional Bio", 
                             placeholder="Brief professional biography")
            notes = st.text_area("Internal Notes", 
                                placeholder="Internal administrative notes")
        
        # Employment Details
        st.subheader("💼 Employment Details")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            joining_date = st.date_input("Joining Date", value=date.today())
            employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Consultant", "Visiting"])
            
        with col2:
            salary = st.number_input("Monthly Salary (₹)", min_value=0, value=100000)
            contract_end = st.date_input("Contract End Date (if applicable)", value=None)
            
        with col3:
            employee_id = st.text_input("Employee ID", placeholder="Auto-generated if empty")
            status = st.selectbox("Status", ["Active", "Inactive", "On Leave"])
        
        # Submit button
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("➕ Add Doctor", use_container_width=True, type="primary")
        
        if submitted:
            # Validate required fields
            if not all([first_name, last_name, phone, email, medical_license, specialization, department, medical_degree]):
                st.error("❌ Please fill in all required fields marked with *")
            else:
                # Generate doctor ID if not provided
                if not employee_id:
                    employee_id = f"DR{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                # Save doctor data
                doctor_data = {
                    'employee_id': employee_id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'gender': gender,
                    'date_of_birth': date_of_birth,
                    'phone': phone,
                    'email': email,
                    'address': address,
                    'emergency_contact': emergency_contact,
                    'blood_group': blood_group,
                    'medical_license': medical_license,
                    'specialization': specialization,
                    'sub_specialization': sub_specialization,
                    'experience_years': experience_years,
                    'department': department,
                    'position': position,
                    'medical_degree': medical_degree,
                    'university': university,
                    'graduation_year': graduation_year,
                    'additional_qualifications': additional_qualifications,
                    'certifications': certifications,
                    'languages': languages,
                    'consultation_fee': consultation_fee,
                    'follow_up_fee': follow_up_fee,
                    'working_days': json.dumps(working_days),
                    'start_time': start_time,
                    'end_time': end_time,
                    'achievements': achievements,
                    'research_interests': research_interests,
                    'bio': bio,
                    'notes': notes,
                    'joining_date': joining_date,
                    'employment_type': employment_type,
                    'salary': salary,
                    'contract_end': contract_end,
                    'status': status
                }
                
                # Save photo if uploaded
                if uploaded_photo:
                    photo_path = save_doctor_photo(employee_id, uploaded_photo)
                    doctor_data['photo_path'] = photo_path
                
                # Save to database (simplified for demo)
                save_doctor_to_database(doctor_data)
                
                st.success(f"✅ Dr. {first_name} {last_name} has been successfully added to the system!")
                st.info(f"Doctor ID: {employee_id}")
                
                # Auto-create user account
                create_doctor_user_account(email, employee_id, f"{first_name} {last_name}")

def manage_existing_doctors():
    """Manage existing doctors with edit/delete functionality"""
    st.header("📋 Manage Existing Doctors")
    
    # Search and filter
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 Search Doctor", placeholder="Name, ID, or specialization")
    
    with col2:
        department_filter = st.selectbox("Filter by Department", 
                                       ["All"] + ["Cardiology", "Neurology", "Orthopedics", "General Medicine"])
    
    with col3:
        status_filter = st.selectbox("Filter by Status", ["All", "Active", "Inactive", "On Leave"])
    
    # Get doctors data (demo data for now)
    doctors_data = get_doctors_list()
    
    # Apply filters
    filtered_doctors = apply_filters(doctors_data, search_term, department_filter, status_filter)
    
    if not filtered_doctors.empty:
        st.subheader(f"📊 Found {len(filtered_doctors)} doctors")
        
        # Display doctors in cards
        for idx, doctor in filtered_doctors.iterrows():
            with st.expander(f"👨‍⚕️ Dr. {doctor['Name']} - {doctor['Specialization']}", expanded=False):
                
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**Doctor ID:** {doctor['ID']}")
                    st.write(f"**Department:** {doctor['Department']}")
                    st.write(f"**Experience:** {doctor['Experience']} years")
                    st.write(f"**Phone:** {doctor['Phone']}")
                    
                with col2:
                    st.write(f"**Email:** {doctor['Email']}")
                    st.write(f"**Consultation Fee:** ₹{doctor['Fee']}")
                    st.write(f"**Status:** {doctor['Status']}")
                    st.write(f"**Joining Date:** {doctor['Joining']}")
                
                with col3:
                    if st.button(f"✏️ Edit", key=f"edit_{doctor['ID']}"):
                        st.session_state[f'edit_doctor_{doctor["ID"]}'] = True
                    
                    if st.button(f"🗑️ Delete", key=f"delete_{doctor['ID']}"):
                        if st.button(f"⚠️ Confirm Delete", key=f"confirm_delete_{doctor['ID']}"):
                            delete_doctor(doctor['ID'])
                            st.success(f"Dr. {doctor['Name']} has been deleted.")
                            st.rerun()
                    
                    if st.button(f"📊 View Profile", key=f"profile_{doctor['ID']}"):
                        show_doctor_profile(doctor)
                
                # Edit form (if edit button clicked)
                if st.session_state.get(f'edit_doctor_{doctor["ID"]}', False):
                    st.markdown("---")
                    st.subheader("✏️ Edit Doctor Information")
                    edit_doctor_form(doctor)
    else:
        st.info("No doctors found matching your criteria.")

def doctor_analytics():
    """Doctor analytics and statistics"""
    st.header("📊 Doctor Analytics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Doctors", "25", delta="+3 this month")
    
    with col2:
        st.metric("Active Doctors", "23", delta="+1")
    
    with col3:
        st.metric("Avg Experience", "12.5 years", delta="+0.5")
    
    with col4:
        st.metric("Specializations", "15", delta="+2")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Department distribution
        import plotly.express as px
        dept_data = {
            'Department': ['Cardiology', 'Neurology', 'Orthopedics', 'General Medicine', 'Pediatrics'],
            'Count': [5, 4, 3, 8, 5]
        }
        fig = px.pie(values=dept_data['Count'], names=dept_data['Department'], 
                    title="Doctors by Department")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Experience distribution
        exp_data = {
            'Experience Range': ['0-5 years', '6-10 years', '11-20 years', '20+ years'],
            'Count': [6, 8, 7, 4]
        }
        fig = px.bar(x=exp_data['Experience Range'], y=exp_data['Count'], 
                    title="Experience Distribution")
        st.plotly_chart(fig, use_container_width=True)

def manage_specializations():
    """Manage medical specializations"""
    st.header("🏥 Manage Specializations")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("➕ Add New Specialization")
        
        with st.form("add_specialization"):
            spec_name = st.text_input("Specialization Name")
            spec_description = st.text_area("Description")
            requirements = st.text_area("Requirements")
            
            if st.form_submit_button("Add Specialization"):
                if spec_name:
                    st.success(f"Specialization '{spec_name}' added successfully!")
    
    with col2:
        st.subheader("📋 Existing Specializations")
        
        # Sample specializations
        specializations = [
            "Cardiology", "Neurology", "Orthopedics", "Pediatrics",
            "Gynecology", "Dermatology", "ENT", "Ophthalmology"
        ]
        
        for spec in specializations:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"• {spec}")
            with col_b:
                if st.button("✏️", key=f"edit_spec_{spec}"):
                    st.info(f"Editing {spec}")

def doctor_settings():
    """Doctor management settings"""
    st.header("⚙️ Doctor Management Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 General Settings")
        
        auto_generate_id = st.checkbox("Auto-generate Doctor IDs", value=True)
        require_photo = st.checkbox("Require doctor photo", value=True)
        email_notifications = st.checkbox("Send email notifications", value=True)
        
        default_consultation_fee = st.number_input("Default Consultation Fee (₹)", value=500)
        max_experience_years = st.number_input("Maximum Experience Years", value=50)
        
    with col2:
        st.subheader("📧 Notification Settings")
        
        notify_new_doctor = st.checkbox("Notify on new doctor addition", value=True)
        notify_doctor_updates = st.checkbox("Notify on doctor profile updates", value=True)
        notify_status_changes = st.checkbox("Notify on status changes", value=True)
        
        notification_email = st.text_input("Notification Email", 
                                         value="admin@hospital.com")
    
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")

# Helper Functions

def save_doctor_photo(doctor_id, uploaded_file):
    """Save doctor photo to file system"""
    try:
        # Create photos directory if it doesn't exist
        photos_dir = "data/doctor_photos"
        os.makedirs(photos_dir, exist_ok=True)
        
        # Save the uploaded file
        photo_path = f"{photos_dir}/{doctor_id}.jpg"
        
        image = Image.open(uploaded_file)
        # Resize image if too large
        if image.size[0] > 500 or image.size[1] > 500:
            image.thumbnail((500, 500), Image.Resampling.LANCZOS)
        
        image.save(photo_path, "JPEG", quality=85)
        return photo_path
        
    except Exception as e:
        st.error(f"Error saving photo: {str(e)}")
        return None

def save_doctor_to_database(doctor_data):
    """Save doctor data to database"""
    # In a real implementation, this would save to the actual database
    # For demo purposes, we'll save to a JSON file
    
    try:
        doctors_file = "data/doctors.json"
        
        # Load existing doctors
        if os.path.exists(doctors_file):
            with open(doctors_file, 'r') as f:
                doctors = json.load(f)
        else:
            doctors = []
        
        # Add new doctor
        doctors.append({
            **doctor_data,
            'created_at': datetime.now().isoformat(),
            'created_by': auth_manager.get_current_user()['username']
        })
        
        # Save back to file
        os.makedirs("data", exist_ok=True)
        with open(doctors_file, 'w') as f:
            json.dump(doctors, f, indent=2, default=str)
            
    except Exception as e:
        st.error(f"Error saving doctor data: {str(e)}")

def create_doctor_user_account(email, doctor_id, full_name):
    """Create user account for the doctor"""
    # Generate temporary password
    temp_password = f"Doc{doctor_id[-4:]}"
    
    # Create user account (simplified)
    user_id = db.create_user(email, temp_password, "doctor", email)
    
    if user_id:
        st.info(f"👤 User account created for Dr. {full_name}")
        st.info(f"📧 Login Email: {email}")
        st.info(f"🔑 Temporary Password: {temp_password}")
        st.warning("⚠️ Doctor should change password on first login")

def get_doctors_list():
    """Get list of doctors (demo data)"""
    return pd.DataFrame({
        'ID': ['DR001', 'DR002', 'DR003', 'DR004', 'DR005'],
        'Name': ['John Smith', 'Sarah Johnson', 'Michael Brown', 'Emily Davis', 'David Wilson'],
        'Specialization': ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'General Medicine'],
        'Department': ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'General Medicine'],
        'Experience': [15, 12, 8, 10, 20],
        'Phone': ['+1-234-567-8901', '+1-234-567-8902', '+1-234-567-8903', '+1-234-567-8904', '+1-234-567-8905'],
        'Email': ['john.smith@hospital.com', 'sarah.j@hospital.com', 'michael.b@hospital.com', 'emily.d@hospital.com', 'david.w@hospital.com'],
        'Fee': [800, 900, 700, 600, 500],
        'Status': ['Active', 'Active', 'Active', 'On Leave', 'Active'],
        'Joining': ['2020-01-15', '2019-03-20', '2021-06-10', '2018-11-05', '2015-08-12']
    })

def apply_filters(doctors_df, search_term, department_filter, status_filter):
    """Apply search and filter criteria"""
    filtered_df = doctors_df.copy()
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['Name'].str.contains(search_term, case=False) |
            filtered_df['ID'].str.contains(search_term, case=False) |
            filtered_df['Specialization'].str.contains(search_term, case=False)
        ]
    
    if department_filter != "All":
        filtered_df = filtered_df[filtered_df['Department'] == department_filter]
    
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['Status'] == status_filter]
    
    return filtered_df

def edit_doctor_form(doctor):
    """Edit doctor form"""
    with st.form(f"edit_doctor_{doctor['ID']}"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_phone = st.text_input("Phone", value=doctor['Phone'])
            new_email = st.text_input("Email", value=doctor['Email'])
            new_fee = st.number_input("Consultation Fee", value=doctor['Fee'])
        
        with col2:
            new_status = st.selectbox("Status", ["Active", "Inactive", "On Leave"], 
                                    index=["Active", "Inactive", "On Leave"].index(doctor['Status']))
            new_department = st.selectbox("Department", 
                                        ["Cardiology", "Neurology", "Orthopedics", "General Medicine"],
                                        index=["Cardiology", "Neurology", "Orthopedics", "General Medicine"].index(doctor['Department']))
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.form_submit_button("💾 Save Changes"):
                st.success(f"Dr. {doctor['Name']} updated successfully!")
                st.session_state[f'edit_doctor_{doctor["ID"]}'] = False
                st.rerun()
        
        with col_b:
            if st.form_submit_button("❌ Cancel"):
                st.session_state[f'edit_doctor_{doctor["ID"]}'] = False
                st.rerun()

def show_doctor_profile(doctor):
    """Show detailed doctor profile"""
    st.markdown("---")
    st.subheader(f"👨‍⚕️ Dr. {doctor['Name']} - Complete Profile")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://via.placeholder.com/200x200/4a90e2/ffffff?text=Doctor", 
                caption=f"Dr. {doctor['Name']}", width=200)
    
    with col2:
        st.write(f"**Doctor ID:** {doctor['ID']}")
        st.write(f"**Specialization:** {doctor['Specialization']}")
        st.write(f"**Department:** {doctor['Department']}")
        st.write(f"**Experience:** {doctor['Experience']} years")
        st.write(f"**Phone:** {doctor['Phone']}")
        st.write(f"**Email:** {doctor['Email']}")
        st.write(f"**Consultation Fee:** ₹{doctor['Fee']}")
        st.write(f"**Status:** {doctor['Status']}")
        st.write(f"**Joining Date:** {doctor['Joining']}")

def delete_doctor(doctor_id):
    """Delete doctor from system"""
    # In real implementation, this would delete from database
    # For demo, we'll just show a success message
    pass