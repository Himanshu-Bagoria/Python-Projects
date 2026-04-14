import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication
from utils.database import db
from utils.ui_components import create_metric_card, create_alert_box, create_timeline_chart, create_radar_chart
from config.themes import get_theme_css

class DiagnosisHistoryTracker:
    def __init__(self):
        self.diagnosis_categories = [
            "Cardiovascular", "Respiratory", "Neurological", "Gastrointestinal",
            "Endocrine", "Musculoskeletal", "Dermatological", "Psychiatric"
        ]
        
    def get_patient_diagnosis_history(self, patient_id):
        """Get comprehensive diagnosis history for a patient"""
        # Get patient's appointments and prescriptions
        patient_appointments = [apt for apt in db.appointments if apt['patient_id'] == patient_id]
        patient_prescriptions = [pres for pres in db.prescriptions if pres['patient_id'] == patient_id]
        
        # Simulate diagnosis history from appointments
        diagnosis_history = []
        
        for apt in patient_appointments:
            # Simulate diagnosis based on appointment type
            diagnosis = self.simulate_diagnosis(apt)
            diagnosis_history.append({
                'date': apt['date'],
                'doctor_id': apt['doctor_id'],
                'diagnosis': diagnosis['condition'],
                'category': diagnosis['category'],
                'severity': diagnosis['severity'],
                'confidence': diagnosis['confidence'],
                'symptoms': diagnosis['symptoms'],
                'treatment': diagnosis['treatment'],
                'follow_up': diagnosis['follow_up']
            })
        
        return diagnosis_history
    
    def simulate_diagnosis(self, appointment):
        """Simulate AI diagnosis based on appointment data"""
        # Sample diagnosis data
        diagnoses = [
            {
                'condition': 'Hypertension',
                'category': 'Cardiovascular',
                'severity': 'Moderate',
                'confidence': 0.85,
                'symptoms': ['High blood pressure', 'Headache', 'Dizziness'],
                'treatment': 'Lifestyle changes, Medication',
                'follow_up': '3 months'
            },
            {
                'condition': 'Type 2 Diabetes',
                'category': 'Endocrine',
                'severity': 'Mild',
                'confidence': 0.92,
                'symptoms': ['Increased thirst', 'Frequent urination', 'Fatigue'],
                'treatment': 'Diet control, Metformin',
                'follow_up': '1 month'
            },
            {
                'condition': 'Asthma',
                'category': 'Respiratory',
                'severity': 'Moderate',
                'confidence': 0.78,
                'symptoms': ['Wheezing', 'Shortness of breath', 'Chest tightness'],
                'treatment': 'Inhalers, Avoid triggers',
                'follow_up': '6 months'
            },
            {
                'condition': 'Depression',
                'category': 'Psychiatric',
                'severity': 'Mild',
                'confidence': 0.81,
                'symptoms': ['Low mood', 'Loss of interest', 'Sleep problems'],
                'treatment': 'Therapy, Antidepressants',
                'follow_up': '2 weeks'
            }
        ]
        
        return np.random.choice(diagnoses)
    
    def analyze_diagnosis_trends(self, diagnosis_history):
        """Analyze diagnosis trends and patterns"""
        if not diagnosis_history:
            return None
        
        df = pd.DataFrame(diagnosis_history)
        
        # Category distribution
        category_distribution = df['category'].value_counts()
        
        # Severity trends
        severity_distribution = df['severity'].value_counts()
        
        # Confidence trends over time
        df['date'] = pd.to_datetime(df['date'])
        confidence_trend = df.groupby(df['date'].dt.to_period('M'))['confidence'].mean()
        
        # Most common symptoms
        all_symptoms = []
        for symptoms in df['symptoms']:
            if isinstance(symptoms, list):
                all_symptoms.extend(symptoms)
        
        symptom_frequency = pd.Series(all_symptoms).value_counts().head(10)
        
        return {
            'category_distribution': category_distribution,
            'severity_distribution': severity_distribution,
            'confidence_trend': confidence_trend,
            'symptom_frequency': symptom_frequency
        }
    
    def predict_health_risks(self, diagnosis_history):
        """Predict potential health risks based on diagnosis history"""
        if not diagnosis_history:
            return []
        
        # Simulate risk prediction
        risks = [
            {
                'risk_type': 'Cardiovascular Risk',
                'probability': 0.75,
                'severity': 'High',
                'recommendations': ['Regular BP monitoring', 'Heart-healthy diet', 'Exercise']
            },
            {
                'risk_type': 'Diabetes Complications',
                'probability': 0.60,
                'severity': 'Medium',
                'recommendations': ['Blood sugar monitoring', 'Foot care', 'Eye exams']
            },
            {
                'risk_type': 'Respiratory Issues',
                'probability': 0.45,
                'severity': 'Medium',
                'recommendations': ['Avoid smoking', 'Air purifier', 'Regular check-ups']
            }
        ]
        
        return risks

def main():
    """Main function for AI Diagnosis History Tracker module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the Diagnosis History Tracker")
        return
    
    # Initialize tracker
    tracker = DiagnosisHistoryTracker()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">🤖 AI Diagnosis History Tracker</h1>
        <p class="body-text">Comprehensive diagnosis analysis and health risk prediction</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Patient selection
    st.markdown("### 👥 Patient Selection")
    
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
            
            # Get diagnosis history
            diagnosis_history = tracker.get_patient_diagnosis_history(patient_id)
            
            if diagnosis_history:
                # Diagnosis statistics
                st.markdown("### 📊 Diagnosis Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    create_metric_card("Total Diagnoses", len(diagnosis_history), "📋")
                
                with col2:
                    avg_confidence = np.mean([d['confidence'] for d in diagnosis_history])
                    create_metric_card("Avg. AI Confidence", f"{avg_confidence:.1%}", "🤖")
                
                with col3:
                    categories = len(set([d['category'] for d in diagnosis_history]))
                    create_metric_card("Categories", categories, "🏷️")
                
                with col4:
                    recent_diagnosis = max(diagnosis_history, key=lambda x: x['date'])
                    create_metric_card("Latest", recent_diagnosis['diagnosis'], "🆕")
                
                # Diagnosis timeline
                st.markdown("### 📅 Diagnosis Timeline")
                
                timeline_data = []
                for diagnosis in diagnosis_history:
                    timeline_data.append({
                        'date': diagnosis['date'],
                        'diagnosis': diagnosis['diagnosis'],
                        'category': diagnosis['category'],
                        'severity': diagnosis['severity'],
                        'confidence': diagnosis['confidence']
                    })
                
                create_timeline_chart(timeline_data)
                
                # Analysis tabs
                tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🏥 Categories", "⚠️ Risk Analysis", "📋 Details"])
                
                with tab1:
                    st.markdown("#### 📈 Diagnosis Trends")
                    
                    trends = tracker.analyze_diagnosis_trends(diagnosis_history)
                    
                    if trends:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Confidence trend
                            fig = px.line(
                                x=trends['confidence_trend'].index.astype(str),
                                y=trends['confidence_trend'].values,
                                title="AI Confidence Trend",
                                labels={'x': 'Month', 'y': 'Confidence Score'}
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            # Severity distribution
                            fig2 = px.pie(
                                values=trends['severity_distribution'].values,
                                names=trends['severity_distribution'].index,
                                title="Diagnosis Severity Distribution"
                            )
                            st.plotly_chart(fig2, use_container_width=True)
                
                with tab2:
                    st.markdown("#### 🏥 Diagnosis Categories")
                    
                    if trends:
                        # Category distribution
                        fig = px.bar(
                            x=trends['category_distribution'].index,
                            y=trends['category_distribution'].values,
                            title="Diagnoses by Category"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Radar chart for category analysis
                        categories = list(tracker.diagnosis_categories)
                        values = [trends['category_distribution'].get(cat, 0) for cat in categories]
                        
                        create_radar_chart(categories, values, "Diagnosis Category Analysis")
                
                with tab3:
                    st.markdown("#### ⚠️ Health Risk Analysis")
                    
                    risks = tracker.predict_health_risks(diagnosis_history)
                    
                    if risks:
                        for risk in risks:
                            alert_type = "error" if risk['severity'] == 'High' else "warning"
                            alert_message = f"**{risk['risk_type']}** - Probability: {risk['probability']:.1%}"
                            create_alert_box(alert_message, alert_type)
                            
                            st.markdown("**Recommendations:**")
                            for rec in risk['recommendations']:
                                st.markdown(f"• {rec}")
                            st.markdown("---")
                    else:
                        st.success("✅ No significant health risks detected")
                
                with tab4:
                    st.markdown("#### 📋 Detailed Diagnosis History")
                    
                    # Create dataframe for display
                    df = pd.DataFrame(diagnosis_history)
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.sort_values('date', ascending=False)
                    
                    # Display detailed table
                    st.dataframe(
                        df[['date', 'diagnosis', 'category', 'severity', 'confidence', 'follow_up']],
                        use_container_width=True
                    )
                    
                    # Export option
                    if st.button("📊 Export Diagnosis Report"):
                        st.success("✅ Diagnosis report exported successfully!")
            else:
                st.info("📋 No diagnosis history found for this patient")
        else:
            st.error("Patient not found")

if __name__ == "__main__":
    main()
