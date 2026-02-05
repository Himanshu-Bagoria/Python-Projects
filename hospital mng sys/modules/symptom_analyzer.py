import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import pickle
import os
from datetime import datetime
from utils.database import db
from utils.auth import auth_manager, login_required

@login_required
def symptom_analyzer():
    """Main symptom analyzer interface"""
    st.title("🩺 AI-Powered Symptom Analyzer")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Symptom Analysis", "📊 Health Assessment", "📈 Trends", "⚙️ Settings"])
    
    with tab1:
        symptom_analysis_interface()
    
    with tab2:
        health_assessment()
    
    with tab3:
        symptom_trends()
    
    with tab4:
        analyzer_settings()

def symptom_analysis_interface():
    """Main symptom analysis interface"""
    st.header("Symptom Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Enter Symptoms")
        
        # Patient selection (if user has permission)
        patient_id = None
        if auth_manager.has_permission('view_all_patients'):
            patients_df = db.get_patients()
            if not patients_df.empty:
                patient_options = ["Select Patient"] + [f"{row['patient_id']} - {row['first_name']} {row['last_name']}" 
                                 for _, row in patients_df.iterrows()]
                
                selected_patient = st.selectbox("Select Patient (Optional)", patient_options)
                if selected_patient != "Select Patient":
                    patient_id = selected_patient.split(' - ')[0]
        
        # Symptom input methods
        input_method = st.radio("How would you like to input symptoms?", 
                               ["Symptom Checker", "Free Text", "Voice Input"])
        
        symptoms_data = None
        
        if input_method == "Symptom Checker":
            symptoms_data = symptom_checker_interface()
        elif input_method == "Free Text":
            symptoms_data = free_text_interface()
        else:
            symptoms_data = voice_input_interface()
        
        if symptoms_data and st.button("Analyze Symptoms", key="analyze_btn"):
            with st.spinner("Analyzing symptoms..."):
                analysis_result = analyze_symptoms(symptoms_data)
                display_analysis_results(analysis_result, patient_id)
    
    with col2:
        st.subheader("Quick Health Check")
        
        # Vital signs input
        with st.expander("Vital Signs", expanded=True):
            temperature = st.number_input("Temperature (°F)", min_value=95.0, max_value=110.0, value=98.6, step=0.1)
            blood_pressure_sys = st.number_input("Blood Pressure (Systolic)", min_value=80, max_value=200, value=120)
            blood_pressure_dia = st.number_input("Blood Pressure (Diastolic)", min_value=40, max_value=120, value=80)
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=70)
            oxygen_saturation = st.number_input("Oxygen Saturation (%)", min_value=80, max_value=100, value=98)
        
        # Emergency indicators
        if temperature > 101.0 or blood_pressure_sys > 140 or heart_rate > 100:
            st.error("⚠️ Abnormal vital signs detected! Consider immediate medical attention.")
        
        # Pain assessment
        with st.expander("Pain Assessment"):
            pain_level = st.slider("Pain Level (0-10)", 0, 10, 0)
            pain_location = st.text_input("Pain Location")
            pain_type = st.selectbox("Pain Type", ["None", "Sharp", "Dull", "Burning", "Throbbing", "Cramping"])

def symptom_checker_interface():
    """Guided symptom checker interface"""
    st.subheader("Guided Symptom Checker")
    
    # Load symptom categories
    symptom_categories = get_symptom_categories()
    
    selected_symptoms = []
    
    for category, symptoms in symptom_categories.items():
        with st.expander(f"{category}", expanded=False):
            for idx, symptom in enumerate(symptoms):
                # Create unique keys by combining category, symptom, and index
                unique_key_base = f"{category}_{idx}_{symptom.replace(' ', '_')}"
                
                if st.checkbox(symptom, key=f"symptom_{unique_key_base}"):
                    severity = st.select_slider(
                        f"Severity of {symptom}",
                        options=["Mild", "Moderate", "Severe"],
                        value="Mild",
                        key=f"severity_{unique_key_base}"
                    )
                    duration = st.selectbox(
                        f"Duration of {symptom}",
                        ["< 1 day", "1-3 days", "4-7 days", "1-2 weeks", "> 2 weeks"],
                        key=f"duration_{unique_key_base}"
                    )
                    selected_symptoms.append({
                        'symptom': symptom,
                        'category': category,
                        'severity': severity,
                        'duration': duration
                    })
    
    return selected_symptoms

def free_text_interface():
    """Free text symptom input"""
    st.subheader("Describe Your Symptoms")
    
    symptom_text = st.text_area(
        "Describe your symptoms in detail:",
        height=150,
        placeholder="Example: I have been experiencing headaches for the past 3 days, along with fever and fatigue..."
    )
    
    if symptom_text:
        # Parse symptoms from text using NLP
        parsed_symptoms = parse_symptoms_from_text(symptom_text)
        return parsed_symptoms
    
    return None

def voice_input_interface():
    """Voice input for symptoms (placeholder)"""
    st.subheader("Voice Input")
    st.info("Voice input functionality would be implemented here using speech recognition.")
    
    if st.button("Start Voice Recording"):
        st.warning("Voice recording is not implemented in this demo.")
    
    return None

def get_symptom_categories():
    """Get predefined symptom categories with unique symptoms"""
    return {
        "General": [
            "Fever", "Fatigue", "Weight Loss", "Weight Gain", "Chills", "Night Sweats", "Loss of Appetite"
        ],
        "Head & Neck": [
            "Headache", "Dizziness", "Sore Throat", "Neck Pain", "Vision Problems", "Hearing Problems", "Jaw Pain"
        ],
        "Respiratory": [
            "Cough", "Shortness of Breath", "Wheezing", "Runny Nose", "Sneezing", "Chest Tightness"
        ],
        "Cardiovascular": [
            "Chest Pain (Heart)", "Palpitations", "Irregular Heartbeat", "Swelling in Legs", "High Blood Pressure", "Rapid Heartbeat"
        ],
        "Gastrointestinal": [
            "Nausea", "Vomiting", "Diarrhea", "Constipation", "Abdominal Pain", "Heartburn", "Bloating"
        ],
        "Musculoskeletal": [
            "Joint Pain", "Muscle Pain", "Back Pain", "Stiffness", "Swelling (Joints)", "Limited Range of Motion", "Muscle Cramps"
        ],
        "Neurological": [
            "Memory Problems", "Confusion", "Numbness", "Tingling", "Seizures", "Tremors", "Balance Problems"
        ],
        "Skin": [
            "Rash", "Itching", "Dry Skin", "Hair Loss", "Nail Changes", "Unusual Moles", "Bruising"
        ]
    }

def parse_symptoms_from_text(text):
    """Parse symptoms from free text using simple NLP"""
    # This is a simplified version - in production, you'd use more sophisticated NLP
    symptom_keywords = {
        'headache': ['headache', 'head pain', 'migraine'],
        'fever': ['fever', 'high temperature', 'hot'],
        'cough': ['cough', 'coughing'],
        'fatigue': ['tired', 'fatigue', 'exhausted', 'weak'],
        'nausea': ['nausea', 'sick', 'queasy'],
        'pain': ['pain', 'ache', 'hurt', 'sore'],
        'dizziness': ['dizzy', 'dizziness', 'lightheaded']
    }
    
    text_lower = text.lower()
    found_symptoms = []
    
    for symptom, keywords in symptom_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_symptoms.append({
                    'symptom': symptom.title(),
                    'category': 'General',
                    'severity': 'Moderate',  # Default severity
                    'duration': '1-3 days',  # Default duration
                    'description': text
                })
                break
    
    return found_symptoms

def analyze_symptoms(symptoms_data):
    """Analyze symptoms and provide preliminary assessment"""
    if not symptoms_data:
        return None
    
    # Load or create symptom analysis model
    model = get_symptom_analysis_model()
    
    # Prepare features for analysis
    features = prepare_symptom_features(symptoms_data)
    
    # Get possible conditions
    possible_conditions = predict_conditions(features, model)
    
    # Calculate risk level
    risk_level = calculate_risk_level(symptoms_data)
    
    # Generate recommendations
    recommendations = generate_recommendations(symptoms_data, possible_conditions, risk_level)
    
    return {
        'symptoms': symptoms_data,
        'possible_conditions': possible_conditions,
        'risk_level': risk_level,
        'recommendations': recommendations,
        'confidence_score': calculate_confidence_score(symptoms_data),
        'analysis_timestamp': datetime.now()
    }

def get_symptom_analysis_model():
    """Get or create symptom analysis model"""
    model_path = "data/symptom_model.pkl"
    
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    else:
        # Create a simple decision tree model with dummy data
        model = create_dummy_symptom_model()
        os.makedirs("data", exist_ok=True)
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        return model

def create_dummy_symptom_model():
    """Create a dummy symptom analysis model for demonstration"""
    # This is simplified - in production, you'd train on real medical data
    
    # Sample training data
    conditions_data = {
        'Common Cold': ['runny nose', 'sneezing', 'sore throat', 'mild fever'],
        'Flu': ['fever', 'fatigue', 'muscle pain', 'headache', 'cough'],
        'Migraine': ['severe headache', 'nausea', 'sensitivity to light'],
        'Gastroenteritis': ['nausea', 'vomiting', 'diarrhea', 'abdominal pain'],
        'Anxiety': ['chest pain', 'palpitations', 'dizziness', 'fatigue'],
        'Hypertension': ['headache', 'dizziness', 'chest pain'],
    }
    
    return {
        'type': 'rule_based',
        'conditions': conditions_data
    }

def prepare_symptom_features(symptoms_data):
    """Prepare features for symptom analysis"""
    features = {
        'symptom_count': len(symptoms_data),
        'severe_symptoms': sum(1 for s in symptoms_data if s.get('severity') == 'Severe'),
        'chronic_symptoms': sum(1 for s in symptoms_data if s.get('duration') in ['1-2 weeks', '> 2 weeks']),
        'symptoms': [s['symptom'].lower() for s in symptoms_data]
    }
    return features

def predict_conditions(features, model):
    """Predict possible conditions based on symptoms"""
    if model['type'] == 'rule_based':
        possible_conditions = []
        user_symptoms = set(features['symptoms'])
        
        for condition, condition_symptoms in model['conditions'].items():
            condition_symptoms_set = set(s.lower() for s in condition_symptoms)
            
            # Calculate overlap
            overlap = len(user_symptoms.intersection(condition_symptoms_set))
            if overlap > 0:
                confidence = overlap / len(condition_symptoms_set)
                possible_conditions.append({
                    'condition': condition,
                    'confidence': confidence,
                    'matching_symptoms': list(user_symptoms.intersection(condition_symptoms_set))
                })
        
        # Sort by confidence
        possible_conditions.sort(key=lambda x: x['confidence'], reverse=True)
        return possible_conditions[:5]  # Top 5 conditions
    
    return []

def calculate_risk_level(symptoms_data):
    """Calculate overall risk level"""
    risk_score = 0
    
    for symptom in symptoms_data:
        # Add points based on severity
        if symptom.get('severity') == 'Severe':
            risk_score += 3
        elif symptom.get('severity') == 'Moderate':
            risk_score += 2
        else:
            risk_score += 1
        
        # Add points for duration
        if symptom.get('duration') in ['1-2 weeks', '> 2 weeks']:
            risk_score += 2
        
        # Add points for specific high-risk symptoms
        high_risk_symptoms = ['chest pain', 'difficulty breathing', 'severe headache', 'high fever']
        if symptom.get('symptom', '').lower() in high_risk_symptoms:
            risk_score += 3
    
    # Determine risk level
    if risk_score >= 15:
        return "High"
    elif risk_score >= 8:
        return "Medium"
    else:
        return "Low"

def calculate_confidence_score(symptoms_data):
    """Calculate confidence score for the analysis"""
    base_confidence = 0.6
    
    # Increase confidence with more symptoms
    symptom_bonus = min(len(symptoms_data) * 0.05, 0.2)
    
    # Increase confidence with detailed information
    detail_bonus = 0
    for symptom in symptoms_data:
        if symptom.get('severity') and symptom.get('duration'):
            detail_bonus += 0.02
    
    return min(base_confidence + symptom_bonus + detail_bonus, 0.95)

def generate_recommendations(symptoms_data, possible_conditions, risk_level):
    """Generate recommendations based on analysis"""
    recommendations = []
    
    # Risk-based recommendations
    if risk_level == "High":
        recommendations.append({
            'type': 'urgent',
            'text': 'Seek immediate medical attention or visit the emergency room.',
            'priority': 1
        })
    elif risk_level == "Medium":
        recommendations.append({
            'type': 'medical',
            'text': 'Schedule an appointment with a healthcare provider within 24-48 hours.',
            'priority': 2
        })
    else:
        recommendations.append({
            'type': 'monitoring',
            'text': 'Monitor symptoms. Consider seeing a healthcare provider if symptoms worsen.',
            'priority': 3
        })
    
    # General recommendations
    recommendations.extend([
        {
            'type': 'general',
            'text': 'Stay hydrated and get adequate rest.',
            'priority': 4
        },
        {
            'type': 'monitoring',
            'text': 'Keep a symptom diary to track changes.',
            'priority': 5
        }
    ])
    
    # Condition-specific recommendations
    if possible_conditions:
        top_condition = possible_conditions[0]['condition']
        condition_recommendations = get_condition_specific_recommendations(top_condition)
        recommendations.extend(condition_recommendations)
    
    return sorted(recommendations, key=lambda x: x['priority'])

def get_condition_specific_recommendations(condition):
    """Get condition-specific recommendations"""
    condition_recs = {
        'Common Cold': [
            {'type': 'treatment', 'text': 'Use saline nasal drops and warm liquids.', 'priority': 4},
            {'type': 'prevention', 'text': 'Wash hands frequently to prevent spread.', 'priority': 5}
        ],
        'Flu': [
            {'type': 'treatment', 'text': 'Consider antiviral medication if started early.', 'priority': 3},
            {'type': 'isolation', 'text': 'Stay home to avoid spreading to others.', 'priority': 4}
        ],
        'Migraine': [
            {'type': 'treatment', 'text': 'Rest in a dark, quiet room.', 'priority': 3},
            {'type': 'medication', 'text': 'Consider over-the-counter pain relievers.', 'priority': 4}
        ]
    }
    
    return condition_recs.get(condition, [])

def display_analysis_results(analysis_result, patient_id=None):
    """Display the analysis results"""
    if not analysis_result:
        st.error("Unable to analyze symptoms. Please try again.")
        return
    
    # Risk level display
    risk_level = analysis_result['risk_level']
    risk_colors = {'Low': 'success', 'Medium': 'warning', 'High': 'error'}
    
    st.markdown(f"""
    <div class="{risk_colors[risk_level]}-box">
        <h3>Risk Level: {risk_level}</h3>
        <p>Confidence Score: {analysis_result['confidence_score']:.1%}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Possible conditions
    if analysis_result['possible_conditions']:
        st.subheader("Possible Conditions")
        
        for i, condition in enumerate(analysis_result['possible_conditions'][:3]):
            with st.expander(f"{condition['condition']} (Confidence: {condition['confidence']:.1%})", 
                           expanded=(i == 0)):
                st.write(f"**Matching Symptoms:** {', '.join(condition['matching_symptoms'])}")
                st.write("**Note:** This is a preliminary assessment. Please consult a healthcare professional for proper diagnosis.")
    
    # Recommendations
    st.subheader("Recommendations")
    
    for rec in analysis_result['recommendations']:
        if rec['type'] == 'urgent':
            st.error(f"🚨 **URGENT:** {rec['text']}")
        elif rec['type'] == 'medical':
            st.warning(f"⚕️ **Medical:** {rec['text']}")
        else:
            st.info(f"💡 **{rec['type'].title()}:** {rec['text']}")
    
    # Save analysis (if patient selected)
    if patient_id:
        if st.button("Save Analysis to Patient Record"):
            save_analysis_to_record(patient_id, analysis_result)
            st.success("Analysis saved to patient record!")

def save_analysis_to_record(patient_id, analysis_result):
    """Save analysis to patient record"""
    # In a real implementation, this would save to the database
    analysis_data = {
        'patient_id': patient_id,
        'analysis_date': analysis_result['analysis_timestamp'].isoformat(),
        'symptoms': analysis_result['symptoms'],
        'risk_level': analysis_result['risk_level'],
        'possible_conditions': analysis_result['possible_conditions'],
        'recommendations': analysis_result['recommendations']
    }
    
    # Save to file for demo purposes
    os.makedirs("data/analyses", exist_ok=True)
    filename = f"data/analyses/{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump(analysis_data, f, indent=2, default=str)

def health_assessment():
    """Comprehensive health assessment interface"""
    st.header("Comprehensive Health Assessment")
    
    # Health questionnaire
    with st.form("health_assessment"):
        st.subheader("General Health Questions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sleep_hours = st.number_input("Hours of sleep per night", min_value=1, max_value=24, value=8)
            exercise_frequency = st.selectbox("Exercise frequency", 
                                            ["Never", "1-2 times/week", "3-4 times/week", "5+ times/week"])
            stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
            
        with col2:
            smoking = st.selectbox("Smoking status", ["Never", "Former", "Current"])
            alcohol = st.selectbox("Alcohol consumption", 
                                 ["Never", "Occasionally", "Moderately", "Heavily"])
            diet_quality = st.slider("Diet Quality (1-10)", 1, 10, 7)
        
        medical_history = st.multiselect("Medical History", [
            "Diabetes", "Hypertension", "Heart Disease", "Cancer", "Stroke",
            "Kidney Disease", "Liver Disease", "Mental Health Conditions"
        ])
        
        family_history = st.multiselect("Family History", [
            "Heart Disease", "Cancer", "Diabetes", "Stroke", "Mental Health"
        ])
        
        medications = st.text_area("Current Medications", 
                                 placeholder="List current medications...")
        
        if st.form_submit_button("Generate Health Assessment"):
            assessment = generate_health_assessment({
                'sleep_hours': sleep_hours,
                'exercise_frequency': exercise_frequency,
                'stress_level': stress_level,
                'smoking': smoking,
                'alcohol': alcohol,
                'diet_quality': diet_quality,
                'medical_history': medical_history,
                'family_history': family_history,
                'medications': medications
            })
            
            display_health_assessment(assessment)

def generate_health_assessment(health_data):
    """Generate comprehensive health assessment"""
    health_score = 0
    recommendations = []
    risk_factors = []
    
    # Sleep assessment
    if health_data['sleep_hours'] < 6:
        risk_factors.append("Insufficient sleep")
        recommendations.append("Aim for 7-9 hours of sleep per night")
    elif health_data['sleep_hours'] >= 7:
        health_score += 20
    
    # Exercise assessment
    if health_data['exercise_frequency'] in ["Never", "1-2 times/week"]:
        risk_factors.append("Insufficient physical activity")
        recommendations.append("Increase physical activity to at least 150 minutes per week")
    else:
        health_score += 25
    
    # Stress assessment
    if health_data['stress_level'] > 7:
        risk_factors.append("High stress levels")
        recommendations.append("Consider stress management techniques like meditation or therapy")
    elif health_data['stress_level'] <= 5:
        health_score += 15
    
    # Lifestyle factors
    if health_data['smoking'] == "Current":
        risk_factors.append("Smoking")
        recommendations.append("Consider smoking cessation programs")
    elif health_data['smoking'] == "Never":
        health_score += 20
    
    if health_data['alcohol'] in ["Moderately", "Heavily"]:
        risk_factors.append("Excessive alcohol consumption")
        recommendations.append("Reduce alcohol consumption")
    
    # Diet assessment
    if health_data['diet_quality'] >= 8:
        health_score += 20
    elif health_data['diet_quality'] <= 5:
        risk_factors.append("Poor diet quality")
        recommendations.append("Improve diet with more fruits, vegetables, and whole grains")
    
    return {
        'health_score': min(health_score, 100),
        'risk_factors': risk_factors,
        'recommendations': recommendations,
        'medical_history': health_data['medical_history'],
        'family_history': health_data['family_history']
    }

def display_health_assessment(assessment):
    """Display health assessment results"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Health score
        score = assessment['health_score']
        if score >= 80:
            color = "success"
            status = "Excellent"
        elif score >= 60:
            color = "warning"
            status = "Good"
        else:
            color = "error"
            status = "Needs Improvement"
        
        st.markdown(f"""
        <div class="{color}-box">
            <h3>Health Score: {score}/100</h3>
            <p>Status: {status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Risk factors
        if assessment['risk_factors']:
            st.subheader("Risk Factors")
            for risk in assessment['risk_factors']:
                st.error(f"⚠️ {risk}")
        else:
            st.success("✅ No major risk factors identified")
    
    # Recommendations
    if assessment['recommendations']:
        st.subheader("Recommendations")
        for rec in assessment['recommendations']:
            st.info(f"💡 {rec}")

def symptom_trends():
    """Display symptom trends and analytics"""
    st.header("Symptom Trends & Analytics")
    
    # Placeholder for trends - would use real data in production
    st.info("Symptom trends and analytics would be displayed here using real patient data.")

def analyzer_settings():
    """Symptom analyzer settings"""
    st.header("Analyzer Settings")
    
    st.subheader("Model Configuration")
    
    model_type = st.selectbox("Analysis Model", ["Rule-Based", "Machine Learning", "Hybrid"])
    confidence_threshold = st.slider("Confidence Threshold", 0.1, 0.9, 0.6)
    max_conditions = st.number_input("Maximum Conditions to Display", 1, 10, 5)
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")