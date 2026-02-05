import streamlit as st
import pandas as pd
from utils.auth import login_required

@login_required
def doctor_recommendation():
    st.title("👨‍⚕️ Doctor Recommendation System")
    
    st.header("Find the Right Doctor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        specialty = st.selectbox("Specialty", [
            "General Medicine", "Cardiology", "Neurology", "Orthopedics"
        ])
        location = st.text_input("Preferred Location")
        language = st.selectbox("Language", ["English", "Spanish", "Hindi"])
    
    with col2:
        availability = st.selectbox("Availability", [
            "Any time", "Morning", "Afternoon", "Evening"
        ])
        experience = st.slider("Minimum Experience (years)", 0, 30, 5)
        rating = st.slider("Minimum Rating", 1.0, 5.0, 4.0)
    
    if st.button("Find Doctors"):
        st.subheader("Recommended Doctors")
        doctors = pd.DataFrame({
            'Name': ['Dr. Smith', 'Dr. Johnson', 'Dr. Brown'],
            'Specialty': [specialty] * 3,
            'Experience': [10, 15, 8],
            'Rating': [4.8, 4.6, 4.7],
            'Available': ['Today', 'Tomorrow', 'Today']
        })
        
        for idx, doctor in doctors.iterrows():
            with st.expander(f"{doctor['Name']} - {doctor['Specialty']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Experience: {doctor['Experience']} years")
                    st.write(f"Rating: {doctor['Rating']}/5.0")
                with col2:
                    st.write(f"Available: {doctor['Available']}")
                    if st.button(f"Book with {doctor['Name']}", key=f"book_{idx}"):
                        st.success(f"Booking appointment with {doctor['Name']}")