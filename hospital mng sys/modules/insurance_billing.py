import streamlit as st
import pandas as pd
from utils.auth import login_required

@login_required
def insurance_billing():
    st.title("💰 Insurance & Billing")
    
    tabs = st.tabs(["💳 Billing", "🏥 Insurance", "📊 Statements"])
    
    with tabs[0]:
        st.header("Generate Bill")
        services = st.multiselect("Services", [
            "Consultation", "Lab Tests", "Medication", "Procedures"
        ])
        total = st.number_input("Total Amount", value=1000.0)
        if st.button("Generate Bill"):
            st.success("Bill generated successfully!")
    
    with tabs[1]:
        st.header("Insurance Information")
        provider = st.text_input("Insurance Provider")
        policy = st.text_input("Policy Number")
        coverage = st.number_input("Coverage %", value=80.0)
        if st.button("Verify Insurance"):
            st.success("Insurance verified!")
    
    with tabs[2]:
        st.header("Billing Statements")
        statements = pd.DataFrame({
            'Date': ['2025-08-25', '2025-08-20'],
            'Service': ['Consultation', 'Lab Test'],
            'Amount': [500, 300],
            'Status': ['Paid', 'Pending']
        })
        st.dataframe(statements, use_container_width=True)