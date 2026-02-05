import streamlit as st
from utils.auth import login_required

@login_required
def navigation_system():
    st.title("🗺️ Hospital Navigation System")
    
    tabs = st.tabs(["🏥 Indoor Map", "🚗 Directions", "📍 Find Services"])
    
    with tabs[0]:
        st.header("Hospital Floor Plan")
        floor = st.selectbox("Select Floor", ["Ground Floor", "1st Floor", "2nd Floor"])
        st.info(f"Interactive map for {floor} would be displayed here")
    
    with tabs[1]:
        st.header("Directions")
        destination = st.selectbox("Where do you want to go?", [
            "Emergency Room", "Cardiology", "Pharmacy", "Lab", "Cafeteria"
        ])
        if st.button("Get Directions"):
            st.success(f"Directions to {destination} generated!")
    
    with tabs[2]:
        st.header("Find Hospital Services")
        service = st.text_input("Search for services...")
        if service:
            st.info(f"Searching for: {service}")