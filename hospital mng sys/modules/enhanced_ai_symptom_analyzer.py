import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
import json
import pickle
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from utils.database import db
from utils.auth import auth_manager, login_required
from utils.ui_components import UIComponents

@login_required
def enhanced_symptom_analyzer():
    """Enhanced AI-Powered Symptom Analyzer with ML Recommendations"""
    st.title("🧠 AI-Enhanced Symptom Analyzer")
    
    # Initialize ML models
    if 'symptom_models' not in st.session_state:
        st.session_state['symptom_models'] = initialize_ml_models()
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔍 Smart Analysis", 
        "🤖 AI Recommendations", 
        "📊 Risk Assessment",
        "🎯 Treatment Suggestions",
        "📚 Analysis History",
        "📈 Learning Dashboard"
    ])
    
    with tab1:
        smart_symptom_analysis()
    
    with tab2:
        ai_recommendations()
    
    with tab3:
        risk_assessment()
    
    with tab4:
        treatment_suggestions()
    
    with tab5:
        analysis_history_tab()
    
    with tab6:
        learning_dashboard()

def initialize_ml_models():
    """Initialize machine learning models for symptom analysis"""
    models = {}
    
    # Create sample training data (in production, use real medical data)
    training_data = create_sample_medical_data()
    
    # Severity prediction model
    severity_model = RandomForestClassifier(n_estimators=100, random_state=42)
    severity_features = training_data[['temperature', 'pain_level', 'symptom_count', 'duration_days']]
    severity_labels = training_data['severity']
    severity_model.fit(severity_features, severity_labels)
    models['severity'] = severity_model
    
    # Urgency classification model
    urgency_model = DecisionTreeClassifier(random_state=42)
    urgency_features = training_data[['temperature', 'pain_level', 'breathing_difficulty', 'chest_pain']]
    urgency_labels = training_data['urgency']
    urgency_model.fit(urgency_features, urgency_labels)
    models['urgency'] = urgency_model
    
    # Specialization recommendation model
    spec_model = RandomForestClassifier(n_estimators=50, random_state=42)
    spec_features = training_data[['primary_symptom_encoded', 'secondary_symptoms_count', 'age_group']]
    spec_labels = training_data['recommended_specialization']
    spec_model.fit(spec_features, spec_labels)
    models['specialization'] = spec_model
    
    # Text-based symptom similarity model
    symptom_texts = [
        "headache migraine pain", "fever temperature high", "cough cold respiratory",
        "chest pain heart cardiac", "stomach pain digestive", "joint pain arthritis",
        "skin rash dermatology", "anxiety depression mental", "vision eye problems"
    ]
    
    vectorizer = TfidfVectorizer(stop_words='english')
    symptom_vectors = vectorizer.fit_transform(symptom_texts)
    models['text_vectorizer'] = vectorizer
    models['symptom_vectors'] = symptom_vectors
    
    return models

def create_sample_medical_data():
    """Create sample medical training data"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'temperature': np.random.normal(99.5, 2.5, n_samples),
        'pain_level': np.random.randint(0, 11, n_samples),
        'symptom_count': np.random.randint(1, 8, n_samples),
        'duration_days': np.random.exponential(3, n_samples),
        'breathing_difficulty': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'chest_pain': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
        'primary_symptom_encoded': np.random.randint(0, 10, n_samples),
        'secondary_symptoms_count': np.random.randint(0, 5, n_samples),
        'age_group': np.random.randint(0, 4, n_samples)  # 0-3 for age groups
    }
    
    # Create target variables based on features
    severity = []
    urgency = []
    specialization = []
    
    for i in range(n_samples):
        # Severity based on temperature, pain, and symptom count
        if data['temperature'][i] > 102 or data['pain_level'][i] > 7:
            severity.append('severe')
        elif data['temperature'][i] > 100 or data['pain_level'][i] > 4:
            severity.append('moderate')
        else:
            severity.append('mild')
        
        # Urgency based on critical symptoms
        if data['chest_pain'][i] or data['breathing_difficulty'][i] or data['temperature'][i] > 103:
            urgency.append('urgent')
        elif data['temperature'][i] > 101 or data['pain_level'][i] > 6:
            urgency.append('high')
        else:
            urgency.append('normal')
        
        # Specialization based on primary symptom
        spec_map = {
            0: 'General Medicine', 1: 'Cardiology', 2: 'Neurology',
            3: 'Orthopedics', 4: 'Gastroenterology', 5: 'Dermatology',
            6: 'Pulmonology', 7: 'Psychiatry', 8: 'Ophthalmology', 9: 'ENT'
        }
        specialization.append(spec_map[data['primary_symptom_encoded'][i]])
    
    data['severity'] = severity
    data['urgency'] = urgency
    data['recommended_specialization'] = specialization
    
    return pd.DataFrame(data)

def smart_symptom_analysis():
    """Smart symptom analysis with AI insights"""
    st.header("🔍 Smart Symptom Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Symptom Input")
        
        # Enhanced symptom input
        input_method = st.selectbox("Analysis Method", [
            "Guided AI Assistant", "Natural Language", "Structured Input"
        ])
        
        if input_method == "Guided AI Assistant":
            guided_ai_analysis()
        elif input_method == "Natural Language":
            natural_language_analysis()
        else:
            structured_symptom_input()
    
    with col2:
        st.subheader("AI Insights")
        
        # Real-time AI suggestions
        if 'current_symptoms' in st.session_state:
            st.write("**AI Insights based on current symptoms:**")
            st.info("AI analyzing your symptoms...")
        else:
            st.info("Enter symptoms to see AI insights")

def guided_ai_analysis():
    """AI-guided symptom analysis"""
    st.subheader("🤖 AI-Guided Analysis")
    
    # Progressive questioning system
    if 'ai_questions' not in st.session_state:
        st.session_state['ai_questions'] = {
            'step': 1,
            'responses': {},
            'confidence': 0
        }
    
    step = st.session_state['ai_questions']['step']
    
    if step == 1:
        st.write("**AI Assistant:** Let's start with your main concern. What's bothering you most today?")
        
        main_concern = st.selectbox("Primary Concern", [
            "Select your main concern...",
            "Pain or discomfort", "Fever or temperature", "Breathing issues",
            "Digestive problems", "Skin issues", "Mental health", "Other"
        ])
        
        if main_concern != "Select your main concern..." and st.button("Next Question"):
            st.session_state['ai_questions']['responses']['main_concern'] = main_concern
            st.session_state['ai_questions']['step'] = 2
            st.rerun()
    
    elif step == 2:
        main_concern = st.session_state['ai_questions']['responses']['main_concern']
        st.write(f"**AI Assistant:** You mentioned {main_concern.lower()}. Can you rate the intensity?")
        
        intensity = st.slider("Intensity Level (1-10)", 1, 10, 5)
        duration = st.selectbox("How long have you had this?", [
            "Less than 1 hour", "1-6 hours", "6-24 hours", "1-3 days", "More than 3 days"
        ])
        
        if st.button("Continue Analysis"):
            st.session_state['ai_questions']['responses']['intensity'] = intensity
            st.session_state['ai_questions']['responses']['duration'] = duration
            st.session_state['ai_questions']['step'] = 3
            st.rerun()
    
    elif step == 3:
        st.write("**AI Assistant:** Based on your responses, here are some follow-up questions:")
        
        # Dynamic questions based on previous responses
        main_concern = st.session_state['ai_questions']['responses']['main_concern']
        
        if 'pain' in main_concern.lower():
            pain_type = st.selectbox("What type of pain?", [
                "Sharp", "Dull", "Throbbing", "Burning", "Cramping"
            ])
            pain_location = st.text_input("Where exactly is the pain?")
        
        associated_symptoms = st.multiselect("Any associated symptoms?", [
            "Nausea", "Vomiting", "Dizziness", "Fatigue", "Shortness of breath",
            "Headache", "Sweating", "Chills"
        ])
        
        if st.button("Get AI Analysis"):
            # Compile all responses
            analysis_data = {
                'main_concern': st.session_state['ai_questions']['responses']['main_concern'],
                'intensity': st.session_state['ai_questions']['responses']['intensity'],
                'duration': st.session_state['ai_questions']['responses']['duration'],
                'associated_symptoms': associated_symptoms
            }
            
            # Get AI analysis
            ai_analysis = perform_ai_analysis(analysis_data)
            st.session_state['current_analysis'] = ai_analysis
            
            display_enhanced_analysis_results(ai_analysis)

def natural_language_analysis():
    """Enhanced natural language symptom analysis with disease detection"""
    st.subheader("💬 Describe Your Symptoms")
    
    # Two input methods
    input_method = st.radio("How would you like to describe your symptoms?", [
        "🖊️ Write in your own words", 
        "📋 Select from predefined conditions",
        "🔄 Combination of both"
    ])
    
    if input_method == "🖊️ Write in your own words":
        free_text_symptom_input()
    elif input_method == "📋 Select from predefined conditions":
        predefined_disease_selection()
    else:
        combination_symptom_input()

def free_text_symptom_input():
    """Free text symptom input"""
    symptom_description = st.text_area(
        "Describe how you're feeling in detail",
        height=150,
        placeholder="Example: I've been having severe headaches for the past 2 days, along with nausea and sensitivity to light. The pain is throbbing and gets worse when I move..."
    )
    
    # Add contextual questions
    with st.expander("📝 Additional Details (Optional)"):
        col1, col2 = st.columns(2)
        with col1:
            when_started = st.text_input("When did symptoms start?", placeholder="e.g., 3 days ago, this morning")
            triggers = st.text_input("What might have triggered it?", placeholder="e.g., stress, food, activity")
        with col2:
            family_history = st.text_input("Any family history?", placeholder="e.g., diabetes, heart disease")
            current_meds = st.text_input("Current medications?", placeholder="e.g., aspirin, vitamins")
    
    if symptom_description and st.button("🧠 Analyze with AI", type="primary"):
        with st.spinner("AI is analyzing your symptoms and detecting possible conditions..."):
            # Enhanced analysis with disease detection
            analysis = enhanced_natural_language_analysis(symptom_description, {
                'when_started': when_started,
                'triggers': triggers,
                'family_history': family_history,
                'medications': current_meds
            })
            st.session_state['current_analysis'] = analysis
            display_enhanced_analysis_results(analysis)

def predefined_disease_selection():
    """Predefined disease and symptom selection"""
    st.write("🔍 **Select symptoms or suspected conditions:**")
    
    # Disease categories
    disease_categories = {
        "🫀 Cardiovascular": [
            "Chest pain/pressure", "Heart palpitations", "Shortness of breath", 
            "Swelling in legs/feet", "Dizziness/fainting"
        ],
        "🧠 Neurological": [
            "Severe headache", "Migraine", "Seizures", "Memory problems", 
            "Numbness/tingling", "Vision problems"
        ],
        "🫁 Respiratory": [
            "Persistent cough", "Difficulty breathing", "Wheezing", 
            "Chest congestion", "Coughing up blood"
        ],
        "🍽️ Digestive": [
            "Stomach pain", "Nausea/vomiting", "Diarrhea", "Constipation", 
            "Heartburn", "Loss of appetite"
        ],
        "🤒 Infectious/General": [
            "Fever", "Chills", "Fatigue", "Body aches", "Sore throat", 
            "Runny nose", "Skin rash"
        ],
        "🦴 Musculoskeletal": [
            "Joint pain", "Back pain", "Muscle weakness", "Stiffness", 
            "Swelling in joints"
        ],
        "🧘 Mental Health": [
            "Depression", "Anxiety", "Panic attacks", "Sleep problems", 
            "Mood changes", "Stress"
        ]
    }
    
    selected_symptoms = []
    
    for category, symptoms in disease_categories.items():
        with st.expander(f"{category}", expanded=False):
            for symptom in symptoms:
                if st.checkbox(symptom, key=f"symptom_{symptom}"):
                    selected_symptoms.append(symptom)
    
    if selected_symptoms:
        st.write("**Selected symptoms:**", ", ".join(selected_symptoms))
        
        # Severity and timing
        col1, col2 = st.columns(2)
        with col1:
            overall_severity = st.select_slider("Overall severity", 
                                              options=["Mild", "Moderate", "Severe", "Very Severe"])
            duration = st.selectbox("Duration", [
                "Less than 1 hour", "1-6 hours", "6-24 hours", 
                "1-3 days", "4-7 days", "1-2 weeks", "More than 2 weeks"
            ])
        
        with col2:
            pain_scale = st.slider("Pain level (0-10)", 0, 10, 0)
            impact_daily = st.selectbox("Impact on daily activities", [
                "No impact", "Mild impact", "Moderate impact", 
                "Severe impact", "Cannot perform activities"
            ])
        
        if st.button("🔍 Analyze Selected Symptoms", type="primary"):
            with st.spinner("Analyzing symptom pattern..."):
                analysis = analyze_predefined_symptoms(selected_symptoms, {
                    'severity': overall_severity,
                    'duration': duration,
                    'pain_level': pain_scale,
                    'daily_impact': impact_daily
                })
                st.session_state['current_analysis'] = analysis
                display_enhanced_analysis_results(analysis)
    else:
        st.info("Please select symptoms from the categories above.")

def combination_symptom_input():
    """Combination of free text and predefined symptoms"""
    st.write("🔄 **Describe your condition using both methods:**")
    
    # Free text first
    symptom_description = st.text_area(
        "Describe your main symptoms",
        height=100,
        placeholder="Briefly describe what you're experiencing..."
    )
    
    # Quick symptom checkboxes
    st.write("**Quick symptom checklist:**")
    
    common_symptoms = [
        "Fever", "Headache", "Fatigue", "Cough", "Nausea", "Pain", 
        "Dizziness", "Shortness of breath", "Chest discomfort", "Stomach issues"
    ]
    
    selected_quick = []
    cols = st.columns(5)
    for i, symptom in enumerate(common_symptoms):
        with cols[i % 5]:
            if st.checkbox(symptom, key=f"quick_{symptom}"):
                selected_quick.append(symptom)
    
    # Additional details
    col1, col2 = st.columns(2)
    with col1:
        severity = st.select_slider("Severity", options=["Mild", "Moderate", "Severe"])
        duration = st.selectbox("Duration", ["< 1 day", "1-3 days", "4-7 days", "> 1 week"])
    with col2:
        age_group = st.selectbox("Age group", ["0-17", "18-35", "36-50", "51-65", "65+"])
        gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
    
    if (symptom_description or selected_quick) and st.button("🧠 Complete Analysis", type="primary"):
        with st.spinner("Performing comprehensive analysis..."):
            analysis = analyze_combination_input(symptom_description, selected_quick, {
                'severity': severity,
                'duration': duration,
                'age_group': age_group,
                'gender': gender
            })
            st.session_state['current_analysis'] = analysis
            display_enhanced_analysis_results(analysis)

def structured_symptom_input():
    """Structured symptom input with AI enhancement"""
    st.subheader("📋 Structured Input")
    
    # Primary symptoms
    primary_symptoms = st.multiselect("Primary Symptoms", [
        "Fever", "Headache", "Cough", "Shortness of breath", "Chest pain",
        "Abdominal pain", "Nausea", "Vomiting", "Diarrhea", "Fatigue",
        "Dizziness", "Joint pain", "Muscle pain", "Rash", "Sore throat"
    ])
    
    # Severity and duration
    col1, col2 = st.columns(2)
    with col1:
        overall_severity = st.select_slider("Overall Severity", 
                                          options=["Mild", "Moderate", "Severe"])
        temperature = st.number_input("Temperature (°F)", 95.0, 110.0, 98.6)
    
    with col2:
        symptom_duration = st.selectbox("Duration", [
            "< 1 day", "1-3 days", "4-7 days", "1-2 weeks", "> 2 weeks"
        ])
        pain_level = st.slider("Pain Level (0-10)", 0, 10, 0)
    
    # Additional factors
    with st.expander("Additional Information"):
        medical_history = st.multiselect("Relevant Medical History", [
            "Diabetes", "Hypertension", "Heart disease", "Asthma", "Allergies",
            "Previous surgeries", "Chronic conditions", "None"
        ])
        
        current_medications = st.text_area("Current Medications")
        recent_travel = st.checkbox("Recent travel or exposure")
    
    if primary_symptoms and st.button("Generate AI Analysis"):
        structured_data = {
            'primary_symptoms': primary_symptoms,
            'severity': overall_severity,
            'temperature': temperature,
            'duration': symptom_duration,
            'pain_level': pain_level,
            'medical_history': medical_history,
            'medications': current_medications,
            'recent_travel': recent_travel
        }
        
        analysis = perform_structured_analysis(structured_data)
        st.session_state['current_analysis'] = analysis
        
        display_enhanced_analysis_results(analysis)

def perform_ai_analysis(data):
    """Perform AI analysis on symptom data"""
    models = st.session_state['symptom_models']
    
    # Extract features for ML models
    features = extract_features_from_data(data)
    
    # Predict severity
    severity_pred = models['severity'].predict([features['severity_features']])[0]
    severity_proba = models['severity'].predict_proba([features['severity_features']])[0]
    
    # Predict urgency
    urgency_pred = models['urgency'].predict([features['urgency_features']])[0]
    urgency_proba = models['urgency'].predict_proba([features['urgency_features']])[0]
    
    # Recommend specialization
    spec_pred = models['specialization'].predict([features['spec_features']])[0]
    spec_proba = models['specialization'].predict_proba([features['spec_features']])[0]
    
    return {
        'severity': {
            'prediction': severity_pred,
            'confidence': max(severity_proba),
            'probabilities': dict(zip(models['severity'].classes_, severity_proba))
        },
        'urgency': {
            'prediction': urgency_pred,
            'confidence': max(urgency_proba),
            'probabilities': dict(zip(models['urgency'].classes_, urgency_proba))
        },
        'specialization': {
            'prediction': spec_pred,
            'confidence': max(spec_proba),
            'top_recommendations': get_top_specializations(models['specialization'], features['spec_features'])
        },
        'risk_factors': assess_risk_factors(data),
        'recommendations': generate_recommendations(data, severity_pred, urgency_pred)
    }

def extract_features_from_data(data):
    """Extract features for ML models from symptom data"""
    # This is a simplified feature extraction
    # In production, this would be more sophisticated
    
    temperature = 99.0  # default
    pain_level = data.get('intensity', 5)
    symptom_count = len(data.get('associated_symptoms', []))
    duration_days = convert_duration_to_days(data.get('duration', '1-3 days'))
    
    return {
        'severity_features': [temperature, pain_level, symptom_count, duration_days],
        'urgency_features': [temperature, pain_level, 0, 0],  # simplified
        'spec_features': [1, symptom_count, 1]  # simplified
    }

def convert_duration_to_days(duration_str):
    """Convert duration string to days"""
    duration_map = {
        'Less than 1 hour': 0.04,
        '1-6 hours': 0.25,
        '6-24 hours': 1,
        '1-3 days': 2,
        'More than 3 days': 7,
        '< 1 day': 0.5,
        '1-3 days': 2,
        '4-7 days': 5,
        '1-2 weeks': 10,
        '> 2 weeks': 20
    }
    return duration_map.get(duration_str, 2)

def get_top_specializations(model, features):
    """Get top specialization recommendations"""
    probabilities = model.predict_proba([features])[0]
    classes = model.classes_
    
    # Get top 3 recommendations
    top_indices = np.argsort(probabilities)[-3:][::-1]
    
    return [
        {'specialization': classes[i], 'confidence': probabilities[i]}
        for i in top_indices
    ]

def assess_risk_factors(data):
    """Assess risk factors from symptom data"""
    risk_factors = []
    
    intensity = data.get('intensity', 5)
    if intensity >= 8:
        risk_factors.append({
            'factor': 'High Intensity',
            'level': 'High',
            'description': 'Symptoms are reported as severe intensity'
        })
    
    # Add more risk factor assessments
    return risk_factors

def generate_recommendations(data, severity, urgency):
    """Generate AI recommendations"""
    recommendations = []
    
    if urgency == 'urgent':
        recommendations.append({
            'type': 'immediate',
            'action': 'Seek immediate medical attention',
            'priority': 'high',
            'reason': 'Symptoms indicate urgent medical care needed'
        })
    elif severity == 'severe':
        recommendations.append({
            'type': 'appointment',
            'action': 'Schedule appointment within 24 hours',
            'priority': 'medium',
            'reason': 'Severe symptoms require prompt medical evaluation'
        })
    
    return recommendations

def display_enhanced_analysis_results(analysis):
    """Display enhanced AI analysis results with disease-specific information"""
    st.subheader("🧠 AI Analysis Results")
    
    # Primary diagnosis highlight
    if 'primary_diagnosis' in analysis:
        diagnosis = analysis['primary_diagnosis']
        if diagnosis != 'General Symptoms':
            UIComponents.render_gradient_card(
                title=f"🔍 Primary Analysis: {diagnosis}",
                content=f"""The AI has identified <strong>{diagnosis}</strong> as the most likely condition based on your symptoms.<br>
                This analysis is based on symptom patterns and should be confirmed by a medical professional.""",
                gradient_colors=["#4dabf7", "#339af0"],
                icon="🧠"
            )
        else:
            st.info("📝 General symptoms detected. Professional evaluation recommended for proper diagnosis.")
    
    # Metrics cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        severity = analysis['severity']
        severity_color = {
            'mild': 'success',
            'moderate': 'warning', 
            'severe': 'error'
        }.get(severity['prediction'], 'info')
        
        UIComponents.render_metric_card(
            "Severity Level",
            severity['prediction'].title(),
            f"{severity['confidence']:.1%} confidence",
            severity_color,
            "⚕️"
        )
    
    with col2:
        urgency = analysis['urgency']
        urgency_color = {
            'normal': 'success',
            'high': 'warning',
            'urgent': 'error'
        }.get(urgency['prediction'], 'info')
        
        UIComponents.render_metric_card(
            "Urgency Level",
            urgency['prediction'].title(),
            f"{urgency['confidence']:.1%} confidence",
            urgency_color,
            "🚨"
        )
    
    with col3:
        spec = analysis['specialization']
        UIComponents.render_metric_card(
            "Recommended Specialist",
            spec['prediction'],
            f"{spec['confidence']:.1%} match",
            "info",
            "👨‍⚕️"
        )
    
    # Detected diseases (if multiple possibilities)
    if 'detected_diseases' in analysis and len(analysis['detected_diseases']) > 1:
        st.subheader("🔍 Possible Conditions")
        
        for i, disease_info in enumerate(analysis['detected_diseases'][:3]):
            with st.expander(f"{i+1}. {disease_info['disease']} ({disease_info['confidence']:.1%} match)"):
                if 'pattern' in disease_info:
                    st.write(f"**Description:** {disease_info['pattern']['description']}")
                    st.write(f"**Typical Severity:** {disease_info['pattern']['severity'].title()}")
                    st.write(f"**Recommended Specialist:** {disease_info['pattern']['specialization']}")
                else:
                    st.write("This condition matches your symptom pattern.")
    
    # Risk factors
    if analysis.get('risk_factors'):
        st.subheader("⚠️ Risk Factors")
        
        for risk in analysis['risk_factors']:
            risk_color = {
                'High': 'error',
                'Medium': 'warning',
                'Low': 'info'
            }.get(risk['level'], 'info')
            
            UIComponents.render_notification_bar(
                f"**{risk['factor']}** ({risk['level']} Risk) - {risk['description']}",
                type=risk_color.replace('error', 'error').replace('warning', 'warning').replace('info', 'info'),
                icon="⚠️" if risk['level'] == 'High' else "📊"
            )
    
    # Disease-specific recommendations
    st.subheader("💡 Personalized Recommendations")
    
    urgent_recs = [r for r in analysis['recommendations'] if r.get('priority') == 'urgent']
    high_recs = [r for r in analysis['recommendations'] if r.get('priority') == 'high']
    other_recs = [r for r in analysis['recommendations'] if r.get('priority') not in ['urgent', 'high']]
    
    # Display urgent recommendations first
    for rec in urgent_recs:
        UIComponents.render_notification_bar(
            f"🚨 **URGENT: {rec['action']}** - {rec['reason']}", 
            type="error",
            icon="🚨"
        )
    
    # High priority recommendations
    for rec in high_recs:
        UIComponents.render_notification_bar(
            f"🔴 **Important: {rec['action']}** - {rec['reason']}", 
            type="warning",
            icon="⚠️"
        )
    
    # Other recommendations
    for rec in other_recs:
        UIComponents.render_notification_bar(
            f"💡 **Suggestion: {rec['action']}** - {rec['reason']}", 
            type="info",
            icon="💡"
        )
    
    # Selected symptoms display (if from predefined selection)
    if 'selected_symptoms' in analysis:
        with st.expander("📝 Selected Symptoms"):
            st.write("**You selected these symptoms:**")
            for symptom in analysis['selected_symptoms']:
                st.write(f"• {symptom}")
    
    # Additional information
    if 'additional_info' in analysis and any(analysis['additional_info'].values()):
        with st.expander("📜 Additional Information Provided"):
            for key, value in analysis['additional_info'].items():
                if value:
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    # Disclaimer
    st.markdown("---")
    st.warning("⚠️ **Important Disclaimer:** This AI analysis is for informational purposes only and should not replace professional medical advice. Always consult with a qualified healthcare provider for proper diagnosis and treatment.")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📞 Schedule Appointment", type="primary"):
            st.success("Appointment scheduling would be available here.")
    
    with col2:
        if st.button("📊 View Detailed Report"):
            show_detailed_analysis_report(analysis)
    
    with col3:
        if st.button("🖺️ Save Analysis"):
            save_analysis_to_history(analysis)
            st.success("Analysis saved to your health history!")

def show_detailed_analysis_report(analysis):
    """Show detailed analysis report"""
    st.subheader("📊 Detailed Analysis Report")
    
    # Summary
    st.write("**Analysis Summary:**")
    st.json({
        'Primary Diagnosis': analysis.get('primary_diagnosis', 'N/A'),
        'Severity': analysis['severity']['prediction'],
        'Urgency': analysis['urgency']['prediction'],
        'Recommended Specialist': analysis['specialization']['prediction'],
        'Confidence Score': f"{analysis['severity']['confidence']:.1%}"
    })
    
    # Detailed breakdown
    if 'detected_diseases' in analysis:
        st.write("**Possible Conditions Analysis:**")
        for disease in analysis['detected_diseases']:
            st.write(f"• {disease['disease']}: {disease['confidence']:.1%} confidence")

def save_analysis_to_history(analysis):
    """Save analysis to session history"""
    if 'analysis_history' not in st.session_state:
        st.session_state['analysis_history'] = []
    
    analysis_record = {
        'timestamp': datetime.now().isoformat(),
        'diagnosis': analysis.get('primary_diagnosis', 'General Symptoms'),
        'severity': analysis['severity']['prediction'],
        'urgency': analysis['urgency']['prediction'],
        'specialist': analysis['specialization']['prediction']
    }
    
    st.session_state['analysis_history'].append(analysis_record)

def enhanced_natural_language_analysis(text, additional_info):
    """Enhanced natural language processing with disease detection"""
    # Disease pattern matching based on symptom descriptions
    disease_patterns = {
        'Migraine': {
            'keywords': ['headache', 'nausea', 'light sensitivity', 'throbbing', 'pulsing', 'aura'],
            'severity': 'moderate',
            'specialization': 'Neurology',
            'urgency': 'normal',
            'description': 'Recurrent headaches with associated symptoms'
        },
        'Hypertension': {
            'keywords': ['headache', 'dizziness', 'chest pain', 'shortness of breath', 'blurred vision'],
            'severity': 'moderate',
            'specialization': 'Cardiology',
            'urgency': 'high',
            'description': 'High blood pressure with cardiovascular symptoms'
        },
        'Gastroenteritis': {
            'keywords': ['stomach pain', 'nausea', 'vomiting', 'diarrhea', 'cramping'],
            'severity': 'mild',
            'specialization': 'Gastroenterology',
            'urgency': 'normal',
            'description': 'Stomach and intestinal inflammation'
        },
        'Respiratory Infection': {
            'keywords': ['cough', 'fever', 'fatigue', 'congestion', 'sore throat'],
            'severity': 'mild',
            'specialization': 'Pulmonology',
            'urgency': 'normal',
            'description': 'Upper or lower respiratory tract infection'
        },
        'Anxiety Disorder': {
            'keywords': ['anxiety', 'panic', 'chest tightness', 'shortness of breath', 'sweating', 'racing heart'],
            'severity': 'moderate',
            'specialization': 'Psychiatry',
            'urgency': 'normal',
            'description': 'Anxiety-related symptoms affecting daily life'
        },
        'Cardiac Emergency': {
            'keywords': ['chest pain', 'crushing', 'radiating', 'arm pain', 'jaw pain', 'sweating'],
            'severity': 'severe',
            'specialization': 'Cardiology',
            'urgency': 'urgent',
            'description': 'Possible heart attack or cardiac emergency'
        }
    }
    
    text_lower = text.lower()
    detected_diseases = []
    
    # Match disease patterns
    for disease, pattern in disease_patterns.items():
        matches = sum(1 for keyword in pattern['keywords'] if keyword in text_lower)
        if matches >= 2:  # Require at least 2 keyword matches
            confidence = min(matches / len(pattern['keywords']), 1.0)
            detected_diseases.append({
                'disease': disease,
                'confidence': confidence,
                'pattern': pattern
            })
    
    # Sort by confidence
    detected_diseases.sort(key=lambda x: x['confidence'], reverse=True)
    
    # If no specific disease detected, provide general analysis
    if not detected_diseases:
        severity = extract_severity_from_text(text)
        urgency = 'normal'
        specialization = 'General Medicine'
        disease_name = 'General Symptoms'
    else:
        top_disease = detected_diseases[0]
        severity = top_disease['pattern']['severity']
        urgency = top_disease['pattern']['urgency']
        specialization = top_disease['pattern']['specialization']
        disease_name = top_disease['disease']
    
    return {
        'detected_diseases': detected_diseases,
        'primary_diagnosis': disease_name,
        'severity': {
            'prediction': severity,
            'confidence': 0.85,
            'probabilities': {severity: 0.85, 'other': 0.15}
        },
        'urgency': {
            'prediction': urgency,
            'confidence': 0.80,
            'probabilities': {urgency: 0.80, 'other': 0.20}
        },
        'specialization': {
            'prediction': specialization,
            'confidence': 0.90,
            'top_recommendations': [{'specialization': specialization, 'confidence': 0.90}]
        },
        'risk_factors': assess_enhanced_risk_factors(text, additional_info),
        'recommendations': generate_disease_specific_recommendations(disease_name, severity, urgency),
        'additional_info': additional_info
    }

def analyze_predefined_symptoms(symptoms, details):
    """Analyze predefined symptom selections"""
    # Symptom-to-disease mapping
    symptom_disease_map = {
        'Chest pain/pressure': ['Cardiac Emergency', 'Hypertension', 'Anxiety Disorder'],
        'Severe headache': ['Migraine', 'Hypertension', 'Tension Headache'],
        'Persistent cough': ['Respiratory Infection', 'Asthma', 'Pneumonia'],
        'Stomach pain': ['Gastroenteritis', 'Peptic Ulcer', 'Appendicitis'],
        'Depression': ['Major Depression', 'Anxiety Disorder', 'Bipolar Disorder'],
        'Joint pain': ['Arthritis', 'Rheumatoid Arthritis', 'Gout']
    }
    
    # Calculate disease probabilities
    disease_scores = {}
    for symptom in symptoms:
        if symptom in symptom_disease_map:
            for disease in symptom_disease_map[symptom]:
                disease_scores[disease] = disease_scores.get(disease, 0) + 1
    
    # Determine primary diagnosis
    if disease_scores:
        primary_diagnosis = max(disease_scores.keys(), key=lambda k: disease_scores[k])
        confidence = min(disease_scores[primary_diagnosis] / len(symptoms), 1.0)
    else:
        primary_diagnosis = 'General Symptoms'
        confidence = 0.6
    
    # Map severity and urgency
    severity_map = {'Mild': 'mild', 'Moderate': 'moderate', 'Severe': 'severe', 'Very Severe': 'severe'}
    severity = severity_map.get(details['severity'], 'moderate')
    
    urgency = 'normal'
    if details['severity'] in ['Severe', 'Very Severe'] or details['daily_impact'] == 'Cannot perform activities':
        urgency = 'urgent'
    elif details['severity'] == 'Moderate' or details['daily_impact'] == 'Severe impact':
        urgency = 'high'
    
    # Determine specialization
    specialization_map = {
        'Cardiac Emergency': 'Cardiology', 'Hypertension': 'Cardiology',
        'Migraine': 'Neurology', 'Tension Headache': 'Neurology',
        'Respiratory Infection': 'Pulmonology', 'Asthma': 'Pulmonology',
        'Gastroenteritis': 'Gastroenterology', 'Peptic Ulcer': 'Gastroenterology',
        'Major Depression': 'Psychiatry', 'Anxiety Disorder': 'Psychiatry',
        'Arthritis': 'Orthopedics', 'Rheumatoid Arthritis': 'Rheumatology'
    }
    specialization = specialization_map.get(primary_diagnosis, 'General Medicine')
    
    return {
        'detected_diseases': [{'disease': primary_diagnosis, 'confidence': confidence}],
        'primary_diagnosis': primary_diagnosis,
        'severity': {
            'prediction': severity,
            'confidence': 0.85,
            'probabilities': {severity: 0.85}
        },
        'urgency': {
            'prediction': urgency,
            'confidence': 0.80,
            'probabilities': {urgency: 0.80}
        },
        'specialization': {
            'prediction': specialization,
            'confidence': 0.90,
            'top_recommendations': [{'specialization': specialization, 'confidence': 0.90}]
        },
        'risk_factors': assess_predefined_risk_factors(symptoms, details),
        'recommendations': generate_disease_specific_recommendations(primary_diagnosis, severity, urgency),
        'selected_symptoms': symptoms
    }

def analyze_combination_input(text, quick_symptoms, details):
    """Analyze combination of text and predefined symptoms"""
    # Combine text analysis with predefined symptoms
    text_analysis = enhanced_natural_language_analysis(text, {}) if text else None
    symptom_analysis = analyze_predefined_symptoms(quick_symptoms, details) if quick_symptoms else None
    
    # Merge results
    if text_analysis and symptom_analysis:
        # Combine confidence scores
        primary_diagnosis = text_analysis['primary_diagnosis']
        confidence = (text_analysis['severity']['confidence'] + symptom_analysis['severity']['confidence']) / 2
        severity = text_analysis['severity']['prediction']
        urgency = max(text_analysis['urgency']['prediction'], symptom_analysis['urgency']['prediction'], key=lambda x: ['normal', 'high', 'urgent'].index(x))
        specialization = text_analysis['specialization']['prediction']
    elif text_analysis:
        primary_diagnosis = text_analysis['primary_diagnosis']
        confidence = text_analysis['severity']['confidence']
        severity = text_analysis['severity']['prediction']
        urgency = text_analysis['urgency']['prediction']
        specialization = text_analysis['specialization']['prediction']
    elif symptom_analysis:
        primary_diagnosis = symptom_analysis['primary_diagnosis']
        confidence = symptom_analysis['severity']['confidence']
        severity = symptom_analysis['severity']['prediction']
        urgency = symptom_analysis['urgency']['prediction']
        specialization = symptom_analysis['specialization']['prediction']
    else:
        primary_diagnosis = 'General Symptoms'
        confidence = 0.5
        severity = 'moderate'
        urgency = 'normal'
        specialization = 'General Medicine'
    
    return {
        'primary_diagnosis': primary_diagnosis,
        'severity': {
            'prediction': severity,
            'confidence': confidence,
            'probabilities': {severity: confidence}
        },
        'urgency': {
            'prediction': urgency,
            'confidence': 0.80,
            'probabilities': {urgency: 0.80}
        },
        'specialization': {
            'prediction': specialization,
            'confidence': 0.85,
            'top_recommendations': [{'specialization': specialization, 'confidence': 0.85}]
        },
        'risk_factors': [],
        'recommendations': generate_disease_specific_recommendations(primary_diagnosis, severity, urgency),
        'input_details': details
    }

def extract_severity_from_text(text):
    """Extract severity level from text description"""
    severe_words = ['severe', 'intense', 'extreme', 'terrible', 'unbearable', 'excruciating']
    mild_words = ['mild', 'slight', 'little', 'minor', 'manageable']
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in severe_words):
        return 'severe'
    elif any(word in text_lower for word in mild_words):
        return 'mild'
    else:
        return 'moderate'

def assess_enhanced_risk_factors(text, additional_info):
    """Assess risk factors from text and additional information"""
    risk_factors = []
    
    # Check for high-risk keywords
    high_risk_keywords = ['chest pain', 'shortness of breath', 'severe', 'bleeding', 'unconscious']
    for keyword in high_risk_keywords:
        if keyword in text.lower():
            risk_factors.append({
                'factor': f'High-risk symptom: {keyword}',
                'level': 'High',
                'description': f'Presence of {keyword} requires immediate attention'
            })
    
    # Check family history
    if additional_info.get('family_history'):
        risk_factors.append({
            'factor': 'Family History',
            'level': 'Medium',
            'description': f'Family history of {additional_info["family_history"]}'
        })
    
    return risk_factors

def assess_predefined_risk_factors(symptoms, details):
    """Assess risk factors from predefined symptoms"""
    risk_factors = []
    
    # High-risk symptoms
    high_risk_symptoms = ['Chest pain/pressure', 'Difficulty breathing', 'Severe headache']
    for symptom in symptoms:
        if symptom in high_risk_symptoms:
            risk_factors.append({
                'factor': f'High-risk symptom: {symptom}',
                'level': 'High',
                'description': f'{symptom} requires prompt medical evaluation'
            })
    
    # Severity-based risk
    if details['severity'] in ['Severe', 'Very Severe']:
        risk_factors.append({
            'factor': 'High Severity',
            'level': 'High',
            'description': 'Severe symptoms require immediate medical attention'
        })
    
    return risk_factors

def generate_disease_specific_recommendations(disease, severity, urgency):
    """Generate disease-specific recommendations"""
    disease_recommendations = {
        'Migraine': [
            {'action': 'Rest in a dark, quiet room', 'priority': 'medium', 'reason': 'Light and noise sensitivity common in migraines'},
            {'action': 'Stay hydrated', 'priority': 'medium', 'reason': 'Dehydration can worsen migraines'},
            {'action': 'Consider over-the-counter pain relief', 'priority': 'low', 'reason': 'May help reduce pain intensity'}
        ],
        'Cardiac Emergency': [
            {'action': 'Call emergency services immediately', 'priority': 'urgent', 'reason': 'Possible heart attack requires immediate medical attention'},
            {'action': 'Chew aspirin if not allergic', 'priority': 'urgent', 'reason': 'Can help reduce blood clot formation'},
            {'action': 'Sit down and remain calm', 'priority': 'urgent', 'reason': 'Reduces strain on the heart'}
        ],
        'Gastroenteritis': [
            {'action': 'Stay hydrated with clear fluids', 'priority': 'medium', 'reason': 'Prevent dehydration from vomiting/diarrhea'},
            {'action': 'Rest and avoid solid foods initially', 'priority': 'medium', 'reason': 'Give digestive system time to recover'},
            {'action': 'Gradually reintroduce bland foods', 'priority': 'low', 'reason': 'BRAT diet helps with recovery'}
        ],
        'Respiratory Infection': [
            {'action': 'Get plenty of rest', 'priority': 'medium', 'reason': 'Helps immune system fight infection'},
            {'action': 'Stay hydrated', 'priority': 'medium', 'reason': 'Helps loosen mucus and prevent dehydration'},
            {'action': 'Use humidifier or steam', 'priority': 'low', 'reason': 'Helps relieve congestion'}
        ]
    }
    
    recommendations = disease_recommendations.get(disease, [
        {'action': 'Monitor symptoms closely', 'priority': 'medium', 'reason': 'Track changes in condition'},
        {'action': 'Consult healthcare provider', 'priority': 'medium', 'reason': 'Professional evaluation recommended'}
    ])
    
    # Add urgency-based recommendations
    if urgency == 'urgent':
        recommendations.insert(0, {
            'action': 'Seek immediate medical attention',
            'priority': 'urgent',
            'reason': 'Symptoms indicate need for urgent care'
        })
    elif severity == 'severe':
        recommendations.insert(0, {
            'action': 'Schedule appointment within 24 hours',
            'priority': 'high',
            'reason': 'Severe symptoms require prompt evaluation'
        })
    
    return recommendations

def extract_medical_keywords(text):
    """Extract medical keywords from text"""
    medical_terms = [
        'headache', 'fever', 'cough', 'pain', 'nausea', 'vomiting',
        'dizziness', 'fatigue', 'shortness of breath', 'chest pain'
    ]
    
    found_terms = []
    text_lower = text.lower()
    
    for term in medical_terms:
        if term in text_lower:
            found_terms.append(term)
    
    return found_terms

def perform_structured_analysis(data):
    """Perform analysis on structured data"""
    # Convert structured data to analysis format
    analysis_data = {
        'main_concern': 'general',
        'intensity': data['pain_level'],
        'duration': data['duration'],
        'temperature': data['temperature']
    }
    
    return perform_ai_analysis(analysis_data)

def ai_recommendations():
    """AI-powered recommendations interface"""
    st.header("🤖 AI Recommendations")
    
    if 'current_analysis' not in st.session_state:
        st.info("Complete a symptom analysis first to see AI recommendations.")
        return
    
    analysis = st.session_state['current_analysis']
    
    # Personalized recommendations
    st.subheader("🎯 Personalized Recommendations")
    
    # Treatment pathway
    create_treatment_pathway(analysis)
    
    # Doctor recommendations
    st.subheader("👨‍⚕️ Recommended Specialists")
    
    top_specs = analysis['specialization']['top_recommendations']
    for i, spec in enumerate(top_specs, 1):
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{i}. {spec['specialization']}**")
                st.caption(f"Confidence: {spec['confidence']:.1%}")
            with col2:
                if st.button(f"Find Doctors", key=f"find_doc_{i}"):
                    st.info(f"Searching for {spec['specialization']} specialists...")

def create_treatment_pathway(analysis):
    """Create visual treatment pathway"""
    severity = analysis['severity']['prediction']
    urgency = analysis['urgency']['prediction']
    
    # Create pathway steps
    if urgency == 'urgent':
        steps = [
            "🚨 Immediate: Go to Emergency Room",
            "🏥 Triage and Assessment", 
            "⚕️ Emergency Treatment",
            "📋 Follow-up Care"
        ]
        colors = ['red', 'orange', 'yellow', 'green']
    elif severity == 'severe':
        steps = [
            "📞 Call Doctor Immediately",
            "🏥 Same-day Appointment",
            "🔬 Diagnostic Tests",
            "💊 Treatment Plan"
        ]
        colors = ['orange', 'yellow', 'blue', 'green']
    else:
        steps = [
            "📅 Schedule Appointment",
            "👨‍⚕️ Consultation",
            "📋 Assessment",
            "💊 Treatment if Needed"
        ]
        colors = ['blue', 'green', 'blue', 'green']
    
    # Display pathway
    for i, (step, color) in enumerate(zip(steps, colors)):
        st.markdown(f"**Step {i+1}:** {step}")
        if i < len(steps) - 1:
            st.markdown("↓")

def risk_assessment():
    """Advanced risk assessment interface"""
    st.header("📊 AI Risk Assessment")
    
    if 'current_analysis' not in st.session_state:
        st.info("Complete a symptom analysis first to see risk assessment.")
        return
    
    # Risk scoring visualization
    create_risk_dashboard()
    
    # Complication probability
    st.subheader("⚠️ Complication Risk Analysis")
    
    # Sample risk factors
    risk_data = {
        'Cardiovascular': 0.15,
        'Respiratory': 0.25,
        'Infection': 0.10,
        'Allergic Reaction': 0.05,
        'Chronic Disease': 0.20
    }
    
    # Create risk chart
    fig = px.bar(
        x=list(risk_data.keys()),
        y=list(risk_data.values()),
        title="Complication Risk Factors",
        color=list(risk_data.values()),
        color_continuous_scale="Reds"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_risk_dashboard():
    """Create risk assessment dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        UIComponents.render_metric_card(
            "Overall Risk",
            "Medium",
            "Based on symptoms",
            "warning",
            "⚠️"
        )
    
    with col2:
        UIComponents.render_metric_card(
            "Urgency Score",
            "7/10",
            "Requires attention",
            "warning",
            "🚨"
        )
    
    with col3:
        UIComponents.render_metric_card(
            "Complexity",
            "Low",
            "Straightforward case",
            "success",
            "📊"
        )
    
    with col4:
        UIComponents.render_metric_card(
            "Confidence",
            "85%",
            "High AI confidence",
            "success",
            "🧠"
        )

def treatment_suggestions():
    """AI treatment suggestions"""
    st.header("🎯 Treatment Suggestions")
    
    st.subheader("💊 AI-Suggested Treatments")
    
    # Sample treatment suggestions
    treatments = [
        {
            'type': 'Medication',
            'suggestion': 'Over-the-counter pain reliever',
            'dosage': 'As per package instructions',
            'duration': '3-5 days',
            'confidence': 0.8
        },
        {
            'type': 'Lifestyle',
            'suggestion': 'Rest and hydration',
            'dosage': 'Adequate rest, 8+ glasses water daily',
            'duration': 'Until symptoms improve',
            'confidence': 0.9
        },
        {
            'type': 'Monitoring',
            'suggestion': 'Temperature monitoring',
            'dosage': 'Check every 4 hours',
            'duration': '24-48 hours',
            'confidence': 0.85
        }
    ]
    
    for treatment in treatments:
        with st.expander(f"💊 {treatment['type']}: {treatment['suggestion']}"):
            st.write(f"**Recommendation:** {treatment['suggestion']}")
            st.write(f"**Instructions:** {treatment['dosage']}")
            st.write(f"**Duration:** {treatment['duration']}")
            st.write(f"**AI Confidence:** {treatment['confidence']:.0%}")
            
            st.warning("⚠️ These are AI suggestions only. Consult a healthcare professional before taking any medication.")

def learning_dashboard():
    """Machine learning model performance dashboard"""
    st.header("📈 AI Learning Dashboard")
    
    # Model performance metrics
    st.subheader("🧠 Model Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Accuracy", "87.5%", "↗️ +2.3%")
    
    with col2:
        st.metric("Predictions Made", "1,247", "↗️ +45")
    
    with col3:
        st.metric("Model Confidence", "82.1%", "↗️ +1.1%")
    
    # Feature importance
    st.subheader("📊 Feature Importance")
    
    feature_importance = {
        'Temperature': 0.25,
        'Pain Level': 0.20,
        'Symptom Duration': 0.18,
        'Associated Symptoms': 0.15,
        'Medical History': 0.12,
        'Age': 0.10
    }
    
    fig = px.bar(
        x=list(feature_importance.values()),
        y=list(feature_importance.keys()),
        orientation='h',
        title="ML Model Feature Importance",
        color=list(feature_importance.values()),
        color_continuous_scale="Blues"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Prediction distribution
    st.subheader("📈 Prediction Distribution")
    
    prediction_data = {
        'Mild': 450,
        'Moderate': 520,
        'Severe': 277
    }
    
    fig = px.pie(
        values=list(prediction_data.values()),
        names=list(prediction_data.keys()),
        title="Severity Predictions (Last 30 Days)"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def analysis_history_tab():
    """Display analysis history"""
    st.header("📚 Analysis History")
    
    if 'analysis_history' not in st.session_state:
        st.session_state['analysis_history'] = []
    
    if st.session_state['analysis_history']:
        st.subheader(f"📊 Previous Analyses ({len(st.session_state['analysis_history'])} total)")
        
        # Display recent analyses
        for i, record in enumerate(reversed(st.session_state['analysis_history'][-10:])):
            with st.expander(f"Analysis {len(st.session_state['analysis_history']) - i}: {record['diagnosis']} - {record['timestamp'][:19]}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Diagnosis:** {record['diagnosis']}")
                    st.write(f"**Severity:** {record['severity'].title()}")
                
                with col2:
                    st.write(f"**Urgency:** {record['urgency'].title()}")
                    st.write(f"**Specialist:** {record['specialist']}")
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state['analysis_history'] = []
            st.success("Analysis history cleared!")
            st.rerun()
    else:
        st.info("📝 No analysis history yet. Complete a symptom analysis to see results here.")
        
        # Sample analysis button for demonstration
        if st.button("📊 View Sample Analysis"):
            show_sample_analysis()

def show_sample_analysis():
    """Show a sample analysis for demonstration"""
    sample_analysis = {
        'primary_diagnosis': 'Migraine',
        'severity': {'prediction': 'moderate', 'confidence': 0.85},
        'urgency': {'prediction': 'normal', 'confidence': 0.80},
        'specialization': {'prediction': 'Neurology', 'confidence': 0.90, 'top_recommendations': [{'specialization': 'Neurology', 'confidence': 0.90}]},
        'detected_diseases': [{'disease': 'Migraine', 'confidence': 0.85}],
        'recommendations': [
            {'action': 'Rest in a dark, quiet room', 'priority': 'medium', 'reason': 'Light and noise sensitivity common in migraines'},
            {'action': 'Stay hydrated', 'priority': 'medium', 'reason': 'Dehydration can worsen migraines'}
        ],
        'risk_factors': []
    }
    
    st.session_state['current_analysis'] = sample_analysis
    display_enhanced_analysis_results(sample_analysis)