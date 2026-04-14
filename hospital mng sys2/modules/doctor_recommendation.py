import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication
from utils.database import db
from utils.ui_components import create_metric_card, create_alert_box, create_progress_bar
from config.themes import get_theme_css

class AIDoctorRecommendationEngine:
    def __init__(self):
        self.specializations = [
            "Cardiology", "Neurology", "Orthopedics", "Dermatology",
            "Pediatrics", "Gynecology", "Psychiatry", "Oncology",
            "Endocrinology", "Gastroenterology", "Pulmonology", "Emergency Medicine"
        ]
        
        self.symptom_specialization_mapping = {
            "chest pain": ["Cardiology", "Emergency Medicine"],
            "headache": ["Neurology", "Emergency Medicine"],
            "joint pain": ["Orthopedics", "Rheumatology"],
            "skin rash": ["Dermatology"],
            "fever": ["Pediatrics", "Internal Medicine", "Emergency Medicine"],
            "depression": ["Psychiatry"],
            "diabetes": ["Endocrinology"],
            "stomach pain": ["Gastroenterology"],
            "shortness of breath": ["Pulmonology", "Cardiology", "Emergency Medicine"],
            "cancer": ["Oncology"]
        }
    
    def get_doctors_by_specialization(self, specialization):
        """Get doctors by specialization"""
        doctors = [doc for doc in db.doctors if doc['specialization'] == specialization]
        return doctors
    
    def recommend_doctors(self, symptoms, preferences=None):
        """Recommend doctors based on symptoms and preferences"""
        # Map symptoms to specializations
        recommended_specializations = set()
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for key, specs in self.symptom_specialization_mapping.items():
                if key in symptom_lower:
                    recommended_specializations.update(specs)
        
        # Get doctors for recommended specializations
        recommended_doctors = []
        
        for spec in recommended_specializations:
            doctors = self.get_doctors_by_specialization(spec)
            for doctor in doctors:
                # Calculate recommendation score
                score = self.calculate_recommendation_score(doctor, symptoms, preferences)
                doctor['recommendation_score'] = score
                recommended_doctors.append(doctor)
        
        # Sort by recommendation score
        recommended_doctors.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        return recommended_doctors
    
    def calculate_recommendation_score(self, doctor, symptoms, preferences=None):
        """Calculate recommendation score for a doctor"""
        score = 0
        
        # Base score from rating
        score += doctor.get('rating', 3.0) * 20
        
        # Experience bonus
        score += min(doctor.get('experience', 0) * 2, 20)
        
        # Availability bonus
        if doctor.get('status') == 'Available':
            score += 10
        
        # Specialization match bonus
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for key, specs in self.symptom_specialization_mapping.items():
                if key in symptom_lower and doctor['specialization'] in specs:
                    score += 15
                    break
        
        # Preferences bonus
        if preferences:
            if preferences.get('gender') and doctor.get('gender') == preferences['gender']:
                score += 5
            
            if preferences.get('language') and doctor.get('language') == preferences['language']:
                score += 10
        
        return score
    
    def get_doctor_details(self, doctor_id):
        """Get detailed information about a doctor"""
        doctor = next((doc for doc in db.doctors if doc['id'] == doctor_id), None)
        
        if doctor:
            # Add additional details
            doctor['education'] = [
                "MBBS - Medical College",
                "MD - Specialization",
                "Fellowship - Advanced Training"
            ]
            
            doctor['certifications'] = [
                "Board Certified",
                "State Medical License",
                "Specialty Certification"
            ]
            
            doctor['languages'] = ["English", "Hindi", "Spanish"]
            
            doctor['availability'] = {
                "Monday": "9:00 AM - 5:00 PM",
                "Tuesday": "9:00 AM - 5:00 PM",
                "Wednesday": "9:00 AM - 5:00 PM",
                "Thursday": "9:00 AM - 5:00 PM",
                "Friday": "9:00 AM - 5:00 PM",
                "Saturday": "9:00 AM - 1:00 PM",
                "Sunday": "Closed"
            }
        
        return doctor
    
    def get_similar_doctors(self, doctor_id):
        """Get similar doctors based on specialization and rating"""
        target_doctor = next((doc for doc in db.doctors if doc['id'] == doctor_id), None)
        
        if not target_doctor:
            return []
        
        similar_doctors = []
        
        for doctor in db.doctors:
            if doctor['id'] != doctor_id:
                similarity_score = 0
                
                # Same specialization
                if doctor['specialization'] == target_doctor['specialization']:
                    similarity_score += 50
                
                # Similar rating
                rating_diff = abs(doctor.get('rating', 0) - target_doctor.get('rating', 0))
                if rating_diff <= 0.5:
                    similarity_score += 30
                
                # Similar experience
                exp_diff = abs(doctor.get('experience', 0) - target_doctor.get('experience', 0))
                if exp_diff <= 2:
                    similarity_score += 20
                
                if similarity_score > 0:
                    doctor['similarity_score'] = similarity_score
                    similar_doctors.append(doctor)
        
        # Sort by similarity score
        similar_doctors.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similar_doctors[:3]  # Return top 3 similar doctors

def main():
    """Main function for AI Doctor Recommendation Engine module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the AI Doctor Recommendation Engine")
        return
    
    # Initialize recommendation engine
    recommendation_engine = AIDoctorRecommendationEngine()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">🤖 AI Doctor Recommendation Engine</h1>
        <p class="body-text">Find the perfect doctor based on your symptoms and preferences</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Find Doctor", "📊 Doctor Details", "🎯 Similar Doctors", "📈 Analytics"
    ])
    
    with tab1:
        st.markdown("### 🔍 Find Your Perfect Doctor")
        
        # Symptom input
        st.markdown("#### 🩺 Describe Your Symptoms")
        
        symptoms_input = st.text_area(
            "Enter your symptoms (separate with commas):",
            placeholder="e.g., chest pain, shortness of breath, fever"
        )
        
        # Preferences
        st.markdown("#### ⚙️ Preferences (Optional)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            preferred_gender = st.selectbox("Preferred Gender", ["Any", "Male", "Female"])
            preferred_language = st.selectbox("Preferred Language", ["Any", "English", "Hindi", "Spanish"])
        
        with col2:
            max_distance = st.slider("Maximum Distance (km)", 1, 50, 10)
            availability = st.selectbox("Availability", ["Any", "Today", "This Week", "Next Week"])
        
        # Find doctors
        if st.button("🔍 Find Doctors"):
            if symptoms_input:
                symptoms = [s.strip() for s in symptoms_input.split(',') if s.strip()]
                
                preferences = {
                    'gender': preferred_gender if preferred_gender != "Any" else None,
                    'language': preferred_language if preferred_language != "Any" else None,
                    'max_distance': max_distance,
                    'availability': availability
                }
                
                # Get recommendations
                recommended_doctors = recommendation_engine.recommend_doctors(symptoms, preferences)
                
                if recommended_doctors:
                    st.success(f"✅ Found {len(recommended_doctors)} doctors matching your criteria!")
                    
                    # Display recommendations
                    st.markdown("#### 🏆 Top Recommendations")
                    
                    for i, doctor in enumerate(recommended_doctors[:5], 1):
                        with st.expander(f"🥇 {i}. Dr. {doctor['name']} - {doctor['specialization']}"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.markdown(f"**Specialization:** {doctor['specialization']}")
                                st.markdown(f"**Experience:** {doctor['experience']} years")
                                st.markdown(f"**Rating:** ⭐ {doctor.get('rating', 'N/A')}")
                                st.markdown(f"**Status:** {doctor.get('status', 'Unknown')}")
                            
                            with col2:
                                create_progress_bar(
                                    doctor['recommendation_score'], 
                                    100, 
                                    f"Match: {doctor['recommendation_score']:.0f}%"
                                )
                            
                            # Action buttons
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                if st.button(f"📋 View Details", key=f"details_{doctor['id']}"):
                                    st.session_state.selected_doctor = doctor['id']
                            
                            with col2:
                                if st.button(f"📅 Book Appointment", key=f"book_{doctor['id']}"):
                                    st.success(f"✅ Redirecting to appointment booking for Dr. {doctor['name']}")
                            
                            with col3:
                                if st.button(f"📞 Contact", key=f"contact_{doctor['id']}"):
                                    st.info(f"📞 Contacting Dr. {doctor['name']}...")
                else:
                    st.warning("⚠️ No doctors found matching your criteria. Try adjusting your symptoms or preferences.")
            else:
                st.warning("⚠️ Please enter your symptoms to find doctors.")
        
        # Quick symptom search
        st.markdown("#### 🚀 Quick Symptom Search")
        
        common_symptoms = [
            "Chest Pain", "Headache", "Fever", "Joint Pain",
            "Skin Rash", "Depression", "Diabetes", "Stomach Pain"
        ]
        
        cols = st.columns(4)
        for i, symptom in enumerate(common_symptoms):
            with cols[i % 4]:
                if st.button(f"🔍 {symptom}", key=f"quick_{symptom}"):
                    st.session_state.quick_symptom = symptom
                    st.rerun()
    
    with tab2:
        st.markdown("### 📊 Doctor Details")
        
        # Doctor selection
        doctors = db.doctors
        if not doctors:
            st.error("No doctors found in the system")
            return
        
        doctor_names = [f"Dr. {d['name']} - {d['specialization']}" for d in doctors]
        selected_doctor_name = st.selectbox("Select Doctor", doctor_names)
        
        if selected_doctor_name:
            doctor_name = selected_doctor_name.split(" - ")[0].replace("Dr. ", "")
            doctor = next((d for d in doctors if d['name'] == doctor_name), None)
            
            if doctor:
                doctor_id = doctor['id']
                doctor_details = recommendation_engine.get_doctor_details(doctor_id)
                
                # Doctor overview
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    create_metric_card("Specialization", doctor_details['specialization'], "🏥")
                    create_metric_card("Experience", f"{doctor_details['experience']} years", "📅")
                
                with col2:
                    create_metric_card("Rating", f"⭐ {doctor_details.get('rating', 'N/A')}", "⭐")
                    create_metric_card("Status", doctor_details.get('status', 'Unknown'), "🟢")
                
                with col3:
                    create_metric_card("Languages", len(doctor_details.get('languages', [])), "🗣️")
                    create_metric_card("Certifications", len(doctor_details.get('certifications', [])), "📜")
                
                # Detailed information
                st.markdown("#### 📋 Detailed Information")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Education:**")
                    for education in doctor_details.get('education', []):
                        st.markdown(f"• {education}")
                    
                    st.markdown("**Certifications:**")
                    for cert in doctor_details.get('certifications', []):
                        st.markdown(f"• {cert}")
                
                with col2:
                    st.markdown("**Languages:**")
                    for lang in doctor_details.get('languages', []):
                        st.markdown(f"• {lang}")
                    
                    st.markdown("**Contact:**")
                    st.markdown(f"• Phone: {doctor_details.get('phone', 'N/A')}")
                    st.markdown(f"• Email: {doctor_details.get('email', 'N/A')}")
                
                # Availability schedule
                st.markdown("#### 📅 Availability Schedule")
                
                availability = doctor_details.get('availability', {})
                if availability:
                    availability_data = []
                    for day, time in availability.items():
                        availability_data.append([day, time])
                    
                    availability_df = pd.DataFrame(availability_data, columns=["Day", "Hours"])
                    st.dataframe(availability_df, use_container_width=True)
                
                # Action buttons
                st.markdown("#### 🔧 Actions")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("📅 Book Appointment"):
                        st.success("✅ Redirecting to appointment booking...")
                
                with col2:
                    if st.button("📞 Contact Doctor"):
                        st.info("📞 Initiating contact...")
                
                with col3:
                    if st.button("📋 View Reviews"):
                        st.info("📋 Loading reviews...")
                
                with col4:
                    if st.button("📊 View Similar Doctors"):
                        st.session_state.show_similar = True
                        st.rerun()
    
    with tab3:
        st.markdown("### 🎯 Similar Doctors")
        
        # Doctor selection for similar doctors
        doctors = db.doctors
        if not doctors:
            st.error("No doctors found in the system")
            return
        
        doctor_names = [f"Dr. {d['name']} - {d['specialization']}" for d in doctors]
        selected_doctor_name = st.selectbox("Select Doctor to Find Similar", doctor_names, key="similar_doctor")
        
        if selected_doctor_name:
            doctor_name = selected_doctor_name.split(" - ")[0].replace("Dr. ", "")
            doctor = next((d for d in doctors if d['name'] == doctor_name), None)
            
            if doctor:
                similar_doctors = recommendation_engine.get_similar_doctors(doctor['id'])
                
                if similar_doctors:
                    st.markdown(f"#### 👥 Similar to Dr. {doctor['name']}")
                    
                    for i, similar_doctor in enumerate(similar_doctors, 1):
                        with st.expander(f"🥈 {i}. Dr. {similar_doctor['name']} - {similar_doctor['specialization']}"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.markdown(f"**Specialization:** {similar_doctor['specialization']}")
                                st.markdown(f"**Experience:** {similar_doctor['experience']} years")
                                st.markdown(f"**Rating:** ⭐ {similar_doctor.get('rating', 'N/A')}")
                                st.markdown(f"**Status:** {similar_doctor.get('status', 'Unknown')}")
                            
                            with col2:
                                create_progress_bar(
                                    similar_doctor['similarity_score'], 
                                    100, 
                                    f"Similarity: {similar_doctor['similarity_score']:.0f}%"
                                )
                            
                            # Action buttons
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                if st.button(f"📋 View Details", key=f"sim_details_{similar_doctor['id']}"):
                                    st.session_state.selected_doctor = similar_doctor['id']
                            
                            with col2:
                                if st.button(f"📅 Book Appointment", key=f"sim_book_{similar_doctor['id']}"):
                                    st.success(f"✅ Redirecting to appointment booking for Dr. {similar_doctor['name']}")
                            
                            with col3:
                                if st.button(f"📞 Contact", key=f"sim_contact_{similar_doctor['id']}"):
                                    st.info(f"📞 Contacting Dr. {similar_doctor['name']}...")
                else:
                    st.info("📋 No similar doctors found.")
    
    with tab4:
        st.markdown("### 📈 Recommendation Analytics")
        
        # Analytics overview
        st.markdown("#### 📊 System Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            create_metric_card("Total Doctors", len(db.doctors), "👨‍⚕️")
        
        with col2:
            specializations = len(set(doc['specialization'] for doc in db.doctors))
            create_metric_card("Specializations", specializations, "🏥")
        
        with col3:
            avg_rating = np.mean([doc.get('rating', 0) for doc in db.doctors])
            create_metric_card("Avg. Rating", f"{avg_rating:.1f}", "⭐")
        
        with col4:
            available_doctors = len([doc for doc in db.doctors if doc.get('status') == 'Available'])
            create_metric_card("Available", available_doctors, "🟢")
        
        # Specialization distribution
        st.markdown("#### 🏥 Doctors by Specialization")
        
        spec_counts = {}
        for doc in db.doctors:
            spec = doc['specialization']
            spec_counts[spec] = spec_counts.get(spec, 0) + 1
        
        if spec_counts:
            spec_data = []
            for spec, count in spec_counts.items():
                spec_data.append([spec, count])
            
            spec_df = pd.DataFrame(spec_data, columns=["Specialization", "Count"])
            st.dataframe(spec_df, use_container_width=True)
        
        # Top rated doctors
        st.markdown("#### ⭐ Top Rated Doctors")
        
        top_doctors = sorted(db.doctors, key=lambda x: x.get('rating', 0), reverse=True)[:5]
        
        for i, doctor in enumerate(top_doctors, 1):
            st.markdown(f"**{i}.** Dr. {doctor['name']} - {doctor['specialization']} (⭐ {doctor.get('rating', 'N/A')})")

if __name__ == "__main__":
    main()
