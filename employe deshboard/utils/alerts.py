import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class AlertSystem:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def check_low_attendance(self, threshold=80):
        """Check for employees with low attendance"""
        attendance_df = self.data_manager.load_attendance()
        employees_df = self.data_manager.load_employees()
        
        if attendance_df.empty or employees_df.empty:
            return []
        
        # Calculate attendance rate for each employee
        attendance_rates = attendance_df.groupby('employee_id').agg({
            'status': lambda x: (x == 'Present').sum() / len(x) * 100
        }).reset_index()
        
        attendance_rates.columns = ['employee_id', 'attendance_rate']
        
        # Filter employees below threshold
        low_attendance = attendance_rates[attendance_rates['attendance_rate'] < threshold]
        
        # Merge with employee details
        low_attendance = low_attendance.merge(employees_df[['employee_id', 'name', 'department']], 
                                            on='employee_id', how='left')
        
        alerts = []
        for _, row in low_attendance.iterrows():
            alerts.append({
                'type': 'Low Attendance',
                'employee_id': row['employee_id'],
                'employee_name': row['name'],
                'department': row['department'],
                'value': f"{row['attendance_rate']:.1f}%",
                'threshold': f"{threshold}%",
                'severity': 'warning' if row['attendance_rate'] > 70 else 'danger'
            })
        
        return alerts
    
    def check_performance_dips(self, threshold=70, period_days=30):
        """Check for performance dips"""
        performance_df = self.data_manager.load_performance()
        employees_df = self.data_manager.load_employees()
        
        if performance_df.empty or employees_df.empty:
            return []
        
        # Filter recent performance data
        cutoff_date = datetime.now() - timedelta(days=period_days)
        recent_performance = performance_df[
            pd.to_datetime(performance_df['date']) >= cutoff_date
        ]
        
        # Calculate average performance scores
        avg_performance = recent_performance.groupby('employee_id').agg({
            'tasks_completed': 'mean',
            'quality_score': 'mean',
            'productivity_score': 'mean'
        }).reset_index()
        
        # Calculate overall score
        avg_performance['overall_score'] = (
            avg_performance['tasks_completed'] * 0.3 +
            avg_performance['quality_score'] * 0.4 +
            avg_performance['productivity_score'] * 0.3
        )
        
        # Filter employees below threshold
        low_performance = avg_performance[avg_performance['overall_score'] < threshold]
        
        # Merge with employee details
        low_performance = low_performance.merge(employees_df[['employee_id', 'name', 'department']], 
                                             on='employee_id', how='left')
        
        alerts = []
        for _, row in low_performance.iterrows():
            alerts.append({
                'type': 'Performance Dip',
                'employee_id': row['employee_id'],
                'employee_name': row['name'],
                'department': row['department'],
                'value': f"{row['overall_score']:.1f}",
                'threshold': f"{threshold}",
                'severity': 'warning' if row['overall_score'] > 60 else 'danger'
            })
        
        return alerts
    
    def check_no_recent_activity(self, days_threshold=7):
        """Check for employees with no recent activity"""
        attendance_df = self.data_manager.load_attendance()
        employees_df = self.data_manager.load_employees()
        
        if attendance_df.empty or employees_df.empty:
            return []
        
        # Get latest attendance date for each employee
        latest_attendance = attendance_df.groupby('employee_id')['date'].max().reset_index()
        latest_attendance['date'] = pd.to_datetime(latest_attendance['date'])
        
        # Calculate days since last activity
        latest_attendance['days_since'] = (datetime.now() - latest_attendance['date']).dt.days
        
        # Filter employees with no recent activity
        no_activity = latest_attendance[latest_attendance['days_since'] > days_threshold]
        
        # Merge with employee details
        no_activity = no_activity.merge(employees_df[['employee_id', 'name', 'department']], 
                                      on='employee_id', how='left')
        
        alerts = []
        for _, row in no_activity.iterrows():
            alerts.append({
                'type': 'No Recent Activity',
                'employee_id': row['employee_id'],
                'employee_name': row['name'],
                'department': row['department'],
                'value': f"{row['days_since']} days",
                'threshold': f"{days_threshold} days",
                'severity': 'warning' if row['days_since'] <= 14 else 'danger'
            })
        
        return alerts
    
    def get_all_alerts(self):
        """Get all types of alerts"""
        all_alerts = []
        
        # Get different types of alerts
        attendance_alerts = self.check_low_attendance()
        performance_alerts = self.check_performance_dips()
        activity_alerts = self.check_no_recent_activity()
        
        # Combine all alerts
        all_alerts.extend(attendance_alerts)
        all_alerts.extend(performance_alerts)
        all_alerts.extend(activity_alerts)
        
        # Sort by severity (danger first, then warning)
        severity_order = {'danger': 0, 'warning': 1}
        all_alerts.sort(key=lambda x: severity_order.get(x['severity'], 2))
        
        return all_alerts
    
    def display_alerts(self, alerts):
        """Display alerts in Streamlit"""
        if not alerts:
            st.success("No alerts at this time! 🎉")
            return
        
        # Group alerts by severity
        danger_alerts = [a for a in alerts if a['severity'] == 'danger']
        warning_alerts = [a for a in alerts if a['severity'] == 'warning']
        
        # Display danger alerts
        if danger_alerts:
            st.error("🚨 Critical Alerts")
            for alert in danger_alerts:
                st.markdown(f"""
                **{alert['type']}** - {alert['employee_name']} ({alert['department']})
                - Current: {alert['value']}
                - Threshold: {alert['threshold']}
                """)
        
        # Display warning alerts
        if warning_alerts:
            st.warning("⚠️ Warning Alerts")
            for alert in warning_alerts:
                st.markdown(f"""
                **{alert['type']}** - {alert['employee_name']} ({alert['department']})
                - Current: {alert['value']}
                - Threshold: {alert['threshold']}
                """)