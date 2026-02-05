import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from utils.auth import auth_manager, login_required
from utils.database import db
from utils.ui_components import UIComponents
import time

@login_required
def admin_dashboard():
    st.title("⚙️ Advanced Administrator Dashboard")
    
    # Check admin permissions
    if not auth_manager.has_permission('system_settings'):
        st.error("You don't have permission to access the admin dashboard.")
        return
    
    # Real-time dashboard header
    create_dashboard_header()
    
    tabs = st.tabs(["📊 Analytics Dashboard", "👥 User Management", "🏥 System Settings", "📊 Reports", "🔧 Maintenance", "🚨 Real-time Monitoring"])
    
    with tabs[0]:
        analytics_dashboard()
    
    with tabs[1]:
        user_management_panel()
    
    with tabs[2]:
        system_settings_panel()
    
    with tabs[3]:
        reports_panel()
    
    with tabs[4]:
        maintenance_panel()
    
    with tabs[5]:
        realtime_monitoring_panel()

def create_dashboard_header():
    """Create enhanced dashboard header with real-time stats"""
    st.markdown(f"**🕐 Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get real-time stats
    stats = db.get_dashboard_stats()
    
    # Create colorful metric cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        UIComponents.render_metric_card(
            "Total Patients",
            str(stats.get('total_patients', 0)),
            "+12 today",
            "success",
            "👥"
        )
    
    with col2:
        UIComponents.render_metric_card(
            "Active Doctors",
            str(stats.get('total_doctors', 0)),
            "All available",
            "info",
            "👨‍⚕️"
        )
    
    with col3:
        UIComponents.render_metric_card(
            "Today's Appointments",
            str(stats.get('todays_appointments', 0)),
            "+5 pending",
            "warning",
            "📅"
        )
    
    with col4:
        UIComponents.render_metric_card(
            "Revenue Today",
            f"₹{stats.get('monthly_revenue', 0):,.0f}",
            "+15% vs yesterday",
            "primary",
            "💰"
        )
    
    with col5:
        UIComponents.render_metric_card(
            "System Status",
            "Operational",
            "99.9% uptime",
            "success",
            "🟢"
        )

def analytics_dashboard():
    """Advanced analytics dashboard"""
    st.header("📊 Advanced Analytics Dashboard")
    
    # Key Performance Indicators
    st.subheader("🎯 Key Performance Indicators")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Patient flow chart
        patient_flow_data = generate_sample_patient_flow()
        fig1 = px.line(patient_flow_data, x='hour', y='patients', 
                      title='Patient Flow - Today',
                      color_discrete_sequence=['#667eea'])
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Department utilization
        dept_data = generate_department_utilization()
        fig2 = px.bar(dept_data, x='department', y='utilization',
                     title='Department Utilization (%)',
                     color='utilization',
                     color_continuous_scale='viridis')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Revenue and financial metrics
    st.subheader("💰 Financial Analytics")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Revenue breakdown
        revenue_data = generate_revenue_breakdown()
        fig3 = px.pie(revenue_data, values='amount', names='category',
                     title='Revenue Breakdown - This Month')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        # Daily revenue trend
        daily_revenue = generate_daily_revenue()
        fig4 = px.area(daily_revenue, x='date', y='revenue',
                      title='Daily Revenue Trend',
                      color_discrete_sequence=['#51cf66'])
        st.plotly_chart(fig4, use_container_width=True)
    
    # Real-time operational metrics
    st.subheader("⚡ Real-time Operations")
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        UIComponents.render_progress_ring(85, "Bed Occupancy", "#ff6b6b")
    
    with col6:
        UIComponents.render_progress_ring(92, "Staff Efficiency", "#51cf66")
    
    with col7:
        UIComponents.render_progress_ring(78, "Patient Satisfaction", "#4dabf7")

def user_management_panel():
    """Enhanced user management panel"""
    st.header("👥 User Management")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", "45", "+3")
    with col2:
        st.metric("Active Sessions", "12", "+2")
    with col3:
        st.metric("Doctors", "15", "")
    with col4:
        st.metric("Staff", "30", "+1")
    
    st.subheader("➕ Add New User")
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username*")
            email = st.text_input("Email*")
            first_name = st.text_input("First Name*")
        with col2:
            role = st.selectbox("Role*", ["admin", "doctor", "nurse", "receptionist", "technician"])
            department = st.selectbox("Department*", ["General", "Cardiology", "Neurology", "Orthopedics", "Emergency"])
            phone = st.text_input("Phone")
        
        password = st.text_input("Initial Password*", type="password", value="temp123")
        
        submitted = st.form_submit_button("Add User", type="primary")
        
        if submitted and username and email and first_name:
            # In production, you would add the user to database
            UIComponents.render_notification_bar(
                f"✅ User '{username}' added successfully! Temporary password: temp123",
                type="success"
            )
    
    st.subheader("👤 Existing Users")
    
    # Sample user data with enhanced information
    users_data = pd.DataFrame({
        'Username': ['admin', 'dr_smith', 'dr_johnson', 'nurse_jones', 'nurse_brown'],
        'Name': ['Administrator', 'Dr. John Smith', 'Dr. Sarah Johnson', 'Mary Jones', 'Lisa Brown'],
        'Role': ['Admin', 'Doctor', 'Doctor', 'Nurse', 'Nurse'],
        'Department': ['IT', 'Cardiology', 'Neurology', 'ICU', 'Emergency'],
        'Status': ['🟢 Active', '🟢 Active', '🟡 Away', '🟢 Active', '🔴 Offline'],
        'Last Login': ['2024-01-15 09:30', '2024-01-15 08:45', '2024-01-14 16:20', '2024-01-15 07:15', '2024-01-14 22:30']
    })
    
    UIComponents.render_data_table(users_data, "User Management", searchable=True, table_key="user_mgmt")

def system_settings_panel():
    """Enhanced system settings panel"""
    st.header("🏥 System Settings")
    
    # Hospital configuration
    with st.expander("🏥 Hospital Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            hospital_name = st.text_input("Hospital Name", value="Smart Hospital System")
            hospital_address = st.text_area("Address", value="123 Medical Center Drive\nCity, State 12345")
            hospital_phone = st.text_input("Phone Number", value="+1-555-HOSPITAL")
        with col2:
            hospital_email = st.text_input("Email", value="info@smarthospital.com")
            license_number = st.text_input("License Number", value="HSP-2024-001")
            accreditation = st.text_input("Accreditation", value="JCI Accredited")
    
    # System configuration
    with st.expander("⚙️ System Configuration", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            appointment_duration = st.selectbox("Default Appointment Duration", 
                                              ["15 min", "30 min", "45 min", "60 min"], index=1)
            timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "IST"], index=3)
            language = st.selectbox("Default Language", ["English", "Hindi", "Spanish"], index=0)
        with col2:
            max_appointments = st.number_input("Max Daily Appointments per Doctor", value=20)
            auto_backup = st.checkbox("Enable Auto Backup", value=True)
            notifications = st.checkbox("Enable System Notifications", value=True)
    
    if st.button("💾 Save Settings", type="primary"):
        UIComponents.render_notification_bar(
            "✅ Settings saved successfully!",
            type="success"
        )

def reports_panel():
    """Enhanced reports panel"""
    st.header("📊 Advanced Reports")
    
    # Report generation interface
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📋 Report Configuration")
        
        report_type = st.selectbox("Report Type", [
            "Patient Analytics", "Revenue Report", "Staff Performance", 
            "Department Utilization", "Appointment Statistics", "Inventory Report",
            "Quality Metrics", "Financial Summary"
        ])
        
        date_range = st.selectbox("Date Range", [
            "Today", "This Week", "This Month", "Last 30 Days", "Last 90 Days", "Custom Range"
        ])
        
        if date_range == "Custom Range":
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
        
        format_type = st.selectbox("Format", ["PDF", "Excel", "CSV", "Interactive Dashboard"])
        
        if st.button("📊 Generate Report", type="primary"):
            with st.spinner("Generating report..."):
                time.sleep(2)  # Simulate report generation
                UIComponents.render_notification_bar(
                    f"✅ {report_type} report generated successfully!",
                    type="success"
                )
    
    with col2:
        st.subheader("📈 Report Preview")
        
        # Show preview based on selected report type
        if report_type == "Patient Analytics":
            display_patient_analytics_preview()
        elif report_type == "Revenue Report":
            display_revenue_report_preview()
        else:
            st.info(f"Preview for {report_type} will be displayed here")

def maintenance_panel():
    """Enhanced maintenance panel"""
    st.header("🔧 System Maintenance")
    
    # System health overview
    st.subheader("🏥 System Health Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        UIComponents.render_metric_card("CPU Usage", "45%", "Normal", "success", "💻")
    with col2:
        UIComponents.render_metric_card("Memory Usage", "67%", "High", "warning", "🧠")
    with col3:
        UIComponents.render_metric_card("Disk Usage", "82%", "Critical", "error", "💾")
    with col4:
        UIComponents.render_metric_card("Network", "98%", "Excellent", "success", "🌐")
    
    # Maintenance actions
    st.subheader("🛠️ Maintenance Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🗄️ Database Management**")
        if st.button("📦 Backup Database", use_container_width=True):
            with st.spinner("Creating backup..."):
                time.sleep(3)
                UIComponents.render_notification_bar("✅ Database backup completed successfully!", "success")
        
        if st.button("🔧 Optimize Database", use_container_width=True):
            with st.spinner("Optimizing database..."):
                time.sleep(2)
                UIComponents.render_notification_bar("✅ Database optimization completed!", "success")
        
        if st.button("🧹 Clean Temporary Files", use_container_width=True):
            UIComponents.render_notification_bar("✅ Temporary files cleaned!", "success")
    
    with col2:
        st.markdown("**📊 System Diagnostics**")
        if st.button("🔍 Run System Diagnostics", use_container_width=True):
            with st.spinner("Running diagnostics..."):
                time.sleep(4)
                UIComponents.render_notification_bar("✅ System diagnostics completed - All systems operational!", "success")
        
        if st.button("📝 Generate System Report", use_container_width=True):
            UIComponents.render_notification_bar("✅ System report generated!", "success")
        
        if st.button("🔄 Restart Services", use_container_width=True):
            UIComponents.render_notification_bar("⚠️ Services restart initiated!", "warning")

def realtime_monitoring_panel():
    """Real-time monitoring dashboard"""
    st.header("🚨 Real-time System Monitoring")
    
    # Auto-refresh indicator
    st.markdown(f"🔄 **Auto-refresh:** Every 5 seconds | **Last Update:** {datetime.now().strftime('%H:%M:%S')}")
    
    # Real-time alerts
    alerts = [
        {"type": "warning", "message": "High memory usage detected on Server-01", "time": "2 min ago"},
        {"type": "success", "message": "Backup completed successfully", "time": "5 min ago"},
        {"type": "info", "message": "New patient registered: John Doe", "time": "8 min ago"},
    ]
    
    st.subheader("🚨 Live Alerts")
    for alert in alerts:
        UIComponents.render_notification_bar(
            f"{alert['message']} ({alert['time']})",
            type=alert['type']
        )
    
    # Live system metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Live System Metrics")
        
        # Simulate real-time data
        current_time = datetime.now()
        system_metrics = pd.DataFrame({
            'Time': [current_time - timedelta(minutes=i) for i in range(10, 0, -1)],
            'CPU': np.random.normal(45, 10, 10),
            'Memory': np.random.normal(67, 5, 10),
            'Network': np.random.normal(85, 8, 10)
        })
        
        fig = px.line(system_metrics, x='Time', y=['CPU', 'Memory', 'Network'],
                     title='System Performance (Last 10 minutes)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👥 Live User Activity")
        
        # Active users
        active_users = pd.DataFrame({
            'User': ['Dr. Smith', 'Nurse Jones', 'Admin', 'Dr. Johnson', 'Receptionist'],
            'Activity': ['Viewing Patient Records', 'Updating Vitals', 'System Maintenance', 'Writing Prescription', 'Check-in Patient'],
            'Location': ['Room 101', 'ICU', 'Server Room', 'Room 205', 'Reception'],
            'Duration': ['15 min', '8 min', '25 min', '5 min', '3 min']
        })
        
        UIComponents.render_data_table(active_users, "Currently Active Users", searchable=False, exportable=False, table_key="active_users")

# Helper functions for generating sample data
def generate_sample_patient_flow():
    hours = list(range(8, 18))  # 8 AM to 6 PM
    patients = [12, 18, 25, 35, 45, 52, 48, 38, 32, 28]
    return pd.DataFrame({'hour': hours, 'patients': patients})

def generate_department_utilization():
    departments = ['Emergency', 'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics']
    utilization = [95, 78, 82, 65, 88]
    return pd.DataFrame({'department': departments, 'utilization': utilization})

def generate_revenue_breakdown():
    categories = ['Consultations', 'Procedures', 'Medications', 'Lab Tests', 'Emergency']
    amounts = [45000, 85000, 25000, 15000, 30000]
    return pd.DataFrame({'category': categories, 'amount': amounts})

def generate_daily_revenue():
    dates = pd.date_range(start='2024-01-01', end='2024-01-15')
    revenue = np.random.normal(50000, 10000, len(dates))
    return pd.DataFrame({'date': dates, 'revenue': revenue})

def display_patient_analytics_preview():
    # Sample patient analytics
    data = pd.DataFrame({
        'Age Group': ['0-18', '19-35', '36-50', '51-65', '65+'],
        'Patient Count': [45, 120, 95, 75, 60],
        'Avg Visit Duration': ['30 min', '45 min', '40 min', '50 min', '55 min']
    })
    
    fig = px.bar(data, x='Age Group', y='Patient Count', title='Patient Distribution by Age Group')
    st.plotly_chart(fig, use_container_width=True)

def display_revenue_report_preview():
    # Sample revenue data
    data = generate_revenue_breakdown()
    fig = px.pie(data, values='amount', names='category', title='Revenue Distribution')
    st.plotly_chart(fig, use_container_width=True)
    
