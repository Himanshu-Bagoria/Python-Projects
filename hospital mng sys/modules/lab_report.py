# Mental Wellness Module
import streamlit as st
import pandas as pd
from utils.auth import login_required

@login_required
def lab_report():
    st.title("🔬 Laboratory Reports")
    
    tabs = st.tabs(["📝 Order Tests", "📊 View Reports", "📈 Trends"])
    
    with tabs[0]:
        st.header("Order Laboratory Tests")
        test_types = ["Blood Test", "Urine Test", "X-Ray", "MRI", "CT Scan"]
        selected_tests = st.multiselect("Select Tests", test_types)
        urgency = st.selectbox("Urgency", ["Routine", "Urgent", "STAT"])
        if st.button("Order Tests"):
            st.success(f"Tests ordered: {', '.join(selected_tests)}")
    
    with tabs[1]:
        st.header("Laboratory Reports")
        reports = pd.DataFrame({
            'Test': ['Blood Test', 'Urine Test', 'X-Ray'],
            'Date': ['2025-08-25', '2025-08-24', '2025-08-23'],
            'Status': ['Ready', 'Processing', 'Ready'],
            'Result': ['Normal', 'Pending', 'Normal']
        })
        st.dataframe(reports, use_container_width=True)
    
    with tabs[2]:
        st.header("Health Trends")
        st.info("Health trends based on lab results would be shown here")

# Navigation System Module
@login_required
def navigation_system():
    st.title("🗺️ Hospital Navigation System")
    
    tabs = st.tabs(["🏥 Indoor Map", "🚗 Directions", "📍 Find Services"])
    
    with tabs[0]:
        st.header("Hospital Floor Plan")
        floor = st.selectbox("Select Floor", ["Ground Floor", "1st Floor", "2nd Floor"])
        st.info(f"Interactive map for {floor} would be displayed here")
    
    with tabs[1]:
        st.header("Directions")
        destination = st.selectbox("Where do you want to go?", [
            "Emergency Room", "Cardiology", "Pharmacy", "Lab", "Cafeteria"
        ])
        if st.button("Get Directions"):
            st.success(f"Directions to {destination} generated!")
    
    with tabs[2]:
        st.header("Find Hospital Services")
        service = st.text_input("Search for services...")
        if service:
            st.info(f"Searching for: {service}")

# Emergency Alert Module
@login_required
def emergency_alert():
    st.title("🚨 Emergency Alert System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Emergency Contacts")
        st.error("🚨 Emergency: 911")
        st.warning("🏥 Hospital Emergency: (555) 123-4567")
        st.info("🚑 Ambulance: (555) 123-4568")
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("🚨 CALL EMERGENCY", type="primary"):
            st.error("Emergency services contacted!")
        
        if st.button("📞 Call Security"):
            st.warning("Security contacted!")
        
        if st.button("🚑 Request Ambulance"):
            st.info("Ambulance requested!")
    
    st.subheader("Report Emergency")
    emergency_type = st.selectbox("Emergency Type", [
        "Medical Emergency", "Fire", "Security Threat", "Equipment Failure"
    ])
    location = st.text_input("Location")
    description = st.text_area("Description")
    
    if st.button("Submit Emergency Report"):
        st.success("Emergency report submitted!")

# Health Education Module
@login_required
def health_education():
    st.title("📚 Health Education Center")
    
    tabs = st.tabs(["📖 Articles", "🎥 Videos", "📊 Health Tips"])
    
    with tabs[0]:
        st.header("Health Articles")
        articles = [
            "Understanding Diabetes",
            "Heart Health Basics",
            "Mental Health Awareness",
            "Nutrition Guidelines"
        ]
        for article in articles:
            if st.button(article):
                st.info(f"Reading: {article}")
    
    with tabs[1]:
        st.header("Educational Videos")
        st.info("Health education videos would be embedded here")
    
    with tabs[2]:
        st.header("Daily Health Tips")
        tips = [
            "Drink 8 glasses of water daily",
            "Exercise for 30 minutes",
            "Get 7-8 hours of sleep",
            "Eat 5 servings of fruits/vegetables"
        ]
        for tip in tips:
            st.success(f"💡 {tip}")

# Insurance & Billing Module
@login_required
def insurance_billing():
    st.title("💰 Insurance & Billing")
    
    tabs = st.tabs(["💳 Billing", "🏥 Insurance", "📊 Statements"])
    
    with tabs[0]:
        st.header("Generate Bill")
        services = st.multiselect("Services", [
            "Consultation", "Lab Tests", "Medication", "Procedures"
        ])
        total = st.number_input("Total Amount", value=1000.0)
        if st.button("Generate Bill"):
            st.success("Bill generated successfully!")
    
    with tabs[1]:
        st.header("Insurance Information")
        provider = st.text_input("Insurance Provider")
        policy = st.text_input("Policy Number")
        coverage = st.number_input("Coverage %", value=80.0)
        if st.button("Verify Insurance"):
            st.success("Insurance verified!")
    
    with tabs[2]:
        st.header("Billing Statements")
        statements = pd.DataFrame({
            'Date': ['2025-08-25', '2025-08-20'],
            'Service': ['Consultation', 'Lab Test'],
            'Amount': [500, 300],
            'Status': ['Paid', 'Pending']
        })
        st.dataframe(statements, use_container_width=True)

# Doctor Recommendation Module
@login_required
def doctor_recommendation():
    st.title("👨‍⚕️ Doctor Recommendation System")
    
    st.header("Find the Right Doctor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        specialty = st.selectbox("Specialty", [
            "General Medicine", "Cardiology", "Neurology", "Orthopedics"
        ])
        location = st.text_input("Preferred Location")
        language = st.selectbox("Language", ["English", "Spanish", "Hindi"])
    
    with col2:
        availability = st.selectbox("Availability", [
            "Any time", "Morning", "Afternoon", "Evening"
        ])
        experience = st.slider("Minimum Experience (years)", 0, 30, 5)
        rating = st.slider("Minimum Rating", 1.0, 5.0, 4.0)
    
    if st.button("Find Doctors"):
        st.subheader("Recommended Doctors")
        doctors = pd.DataFrame({
            'Name': ['Dr. Smith', 'Dr. Johnson', 'Dr. Brown'],
            'Specialty': [specialty] * 3,
            'Experience': [10, 15, 8],
            'Rating': [4.8, 4.6, 4.7],
            'Available': ['Today', 'Tomorrow', 'Today']
        })
        
        for idx, doctor in doctors.iterrows():
            with st.expander(f"{doctor['Name']} - {doctor['Specialty']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Experience: {doctor['Experience']} years")
                    st.write(f"Rating: {doctor['Rating']}/5.0")
                with col2:
                    st.write(f"Available: {doctor['Available']}")
                    if st.button(f"Book with {doctor['Name']}", key=f"book_{idx}"):
                        st.success(f"Booking appointment with {doctor['Name']}")

# Ward Monitoring Module
@login_required
def ward_monitoring():
    st.title("🏥 Ward Monitoring System")
    
    tabs = st.tabs(["🛏️ Bed Status", "👥 Patient List", "📊 Ward Analytics"])
    
    with tabs[0]:
        st.header("Bed Occupancy Status")
        beds = pd.DataFrame({
            'Ward': ['ICU', 'General', 'Pediatric', 'Maternity'],
            'Total Beds': [20, 50, 15, 10],
            'Occupied': [18, 35, 8, 7],
            'Available': [2, 15, 7, 3]
        })
        
        for idx, ward in beds.iterrows():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(f"{ward['Ward']} Ward", f"{ward['Occupied']}/{ward['Total Beds']}")
            with col2:
                occupancy = (ward['Occupied'] / ward['Total Beds']) * 100
                st.metric("Occupancy", f"{occupancy:.1f}%")
            with col3:
                st.metric("Available", ward['Available'])
            with col4:
                if ward['Available'] > 0:
                    st.success("Available")
                else:
                    st.error("Full")
    
    with tabs[1]:
        st.header("Current Patients")
        patients = pd.DataFrame({
            'Patient': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'Ward': ['ICU', 'General', 'General'],
            'Bed': ['ICU-01', 'GEN-15', 'GEN-22'],
            'Admission': ['2025-08-23', '2025-08-24', '2025-08-25'],
            'Condition': ['Critical', 'Stable', 'Stable']
        })
        st.dataframe(patients, use_container_width=True)
    
    with tabs[2]:
        st.header("Ward Analytics")
        st.info("Ward performance analytics would be displayed here")

# Admin Dashboard Module
@login_required
def admin_dashboard():
    st.title("⚙️ Administrator Dashboard")
    
    # Check admin permissions
    from utils.auth import auth_manager
    if not auth_manager.has_permission('system_settings'):
        st.error("You don't have permission to access the admin dashboard.")
        return
    
    tabs = st.tabs(["👥 User Management", "🏥 System Settings", "📊 Reports", "🔧 Maintenance"])
    
    with tabs[0]:
        st.header("User Management")
        
        st.subheader("Add New User")
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username")
            email = st.text_input("Email")
        with col2:
            role = st.selectbox("Role", ["admin", "doctor", "nurse", "receptionist"])
            department = st.text_input("Department")
        
        if st.button("Add User"):
            st.success(f"User {username} added successfully!")
        
        st.subheader("Existing Users")
        users = pd.DataFrame({
            'Username': ['admin', 'dr_smith', 'nurse_jones'],
            'Role': ['Admin', 'Doctor', 'Nurse'],
            'Department': ['IT', 'Cardiology', 'ICU'],
            'Status': ['Active', 'Active', 'Active']
        })
        st.dataframe(users, use_container_width=True)
    
    with tabs[1]:
        st.header("System Settings")
        
        st.subheader("Hospital Information")
        hospital_name = st.text_input("Hospital Name", value="Advanced Medical Center")
        hospital_address = st.text_area("Address")
        hospital_phone = st.text_input("Phone Number")
        
        st.subheader("System Configuration")
        appointment_duration = st.selectbox("Default Appointment Duration", 
                                          ["15 min", "30 min", "45 min", "60 min"])
        timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "IST"])
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")
    
    with tabs[2]:
        st.header("System Reports")
        
        report_type = st.selectbox("Report Type", [
            "Patient Statistics", "Revenue Report", "Staff Performance", "System Usage"
        ])
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")
        
        if st.button("Generate Report"):
            st.success(f"{report_type} report generated for {start_date} to {end_date}")
    
    with tabs[3]:
        st.header("System Maintenance")
        
        st.subheader("Database")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Backup Database"):
                st.success("Database backup initiated")
        with col2:
            if st.button("Optimize Database"):
                st.success("Database optimization completed")
        
        st.subheader("System Health")
        st.metric("CPU Usage", "45%")
        st.metric("Memory Usage", "67%")
        st.metric("Disk Usage", "82%")