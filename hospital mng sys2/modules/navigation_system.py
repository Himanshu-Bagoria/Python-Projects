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
from utils.ui_components import create_metric_card, create_alert_box
from config.themes import get_theme_css

class SmartNavigationSystem:
    def __init__(self):
        self.hospital_floors = {
            "Ground Floor": {
                "Emergency": "Room 101-110",
                "Reception": "Room 001-005",
                "Pharmacy": "Room 201-205",
                "Cafeteria": "Room 301-305",
                "Security": "Room 401-405"
            },
            "First Floor": {
                "Cardiology": "Room 501-520",
                "Radiology": "Room 521-540",
                "Laboratory": "Room 541-560",
                "Admin": "Room 561-580"
            },
            "Second Floor": {
                "General Ward": "Room 601-650",
                "ICU": "Room 651-670",
                "Operation Theater": "Room 671-690",
                "Recovery": "Room 691-710"
            },
            "Third Floor": {
                "Pediatrics": "Room 711-730",
                "Maternity": "Room 731-750",
                "Neonatal": "Room 751-760",
                "Gynecology": "Room 761-780"
            }
        }
        
        self.doctors_locations = {
            "Dr. Smith": {"floor": "First Floor", "department": "Cardiology", "room": "Room 501"},
            "Dr. Johnson": {"floor": "Second Floor", "department": "ICU", "room": "Room 651"},
            "Dr. Williams": {"floor": "Third Floor", "department": "Pediatrics", "room": "Room 711"},
            "Dr. Brown": {"floor": "Ground Floor", "department": "Emergency", "room": "Room 101"},
            "Dr. Davis": {"floor": "First Floor", "department": "Radiology", "room": "Room 521"}
        }
        
        self.patients_locations = {
            "patient_001": {"floor": "Second Floor", "ward": "General Ward", "room": "Room 601"},
            "patient_002": {"floor": "Third Floor", "ward": "Pediatrics", "room": "Room 711"},
            "patient_003": {"floor": "Second Floor", "ward": "ICU", "room": "Room 651"}
        }
    
    def find_location(self, search_term):
        """Find location of department, doctor, or patient"""
        results = []
        
        # Search in departments
        for floor, departments in self.hospital_floors.items():
            for dept, rooms in departments.items():
                if search_term.lower() in dept.lower():
                    results.append({
                        'type': 'Department',
                        'name': dept,
                        'floor': floor,
                        'location': rooms
                    })
        
        # Search in doctors
        for doctor, location in self.doctors_locations.items():
            if search_term.lower() in doctor.lower():
                results.append({
                    'type': 'Doctor',
                    'name': doctor,
                    'floor': location['floor'],
                    'location': location['room']
                })
        
        # Search in patients
        for patient_id, location in self.patients_locations.items():
            if search_term.lower() in patient_id.lower():
                results.append({
                    'type': 'Patient',
                    'name': patient_id,
                    'floor': location['floor'],
                    'location': location['room']
                })
        
        return results
    
    def get_route(self, from_location, to_location):
        """Get route between two locations"""
        # Simple route calculation
        routes = {
            "Ground Floor": 0,
            "First Floor": 1,
            "Second Floor": 2,
            "Third Floor": 3
        }
        
        from_floor = from_location.get('floor', 'Ground Floor')
        to_floor = to_location.get('floor', 'Ground Floor')
        
        floor_diff = abs(routes.get(from_floor, 0) - routes.get(to_floor, 0))
        
        route_steps = []
        
        if floor_diff > 0:
            route_steps.append(f"Take elevator/stairs to {to_floor}")
        
        route_steps.append(f"Go to {to_location.get('location', 'destination')}")
        
        return {
            'steps': route_steps,
            'estimated_time': floor_diff * 2 + 3,  # 2 min per floor + 3 min walking
            'distance': floor_diff * 50 + 100  # 50m per floor + 100m walking
        }
    
    def get_floor_map(self, floor_name):
        """Get floor map layout"""
        if floor_name in self.hospital_floors:
            return self.hospital_floors[floor_name]
        return {}
    
    def get_emergency_exit_routes(self, current_location):
        """Get emergency exit routes"""
        current_floor = current_location.get('floor', 'Ground Floor')
        
        if current_floor == "Ground Floor":
            return ["Main Exit", "Emergency Exit A", "Emergency Exit B"]
        else:
            return [
                f"Emergency Stairs to Ground Floor",
                f"Emergency Elevator to Ground Floor",
                f"Emergency Exit on {current_floor}"
            ]

def main():
    """Main function for Smart Navigation System module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the Smart Navigation System")
        return
    
    # Initialize navigation system
    nav_system = SmartNavigationSystem()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">🧭 Smart Navigation System</h1>
        <p class="body-text">Find your way around the hospital with ease</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "🗺️ Floor Maps", "🚨 Emergency", "📍 Quick Access"])
    
    with tab1:
        st.markdown("### 🔍 Location Search")
        
        # Search interface
        search_term = st.text_input("Search for department, doctor, or patient:")
        
        if search_term:
            results = nav_system.find_location(search_term)
            
            if results:
                st.markdown(f"**Found {len(results)} result(s):**")
                
                for result in results:
                    with st.expander(f"{result['type']}: {result['name']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Floor:** {result['floor']}")
                            st.markdown(f"**Location:** {result['location']}")
                        
                        with col2:
                            if st.button(f"🗺️ Get Directions", key=f"dir_{result['name']}"):
                                # Simulate getting directions
                                st.info(f"Calculating route to {result['name']}...")
                                st.success(f"Route: Take elevator to {result['floor']} → Go to {result['location']}")
            else:
                st.info("No locations found matching your search.")
        
        # Quick search options
        st.markdown("### 🚀 Quick Search")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🏥 Emergency"):
                results = nav_system.find_location("Emergency")
                if results:
                    st.success(f"Emergency: {results[0]['floor']} - {results[0]['location']}")
        
        with col2:
            if st.button("💊 Pharmacy"):
                results = nav_system.find_location("Pharmacy")
                if results:
                    st.success(f"Pharmacy: {results[0]['floor']} - {results[0]['location']}")
        
        with col3:
            if st.button("🩺 Reception"):
                results = nav_system.find_location("Reception")
                if results:
                    st.success(f"Reception: {results[0]['floor']} - {results[0]['location']}")
    
    with tab2:
        st.markdown("### 🗺️ Floor Maps")
        
        # Floor selection
        floor_options = list(nav_system.hospital_floors.keys())
        selected_floor = st.selectbox("Select Floor", floor_options)
        
        if selected_floor:
            floor_map = nav_system.get_floor_map(selected_floor)
            
            st.markdown(f"#### {selected_floor} Layout")
            
            # Display floor layout
            for department, rooms in floor_map.items():
                with st.expander(f"🏥 {department}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Rooms:** {rooms}")
                        st.markdown(f"**Status:** Open")
                    
                    with col2:
                        if st.button(f"📍 Navigate to {department}", key=f"nav_{department}"):
                            st.success(f"Route to {department}: {rooms}")
            
            # Floor statistics
            st.markdown("#### 📊 Floor Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                create_metric_card("Departments", len(floor_map), "🏥")
            
            with col2:
                total_rooms = sum(len(rooms.split('-')) if '-' in rooms else 1 for rooms in floor_map.values())
                create_metric_card("Total Rooms", total_rooms, "🚪")
            
            with col3:
                create_metric_card("Available", total_rooms - 5, "✅")
    
    with tab3:
        st.markdown("### 🚨 Emergency Navigation")
        
        # Current location for emergency
        st.markdown("#### 📍 Your Current Location")
        
        current_floor = st.selectbox("Current Floor", list(nav_system.hospital_floors.keys()))
        current_location = {"floor": current_floor, "location": "Current Position"}
        
        # Emergency exit routes
        exit_routes = nav_system.get_emergency_exit_routes(current_location)
        
        st.markdown("#### 🚪 Emergency Exit Routes")
        
        for i, route in enumerate(exit_routes, 1):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Route {i}:** {route}")
            
            with col2:
                if st.button(f"🗺️ Follow", key=f"emergency_{i}"):
                    st.success(f"Following emergency route: {route}")
                    create_alert_box("🚨 Emergency route activated! Follow the signs.", "error")
        
        # Emergency contacts
        st.markdown("#### 📞 Emergency Contacts")
        
        emergency_contacts = [
            "Hospital Security: Ext. 100",
            "Emergency Services: 911",
            "Fire Department: 911",
            "Police: 911"
        ]
        
        for contact in emergency_contacts:
            st.markdown(f"• **{contact}**")
    
    with tab4:
        st.markdown("### 📍 Quick Access")
        
        # Popular destinations
        st.markdown("#### 🎯 Popular Destinations")
        
        destinations = [
            ("🏥 Emergency", "Ground Floor - Room 101-110"),
            ("💊 Pharmacy", "Ground Floor - Room 201-205"),
            ("🩺 Reception", "Ground Floor - Room 001-005"),
            ("🍽️ Cafeteria", "Ground Floor - Room 301-305"),
            ("🛏️ General Ward", "Second Floor - Room 601-650"),
            ("👶 Pediatrics", "Third Floor - Room 711-730")
        ]
        
        cols = st.columns(2)
        for i, (name, location) in enumerate(destinations):
            with cols[i % 2]:
                with st.expander(name):
                    st.markdown(f"**Location:** {location}")
                    if st.button(f"🗺️ Navigate", key=f"quick_{i}"):
                        st.success(f"Route to {name}: {location}")
        
        # Voice navigation
        st.markdown("#### 🎤 Voice Navigation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🎤 Where am I?"):
                st.info("You are on the Ground Floor near Reception")
        
        with col2:
            if st.button("🎤 Find Emergency"):
                st.info("Emergency is on Ground Floor, Room 101-110")
        
        with col3:
            if st.button("🎤 Nearest Exit"):
                st.info("Nearest exit is Main Exit on Ground Floor")
        
        # Navigation history
        st.markdown("#### 📋 Recent Navigation")
        
        recent_nav = [
            "Emergency → Room 101 (2 min ago)",
            "Pharmacy → Room 201 (15 min ago)",
            "Reception → Room 001 (1 hour ago)"
        ]
        
        for nav in recent_nav:
            st.markdown(f"• {nav}")

if __name__ == "__main__":
    main()
