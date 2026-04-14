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
from utils.ui_components import create_metric_card, create_alert_box
from config.themes import get_theme_css

class LabReportVisualizer:
    def __init__(self):
        self.normal_ranges = {
            "Hemoglobin": {"min": 12.0, "max": 16.0, "unit": "g/dL"},
            "Glucose": {"min": 70, "max": 100, "unit": "mg/dL"},
            "Cholesterol": {"min": 0, "max": 200, "unit": "mg/dL"}
        }
    
    def get_lab_reports(self, patient_id):
        """Get lab reports for a patient"""
        reports = [report for report in db.lab_reports if report['patient_id'] == patient_id]
        
        # Add simulated detailed data
        for report in reports:
            report['detailed_results'] = self.generate_detailed_results()
            report['abnormal_values'] = self.identify_abnormal_values(report['detailed_results'])
        
        return reports
    
    def generate_detailed_results(self):
        """Generate detailed lab results"""
        return {
            "Hemoglobin": np.random.uniform(11.5, 16.5),
            "Glucose": np.random.uniform(65, 105),
            "Cholesterol": np.random.uniform(150, 250)
        }
    
    def identify_abnormal_values(self, results):
        """Identify abnormal values in lab results"""
        abnormal = []
        
        for test, value in results.items():
            if test in self.normal_ranges:
                range_info = self.normal_ranges[test]
                if value < range_info['min'] or value > range_info['max']:
                    abnormal.append({
                        'test': test,
                        'value': value,
                        'normal_range': f"{range_info['min']}-{range_info['max']} {range_info['unit']}",
                        'status': 'Low' if value < range_info['min'] else 'High'
                    })
        
        return abnormal

def main():
    """Main function for Lab Report Visualizer module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the Lab Report Visualizer")
        return
    
    # Initialize visualizer
    visualizer = LabReportVisualizer()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">🔬 Lab Report Visualizer</h1>
        <p class="body-text">Interactive lab report analysis and visualization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Patient selection
    patients = db.patients
    if not patients:
        st.error("No patients found in the system")
        return
    
    patient_names = [f"{p['name']} (ID: {p['id']})" for p in patients]
    selected_patient = st.selectbox("Select Patient", patient_names)
    
    if selected_patient:
        patient_id = selected_patient.split("(ID: ")[1].split(")")[0]
        patient = next((p for p in patients if p['id'] == patient_id), None)
        
        if patient:
            # Display patient info
            col1, col2, col3 = st.columns(3)
            
            with col1:
                create_metric_card("Patient Name", patient['name'], "👤")
            
            with col2:
                create_metric_card("Age", f"{patient['age']} years", "📅")
            
            with col3:
                create_metric_card("Blood Group", patient['blood_group'], "🩸")
            
            # Get lab reports
            lab_reports = visualizer.get_lab_reports(patient_id)
            
            if lab_reports:
                # Lab report statistics
                st.markdown("### 📊 Lab Report Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    create_metric_card("Total Reports", len(lab_reports), "📋")
                
                with col2:
                    total_abnormal = sum(len(report['abnormal_values']) for report in lab_reports)
                    create_metric_card("Abnormal Values", total_abnormal, "⚠️")
                
                with col3:
                    recent_report = max(lab_reports, key=lambda x: x['date'])
                    create_metric_card("Latest Report", recent_report['test_type'][:20] + "...", "🆕")
                
                with col4:
                    avg_values = sum(len(report['detailed_results']) for report in lab_reports) / len(lab_reports)
                    create_metric_card("Avg. Tests/Report", f"{avg_values:.1f}", "🔬")
                
                # Display reports
                st.markdown("### 📋 Lab Reports")
                
                for i, report in enumerate(lab_reports):
                    with st.expander(f"{report['test_type']} - {report['date']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Lab:** {report['lab_name']}")
                            st.markdown(f"**Doctor:** {report['doctor_name']}")
                            st.markdown(f"**Status:** {report['status']}")
                        
                        with col2:
                            st.markdown(f"**Notes:** {report['notes']}")
                        
                        # Results table
                        results_data = []
                        for test, value in report['detailed_results'].items():
                            unit = visualizer.normal_ranges.get(test, {}).get('unit', 'units')
                            normal_range = visualizer.normal_ranges.get(test, {})
                            if normal_range:
                                normal_str = f"{normal_range['min']}-{normal_range['max']} {unit}"
                                status = 'Normal'
                                if test in [ab['test'] for ab in report['abnormal_values']]:
                                    status = 'Abnormal'
                            else:
                                normal_str = 'N/A'
                                status = 'Unknown'
                            
                            results_data.append({
                                'Test': test,
                                'Value': f"{value:.2f}",
                                'Unit': unit,
                                'Normal Range': normal_str,
                                'Status': status
                            })
                        
                        results_df = pd.DataFrame(results_data)
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Abnormal values
                        if report['abnormal_values']:
                            st.markdown("**⚠️ Abnormal Values:**")
                            for abnormal in report['abnormal_values']:
                                alert_type = "error" if abnormal['status'] in ['High', 'Low'] else "warning"
                                alert_message = f"**{abnormal['test']}**: {abnormal['value']:.2f} ({abnormal['status']}) - Normal: {abnormal['normal_range']}"
                                create_alert_box(alert_message, alert_type)
                
                # Export option
                if st.button("📊 Export Lab Reports"):
                    st.success("✅ Lab reports exported successfully!")
            else:
                st.info("📋 No lab reports found for this patient")
        else:
            st.error("Patient not found")

if __name__ == "__main__":
    main()
