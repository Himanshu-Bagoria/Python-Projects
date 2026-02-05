import streamlit as st
from utils.auth import login_required

@login_required
def emergency_alert():
    st.title("🚨 Emergency Alert System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Emergency Contacts")
        st.error("🚨 Emergency: 911")
        st.warning("🏥 Hospital Emergency: (555) 123-4567")
        st.info("🚑 Ambulance: (555) 123-4568")
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("🚨 CALL EMERGENCY", type="primary"):
            st.error("Emergency services contacted!")
        
        if st.button("📞 Call Security"):
            st.warning("Security contacted!")
        
        if st.button("🚑 Request Ambulance"):
            st.info("Ambulance requested!")
    
    st.subheader("Report Emergency")
    emergency_type = st.selectbox("Emergency Type", [
        "Medical Emergency", "Fire", "Security Threat", "Equipment Failure"
    ])
    location = st.text_input("Location")
    description = st.text_area("Description")
    
    if st.button("Submit Emergency Report"):
        st.success("Emergency report submitted!")