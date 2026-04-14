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
from utils.ui_components import create_metric_card, create_alert_box, create_progress_bar
from config.themes import get_theme_css

class InsuranceBillingAssistant:
    def __init__(self):
        self.insurance_providers = [
            "Blue Cross Blue Shield",
            "Aetna",
            "Cigna",
            "UnitedHealth Group",
            "Humana",
            "Kaiser Permanente"
        ]
        
        self.billing_categories = {
            "Consultation": {"base_cost": 150, "insurance_coverage": 0.8},
            "Laboratory Tests": {"base_cost": 200, "insurance_coverage": 0.9},
            "Imaging": {"base_cost": 300, "insurance_coverage": 0.85},
            "Medication": {"base_cost": 100, "insurance_coverage": 0.7},
            "Emergency Services": {"base_cost": 500, "insurance_coverage": 0.9},
            "Surgery": {"base_cost": 5000, "insurance_coverage": 0.8}
        }
    
    def verify_insurance(self, patient_id, insurance_provider, policy_number):
        """Verify patient's insurance coverage"""
        # Simulate insurance verification
        verification_result = {
            "verified": True,
            "coverage_type": "Comprehensive",
            "deductible": 1000,
            "copay": 25,
            "coverage_percentage": 0.8,
            "expiry_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
            "network_status": "In-Network"
        }
        
        return verification_result
    
    def calculate_bill(self, patient_id, services):
        """Calculate bill for services"""
        total_bill = 0
        insurance_coverage = 0
        patient_responsibility = 0
        
        bill_details = []
        
        for service in services:
            if service['type'] in self.billing_categories:
                category = self.billing_categories[service['type']]
                base_cost = category['base_cost']
                coverage = category['insurance_coverage']
                
                # Apply insurance coverage
                covered_amount = base_cost * coverage
                patient_amount = base_cost - covered_amount
                
                total_bill += base_cost
                insurance_coverage += covered_amount
                patient_responsibility += patient_amount
                
                bill_details.append({
                    'service': service['type'],
                    'base_cost': base_cost,
                    'covered_amount': covered_amount,
                    'patient_amount': patient_amount
                })
        
        return {
            'total_bill': total_bill,
            'insurance_coverage': insurance_coverage,
            'patient_responsibility': patient_responsibility,
            'details': bill_details
        }
    
    def get_payment_history(self, patient_id):
        """Get patient's payment history"""
        # Simulate payment history
        payments = [
            {
                'date': (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                'amount': 150,
                'service': 'Consultation',
                'status': 'Paid'
            },
            {
                'date': (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d"),
                'amount': 200,
                'service': 'Laboratory Tests',
                'status': 'Paid'
            },
            {
                'date': (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                'amount': 300,
                'service': 'Imaging',
                'status': 'Paid'
            }
        ]
        
        return payments
    
    def process_payment(self, patient_id, amount, payment_method):
        """Process payment for patient"""
        # Simulate payment processing
        payment_result = {
            'success': True,
            'transaction_id': f"TXN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'amount': amount,
            'payment_method': payment_method,
            'timestamp': datetime.now().isoformat()
        }
        
        return payment_result

def main():
    """Main function for Insurance & Billing Assistant module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the Insurance & Billing Assistant")
        return
    
    # Initialize billing assistant
    billing_assistant = InsuranceBillingAssistant()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">💳 Insurance & Billing Assistant</h1>
        <p class="body-text">Manage insurance verification and billing processes</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏥 Insurance Verification", "💰 Billing Calculator", 
        "💳 Payment Processing", "📊 Billing History"
    ])
    
    with tab1:
        st.markdown("### 🏥 Insurance Verification")
        
        # Patient selection
        patients = db.patients
        if not patients:
            st.error("No patients found in the system")
            return
        
        patient_names = [f"{p['name']} (ID: {p['id']})" for p in patients]
        selected_patient = st.selectbox("Select Patient", patient_names)
        
        if selected_patient:
            patient_id = selected_patient.split("(ID: ")[1].split(")")[0]
            
            # Insurance verification form
            with st.form("insurance_verification"):
                st.markdown("#### Insurance Information")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    insurance_provider = st.selectbox("Insurance Provider", billing_assistant.insurance_providers)
                    policy_number = st.text_input("Policy Number", placeholder="Enter policy number")
                
                with col2:
                    group_number = st.text_input("Group Number (Optional)", placeholder="Enter group number")
                    member_id = st.text_input("Member ID", placeholder="Enter member ID")
                
                if st.form_submit_button("🔍 Verify Insurance"):
                    if policy_number and member_id:
                        # Verify insurance
                        verification_result = billing_assistant.verify_insurance(
                            patient_id, insurance_provider, policy_number
                        )
                        
                        if verification_result['verified']:
                            st.success("✅ Insurance verified successfully!")
                            
                            # Display verification details
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                create_metric_card("Coverage Type", verification_result['coverage_type'], "🏥")
                                create_metric_card("Deductible", f"${verification_result['deductible']}", "💰")
                            
                            with col2:
                                create_metric_card("Copay", f"${verification_result['copay']}", "💳")
                                create_metric_card("Coverage", f"{verification_result['coverage_percentage']*100}%", "📊")
                            
                            with col3:
                                create_metric_card("Network Status", verification_result['network_status'], "🌐")
                                create_metric_card("Expiry Date", verification_result['expiry_date'], "📅")
                            
                            # Insurance details
                            st.markdown("#### 📋 Insurance Details")
                            
                            details_data = [
                                ["Provider", insurance_provider],
                                ["Policy Number", policy_number],
                                ["Member ID", member_id],
                                ["Coverage Type", verification_result['coverage_type']],
                                ["Deductible", f"${verification_result['deductible']}"],
                                ["Copay", f"${verification_result['copay']}"],
                                ["Coverage Percentage", f"{verification_result['coverage_percentage']*100}%"],
                                ["Network Status", verification_result['network_status']],
                                ["Expiry Date", verification_result['expiry_date']]
                            ]
                            
                            details_df = pd.DataFrame(details_data, columns=["Field", "Value"])
                            st.dataframe(details_df, use_container_width=True)
                        else:
                            st.error("❌ Insurance verification failed. Please check the information.")
                    else:
                        st.warning("⚠️ Please fill in all required fields.")
    
    with tab2:
        st.markdown("### 💰 Billing Calculator")
        
        # Service selection
        st.markdown("#### Select Services")
        
        selected_services = []
        
        for service_type in billing_assistant.billing_categories.keys():
            if st.checkbox(f"✅ {service_type}", key=f"service_{service_type}"):
                selected_services.append({
                    'type': service_type,
                    'quantity': st.number_input(f"Quantity for {service_type}", min_value=1, value=1, key=f"qty_{service_type}")
                })
        
        if selected_services:
            # Calculate bill
            bill_result = billing_assistant.calculate_bill("patient_001", selected_services)
            
            st.markdown("#### 📊 Bill Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                create_metric_card("Total Bill", f"${bill_result['total_bill']}", "💰")
            
            with col2:
                create_metric_card("Insurance Coverage", f"${bill_result['insurance_coverage']}", "🏥")
            
            with col3:
                create_metric_card("Patient Responsibility", f"${bill_result['patient_responsibility']}", "💳")
            
            # Bill details
            st.markdown("#### 📋 Bill Details")
            
            details_data = []
            for detail in bill_result['details']:
                details_data.append([
                    detail['service'],
                    f"${detail['base_cost']}",
                    f"${detail['covered_amount']}",
                    f"${detail['patient_amount']}"
                ])
            
            details_df = pd.DataFrame(
                details_data, 
                columns=["Service", "Base Cost", "Insurance Coverage", "Patient Amount"]
            )
            st.dataframe(details_df, use_container_width=True)
            
            # Payment options
            st.markdown("#### 💳 Payment Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💳 Pay Now"):
                    st.info("Redirecting to payment gateway...")
            
            with col2:
                if st.button("📧 Send Bill"):
                    st.success("✅ Bill sent to patient email!")
            
            with col3:
                if st.button("📄 Download Bill"):
                    st.success("✅ Bill downloaded successfully!")
    
    with tab3:
        st.markdown("### 💳 Payment Processing")
        
        # Payment form
        with st.form("payment_processing"):
            st.markdown("#### Payment Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                payment_amount = st.number_input("Payment Amount ($)", min_value=0.01, value=100.0)
                payment_method = st.selectbox("Payment Method", [
                    "Credit Card", "Debit Card", "Bank Transfer", "Cash", "Insurance"
                ])
            
            with col2:
                card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
                expiry_date = st.text_input("Expiry Date", placeholder="MM/YY")
            
            cvv = st.text_input("CVV", placeholder="123", max_chars=4)
            
            if st.form_submit_button("💳 Process Payment"):
                if payment_amount and payment_method:
                    # Process payment
                    payment_result = billing_assistant.process_payment(
                        "patient_001", payment_amount, payment_method
                    )
                    
                    if payment_result['success']:
                        st.success("✅ Payment processed successfully!")
                        
                        # Payment confirmation
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            create_metric_card("Transaction ID", payment_result['transaction_id'], "🆔")
                        
                        with col2:
                            create_metric_card("Amount", f"${payment_result['amount']}", "💰")
                        
                        with col3:
                            create_metric_card("Method", payment_result['payment_method'], "💳")
                        
                        # Payment receipt
                        st.markdown("#### 📄 Payment Receipt")
                        
                        receipt_data = [
                            ["Transaction ID", payment_result['transaction_id']],
                            ["Amount", f"${payment_result['amount']}"],
                            ["Payment Method", payment_result['payment_method']],
                            ["Date", payment_result['timestamp'][:10]],
                            ["Time", payment_result['timestamp'][11:19]]
                        ]
                        
                        receipt_df = pd.DataFrame(receipt_data, columns=["Field", "Value"])
                        st.dataframe(receipt_df, use_container_width=True)
                        
                        # Receipt actions
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if st.button("📄 Download Receipt"):
                                st.success("✅ Receipt downloaded!")
                        
                        with col2:
                            if st.button("📧 Email Receipt"):
                                st.success("✅ Receipt sent to email!")
                    else:
                        st.error("❌ Payment processing failed. Please try again.")
                else:
                    st.warning("⚠️ Please fill in all required fields.")
        
        # Payment methods info
        st.markdown("#### 💳 Accepted Payment Methods")
        
        payment_methods = [
            "💳 Visa", "💳 Mastercard", "💳 American Express", "💳 Discover",
            "🏦 Bank Transfer", "💰 Cash", "🏥 Insurance"
        ]
        
        cols = st.columns(4)
        for i, method in enumerate(payment_methods):
            with cols[i % 4]:
                st.markdown(f"• {method}")
    
    with tab4:
        st.markdown("### 📊 Billing History")
        
        # Patient selection for history
        patient_names = [f"{p['name']} (ID: {p['id']})" for p in patients]
        selected_patient_history = st.selectbox("Select Patient for History", patient_names, key="history_patient")
        
        if selected_patient_history:
            patient_id = selected_patient_history.split("(ID: ")[1].split(")")[0]
            
            # Get payment history
            payment_history = billing_assistant.get_payment_history(patient_id)
            
            if payment_history:
                # Payment history statistics
                st.markdown("#### 📊 Payment Statistics")
                
                total_paid = sum(payment['amount'] for payment in payment_history)
                total_payments = len(payment_history)
                avg_payment = total_paid / total_payments if total_payments > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    create_metric_card("Total Paid", f"${total_paid}", "💰")
                
                with col2:
                    create_metric_card("Total Payments", total_payments, "💳")
                
                with col3:
                    create_metric_card("Average Payment", f"${avg_payment:.2f}", "📊")
                
                # Payment history table
                st.markdown("#### 📋 Payment History")
                
                history_data = []
                for payment in payment_history:
                    history_data.append([
                        payment['date'],
                        payment['service'],
                        f"${payment['amount']}",
                        payment['status']
                    ])
                
                history_df = pd.DataFrame(
                    history_data,
                    columns=["Date", "Service", "Amount", "Status"]
                )
                st.dataframe(history_df, use_container_width=True)
                
                # Export options
                st.markdown("#### 📤 Export Options")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📊 Export Payment History"):
                        st.success("✅ Payment history exported!")
                
                with col2:
                    if st.button("📄 Generate Statement"):
                        st.success("✅ Statement generated!")
                
                with col3:
                    if st.button("📧 Email Statement"):
                        st.success("✅ Statement sent to email!")
            else:
                st.info("📋 No payment history found for this patient.")

if __name__ == "__main__":
    main()
