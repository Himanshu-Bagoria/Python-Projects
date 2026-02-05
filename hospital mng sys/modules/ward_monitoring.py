import streamlit as st
import pandas as pd
from utils.auth import login_required

@login_required
def ward_monitoring():
    st.title("🏥 Ward Monitoring System")
    
    tabs = st.tabs(["🛏️ Bed Status", "👥 Patient List", "📊 Ward Analytics"])
    
    with tabs[0]:
        st.header("Bed Occupancy Status")
        beds = pd.DataFrame({
            'Ward': ['ICU', 'General', 'Pediatric', 'Maternity'],
            'Total Beds': [20, 50, 15, 10],
            'Occupied': [18, 35, 8, 7],
            'Available': [2, 15, 7, 3]
        })
        
        for idx, ward in beds.iterrows():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(f"{ward['Ward']} Ward", f"{ward['Occupied']}/{ward['Total Beds']}")
            with col2:
                occupancy = (ward['Occupied'] / ward['Total Beds']) * 100
                st.metric("Occupancy", f"{occupancy:.1f}%")
            with col3:
                st.metric("Available", ward['Available'])
            with col4:
                if ward['Available'] > 0:
                    st.success("Available")
                else:
                    st.error("Full")
    
    with tabs[1]:
        st.header("Current Patients")
        patients = pd.DataFrame({
            'Patient': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'Ward': ['ICU', 'General', 'General'],
            'Bed': ['ICU-01', 'GEN-15', 'GEN-22'],
            'Admission': ['2025-08-23', '2025-08-24', '2025-08-25'],
            'Condition': ['Critical', 'Stable', 'Stable']
        })
        st.dataframe(patients, use_container_width=True)
    
    with tabs[2]:
        st.header("Ward Analytics")
        st.info("Ward performance analytics would be displayed here")