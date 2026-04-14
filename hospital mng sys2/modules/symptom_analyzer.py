import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication
from utils.ui_components import create_body_map, create_alert_box, create_metric_card
from utils.voice_utils import VoiceAssistant, create_voice_input_widget
from utils.image_utils import create_disease_image_display, create_image_url_input
from config.themes import get_theme_css

class SymptomAnalyzer:
    def __init__(self):
        self.symptoms_data = self.load_symptoms_data()
        self.diseases_data = self.load_diseases_data()
        self.model = self.train_model()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
    def load_symptoms_data(self):
        """Load symptoms and disease mapping data"""
        return {
            "fever": ["Common Cold", "Flu", "COVID-19", "Malaria", "Dengue"],
            "headache": ["Migraine", "Tension Headache", "Sinusitis", "Hypertension"],
            "cough": ["Common Cold", "Bronchitis", "Pneumonia", "COVID-19", "Asthma"],
            "fatigue": ["Anemia", "Depression", "Chronic Fatigue Syndrome", "Diabetes"],
            "nausea": ["Food Poisoning", "Gastritis", "Migraine", "Pregnancy"],
            "chest_pain": ["Angina", "Heart Attack", "Pneumonia", "Anxiety"],
            "abdominal_pain": ["Appendicitis", "Gastritis", "Food Poisoning", "Ulcer"],
            "shortness_of_breath": ["Asthma", "Pneumonia", "Anxiety", "Heart Failure"],
            "dizziness": ["Vertigo", "Anemia", "Low Blood Pressure", "Dehydration"],
            "joint_pain": ["Arthritis", "Lupus", "Fibromyalgia", "Injury"]
        }
    
    def load_diseases_data(self):
        """Load detailed disease information"""
        return {
            "Common Cold": {
                "description": "Viral infection of the upper respiratory tract",
                "severity": "Mild",
                "treatment": "Rest, fluids, over-the-counter medications",
                "image_url": None,
                "hindi_name": "सर्दी जुकाम",
                "hindi_description": "ऊपरी श्वसन पथ का वायरल संक्रमण"
            },
            "Flu": {
                "description": "Influenza virus infection affecting respiratory system",
                "severity": "Moderate",
                "treatment": "Rest, fluids, antiviral medications if severe",
                "image_url": None,
                "hindi_name": "फ्लू",
                "hindi_description": "श्वसन प्रणाली को प्रभावित करने वाला इन्फ्लूएंजा वायरस संक्रमण"
            },
            "COVID-19": {
                "description": "Coronavirus disease caused by SARS-CoV-2",
                "severity": "Variable",
                "treatment": "Rest, isolation, medical care if severe",
                "image_url": None,
                "hindi_name": "कोविड-19",
                "hindi_description": "SARS-CoV-2 के कारण होने वाला कोरोनावायरस रोग"
            },
            "Diabetes": {
                "description": "Metabolic disorder affecting blood sugar regulation",
                "severity": "Chronic",
                "treatment": "Diet, exercise, medication, insulin if needed",
                "image_url": None,
                "hindi_name": "मधुमेह",
                "hindi_description": "रक्त शर्करा विनियमन को प्रभावित करने वाला चयापचय विकार"
            },
            "Hypertension": {
                "description": "High blood pressure affecting cardiovascular system",
                "severity": "Chronic",
                "treatment": "Lifestyle changes, medication, regular monitoring",
                "image_url": None,
                "hindi_name": "उच्च रक्तचाप",
                "hindi_description": "हृदय प्रणाली को प्रभावित करने वाला उच्च रक्तचाप"
            }
        }
    
    def train_model(self):
        """Train a simple ML model for symptom analysis"""
        # Create training data
        symptoms = []
        diseases = []
        
        for symptom, disease_list in self.symptoms_data.items():
            for disease in disease_list:
                symptoms.append(symptom)
                diseases.append(disease)
        
        # Create feature matrix
        symptom_features = pd.get_dummies(symptoms)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(symptom_features, diseases)
        
        return model
    
    def analyze_symptoms(self, selected_symptoms, body_areas=None):
        """Analyze symptoms and predict possible conditions"""
        if not selected_symptoms:
            return []
        
        # Create feature vector
        all_symptoms = list(self.symptoms_data.keys())
        feature_vector = [1 if symptom in selected_symptoms else 0 for symptom in all_symptoms]
        
        # Get predictions
        predictions = self.model.predict_proba([feature_vector])[0]
        disease_names = self.model.classes_
        
        # Create results with confidence scores
        results = []
        for disease, confidence in zip(disease_names, predictions):
            if confidence > 0.1:  # Only show diseases with >10% confidence
                results.append({
                    "disease": disease,
                    "confidence": confidence,
                    "severity": self.diseases_data.get(disease, {}).get("severity", "Unknown"),
                    "description": self.diseases_data.get(disease, {}).get("description", "No description available")
                })
        
        # Sort by confidence
        results.sort(key=lambda x: x["confidence"], reverse=True)
        return results[:5]  # Return top 5 predictions

def main():
    """Main function for AI Symptom Analyzer module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the Symptom Analyzer")
        return
    
    # Initialize symptom analyzer
    analyzer = SymptomAnalyzer()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">🤖 AI Symptom Analyzer</h1>
        <p class="body-text">Advanced AI-powered symptom analysis and disease prediction</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language selection
    language = st.session_state.get('language', 'English')
    
    # Voice assistant
    voice_assistant = VoiceAssistant()
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Symptom Input")
        
        # Symptom selection methods
        input_method = st.selectbox(
            "Choose Input Method",
            ["Manual Selection", "Voice Input", "Body Map Selection"],
            key="symptom_input_method"
        )
        
        selected_symptoms = []
        body_areas = []
        
        if input_method == "Manual Selection":
            selected_symptoms = manual_symptom_selection(analyzer, language)
        elif input_method == "Voice Input":
            selected_symptoms = voice_symptom_input(voice_assistant, language)
        else:
            selected_symptoms, body_areas = body_map_selection(analyzer, language)
        
        # Analyze symptoms
        if selected_symptoms:
            st.markdown("### 🔍 Analysis Results")
            
            # Show selected symptoms
            st.markdown(f"**Selected Symptoms:** {', '.join(selected_symptoms)}")
            
            # Get predictions
            predictions = analyzer.analyze_symptoms(selected_symptoms, body_areas)
            
            if predictions:
                display_predictions(predictions, language)
            else:
                st.warning("⚠️ No specific conditions found. Please consult a healthcare professional.")
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        
        create_metric_card("Symptoms Analyzed", len(selected_symptoms) if selected_symptoms else 0)
        create_metric_card("Conditions Found", len(predictions) if 'predictions' in locals() else 0)
        create_metric_card("Confidence Level", f"{predictions[0]['confidence']*100:.1f}%" if 'predictions' in locals() and predictions else "N/A")
        
        # Voice commands
        st.markdown("### 🎤 Voice Commands")
        
        if st.button("🎤 Start Analysis"):
            voice_assistant.speak("Please describe your symptoms for AI analysis.")
        
        if st.button("🔊 Explain Results"):
            if 'predictions' in locals() and predictions:
                explanation = f"Based on your symptoms, the most likely condition is {predictions[0]['disease']} with {predictions[0]['confidence']*100:.1f}% confidence."
                voice_assistant.speak(explanation)
    
    # Disease image integration
    if 'predictions' in locals() and predictions:
        st.markdown("### 🖼️ Disease Visualizations")
        
        # Allow user to add custom image URLs
        st.markdown("#### Add Custom Disease Images")
        
        for prediction in predictions[:3]:  # Show top 3 predictions
            disease_name = prediction['disease']
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"**{disease_name}**")
                st.write(f"Confidence: {prediction['confidence']*100:.1f}%")
                st.write(f"Severity: {prediction['severity']}")
            
            with col2:
                image_url = create_image_url_input(
                    f"Image URL for {disease_name}",
                    key=f"image_url_{disease_name.lower().replace(' ', '_')}"
                )
                
                if image_url:
                    create_disease_image_display(disease_name, image_url)
                else:
                    create_disease_image_display(disease_name)

def manual_symptom_selection(analyzer, language):
    """Manual symptom selection interface"""
    st.markdown("#### Select Your Symptoms")
    
    # Get available symptoms
    available_symptoms = list(analyzer.symptoms_data.keys())
    
    # Create symptom selection
    selected_symptoms = st.multiselect(
        "Choose symptoms that apply to you:",
        available_symptoms,
        help="Select all symptoms you are experiencing"
    )
    
    # Additional symptom input
    additional_symptoms = st.text_area(
        "Additional symptoms (describe in your own words):",
        help="Describe any other symptoms not listed above"
    )
    
    if additional_symptoms:
        # Simple keyword matching for additional symptoms
        additional_list = [s.strip() for s in additional_symptoms.split(',')]
        selected_symptoms.extend(additional_list)
    
    return selected_symptoms

def voice_symptom_input(voice_assistant, language):
    """Voice-based symptom input"""
    st.markdown("#### 🎤 Voice Symptom Input")
    
    if st.button("🎤 Start Voice Recording"):
        st.info("🎤 Please describe your symptoms clearly...")
        
        # Simulate voice input processing
        import time
        time.sleep(2)
        
        # For demo, use predefined symptoms
        demo_symptoms = ["fever", "headache", "fatigue"]
        st.success(f"✅ Recognized symptoms: {', '.join(demo_symptoms)}")
        
        return demo_symptoms
    
    # Fallback text input
    voice_text = st.text_area(
        "Or type your symptoms here:",
        placeholder="Describe your symptoms in detail..."
    )
    
    if voice_text:
        # Simple keyword extraction
        symptoms = [s.strip() for s in voice_text.split(',')]
        return symptoms
    
    return []

def body_map_selection(analyzer, language):
    """Interactive body map symptom selection"""
    st.markdown("#### 🗺️ Body Map Selection")
    
    # Create body map
    create_body_map()
    
    # Body area selection
    body_areas = st.multiselect(
        "Select affected body areas:",
        ["Head", "Chest", "Abdomen", "Arms", "Legs", "Back"],
        help="Select areas where you're experiencing symptoms"
    )
    
    # Symptom selection based on body areas
    selected_symptoms = []
    
    if "Head" in body_areas:
        head_symptoms = st.multiselect(
            "Head symptoms:",
            ["headache", "dizziness", "fever"]
        )
        selected_symptoms.extend(head_symptoms)
    
    if "Chest" in body_areas:
        chest_symptoms = st.multiselect(
            "Chest symptoms:",
            ["chest_pain", "shortness_of_breath", "cough"]
        )
        selected_symptoms.extend(chest_symptoms)
    
    if "Abdomen" in body_areas:
        abdomen_symptoms = st.multiselect(
            "Abdomen symptoms:",
            ["abdominal_pain", "nausea", "fatigue"]
        )
        selected_symptoms.extend(abdomen_symptoms)
    
    return selected_symptoms, body_areas

def display_predictions(predictions, language):
    """Display AI predictions with confidence scores"""
    st.markdown("#### 🤖 AI Analysis Results")
    
    for i, prediction in enumerate(predictions):
        disease_name = prediction['disease']
        confidence = prediction['confidence']
        severity = prediction['severity']
        description = prediction['description']
        
        # Get disease info
        disease_info = analyzer.diseases_data.get(disease_name, {})
        
        # Create prediction card
        with st.expander(f"🏥 {disease_name} ({confidence*100:.1f}% confidence)"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {description}")
                st.markdown(f"**Severity:** {severity}")
                
                if language == "Hindi" and disease_info.get("hindi_description"):
                    st.markdown(f"**हिंदी विवरण:** {disease_info['hindi_description']}")
                
                # Treatment recommendations
                treatment = disease_info.get("treatment", "Consult a healthcare professional")
                st.markdown(f"**Recommended Treatment:** {treatment}")
            
            with col2:
                # Confidence visualization
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=confidence * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Confidence"},
                    delta={'reference': 50},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgray"},
                            {'range': [30, 70], 'color': "gray"},
                            {'range': [70, 100], 'color': "darkgray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                
                fig.update_layout(height=200)
                st.plotly_chart(fig, use_container_width=True)
        
        # Severity alert
        if severity in ["Severe", "Critical"]:
            create_alert_box(
                f"⚠️ {disease_name} is classified as {severity}. Please seek immediate medical attention.",
                "error"
            )

if __name__ == "__main__":
    main()
