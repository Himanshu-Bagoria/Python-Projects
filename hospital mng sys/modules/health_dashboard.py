import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from utils.database import db
from utils.auth import auth_manager, login_required
from utils.ui_components import UIComponents
from utils.notifications import notification_system

@login_required
def health_dashboard():
    """Main health dashboard interface"""
    st.title("📊 Comprehensive Health Dashboard")
    
    # Get current user and determine dashboard type
    user = auth_manager.get_current_user()
    
    if user and user['role'] in ['admin', 'doctor']:
        admin_dashboard()
    elif user and user['role'] == 'patient':
        patient_dashboard()
    else:
        staff_dashboard()

def admin_dashboard():
    """Administrator dashboard with system-wide analytics"""
    st.header("🎛️ System Overview")
    
    # Add notification system
    col_notif1, col_notif2 = st.columns([3, 1])
    with col_notif2:
        if st.button("🔔 Notifications"):
            try:
                notification_system.display_notification_center()
            except Exception as e:
                st.info("Notification system initializing...")
    
    # Enhanced welcome message
    UIComponents.render_gradient_card(
        title="👨‍💼 Administrator Dashboard",
        content="Welcome to your comprehensive hospital management command center. Monitor all systems, track performance, and manage operations efficiently.",
        gradient_colors=["#667eea", "#764ba2"],
        icon="👨‍💼"
    )
    
    # Interactive widgets section
    st.subheader("📊 Real-time Monitoring")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_quick_stats_widget()
    
    with col2:
        render_weather_widget()
        render_system_status_widget()
    
    # Enhanced key metrics with new UI components
    stats = db.get_dashboard_stats()
    
    enhanced_stats = [
        {"title": "Total Patients", "value": str(stats['total_patients']), "delta": "+12 this week", "color": "primary", "icon": "👥"},
        {"title": "Total Doctors", "value": str(stats['total_doctors']), "delta": "+2 new", "color": "success", "icon": "👨‍⚕️"},
        {"title": "Today's Appointments", "value": str(stats['todays_appointments']), "delta": "+5 vs yesterday", "color": "info", "icon": "📅"},
        {"title": "Monthly Revenue", "value": f"₹{stats['monthly_revenue']:,.0f}", "delta": "+8.5%", "color": "warning", "icon": "💰"}
    ]
    
    UIComponents.render_stats_grid(enhanced_stats, columns=4)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Patient demographics
        fig = create_patient_demographics_chart()
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenue trend
        fig = create_revenue_trend_chart()
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional widgets
    st.subheader("🎛️ Management Widgets")
    
    col3, col4 = st.columns(2)
    
    with col3:
        render_patient_flow_widget()
        render_emergency_contacts_widget()
    
    with col4:
        render_medication_alerts_widget()
        render_appointment_reminder_widget()

def patient_dashboard():
    """Patient-specific health dashboard"""
    user = auth_manager.get_current_user()
    username = user['username'] if user else 'User'
    
    # Enhanced welcome with gradient card
    UIComponents.render_gradient_card(
        title=f"👋 Welcome, {username}!",
        content="Access your personal health information, upcoming appointments, and health insights all in one place.",
        gradient_colors=["#11998e", "#38ef7d"],
        icon="👤"
    )
    
    # Health tips widget
    render_health_tips_widget()
    
    # Enhanced patient health metrics
    patient_stats = [
        {"title": "Upcoming Appointments", "value": "2", "delta": "+1 this week", "color": "primary", "icon": "📅"},
        {"title": "Pending Reports", "value": "1", "delta": "-2 completed", "color": "warning", "icon": "📊"},
        {"title": "Health Score", "value": "85/100", "delta": "+5 improved", "color": "success", "icon": "❤️"}
    ]
    
    UIComponents.render_stats_grid(patient_stats, columns=3)
    
    # Personal health charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_vitals_chart()
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_medication_adherence_chart()
        st.plotly_chart(fig, use_container_width=True)

def staff_dashboard():
    """Staff dashboard for nurses and receptionists"""
    
    # Enhanced staff welcome
    UIComponents.render_gradient_card(
        title="👩‍⚕️ Staff Dashboard",
        content="Manage your daily tasks, patient care activities, and stay updated with hospital operations.",
        gradient_colors=["#fa709a", "#fee140"],
        icon="👩‍⚕️"
    )
    
    # Staff metrics
    staff_stats = [
        {"title": "Check-ins Today", "value": "25", "delta": "+3 vs yesterday", "color": "success", "icon": "✅"},
        {"title": "Pending Tasks", "value": "8", "delta": "-2 completed", "color": "warning", "icon": "📋"},
        {"title": "Active Patients", "value": "45", "delta": "+5", "color": "info", "icon": "👥"}
    ]
    
    UIComponents.render_stats_grid(staff_stats, columns=3)
    
    # Add appointment reminders
    col1, col2 = st.columns(2)
    
    with col1:
        render_appointment_reminder_widget()
    
    with col2:
        render_medication_alerts_widget()

def create_patient_demographics_chart():
    """Create patient demographics pie chart"""
    data = {'Age Group': ['0-18', '19-35', '36-50', '51-65', '65+'],
            'Count': [120, 250, 180, 150, 100]}
    
    fig = px.pie(values=data['Count'], names=data['Age Group'], 
                title="Patient Demographics by Age")
    return fig

def create_revenue_trend_chart():
    """Create revenue trend line chart"""
    dates = pd.date_range(start='2025-01-01', periods=30, freq='D')
    revenue = [50000 + i*1000 + (i%7)*5000 for i in range(30)]
    
    fig = px.line(x=dates, y=revenue, title="Daily Revenue Trend")
    fig.update_layout(xaxis_title="Date", yaxis_title="Revenue (₹)")
    return fig

def create_vitals_chart():
    """Create patient vitals chart"""
    dates = pd.date_range(start='2025-01-01', periods=14, freq='D')
    bp_sys = [120 + i%10 for i in range(14)]
    bp_dia = [80 + i%5 for i in range(14)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=bp_sys, name='Systolic BP'))
    fig.add_trace(go.Scatter(x=dates, y=bp_dia, name='Diastolic BP'))
    fig.update_layout(title="Blood Pressure Trend", xaxis_title="Date", yaxis_title="mmHg")
    return fig

def create_medication_adherence_chart():
    """Create medication adherence chart"""
    medications = ['Med A', 'Med B', 'Med C', 'Med D']
    adherence = [95, 88, 92, 85]
    
    fig = px.bar(x=medications, y=adherence, title="Medication Adherence (%)")
    fig.update_layout(yaxis_title="Adherence %")
    return fig

def get_department_performance():
    """Get department performance data"""
    return pd.DataFrame({
        'Department': ['Cardiology', 'Neurology', 'Orthopedics', 'General Medicine'],
        'Patients': [45, 32, 28, 67],
        'Revenue': [125000, 98000, 87000, 156000],
        'Satisfaction': [4.8, 4.6, 4.7, 4.5]
    })

# Widget functions
def render_quick_stats_widget():
    """Render quick stats widget"""
    UIComponents.render_gradient_card(
        title="📊 Quick Stats",
        content="Real-time system statistics and key performance indicators for immediate insight into hospital operations.",
        gradient_colors=["#667eea", "#764ba2"],
        icon="📊"
    )

def render_weather_widget():
    """Render weather widget"""
    UIComponents.render_gradient_card(
        title="🌤️ Weather",
        content="Today: 24°C, Sunny<br>Perfect weather for outdoor patient activities and emergency response.",
        gradient_colors=["#11998e", "#38ef7d"],
        icon="☀️"
    )

def render_system_status_widget():
    """Render system status widget"""
    UIComponents.render_gradient_card(
        title="🟢 System Status",
        content="All systems operational<br>Database: Online<br>Backup: Complete<br>Security: Active",
        gradient_colors=["#51cf66", "#37b24d"],
        icon="✅"
    )

def render_patient_flow_widget():
    """Render patient flow widget"""
    UIComponents.render_gradient_card(
        title="🌊 Patient Flow",
        content="Current: 45 patients<br>Check-ins: 12 today<br>Waiting: 8 patients<br>Peak time: 2-4 PM",
        gradient_colors=["#4dabf7", "#339af0"],
        icon="🌊"
    )

def render_emergency_contacts_widget():
    """Render emergency contacts widget"""
    UIComponents.render_gradient_card(
        title="🚨 Emergency Contacts",
        content="Emergency: 911<br>Security: ext. 1234<br>Admin: ext. 5678<br>IT Support: ext. 9999",
        gradient_colors=["#ff6b6b", "#ff5252"],
        icon="📞"
    )

def render_medication_alerts_widget():
    """Render medication alerts widget"""
    UIComponents.render_gradient_card(
        title="💊 Medication Alerts",
        content="Low stock: 3 items<br>Expired: 0 items<br>Reorder: 5 items<br>Critical: Insulin supplies",
        gradient_colors=["#ffd43b", "#fab005"],
        icon="⚠️"
    )

def render_appointment_reminder_widget():
    """Render appointment reminder widget"""
    UIComponents.render_gradient_card(
        title="📅 Upcoming Appointments",
        content="Next: Dr. Smith (10:30 AM)<br>Patient: John Doe<br>Type: Consultation<br>Room: 205",
        gradient_colors=["#845ec2", "#b39bc8"],
        icon="🔔"
    )

def render_health_tips_widget():
    """Render health tips widget"""
    UIComponents.render_gradient_card(
        title="✨ Health Tip of the Day",
        content="Stay hydrated! Drink at least 8 glasses of water daily to maintain optimal health and support your body's natural functions.",
        gradient_colors=["#fa709a", "#fee140"],
        icon="💧"
    )