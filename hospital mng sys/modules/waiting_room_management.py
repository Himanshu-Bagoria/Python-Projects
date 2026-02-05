import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time
import plotly.graph_objects as go
import plotly.express as px
from utils.database import db
from utils.auth import auth_manager, login_required
from utils.ui_components import UIComponents
import queue
import threading

@login_required
def waiting_room_management():
    """Advanced Waiting Room Management System"""
    st.title("⏰ Smart Waiting Room Management")
    
    # Initialize session state
    if 'waiting_queue' not in st.session_state:
        st.session_state['waiting_queue'] = []
    if 'current_serving' not in st.session_state:
        st.session_state['current_serving'] = []
    if 'completed_today' not in st.session_state:
        st.session_state['completed_today'] = []
    if 'last_update' not in st.session_state:
        st.session_state['last_update'] = datetime.now()
    
    # Auto-refresh mechanism
    placeholder = st.empty()
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Queue Management", 
        "📊 Real-time Dashboard", 
        "⚙️ Queue Settings",
        "📈 Analytics"
    ])
    
    with tab1:
        queue_management_interface()
    
    with tab2:
        realtime_dashboard()
    
    with tab3:
        queue_settings()
    
    with tab4:
        waiting_analytics()

def queue_management_interface():
    """Main queue management interface"""
    st.header("🎯 Queue Management")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        UIComponents.render_metric_card(
            "In Queue", 
            len(st.session_state['waiting_queue']),
            color="primary",
            icon="⏳"
        )
    
    with col2:
        UIComponents.render_metric_card(
            "Being Served", 
            len(st.session_state['current_serving']),
            color="warning",
            icon="🔄"
        )
    
    with col3:
        UIComponents.render_metric_card(
            "Completed Today", 
            len(st.session_state['completed_today']),
            color="success",
            icon="✅"
        )
    
    with col4:
        avg_wait = calculate_average_wait_time()
        UIComponents.render_metric_card(
            "Avg Wait Time", 
            f"{avg_wait} min",
            color="info",
            icon="⏱️"
        )
    
    st.markdown("---")
    
    # Queue management actions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Current Queue")
        
        if st.session_state['waiting_queue']:
            # Create queue display
            queue_df = pd.DataFrame(st.session_state['waiting_queue'])
            queue_df['Wait Time'] = queue_df.apply(
                lambda row: calculate_wait_time(row['check_in_time']), axis=1
            )
            
            # Display queue with actions
            for idx, patient in enumerate(st.session_state['waiting_queue']):
                with st.container():
                    col_a, col_b, col_c, col_d = st.columns([3, 2, 1, 1])
                    
                    with col_a:
                        priority_icon = "🔴" if patient.get('priority') == 'urgent' else "🟡" if patient.get('priority') == 'high' else "🟢"
                        st.write(f"{priority_icon} **{patient['name']}**")
                        st.caption(f"ID: {patient['patient_id']} | Reason: {patient.get('reason', 'Consultation')}")
                    
                    with col_b:
                        wait_time = calculate_wait_time(patient['check_in_time'])
                        st.write(f"⏰ Wait: {wait_time}")
                        st.caption(f"Checked in: {patient['check_in_time'].strftime('%H:%M')}")
                    
                    with col_c:
                        if st.button("▶️", key=f"serve_{idx}", help="Start serving"):
                            start_serving_patient(idx)
                            st.rerun()
                    
                    with col_d:
                        if st.button("❌", key=f"remove_{idx}", help="Remove from queue"):
                            remove_from_queue(idx)
                            st.rerun()
                    
                    st.divider()
        else:
            st.info("No patients in queue currently.")
    
    with col2:
        st.subheader("➕ Add to Queue")
        
        # Quick add form
        with st.form("add_to_queue"):
            # Patient selection
            patients_df = db.get_patients()
            if not patients_df.empty:
                patient_options = [
                    f"{row['patient_id']} - {row['first_name']} {row['last_name']}" 
                    for _, row in patients_df.iterrows()
                ]
                
                selected_patient = st.selectbox("Select Patient", [""] + patient_options)
                
                # Additional info
                reason = st.selectbox("Reason for Visit", [
                    "General Consultation", "Follow-up", "Emergency", 
                    "Lab Results", "Prescription Refill", "Specialist Consultation"
                ])
                
                priority = st.selectbox("Priority Level", [
                    "normal", "high", "urgent"
                ])
                
                notes = st.text_area("Notes (Optional)", max_chars=200)
                
                submitted = st.form_submit_button("➕ Add to Queue", type="primary")
                
                if submitted and selected_patient:
                    patient_id = selected_patient.split(' - ')[0]
                    patient_name = selected_patient.split(' - ')[1]
                    
                    add_to_queue(patient_id, patient_name, reason, priority, notes)
                    st.success(f"Added {patient_name} to queue!")
                    time.sleep(1)
                    st.rerun()
        
        # Currently being served
        st.subheader("🔄 Currently Serving")
        
        if st.session_state['current_serving']:
            for idx, patient in enumerate(st.session_state['current_serving']):
                with st.container():
                    st.write(f"👨‍⚕️ **{patient['name']}**")
                    st.caption(f"Started: {patient['service_start_time'].strftime('%H:%M')}")
                    service_duration = (datetime.now() - patient['service_start_time']).seconds // 60
                    st.caption(f"Duration: {service_duration} min")
                    
                    if st.button("✅ Complete", key=f"complete_{idx}"):
                        complete_service(idx)
                        st.success("Service completed!")
                        st.rerun()
                    
                    st.divider()
        else:
            st.info("No patients currently being served.")

def add_to_queue(patient_id, patient_name, reason, priority, notes=""):
    """Add patient to waiting queue"""
    queue_entry = {
        'patient_id': patient_id,
        'name': patient_name,
        'reason': reason,
        'priority': priority,
        'notes': notes,
        'check_in_time': datetime.now(),
        'queue_number': get_next_queue_number(),
        'estimated_wait': calculate_estimated_wait_time()
    }
    
    # Insert based on priority
    if priority == 'urgent':
        st.session_state['waiting_queue'].insert(0, queue_entry)
    elif priority == 'high':
        # Insert after urgent patients
        insert_pos = 0
        for i, patient in enumerate(st.session_state['waiting_queue']):
            if patient.get('priority') != 'urgent':
                insert_pos = i
                break
        else:
            insert_pos = len(st.session_state['waiting_queue'])
        st.session_state['waiting_queue'].insert(insert_pos, queue_entry)
    else:
        st.session_state['waiting_queue'].append(queue_entry)

def start_serving_patient(queue_index):
    """Move patient from queue to currently serving"""
    if queue_index < len(st.session_state['waiting_queue']):
        patient = st.session_state['waiting_queue'].pop(queue_index)
        patient['service_start_time'] = datetime.now()
        patient['actual_wait_time'] = (patient['service_start_time'] - patient['check_in_time']).seconds // 60
        st.session_state['current_serving'].append(patient)

def complete_service(serving_index):
    """Complete service for a patient"""
    if serving_index < len(st.session_state['current_serving']):
        patient = st.session_state['current_serving'].pop(serving_index)
        patient['service_end_time'] = datetime.now()
        patient['total_service_time'] = (patient['service_end_time'] - patient['service_start_time']).seconds // 60
        st.session_state['completed_today'].append(patient)

def remove_from_queue(queue_index):
    """Remove patient from queue"""
    if queue_index < len(st.session_state['waiting_queue']):
        st.session_state['waiting_queue'].pop(queue_index)

def calculate_wait_time(check_in_time):
    """Calculate current wait time"""
    wait_minutes = (datetime.now() - check_in_time).seconds // 60
    if wait_minutes < 60:
        return f"{wait_minutes} min"
    else:
        hours = wait_minutes // 60
        minutes = wait_minutes % 60
        return f"{hours}h {minutes}m"

def calculate_average_wait_time():
    """Calculate average wait time"""
    if not st.session_state['completed_today']:
        return "0"
    
    total_wait = sum(patient.get('actual_wait_time', 0) for patient in st.session_state['completed_today'])
    avg_wait = total_wait // len(st.session_state['completed_today'])
    return str(avg_wait)

def calculate_estimated_wait_time():
    """Calculate estimated wait time for new patients"""
    queue_length = len(st.session_state['waiting_queue'])
    avg_service_time = 15  # minutes per patient
    return queue_length * avg_service_time

def get_next_queue_number():
    """Get next queue number"""
    if not st.session_state['waiting_queue']:
        return 1
    return max(patient.get('queue_number', 0) for patient in st.session_state['waiting_queue']) + 1

def realtime_dashboard():
    """Real-time waiting room dashboard"""
    st.header("📊 Real-time Dashboard")
    
    # Auto-refresh indicator
    st.markdown(f"🔄 Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    # Real-time metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_queue_size = len(st.session_state['waiting_queue'])
        st.metric("Current Queue", current_queue_size, 
                 delta=current_queue_size - st.session_state.get('prev_queue_size', 0))
    
    with col2:
        serving_count = len(st.session_state['current_serving'])
        st.metric("Being Served", serving_count)
    
    with col3:
        completed_count = len(st.session_state['completed_today'])
        st.metric("Completed Today", completed_count)
    
    with col4:
        avg_wait = calculate_average_wait_time()
        st.metric("Avg Wait (min)", avg_wait)
    
    # Queue visualization
    st.subheader("📈 Queue Visualization")
    
    if st.session_state['waiting_queue'] or st.session_state['current_serving']:
        # Create queue timeline
        fig = create_queue_timeline()
        st.plotly_chart(fig, use_container_width=True)
    
    # Priority distribution
    if st.session_state['waiting_queue']:
        st.subheader("🎯 Priority Distribution")
        
        priority_counts = {}
        for patient in st.session_state['waiting_queue']:
            priority = patient.get('priority', 'normal')
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        fig = px.pie(
            values=list(priority_counts.values()),
            names=list(priority_counts.keys()),
            title="Queue by Priority Level",
            color_discrete_map={
                'urgent': '#ff6b6b',
                'high': '#ffd43b',
                'normal': '#51cf66'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Patient flow today
    st.subheader("📊 Today's Patient Flow")
    
    if st.session_state['completed_today']:
        hourly_flow = create_hourly_flow_chart()
        st.plotly_chart(hourly_flow, use_container_width=True)

def create_queue_timeline():
    """Create queue timeline visualization"""
    fig = go.Figure()
    
    # Current queue
    if st.session_state['waiting_queue']:
        queue_times = [patient['check_in_time'] for patient in st.session_state['waiting_queue']]
        queue_names = [patient['name'] for patient in st.session_state['waiting_queue']]
        
        fig.add_trace(go.Scatter(
            x=queue_times,
            y=queue_names,
            mode='markers+text',
            marker=dict(color='orange', size=12),
            text=['⏳'] * len(queue_names),
            textposition='middle right',
            name='Waiting'
        ))
    
    # Currently serving
    if st.session_state['current_serving']:
        serving_times = [patient['service_start_time'] for patient in st.session_state['current_serving']]
        serving_names = [patient['name'] for patient in st.session_state['current_serving']]
        
        fig.add_trace(go.Scatter(
            x=serving_times,
            y=serving_names,
            mode='markers+text',
            marker=dict(color='blue', size=12),
            text=['🔄'] * len(serving_names),
            textposition='middle right',
            name='Being Served'
        ))
    
    fig.update_layout(
        title="Patient Queue Timeline",
        xaxis_title="Time",
        yaxis_title="Patients",
        height=400
    )
    
    return fig

def create_hourly_flow_chart():
    """Create hourly patient flow chart"""
    if not st.session_state['completed_today']:
        return go.Figure()
    
    # Group by hour
    hourly_counts = {}
    for patient in st.session_state['completed_today']:
        hour = patient['service_end_time'].hour
        hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
    
    hours = list(range(8, 18))  # 8 AM to 6 PM
    counts = [hourly_counts.get(hour, 0) for hour in hours]
    
    fig = go.Figure(data=go.Bar(x=hours, y=counts, marker_color='lightblue'))
    fig.update_layout(
        title="Patients Served by Hour",
        xaxis_title="Hour of Day",
        yaxis_title="Number of Patients",
        height=300
    )
    
    return fig

def queue_settings():
    """Queue configuration settings"""
    st.header("⚙️ Queue Settings")
    
    # General settings
    st.subheader("🔧 General Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        avg_service_time = st.number_input("Average Service Time (minutes)", 
                                         min_value=5, max_value=60, value=15)
        
        max_queue_size = st.number_input("Maximum Queue Size", 
                                        min_value=10, max_value=100, value=50)
        
        auto_refresh = st.checkbox("Auto-refresh Dashboard", value=True)
        
    with col2:
        priority_levels = st.multiselect("Priority Levels", 
                                       ['urgent', 'high', 'normal'], 
                                       default=['urgent', 'high', 'normal'])
        
        notification_threshold = st.number_input("Long Wait Alert (minutes)", 
                                               min_value=15, max_value=120, value=45)
        
        enable_sms = st.checkbox("Enable SMS Notifications", value=False)
    
    # Department-specific settings
    st.subheader("🏥 Department Settings")
    
    departments = ['General', 'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics']
    
    for dept in departments:
        with st.expander(f"{dept} Department"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.number_input(f"{dept} - Service Time (min)", 
                              min_value=5, max_value=60, value=15, 
                              key=f"{dept}_service_time")
            with col_b:
                st.number_input(f"{dept} - Max Queue", 
                              min_value=5, max_value=50, value=20, 
                              key=f"{dept}_max_queue")
    
    # Save settings
    if st.button("💾 Save Settings", type="primary"):
        # In production, save to database
        st.success("Settings saved successfully!")

def waiting_analytics():
    """Waiting room analytics and insights"""
    st.header("📈 Waiting Room Analytics")
    
    # Sample data for analytics (in production, get from database)
    analytics_data = generate_sample_analytics()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Daily Average Wait", "23 min", "-2 min")
    
    with col2:
        st.metric("Patient Satisfaction", "4.2/5", "+0.3")
    
    with col3:
        st.metric("Queue Efficiency", "87%", "+5%")
    
    with col4:
        st.metric("No-Show Rate", "12%", "-3%")
    
    # Charts
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Wait time distribution
        st.subheader("Wait Time Distribution")
        wait_times = np.random.normal(20, 8, 100)  # Sample data
        fig = px.histogram(x=wait_times, nbins=20, title="Wait Time Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        # Peak hours analysis
        st.subheader("Peak Hours Analysis")
        hours = list(range(8, 18))
        patients = [12, 18, 25, 35, 45, 52, 48, 38, 32, 28]
        fig = go.Figure(data=go.Scatter(x=hours, y=patients, mode='lines+markers'))
        fig.update_layout(title="Patient Volume by Hour")
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("💡 AI Recommendations")
    
    recommendations = [
        "Consider adding an extra doctor during 11 AM - 2 PM peak hours",
        "Implement appointment reminders to reduce no-show rate",
        "Optimize check-in process to reduce initial wait time",
        "Consider priority lanes for elderly patients and emergencies"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        st.info(f"**{i}.** {rec}")

def generate_sample_analytics():
    """Generate sample analytics data"""
    # In production, this would query the database
    return {
        'daily_stats': {
            'total_patients': 45,
            'avg_wait_time': 23,
            'satisfaction_score': 4.2,
            'no_show_rate': 0.12
        },
        'hourly_distribution': [12, 18, 25, 35, 45, 52, 48, 38, 32, 28]
    }