import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication
from utils.database import db
from utils.ui_components import create_metric_card, create_alert_box, create_progress_bar
from config.themes import get_theme_css

class SmartWardMonitoring:
    def __init__(self):
        self.ward_types = {
            "General Ward": {"capacity": 50, "occupied": 35},
            "ICU": {"capacity": 20, "occupied": 18},
            "Pediatric Ward": {"capacity": 30, "occupied": 22},
            "Maternity Ward": {"capacity": 25, "occupied": 20},
            "Emergency Ward": {"capacity": 15, "occupied": 12}
        }
        
        self.patient_statuses = ["Stable", "Critical", "Recovering", "Under Observation"]
    
    def get_ward_occupancy(self):
        """Get current ward occupancy data"""
        occupancy_data = []
        
        for ward_name, ward_info in self.ward_types.items():
            occupancy_rate = (ward_info['occupied'] / ward_info['capacity']) * 100
            available_beds = ward_info['capacity'] - ward_info['occupied']
            
            occupancy_data.append({
                'ward': ward_name,
                'capacity': ward_info['capacity'],
                'occupied': ward_info['occupied'],
                'available': available_beds,
                'occupancy_rate': occupancy_rate
            })
        
        return occupancy_data
    
    def get_patient_monitoring_data(self, ward_name):
        """Get patient monitoring data for a specific ward"""
        # Simulate patient monitoring data
        patients = []
        
        num_patients = self.ward_types[ward_name]['occupied']
        
        for i in range(num_patients):
            patient = {
                'id': f"patient_{ward_name.lower().replace(' ', '_')}_{i+1}",
                'name': f"Patient {i+1}",
                'bed_number': f"Bed {i+1:02d}",
                'status': np.random.choice(self.patient_statuses),
                'heart_rate': np.random.randint(60, 120),
                'blood_pressure': f"{np.random.randint(110, 140)}/{np.random.randint(70, 90)}",
                'temperature': round(np.random.uniform(36.5, 38.5), 1),
                'oxygen_saturation': np.random.randint(95, 100),
                'last_updated': (datetime.now() - timedelta(minutes=np.random.randint(1, 60))).strftime("%H:%M")
            }
            
            # Add alerts for critical patients
            if patient['status'] == 'Critical':
                patient['alerts'] = ['High Heart Rate', 'Low Oxygen Saturation']
            elif patient['status'] == 'Under Observation':
                patient['alerts'] = ['Temperature Elevated']
            else:
                patient['alerts'] = []
            
            patients.append(patient)
        
        return patients
    
    def get_ward_analytics(self, ward_name):
        """Get analytics data for a specific ward"""
        # Simulate analytics data
        analytics = {
            'average_stay_duration': np.random.uniform(3, 7),
            'readmission_rate': np.random.uniform(5, 15),
            'patient_satisfaction': np.random.uniform(4.0, 5.0),
            'staff_efficiency': np.random.uniform(85, 95),
            'infection_rate': np.random.uniform(0, 2),
            'discharge_rate': np.random.uniform(80, 95)
        }
        
        return analytics
    
    def generate_alerts(self, ward_name):
        """Generate alerts for a ward"""
        alerts = []
        
        # Simulate various alerts
        alert_types = [
            "Patient requires immediate attention",
            "Medication due",
            "Vital signs abnormal",
            "Equipment malfunction",
            "Staff shortage",
            "Bed availability low"
        ]
        
        num_alerts = np.random.randint(0, 4)
        
        for i in range(num_alerts):
            alert = {
                'id': f"alert_{i+1}",
                'type': np.random.choice(alert_types),
                'severity': np.random.choice(['Low', 'Medium', 'High', 'Critical']),
                'timestamp': (datetime.now() - timedelta(minutes=np.random.randint(1, 120))).strftime("%H:%M"),
                'status': 'Active'
            }
            alerts.append(alert)
        
        return alerts
    
    def get_staff_assignment(self, ward_name):
        """Get staff assignment for a ward"""
        # Simulate staff data
        staff_roles = ["Nurse", "Doctor", "Technician", "Caregiver"]
        
        staff = []
        num_staff = self.ward_types[ward_name]['occupied'] // 3  # 1 staff per 3 patients
        
        for i in range(num_staff):
            staff_member = {
                'id': f"staff_{i+1}",
                'name': f"Staff Member {i+1}",
                'role': np.random.choice(staff_roles),
                'status': np.random.choice(['On Duty', 'On Break', 'Off Duty']),
                'patients_assigned': np.random.randint(1, 5)
            }
            staff.append(staff_member)
        
        return staff

def main():
    """Main function for Smart Ward Monitoring module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the Smart Ward Monitoring")
        return
    
    # Initialize ward monitoring
    ward_monitoring = SmartWardMonitoring()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">🏥 Smart Ward Monitoring</h1>
        <p class="body-text">Real-time patient monitoring and ward management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overall hospital statistics
    st.markdown("### 📊 Hospital Overview")
    
    total_capacity = sum(ward['capacity'] for ward in ward_monitoring.ward_types.values())
    total_occupied = sum(ward['occupied'] for ward in ward_monitoring.ward_types.values())
    total_available = total_capacity - total_occupied
    overall_occupancy = (total_occupied / total_capacity) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card("Total Beds", total_capacity, "🛏️")
    
    with col2:
        create_metric_card("Occupied Beds", total_occupied, "👥")
    
    with col3:
        create_metric_card("Available Beds", total_available, "✅")
    
    with col4:
        create_metric_card("Occupancy Rate", f"{overall_occupancy:.1f}%", "📊")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏥 Ward Overview", "👥 Patient Monitoring", "🚨 Alerts & Notifications", "📈 Analytics"
    ])
    
    with tab1:
        st.markdown("### 🏥 Ward Overview")
        
        # Ward selection
        ward_options = list(ward_monitoring.ward_types.keys())
        selected_ward = st.selectbox("Select Ward", ward_options)
        
        if selected_ward:
            ward_info = ward_monitoring.ward_types[selected_ward]
            occupancy_rate = (ward_info['occupied'] / ward_info['capacity']) * 100
            
            # Ward statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                create_metric_card("Capacity", ward_info['capacity'], "🛏️")
                create_metric_card("Occupied", ward_info['occupied'], "👥")
            
            with col2:
                create_metric_card("Available", ward_info['capacity'] - ward_info['occupied'], "✅")
                create_metric_card("Occupancy Rate", f"{occupancy_rate:.1f}%", "📊")
            
            with col3:
                # Get alerts for this ward
                alerts = ward_monitoring.generate_alerts(selected_ward)
                create_metric_card("Active Alerts", len(alerts), "🚨")
                
                # Get staff for this ward
                staff = ward_monitoring.get_staff_assignment(selected_ward)
                create_metric_card("Staff on Duty", len([s for s in staff if s['status'] == 'On Duty']), "👨‍⚕️")
            
            # Occupancy visualization
            st.markdown("#### 📊 Occupancy Visualization")
            
            occupancy_data = ward_monitoring.get_ward_occupancy()
            
            # Create occupancy chart
            fig = px.bar(
                occupancy_data,
                x='ward',
                y=['occupied', 'available'],
                title=f"Bed Occupancy by Ward",
                barmode='stack',
                color_discrete_map={'occupied': '#ff6b6b', 'available': '#51cf66'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Staff assignment
            st.markdown("#### 👨‍⚕️ Staff Assignment")
            
            if staff:
                staff_data = []
                for member in staff:
                    staff_data.append([
                        member['name'],
                        member['role'],
                        member['status'],
                        member['patients_assigned']
                    ])
                
                staff_df = pd.DataFrame(
                    staff_data,
                    columns=["Name", "Role", "Status", "Patients Assigned"]
                )
                st.dataframe(staff_df, use_container_width=True)
            else:
                st.info("No staff data available for this ward.")
    
    with tab2:
        st.markdown("### 👥 Patient Monitoring")
        
        # Ward selection for patient monitoring
        ward_options = list(ward_monitoring.ward_types.keys())
        selected_ward_monitoring = st.selectbox("Select Ward for Monitoring", ward_options, key="monitoring_ward")
        
        if selected_ward_monitoring:
            patients = ward_monitoring.get_patient_monitoring_data(selected_ward_monitoring)
            
            if patients:
                # Patient monitoring dashboard
                st.markdown(f"#### 📊 {selected_ward_monitoring} - Patient Status")
                
                # Status summary
                status_counts = {}
                for patient in patients:
                    status = patient['status']
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    create_metric_card("Stable", status_counts.get('Stable', 0), "🟢")
                
                with col2:
                    create_metric_card("Critical", status_counts.get('Critical', 0), "🔴")
                
                with col3:
                    create_metric_card("Recovering", status_counts.get('Recovering', 0), "🟡")
                
                with col4:
                    create_metric_card("Under Observation", status_counts.get('Under Observation', 0), "🔵")
                
                # Patient details
                st.markdown("#### 📋 Patient Details")
                
                for patient in patients:
                    with st.expander(f"🛏️ {patient['bed_number']} - {patient['name']} ({patient['status']})"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Patient ID:** {patient['id']}")
                            st.markdown(f"**Bed Number:** {patient['bed_number']}")
                            st.markdown(f"**Status:** {patient['status']}")
                            st.markdown(f"**Last Updated:** {patient['last_updated']}")
                        
                        with col2:
                            st.markdown(f"**Heart Rate:** {patient['heart_rate']} bpm")
                            st.markdown(f"**Blood Pressure:** {patient['blood_pressure']} mmHg")
                            st.markdown(f"**Temperature:** {patient['temperature']}°C")
                            st.markdown(f"**Oxygen Saturation:** {patient['oxygen_saturation']}%")
                        
                        # Alerts
                        if patient['alerts']:
                            st.markdown("**🚨 Alerts:**")
                            for alert in patient['alerts']:
                                create_alert_box(alert, "warning")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button(f"📊 View Details", key=f"details_{patient['id']}"):
                                st.info(f"Opening detailed view for {patient['name']}")
                        
                        with col2:
                            if st.button(f"📞 Call Staff", key=f"call_{patient['id']}"):
                                st.success(f"Calling staff for {patient['name']}")
                        
                        with col3:
                            if st.button(f"📝 Update Status", key=f"update_{patient['id']}"):
                                st.info(f"Updating status for {patient['name']}")
            else:
                st.info("No patients found in this ward.")
    
    with tab3:
        st.markdown("### 🚨 Alerts & Notifications")
        
        # All ward alerts
        all_alerts = []
        
        for ward_name in ward_monitoring.ward_types.keys():
            alerts = ward_monitoring.generate_alerts(ward_name)
            for alert in alerts:
                alert['ward'] = ward_name
                all_alerts.append(alert)
        
        if all_alerts:
            # Alert statistics
            st.markdown("#### 📊 Alert Overview")
            
            critical_alerts = len([a for a in all_alerts if a['severity'] == 'Critical'])
            high_alerts = len([a for a in all_alerts if a['severity'] == 'High'])
            medium_alerts = len([a for a in all_alerts if a['severity'] == 'Medium'])
            low_alerts = len([a for a in all_alerts if a['severity'] == 'Low'])
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                create_metric_card("Critical", critical_alerts, "🔴")
            
            with col2:
                create_metric_card("High", high_alerts, "🟠")
            
            with col3:
                create_metric_card("Medium", medium_alerts, "🟡")
            
            with col4:
                create_metric_card("Low", low_alerts, "🟢")
            
            # Alert list
            st.markdown("#### 🚨 Active Alerts")
            
            # Sort alerts by severity
            severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
            sorted_alerts = sorted(all_alerts, key=lambda x: severity_order[x['severity']])
            
            for alert in sorted_alerts:
                severity_color = {
                    'Critical': 'error',
                    'High': 'warning',
                    'Medium': 'info',
                    'Low': 'success'
                }
                
                alert_message = f"**{alert['ward']}:** {alert['type']}"
                create_alert_box(alert_message, severity_color[alert['severity']])
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**Time:** {alert['timestamp']}")
                
                with col2:
                    if st.button(f"✅ Acknowledge", key=f"ack_{alert['id']}"):
                        st.success(f"Alert acknowledged: {alert['type']}")
                
                with col3:
                    if st.button(f"📞 Respond", key=f"respond_{alert['id']}"):
                        st.info(f"Responding to alert: {alert['type']}")
                
                st.markdown("---")
        else:
            st.success("✅ No active alerts at the moment!")
        
        # Notification settings
        st.markdown("#### ⚙️ Notification Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Critical Alerts", value=True)
            st.checkbox("High Priority Alerts", value=True)
        
        with col2:
            st.checkbox("Medium Priority Alerts", value=False)
            st.checkbox("Low Priority Alerts", value=False)
        
        if st.button("💾 Save Settings"):
            st.success("✅ Notification settings saved!")
    
    with tab4:
        st.markdown("### 📈 Ward Analytics")
        
        # Ward selection for analytics
        ward_options = list(ward_monitoring.ward_types.keys())
        selected_ward_analytics = st.selectbox("Select Ward for Analytics", ward_options, key="analytics_ward")
        
        if selected_ward_analytics:
            analytics = ward_monitoring.get_ward_analytics(selected_ward_analytics)
            
            # Analytics overview
            st.markdown(f"#### 📊 {selected_ward_analytics} Analytics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                create_metric_card("Avg. Stay Duration", f"{analytics['average_stay_duration']:.1f} days", "📅")
                create_metric_card("Readmission Rate", f"{analytics['readmission_rate']:.1f}%", "🔄")
            
            with col2:
                create_metric_card("Patient Satisfaction", f"{analytics['patient_satisfaction']:.1f}/5.0", "⭐")
                create_metric_card("Staff Efficiency", f"{analytics['staff_efficiency']:.1f}%", "👨‍⚕️")
            
            with col3:
                create_metric_card("Infection Rate", f"{analytics['infection_rate']:.1f}%", "🦠")
                create_metric_card("Discharge Rate", f"{analytics['discharge_rate']:.1f}%", "✅")
            
            # Performance indicators
            st.markdown("#### 📈 Performance Indicators")
            
            # Create performance chart
            performance_data = {
                'Metric': ['Stay Duration', 'Readmission Rate', 'Patient Satisfaction', 'Staff Efficiency', 'Infection Rate', 'Discharge Rate'],
                'Value': [
                    analytics['average_stay_duration'],
                    analytics['readmission_rate'],
                    analytics['patient_satisfaction'] * 20,  # Scale to percentage
                    analytics['staff_efficiency'],
                    analytics['infection_rate'],
                    analytics['discharge_rate']
                ]
            }
            
            fig = px.bar(
                performance_data,
                x='Metric',
                y='Value',
                title=f"{selected_ward_analytics} Performance Metrics"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Trend analysis
            st.markdown("#### 📊 Trend Analysis")
            
            # Simulate trend data
            dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30, 0, -1)]
            occupancy_trend = [np.random.uniform(70, 95) for _ in dates]
            
            trend_data = pd.DataFrame({
                'Date': dates,
                'Occupancy Rate (%)': occupancy_trend
            })
            
            fig2 = px.line(
                trend_data,
                x='Date',
                y='Occupancy Rate (%)',
                title=f"{selected_ward_analytics} - 30-Day Occupancy Trend"
            )
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)
            
            # Export options
            st.markdown("#### 📤 Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📊 Export Analytics"):
                    st.success("✅ Analytics report exported!")
            
            with col2:
                if st.button("📈 Export Trends"):
                    st.success("✅ Trend data exported!")
            
            with col3:
                if st.button("📄 Generate Report"):
                    st.success("✅ Comprehensive report generated!")

if __name__ == "__main__":
    main()
