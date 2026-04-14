import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication
from utils.database import db
from utils.ui_components import create_metric_card, create_alert_box
from config.themes import get_theme_css

def main():
    """Main function for Admin Dashboard module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication and admin role
    if not check_authentication():
        st.error("🔒 Please log in to access the Admin Dashboard")
        return
    
    user_role = st.session_state.get('role', 'patient')
    if user_role != 'admin':
        st.error("🚫 Access denied. Admin privileges required.")
        return
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">⚙️ Admin Dashboard</h1>
        <p class="body-text">System management and analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # System statistics
    stats = db.get_statistics()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card("Total Patients", stats["total_patients"], "👥")
    
    with col2:
        create_metric_card("Total Doctors", stats["total_doctors"], "👨‍⚕️")
    
    with col3:
        create_metric_card("Total Appointments", stats["total_appointments"], "📅")
    
    with col4:
        create_metric_card("Active Emergencies", stats["active_emergencies"], "🚨")
    
    # Admin modules
    st.markdown("### 🧭 Admin Modules")
    
    modules = [
        ("Patient Management", "👥"),
        ("Staff Management", "👨‍⚕️"),
        ("Appointment Management", "📅"),
        ("Inventory Management", "📦"),
        ("Financial Reports", "💰"),
        ("System Analytics", "📊"),
        ("Settings", "⚙️")
    ]
    
    cols = st.columns(3)
    for i, (module_name, icon) in enumerate(modules):
        with cols[i % 3]:
            if st.button(f"{icon} {module_name}", use_container_width=True):
                st.info(f"Opening {module_name}...")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Report"):
            st.success("✅ System report exported!")
    
    with col2:
        if st.button("🔒 Security Check"):
            st.success("✅ Security audit completed!")
    
    with col3:
        if st.button("🔄 Refresh Data"):
            st.rerun()

if __name__ == "__main__":
    main()
