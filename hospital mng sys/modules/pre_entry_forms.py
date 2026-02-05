import streamlit as st
import pandas as pd
import qrcode
import io
import base64
import json
import uuid
from datetime import datetime, timedelta
from PIL import Image
from utils.database import db
from utils.auth import auth_manager, login_required
from utils.ui_components import UIComponents
import hashlib
import secrets

@login_required
def pre_entry_forms():
    """Pre-entry Patient Forms with QR Token Authentication"""
    st.title("📝 Smart Pre-Entry Forms")
    
    # Initialize session state
    if 'form_tokens' not in st.session_state:
        st.session_state['form_tokens'] = {}
    if 'submitted_forms' not in st.session_state:
        st.session_state['submitted_forms'] = []
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎫 Generate QR Token", 
        "📋 Fill Form", 
        "✅ Verify Submission",
        "📊 Form Analytics"
    ])
    
    with tab1:
        generate_qr_token()
    
    with tab2:
        fill_pre_entry_form()
    
    with tab3:
        verify_form_submission()
    
    with tab4:
        form_analytics()

def generate_qr_token():
    """Generate QR tokens for pre-entry forms"""
    st.header("🎫 Generate QR Token for Pre-Entry")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Token Generation")
        
        # Form type selection
        form_type = st.selectbox("Select Form Type", [
            "New Patient Registration",
            "Appointment Pre-Check",
            "Emergency Information",
            "Specialist Consultation",
            "Lab Test Preparation",
            "Surgery Pre-Assessment"
        ])
        
        # Patient selection (optional for new patients)
        patients_df = db.get_patients()
        patient_options = ["New Patient"] + [
            f"{row['patient_id']} - {row['first_name']} {row['last_name']}" 
            for _, row in patients_df.iterrows()
        ] if not patients_df.empty else ["New Patient"]
        
        selected_patient = st.selectbox("Patient", patient_options)
        
        # Additional parameters
        expiry_hours = st.number_input("Token Validity (Hours)", 
                                     min_value=1, max_value=72, value=24)
        
        department = st.selectbox("Department", [
            "General Medicine", "Cardiology", "Neurology", 
            "Orthopedics", "Pediatrics", "Emergency", "Surgery"
        ])
        
        appointment_date = st.date_input("Appointment Date (Optional)")
        
        special_instructions = st.text_area("Special Instructions", 
                                          placeholder="Any special instructions for the patient...")
        
        # Generate token button
        if st.button("🎫 Generate QR Token", type="primary"):
            token_data = create_form_token(
                form_type, selected_patient, expiry_hours, 
                department, appointment_date, special_instructions
            )
            
            if token_data:
                st.success("✅ QR Token generated successfully!")
                st.session_state['latest_token'] = token_data
                st.rerun()
    
    with col2:
        st.subheader("📱 Generated Token")
        
        if 'latest_token' in st.session_state:
            token = st.session_state['latest_token']
            
            # Display QR code
            qr_img = generate_token_qr_code(token)
            
            # Convert PIL Image to bytes for Streamlit display
            img_buffer = io.BytesIO()
            qr_img.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            
            st.image(img_buffer, caption="QR Token", width=300)
            
            # Token information
            with st.expander("🔍 Token Details", expanded=True):
                st.write(f"**Token ID:** {token['token_id']}")
                st.write(f"**Form Type:** {token['form_type']}")
                st.write(f"**Department:** {token['department']}")
                st.write(f"**Valid Until:** {token['expires_at']}")
                st.write(f"**Instructions:** {token.get('instructions', 'None')}")
            
            # Download options
            col_a, col_b = st.columns(2)
            
            with col_a:
                # Download QR code
                download_buffer = io.BytesIO()
                qr_img.save(download_buffer, format="PNG")
                
                st.download_button(
                    label="📥 Download QR",
                    data=download_buffer.getvalue(),
                    file_name=f"form_token_{token['token_id'][:8]}.png",
                    mime="image/png"
                )
            
            with col_b:
                # Generate printable version
                if st.button("🖨️ Print Version"):
                    printable = create_printable_token(token, qr_img)
                    
                    # Convert printable PIL Image to bytes
                    printable_buffer = io.BytesIO()
                    printable.save(printable_buffer, format="PNG")
                    printable_buffer.seek(0)
                    
                    st.image(printable_buffer, caption="Printable Token")
        else:
            st.info("Generate a token to see the QR code and details here.")
        
        # Recent tokens
        st.subheader("📜 Recent Tokens")
        if st.session_state['form_tokens']:
            for token_id, token in list(st.session_state['form_tokens'].items())[-5:]:
                status = "🟢 Active" if is_token_valid(token) else "🔴 Expired"
                st.write(f"{status} {token['form_type']} - {token_id[:8]}")
        else:
            st.info("No tokens generated yet.")

def create_form_token(form_type, patient, expiry_hours, department, appointment_date, instructions):
    """Create a secure form token"""
    # Generate unique token ID
    token_id = str(uuid.uuid4())
    
    # Extract patient info
    patient_id = None
    patient_name = "New Patient"
    if patient != "New Patient":
        patient_id = patient.split(' - ')[0]
        patient_name = patient.split(' - ')[1]
    
    # Create token data
    token_data = {
        'token_id': token_id,
        'form_type': form_type,
        'patient_id': patient_id,
        'patient_name': patient_name,
        'department': department,
        'appointment_date': appointment_date.isoformat() if appointment_date else None,
        'instructions': instructions,
        'created_at': datetime.now().isoformat(),
        'expires_at': (datetime.now() + timedelta(hours=expiry_hours)).isoformat(),
        'is_used': False,
        'form_url': f"https://hospital.forms/{token_id[:16]}",
        'security_hash': generate_security_hash(token_id, form_type, patient_id)
    }
    
    # Store token
    st.session_state['form_tokens'][token_id] = token_data
    
    return token_data

def generate_security_hash(token_id, form_type, patient_id):
    """Generate security hash for token validation"""
    data = f"{token_id}{form_type}{patient_id}{datetime.now().date()}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]

def generate_token_qr_code(token_data):
    """Generate QR code for the token"""
    # Create compact QR data
    qr_data = {
        'type': 'pre_entry_form',
        'token_id': token_data['token_id'],
        'form_type': token_data['form_type'],
        'department': token_data['department'],
        'expires_at': token_data['expires_at'],
        'form_url': token_data['form_url'],
        'hash': token_data['security_hash']
    }
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img

def create_printable_token(token_data, qr_img):
    """Create printable version of token"""
    # Create a printable layout with QR code and instructions
    from PIL import ImageDraw, ImageFont
    
    # Create canvas
    width, height = 600, 800
    printable = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(printable)
    
    # Try to load font
    try:
        title_font = ImageFont.truetype("arial.ttf", 24)
        text_font = ImageFont.truetype("arial.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Header
    draw.text((50, 30), "Smart Hospital System", font=title_font, fill='black')
    draw.text((50, 60), "Pre-Entry Form Token", font=text_font, fill='gray')
    
    # QR code
    qr_size = (200, 200)
    qr_resized = qr_img.resize(qr_size)
    printable.paste(qr_resized, (200, 100))
    
    # Token information
    y_pos = 320
    info_lines = [
        f"Token ID: {token_data['token_id'][:16]}",
        f"Form Type: {token_data['form_type']}",
        f"Department: {token_data['department']}",
        f"Valid Until: {token_data['expires_at'][:19]}",
        "",
        "Instructions:",
        "1. Scan QR code with your phone",
        "2. Fill out the form completely",
        "3. Submit before expiry time",
        "4. Show confirmation at reception"
    ]
    
    for line in info_lines:
        draw.text((50, y_pos), line, font=text_font, fill='black')
        y_pos += 25
    
    return printable

def fill_pre_entry_form():
    """Interface for filling pre-entry forms"""
    st.header("📋 Fill Pre-Entry Form")
    
    # Token verification
    st.subheader("🔍 Verify Token")
    
    token_input_method = st.radio("How do you want to provide the token?", 
                                 ["Upload QR Code", "Enter Token ID", "Scan Live QR"])
    
    token_data = None
    
    if token_input_method == "Upload QR Code":
        uploaded_qr = st.file_uploader("Upload QR Code Image", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_qr:
            try:
                # Decode QR code
                qr_data = decode_qr_code(Image.open(uploaded_qr))
                if qr_data and qr_data.get('type') == 'pre_entry_form':
                    token_id = qr_data.get('token_id')
                    token_data = st.session_state['form_tokens'].get(token_id)
                    
                    if token_data:
                        if is_token_valid(token_data):
                            st.success("✅ Valid token found!")
                        else:
                            st.error("❌ Token has expired!")
                            token_data = None
                    else:
                        st.error("❌ Token not found!")
                else:
                    st.error("❌ Invalid QR code!")
            except Exception as e:
                st.error(f"Error reading QR code: {str(e)}")
    
    elif token_input_method == "Enter Token ID":
        token_id_input = st.text_input("Enter Token ID")
        
        if token_id_input and st.button("Verify Token"):
            token_data = st.session_state['form_tokens'].get(token_id_input)
            
            if token_data:
                if is_token_valid(token_data):
                    st.success("✅ Valid token found!")
                else:
                    st.error("❌ Token has expired!")
                    token_data = None
            else:
                st.error("❌ Token not found!")
    
    else:  # Scan Live QR
        st.info("Live QR scanning would be implemented using camera access.")
    
    # Form filling interface
    if token_data:
        st.markdown("---")
        display_form_interface(token_data)

def display_form_interface(token_data):
    """Display the appropriate form based on token type"""
    st.subheader(f"📝 {token_data['form_type']}")
    
    form_type = token_data['form_type']
    
    if form_type == "New Patient Registration":
        display_new_patient_form(token_data)
    elif form_type == "Appointment Pre-Check":
        display_precheck_form(token_data)
    elif form_type == "Emergency Information":
        display_emergency_form(token_data)
    elif form_type == "Specialist Consultation":
        display_specialist_form(token_data)
    elif form_type == "Lab Test Preparation":
        display_lab_prep_form(token_data)
    elif form_type == "Surgery Pre-Assessment":
        display_surgery_prep_form(token_data)

def display_new_patient_form(token_data):
    """New patient registration form"""
    with st.form("new_patient_form"):
        st.subheader("👤 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name*", key="np_first_name")
            last_name = st.text_input("Last Name*", key="np_last_name")
            date_of_birth = st.date_input("Date of Birth*", key="np_dob")
            gender = st.selectbox("Gender*", ["Male", "Female", "Other"], key="np_gender")
        
        with col2:
            phone = st.text_input("Phone Number*", key="np_phone")
            email = st.text_input("Email", key="np_email")
            blood_group = st.selectbox("Blood Group", 
                                     ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"], 
                                     key="np_blood")
            marital_status = st.selectbox("Marital Status", 
                                        ["Single", "Married", "Divorced", "Widowed"], 
                                        key="np_marital")
        
        st.subheader("📍 Address Information")
        address = st.text_area("Address*", key="np_address")
        
        col3, col4 = st.columns(2)
        with col3:
            city = st.text_input("City*", key="np_city")
            state = st.text_input("State*", key="np_state")
        with col4:
            postal_code = st.text_input("Postal Code*", key="np_postal")
            country = st.text_input("Country*", value="India", key="np_country")
        
        st.subheader("🚨 Emergency Contact")
        col5, col6 = st.columns(2)
        with col5:
            emergency_name = st.text_input("Emergency Contact Name*", key="np_em_name")
            emergency_phone = st.text_input("Emergency Contact Phone*", key="np_em_phone")
        with col6:
            emergency_relation = st.text_input("Relationship*", key="np_em_relation")
        
        st.subheader("🏥 Medical Information")
        medical_history = st.text_area("Medical History", key="np_medical")
        allergies = st.text_area("Allergies", key="np_allergies")
        current_medications = st.text_area("Current Medications", key="np_medications")
        
        st.subheader("💳 Insurance Information")
        col7, col8 = st.columns(2)
        with col7:
            insurance_provider = st.text_input("Insurance Provider", key="np_insurance")
            policy_number = st.text_input("Policy Number", key="np_policy")
        with col8:
            insurance_expiry = st.date_input("Insurance Expiry", key="np_ins_expiry")
        
        # Consent and agreements
        st.subheader("✅ Consent & Agreements")
        consent_treatment = st.checkbox("I consent to medical treatment*", key="np_consent1")
        consent_data = st.checkbox("I agree to data processing for medical purposes*", key="np_consent2")
        consent_communication = st.checkbox("I agree to receive appointment reminders", key="np_consent3")
        
        submitted = st.form_submit_button("✅ Submit Registration", type="primary")
        
        if submitted:
            if all([first_name, last_name, date_of_birth, phone, address, city, state, 
                   postal_code, emergency_name, emergency_phone, emergency_relation,
                   consent_treatment, consent_data]):
                
                # Process form submission
                form_data = {
                    'token_id': token_data['token_id'],
                    'form_type': token_data['form_type'],
                    'patient_data': {
                        'first_name': first_name,
                        'last_name': last_name,
                        'date_of_birth': date_of_birth.isoformat(),
                        'gender': gender,
                        'phone': phone,
                        'email': email,
                        'blood_group': blood_group,
                        'marital_status': marital_status,
                        'address': address,
                        'city': city,
                        'state': state,
                        'postal_code': postal_code,
                        'country': country,
                        'emergency_name': emergency_name,
                        'emergency_phone': emergency_phone,
                        'emergency_relation': emergency_relation,
                        'medical_history': medical_history,
                        'allergies': allergies,
                        'current_medications': current_medications,
                        'insurance_provider': insurance_provider,
                        'policy_number': policy_number,
                        'insurance_expiry': insurance_expiry.isoformat() if insurance_expiry else None
                    },
                    'consents': {
                        'treatment': consent_treatment,
                        'data_processing': consent_data,
                        'communication': consent_communication
                    },
                    'submitted_at': datetime.now().isoformat()
                }
                
                submit_form(form_data)
                st.success("✅ Registration submitted successfully!")
            else:
                st.error("❌ Please fill all required fields marked with *")

def display_precheck_form(token_data):
    """Appointment pre-check form"""
    with st.form("precheck_form"):
        st.subheader("📋 Pre-Appointment Check")
        
        # Current symptoms
        st.subheader("🩺 Current Symptoms")
        symptoms = st.text_area("Describe your current symptoms", 
                               placeholder="Please describe what you're experiencing...")
        
        symptom_duration = st.selectbox("How long have you had these symptoms?", [
            "Less than 24 hours", "1-3 days", "4-7 days", "1-2 weeks", "More than 2 weeks"
        ])
        
        pain_level = st.slider("Pain Level (0-10)", 0, 10, 0)
        
        # Vital signs
        st.subheader("📊 Self-Reported Vitals")
        col1, col2 = st.columns(2)
        
        with col1:
            temperature = st.number_input("Temperature (°F)", min_value=95.0, max_value=110.0, value=98.6)
            has_fever = st.checkbox("Do you have fever?")
        
        with col2:
            difficulty_breathing = st.checkbox("Difficulty breathing?")
            chest_pain = st.checkbox("Chest pain?")
        
        # Recent changes
        st.subheader("📝 Recent Changes")
        medication_changes = st.text_area("Any recent medication changes?")
        travel_history = st.text_area("Recent travel history (last 14 days)")
        
        # COVID screening
        st.subheader("🦠 COVID-19 Screening")
        covid_symptoms = st.multiselect("Do you have any of these symptoms?", [
            "Fever", "Cough", "Shortness of breath", "Loss of taste/smell", 
            "Fatigue", "Body aches", "Sore throat", "Congestion"
        ])
        
        covid_exposure = st.checkbox("Have you been exposed to COVID-19 in the last 14 days?")
        
        submitted = st.form_submit_button("✅ Submit Pre-Check", type="primary")
        
        if submitted:
            form_data = {
                'token_id': token_data['token_id'],
                'form_type': token_data['form_type'],
                'precheck_data': {
                    'symptoms': symptoms,
                    'symptom_duration': symptom_duration,
                    'pain_level': pain_level,
                    'temperature': temperature,
                    'has_fever': has_fever,
                    'difficulty_breathing': difficulty_breathing,
                    'chest_pain': chest_pain,
                    'medication_changes': medication_changes,
                    'travel_history': travel_history,
                    'covid_symptoms': covid_symptoms,
                    'covid_exposure': covid_exposure
                },
                'submitted_at': datetime.now().isoformat()
            }
            
            submit_form(form_data)
            st.success("✅ Pre-check submitted successfully!")

def display_emergency_form(token_data):
    """Emergency information form"""
    with st.form("emergency_form"):
        st.subheader("🚨 Emergency Information")
        
        # Emergency type
        emergency_type = st.selectbox("Type of Emergency", [
            "Chest Pain", "Difficulty Breathing", "Severe Injury", "Stroke Symptoms",
            "Severe Allergic Reaction", "Poisoning", "Mental Health Crisis", "Other"
        ])
        
        if emergency_type == "Other":
            other_emergency = st.text_input("Please specify")
        
        # Severity assessment
        severity = st.selectbox("How would you rate the severity?", [
            "Life-threatening", "Severe", "Moderate", "Mild"
        ])
        
        # Current condition
        current_condition = st.text_area("Describe current condition", 
                                       placeholder="Please describe the emergency situation...")
        
        # Timeline
        when_started = st.selectbox("When did this start?", [
            "Within the last hour", "1-6 hours ago", "6-24 hours ago", "More than 24 hours ago"
        ])
        
        # Current vital signs
        st.subheader("📊 Current Vital Signs")
        col1, col2 = st.columns(2)
        
        with col1:
            is_conscious = st.checkbox("Patient is conscious", value=True)
            is_breathing = st.checkbox("Patient is breathing normally", value=True)
        
        with col2:
            pulse_rate = st.number_input("Pulse rate (if known)", min_value=0, max_value=200, value=0)
            blood_pressure = st.text_input("Blood pressure (if known)")
        
        # Current medications
        emergency_medications = st.text_area("Current medications patient is taking")
        
        # Allergies
        known_allergies = st.text_area("Known allergies")
        
        submitted = st.form_submit_button("🚨 Submit Emergency Form", type="primary")
        
        if submitted:
            form_data = {
                'token_id': token_data['token_id'],
                'form_type': token_data['form_type'],
                'emergency_data': {
                    'emergency_type': emergency_type,
                    'other_emergency': other_emergency if emergency_type == "Other" else None,
                    'severity': severity,
                    'current_condition': current_condition,
                    'when_started': when_started,
                    'is_conscious': is_conscious,
                    'is_breathing': is_breathing,
                    'pulse_rate': pulse_rate if pulse_rate > 0 else None,
                    'blood_pressure': blood_pressure,
                    'emergency_medications': emergency_medications,
                    'known_allergies': known_allergies
                },
                'submitted_at': datetime.now().isoformat(),
                'priority': 'urgent' if severity in ['Life-threatening', 'Severe'] else 'high'
            }
            
            submit_form(form_data)
            st.success("🚨 Emergency form submitted! Please proceed to reception immediately.")

def display_specialist_form(token_data):
    """Specialist consultation form"""
    st.info("Specialist consultation form would be displayed here with relevant medical history questions.")

def display_lab_prep_form(token_data):
    """Lab test preparation form"""
    st.info("Lab test preparation form would be displayed here with pre-test instructions.")

def display_surgery_prep_form(token_data):
    """Surgery preparation assessment form"""
    st.info("Surgery pre-assessment form would be displayed here with pre-operative questions.")

def decode_qr_code(image):
    """Decode QR code from image"""
    try:
        import cv2
        import numpy as np
        
        # Convert PIL to OpenCV
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Detect and decode QR code
        detector = cv2.QRCodeDetector()
        data, vertices, _ = detector.detectAndDecode(opencv_image)
        
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        st.error(f"Error decoding QR code: {str(e)}")
        return None

def is_token_valid(token_data):
    """Check if token is still valid"""
    expires_at = datetime.fromisoformat(token_data['expires_at'])
    return datetime.now() < expires_at and not token_data.get('is_used', False)

def submit_form(form_data):
    """Submit form data"""
    # Mark token as used
    token_id = form_data['token_id']
    if token_id in st.session_state['form_tokens']:
        st.session_state['form_tokens'][token_id]['is_used'] = True
    
    # Store submitted form
    form_data['submission_id'] = str(uuid.uuid4())
    st.session_state['submitted_forms'].append(form_data)
    
    # In production, save to database and trigger notifications

def verify_form_submission():
    """Verify form submissions"""
    st.header("✅ Verify Form Submission")
    
    verification_method = st.radio("Verification Method", 
                                 ["Submission ID", "Token ID", "Patient Phone"])
    
    if verification_method == "Submission ID":
        submission_id = st.text_input("Enter Submission ID")
        
        if submission_id and st.button("Verify Submission"):
            # Find submission
            submission = next((form for form in st.session_state['submitted_forms'] 
                             if form['submission_id'] == submission_id), None)
            
            if submission:
                display_submission_details(submission)
            else:
                st.error("Submission not found!")
    
    elif verification_method == "Token ID":
        token_id = st.text_input("Enter Token ID")
        
        if token_id and st.button("Find Submission"):
            # Find submission by token
            submission = next((form for form in st.session_state['submitted_forms'] 
                             if form['token_id'] == token_id), None)
            
            if submission:
                display_submission_details(submission)
            else:
                st.error("No submission found for this token!")

def display_submission_details(submission):
    """Display submission details"""
    st.success("✅ Submission Found!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Submission ID:** {submission['submission_id']}")
        st.write(f"**Form Type:** {submission['form_type']}")
        st.write(f"**Submitted At:** {submission['submitted_at']}")
    
    with col2:
        st.write(f"**Token ID:** {submission['token_id'][:16]}...")
        st.write(f"**Status:** {'✅ Verified' if submission.get('verified') else '⏳ Pending'}")
    
    # Display form data based on type
    if submission['form_type'] == "New Patient Registration":
        with st.expander("Patient Data"):
            st.json(submission['patient_data'])
    elif submission['form_type'] == "Appointment Pre-Check":
        with st.expander("Pre-Check Data"):
            st.json(submission['precheck_data'])
    elif submission['form_type'] == "Emergency Information":
        with st.expander("Emergency Data"):
            st.json(submission['emergency_data'])

def form_analytics():
    """Form analytics and insights"""
    st.header("📊 Form Analytics")
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tokens Generated", len(st.session_state['form_tokens']))
    
    with col2:
        used_tokens = sum(1 for token in st.session_state['form_tokens'].values() if token.get('is_used'))
        st.metric("Forms Submitted", used_tokens)
    
    with col3:
        expired_tokens = sum(1 for token in st.session_state['form_tokens'].values() if not is_token_valid(token))
        st.metric("Expired Tokens", expired_tokens)
    
    with col4:
        completion_rate = (used_tokens / len(st.session_state['form_tokens']) * 100) if st.session_state['form_tokens'] else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    # Form type distribution
    if st.session_state['form_tokens']:
        form_types = [token['form_type'] for token in st.session_state['form_tokens'].values()]
        type_counts = pd.Series(form_types).value_counts()
        
        import plotly.express as px
        fig = px.pie(values=type_counts.values, names=type_counts.index, 
                    title="Form Types Distribution")
        st.plotly_chart(fig, use_container_width=True)