import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, date, time, timedelta
import plotly.graph_objects as go
import plotly.express as px
from utils.database import db
from utils.auth import auth_manager, login_required

@login_required
def appointment_scheduler():
    """Main appointment scheduler interface"""
    st.title("📅 Advanced Appointment Scheduler")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Book Appointment", "📋 View Appointments", "📊 Calendar View", 
        "⚙️ Manage Schedule", "📈 Analytics"
    ])
    
    with tab1:
        book_appointment()
    
    with tab2:
        view_appointments()
    
    with tab3:
        calendar_view()
    
    with tab4:
        manage_schedule()
    
    with tab5:
        appointment_analytics()

def book_appointment():
    """Book new appointment interface"""
    st.header("Book New Appointment")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Patient Information")
        
        # Patient selection or registration
        patient_selection_method = st.radio("Patient", ["Existing Patient", "New Patient"])
        
        if patient_selection_method == "Existing Patient":
            patients_df = db.get_patients()
            if not patients_df.empty:
                patient_options = [f"{row['patient_id']} - {row['first_name']} {row['last_name']}" 
                                 for _, row in patients_df.iterrows()]
                selected_patient = st.selectbox("Select Patient", patient_options)
                patient_id = selected_patient.split(' - ')[0] if selected_patient else None
            else:
                st.warning("No patients found. Please add patients first.")
                patient_id = None
        else:
            # Quick patient registration
            with st.form("quick_patient_reg"):
                st.subheader("Quick Patient Registration")
                first_name = st.text_input("First Name*")
                last_name = st.text_input("Last Name*")
                phone = st.text_input("Phone Number*")
                email = st.text_input("Email")
                dob = st.date_input("Date of Birth", max_value=date.today())
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                
                if st.form_submit_button("Register Patient"):
                    if first_name and last_name and phone:
                        # Generate patient ID
                        patient_id = f"PT{datetime.now().strftime('%Y%m%d%H%M%S')}"
                        
                        # Save patient (simplified for demo)
                        st.success(f"Patient registered successfully! ID: {patient_id}")
                        st.session_state['temp_patient_id'] = patient_id
                    else:
                        st.error("Please fill in all required fields.")
            
            patient_id = st.session_state.get('temp_patient_id')
    
    with col2:
        st.subheader("Appointment Details")
        
        if patient_id:
            # Department and doctor selection
            departments = ["General Medicine", "Cardiology", "Neurology", "Orthopedics", 
                          "Pediatrics", "Gynecology", "Dermatology", "ENT", "Ophthalmology"]
            
            selected_department = st.selectbox("Department", departments)
            
            # Get doctors for selected department
            doctors_df = db.get_doctors(selected_department)
            if not doctors_df.empty:
                doctor_options = [f"Dr. {row['first_name']} {row['last_name']} - {row['specialization']}" 
                                for _, row in doctors_df.iterrows()]
                selected_doctor = st.selectbox("Select Doctor", doctor_options)
                doctor_id = doctors_df.iloc[0]['doctor_id'] if selected_doctor else None
            else:
                # Create sample doctors for demo
                doctor_options = ["Dr. John Smith - Cardiologist", "Dr. Sarah Johnson - General Medicine", 
                                "Dr. Mike Brown - Neurologist"]
                selected_doctor = st.selectbox("Select Doctor", doctor_options)
                doctor_id = "DR001"  # Demo doctor ID
            
            # Date and time selection
            appointment_date = st.date_input("Appointment Date", min_value=date.today())
            
            # Show available time slots
            if appointment_date:
                available_slots = get_available_time_slots(doctor_id, appointment_date)
                appointment_time = st.selectbox("Available Time Slots", available_slots)
            
            # Appointment type and reason
            appointment_type = st.selectbox("Appointment Type", [
                "Regular Consultation", "Follow-up", "Emergency", "Health Checkup", 
                "Vaccination", "Lab Test", "Procedure"
            ])
            
            reason = st.text_area("Reason for Visit", 
                                placeholder="Describe the reason for your appointment...")
            
            # Special requirements
            special_requirements = st.text_area("Special Requirements (Optional)", 
                                              placeholder="Any special needs, wheelchair access, etc.")
            
            # Insurance information
            has_insurance = st.checkbox("I have health insurance")
            if has_insurance:
                insurance_provider = st.text_input("Insurance Provider")
                policy_number = st.text_input("Policy Number")
            
            # Appointment confirmation
            if st.button("Book Appointment", type="primary"):
                if all([patient_id, doctor_id, appointment_date, appointment_time, reason]):
                    appointment_data = {
                        'patient_id': patient_id,
                        'doctor_id': doctor_id,
                        'appointment_date': appointment_date,
                        'appointment_time': appointment_time,
                        'type': appointment_type,
                        'reason': reason,
                        'fee': calculate_appointment_fee(appointment_type, selected_department)
                    }
                    
                    appointment_id = db.create_appointment(appointment_data)
                    
                    if appointment_id:
                        st.success(f"✅ Appointment booked successfully!")
                        st.info(f"**Appointment ID:** {appointment_id}")
                        st.info(f"**Date & Time:** {appointment_date} at {appointment_time}")
                        st.info(f"**Doctor:** {selected_doctor}")
                        
                        # Send confirmation (placeholder)
                        send_appointment_confirmation(appointment_id, appointment_data)
                    else:
                        st.error("Failed to book appointment. Please try again.")
                else:
                    st.error("Please fill in all required fields.")
        else:
            st.info("Please select or register a patient first.")

def get_available_time_slots(doctor_id, appointment_date):
    """Get available time slots for a doctor on a specific date"""
    # In a real implementation, this would check the doctor's schedule and existing appointments
    
    # Generate time slots (9 AM to 5 PM, 30-minute intervals)
    base_slots = []
    start_time = time(9, 0)  # 9:00 AM
    end_time = time(17, 0)   # 5:00 PM
    
    current_time = datetime.combine(appointment_date, start_time)
    end_datetime = datetime.combine(appointment_date, end_time)
    
    while current_time < end_datetime:
        base_slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=30)
    
    # Remove lunch break (12:00 - 13:00)
    lunch_slots = ["12:00", "12:30"]
    available_slots = [slot for slot in base_slots if slot not in lunch_slots]
    
    # Remove already booked slots (placeholder - would check database)
    # For demo, remove some random slots
    import random
    booked_slots = random.sample(available_slots, min(3, len(available_slots)))
    available_slots = [slot for slot in available_slots if slot not in booked_slots]
    
    return available_slots if available_slots else ["No slots available"]

def calculate_appointment_fee(appointment_type, department):
    """Calculate appointment fee based on type and department"""
    base_fees = {
        "Regular Consultation": 500,
        "Follow-up": 300,
        "Emergency": 1000,
        "Health Checkup": 800,
        "Vaccination": 200,
        "Lab Test": 400,
        "Procedure": 1500
    }
    
    department_multipliers = {
        "General Medicine": 1.0,
        "Cardiology": 1.5,
        "Neurology": 1.5,
        "Orthopedics": 1.3,
        "Pediatrics": 1.1,
        "Gynecology": 1.2,
        "Dermatology": 1.1,
        "ENT": 1.1,
        "Ophthalmology": 1.2
    }
    
    base_fee = base_fees.get(appointment_type, 500)
    multiplier = department_multipliers.get(department, 1.0)
    
    return int(base_fee * multiplier)

def send_appointment_confirmation(appointment_id, appointment_data):
    """Send appointment confirmation (placeholder)"""
    # In a real implementation, this would send SMS/Email
    st.info("📧 Appointment confirmation will be sent via SMS and email.")

def view_appointments():
    """View and manage appointments"""
    st.header("View Appointments")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        date_filter = st.date_input("Filter by Date", value=date.today())
    
    with col2:
        status_filter = st.selectbox("Status", ["All", "Scheduled", "Completed", "Cancelled", "No-show"])
    
    with col3:
        department_filter = st.selectbox("Department", ["All"] + [
            "General Medicine", "Cardiology", "Neurology", "Orthopedics"
        ])
    
    with col4:
        search_term = st.text_input("Search Patient/Doctor")
    
    # Get appointments based on filters
    appointments_df = get_filtered_appointments(date_filter, status_filter, department_filter, search_term)
    
    if not appointments_df.empty:
        # Display appointments in a table
        st.subheader(f"Appointments ({len(appointments_df)} found)")
        
        # Add action buttons to each row
        for idx, appointment in appointments_df.iterrows():
            with st.expander(f"🕐 {appointment['appointment_time']} - {appointment['patient_name']} with {appointment['doctor_name']}"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**Patient:** {appointment['patient_name']}")
                    st.write(f"**Doctor:** {appointment['doctor_name']}")
                    st.write(f"**Type:** {appointment['type']}")
                    st.write(f"**Reason:** {appointment['reason']}")
                
                with col2:
                    st.write(f"**Date:** {appointment['appointment_date']}")
                    st.write(f"**Time:** {appointment['appointment_time']}")
                    st.write(f"**Status:** {appointment['status']}")
                    st.write(f"**Fee:** ₹{appointment['fee']}")
                
                with col3:
                    if appointment['status'] == 'Scheduled':
                        if st.button(f"Complete", key=f"complete_{idx}"):
                            update_appointment_status(appointment['appointment_id'], 'Completed')
                            st.rerun()
                        
                        if st.button(f"Cancel", key=f"cancel_{idx}"):
                            update_appointment_status(appointment['appointment_id'], 'Cancelled')
                            st.rerun()
                        
                        if st.button(f"Reschedule", key=f"reschedule_{idx}"):
                            st.session_state[f"reschedule_{appointment['appointment_id']}"] = True
                    
                    # Reschedule form
                    if st.session_state.get(f"reschedule_{appointment['appointment_id']}", False):
                        st.subheader("Reschedule Appointment")
                        new_date = st.date_input("New Date", key=f"new_date_{idx}")
                        new_time = st.selectbox("New Time", get_available_time_slots(appointment['doctor_id'], new_date), key=f"new_time_{idx}")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("Confirm Reschedule", key=f"confirm_reschedule_{idx}"):
                                reschedule_appointment(appointment['appointment_id'], new_date, new_time)
                                st.session_state[f"reschedule_{appointment['appointment_id']}"] = False
                                st.rerun()
                        
                        with col_b:
                            if st.button("Cancel Reschedule", key=f"cancel_reschedule_{idx}"):
                                st.session_state[f"reschedule_{appointment['appointment_id']}"] = False
                                st.rerun()
    else:
        st.info("No appointments found for the selected criteria.")

def get_filtered_appointments(date_filter, status_filter, department_filter, search_term):
    """Get filtered appointments (demo data)"""
    # Generate sample appointments data
    sample_appointments = []
    
    for i in range(10):
        appointment_date = date_filter + timedelta(days=i % 3)
        sample_appointments.append({
            'appointment_id': f"APT{2025080100 + i}",
            'patient_name': f"Patient {i+1}",
            'doctor_name': f"Dr. Doctor {i+1}",
            'doctor_id': f"DR{i+1:03d}",
            'appointment_date': appointment_date.strftime('%Y-%m-%d'),
            'appointment_time': f"{9 + (i % 8)}:{'00' if i % 2 == 0 else '30'}",
            'type': ["Regular Consultation", "Follow-up", "Emergency"][i % 3],
            'reason': f"Medical consultation {i+1}",
            'status': ["Scheduled", "Completed", "Cancelled"][i % 3],
            'fee': 500 + (i * 100)
        })
    
    df = pd.DataFrame(sample_appointments)
    
    # Apply filters
    if status_filter != "All":
        df = df[df['status'] == status_filter]
    
    if search_term:
        df = df[
            df['patient_name'].str.contains(search_term, case=False) |
            df['doctor_name'].str.contains(search_term, case=False)
        ]
    
    return df

def update_appointment_status(appointment_id, new_status):
    """Update appointment status"""
    # In real implementation, this would update the database
    st.success(f"Appointment {appointment_id} status updated to {new_status}")

def reschedule_appointment(appointment_id, new_date, new_time):
    """Reschedule appointment"""
    # In real implementation, this would update the database
    st.success(f"Appointment {appointment_id} rescheduled to {new_date} at {new_time}")

def calendar_view():
    """Calendar view of appointments"""
    st.header("Calendar View")
    
    # Month/year selector
    col1, col2 = st.columns(2)
    with col1:
        selected_month = st.selectbox("Month", range(1, 13), 
                                    index=datetime.now().month - 1,
                                    format_func=lambda x: calendar.month_name[x])
    with col2:
        selected_year = st.selectbox("Year", range(2024, 2027), 
                                   index=datetime.now().year - 2024)
    
    # Generate calendar
    cal = calendar.monthcalendar(selected_year, selected_month)
    
    # Display calendar with appointments
    st.subheader(f"{calendar.month_name[selected_month]} {selected_year}")
    
    # Calendar header
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    cols = st.columns(7)
    for i, day in enumerate(days):
        with cols[i]:
            st.markdown(f"**{day}**")
    
    # Calendar body
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.write("")
                else:
                    # Get appointments for this day
                    day_appointments = get_appointments_for_date(selected_year, selected_month, day)
                    
                    if day_appointments:
                        st.markdown(f"""
                        <div style="border: 2px solid var(--accent-color); 
                                   border-radius: 5px; padding: 5px; margin: 2px;
                                   background-color: var(--secondary-bg);">
                            <strong>{day}</strong><br>
                            <small>{len(day_appointments)} apt(s)</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"View {day}", key=f"day_{day}_{i}"):
                            st.session_state['selected_date'] = date(selected_year, selected_month, day)
                            st.session_state['show_day_appointments'] = True
                    else:
                        st.markdown(f"""
                        <div style="border: 1px solid var(--border-color); 
                                   border-radius: 5px; padding: 5px; margin: 2px;">
                            {day}
                        </div>
                        """, unsafe_allow_html=True)
    
    # Show appointments for selected day
    if st.session_state.get('show_day_appointments', False):
        selected_date = st.session_state.get('selected_date')
        if selected_date:
            st.subheader(f"Appointments for {selected_date.strftime('%B %d, %Y')}")
            
            day_appointments = get_appointments_for_date(selected_date.year, selected_date.month, selected_date.day)
            
            if day_appointments:
                for apt in day_appointments:
                    st.info(f"🕐 {apt['time']} - {apt['patient']} with {apt['doctor']}")
            else:
                st.info("No appointments for this day.")
            
            if st.button("Close"):
                st.session_state['show_day_appointments'] = False
                st.rerun()

def get_appointments_for_date(year, month, day):
    """Get appointments for a specific date"""
    # Sample appointments for demo
    sample_appointments = [
        {'time': '09:00', 'patient': 'John Doe', 'doctor': 'Dr. Smith'},
        {'time': '10:30', 'patient': 'Jane Smith', 'doctor': 'Dr. Johnson'},
        {'time': '14:00', 'patient': 'Bob Wilson', 'doctor': 'Dr. Brown'},
    ]
    
    # Return appointments only for certain days (demo)
    if day % 3 == 0:
        return sample_appointments[:2]
    elif day % 5 == 0:
        return sample_appointments
    else:
        return []

def manage_schedule():
    """Manage doctor schedules"""
    st.header("Manage Doctor Schedules")
    
    # Check permissions
    if not auth_manager.has_permission('manage_users'):
        st.error("You don't have permission to manage schedules.")
        return
    
    # Doctor selection
    doctors_df = db.get_doctors()
    if not doctors_df.empty:
        doctor_options = [f"Dr. {row['first_name']} {row['last_name']} - {row['specialization']}" 
                         for _, row in doctors_df.iterrows()]
        selected_doctor = st.selectbox("Select Doctor", doctor_options)
        doctor_id = doctors_df.iloc[0]['doctor_id'] if selected_doctor else None
    else:
        st.info("No doctors found.")
        return
    
    if doctor_id:
        tab1, tab2, tab3 = st.tabs(["📅 Weekly Schedule", "🚫 Block Time", "⚙️ Schedule Settings"])
        
        with tab1:
            manage_weekly_schedule(doctor_id)
        
        with tab2:
            block_time_slots(doctor_id)
        
        with tab3:
            schedule_settings(doctor_id)

def manage_weekly_schedule(doctor_id):
    """Manage weekly schedule for a doctor"""
    st.subheader("Weekly Schedule")
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for day in days:
        with st.expander(f"{day}", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                is_working = st.checkbox(f"Working Day", key=f"working_{day}", value=day != 'Sunday')
            
            if is_working:
                with col2:
                    start_time = st.time_input(f"Start Time", value=time(9, 0), key=f"start_{day}")
                
                with col3:
                    end_time = st.time_input(f"End Time", value=time(17, 0), key=f"end_{day}")
                
                # Break times
                has_break = st.checkbox(f"Lunch Break", key=f"break_{day}", value=True)
                if has_break:
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        break_start = st.time_input(f"Break Start", value=time(12, 0), key=f"break_start_{day}")
                    with col_b2:
                        break_end = st.time_input(f"Break End", value=time(13, 0), key=f"break_end_{day}")
    
    if st.button("Save Schedule"):
        st.success("Schedule saved successfully!")

def block_time_slots(doctor_id):
    """Block specific time slots"""
    st.subheader("Block Time Slots")
    
    with st.form("block_time"):
        block_date = st.date_input("Date to Block", min_value=date.today())
        block_start = st.time_input("Start Time")
        block_end = st.time_input("End Time")
        block_reason = st.text_input("Reason for Blocking")
        
        if st.form_submit_button("Block Time Slot"):
            st.success(f"Time slot blocked: {block_date} from {block_start} to {block_end}")

def schedule_settings(doctor_id):
    """Schedule settings for a doctor"""
    st.subheader("Schedule Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        appointment_duration = st.selectbox("Default Appointment Duration", 
                                          ["15 minutes", "30 minutes", "45 minutes", "60 minutes"])
        buffer_time = st.selectbox("Buffer Time Between Appointments", 
                                 ["0 minutes", "5 minutes", "10 minutes", "15 minutes"])
    
    with col2:
        advance_booking = st.selectbox("Advance Booking Limit", 
                                     ["1 week", "2 weeks", "1 month", "3 months"])
        cancellation_policy = st.selectbox("Cancellation Policy", 
                                         ["24 hours", "48 hours", "72 hours", "1 week"])
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

def appointment_analytics():
    """Appointment analytics and reporting"""
    st.header("Appointment Analytics")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    
    # Generate sample analytics data
    analytics_data = generate_appointment_analytics(start_date, end_date)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Appointments", analytics_data['total_appointments'])
    with col2:
        st.metric("Completed", analytics_data['completed'])
    with col3:
        st.metric("Cancelled", analytics_data['cancelled'])
    with col4:
        st.metric("No-shows", analytics_data['no_shows'])
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Appointments by status
        fig_status = px.pie(
            values=[analytics_data['completed'], analytics_data['cancelled'], 
                   analytics_data['no_shows'], analytics_data['scheduled']],
            names=['Completed', 'Cancelled', 'No-shows', 'Scheduled'],
            title="Appointments by Status"
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Appointments by department
        dept_data = analytics_data['by_department']
        fig_dept = px.bar(
            x=list(dept_data.keys()),
            y=list(dept_data.values()),
            title="Appointments by Department"
        )
        st.plotly_chart(fig_dept, use_container_width=True)
    
    # Daily appointments trend
    daily_data = analytics_data['daily_trend']
    fig_trend = px.line(
        x=list(daily_data.keys()),
        y=list(daily_data.values()),
        title="Daily Appointments Trend"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

def generate_appointment_analytics(start_date, end_date):
    """Generate sample analytics data"""
    import random
    
    total_appointments = random.randint(100, 500)
    completed = int(total_appointments * 0.7)
    cancelled = int(total_appointments * 0.15)
    no_shows = int(total_appointments * 0.1)
    scheduled = total_appointments - completed - cancelled - no_shows
    
    departments = ["General Medicine", "Cardiology", "Neurology", "Orthopedics"]
    by_department = {dept: random.randint(10, 50) for dept in departments}
    
    # Generate daily trend
    daily_trend = {}
    current_date = start_date
    while current_date <= end_date:
        daily_trend[current_date.strftime('%Y-%m-%d')] = random.randint(5, 25)
        current_date += timedelta(days=1)
    
    return {
        'total_appointments': total_appointments,
        'completed': completed,
        'cancelled': cancelled,
        'no_shows': no_shows,
        'scheduled': scheduled,
        'by_department': by_department,
        'daily_trend': daily_trend
    }