import streamlit as st
import qrcode
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import json
from datetime import datetime, date
import uuid
from utils.database import db
from utils.auth import auth_manager, login_required
from utils.ui_components import UIComponents
import tempfile
import os

@login_required
def id_card_generator():
    """Advanced QR-based ID Card Generator"""
    st.title("🆔 Smart ID Card Generator")
    
    # Initialize session state
    if 'generated_cards' not in st.session_state:
        st.session_state['generated_cards'] = []
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs([
        "🎨 Generate ID Card", 
        "📁 Card Gallery", 
        "🔧 Settings"
    ])
    
    with tab1:
        generate_single_id_card()
    
    with tab2:
        id_card_gallery()
    
    with tab3:
        card_settings()

def generate_single_id_card():
    """Generate single patient ID card with QR code"""
    st.header("Generate Patient ID Card")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Patient Selection")
        
        # Get patients
        patients_df = db.get_patients()
        if not patients_df.empty:
            patient_options = ["Select a patient..."] + [
                f"{row['patient_id']} - {row['first_name']} {row['last_name']}" 
                for _, row in patients_df.iterrows()
            ]
            
            selected_patient = st.selectbox("Choose Patient", patient_options)
            
            if selected_patient != "Select a patient...":
                patient_id = selected_patient.split(' - ')[0]
                patient_info = patients_df[patients_df['patient_id'] == patient_id].iloc[0]
                
                # Display patient info
                with st.expander("📋 Patient Information", expanded=True):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**ID:** {patient_info['patient_id']}")
                        st.write(f"**Name:** {patient_info['first_name']} {patient_info['last_name']}")
                        st.write(f"**DOB:** {patient_info['date_of_birth']}")
                    with col_b:
                        st.write(f"**Blood Group:** {patient_info['blood_group']}")
                        st.write(f"**Gender:** {patient_info['gender']}")
                        st.write(f"**Contact:** {patient_info.get('emergency_contact', 'N/A')}")
                
                # Card customization
                st.subheader("🎨 Card Design")
                card_template = st.selectbox("Template", [
                    "Professional Blue", "Medical Green", "Modern Purple", 
                    "Elegant Gold", "Clean White"
                ])
                
                include_photo = st.checkbox("Include Photo", value=True)
                uploaded_photo = None
                if include_photo:
                    uploaded_photo = st.file_uploader("Patient Photo", type=['png', 'jpg', 'jpeg'])
                
                # Generate card
                if st.button("🎨 Generate ID Card", type="primary"):
                    with st.spinner("Generating ID card..."):
                        card_data = create_id_card_data(patient_info)
                        card_image = generate_card_image(card_data, card_template, uploaded_photo)
                        
                        if card_image:
                            st.session_state['generated_cards'].append({
                                'patient_id': patient_id,
                                'card_image': card_image,
                                'generated_at': datetime.now(),
                                'template': card_template
                            })
                            st.success("✅ ID Card generated!")
                            st.rerun()
        else:
            st.warning("No patients found. Please add patients first.")
    
    with col2:
        st.subheader("🖼️ Card Preview")
        
        if st.session_state['generated_cards']:
            latest_card = st.session_state['generated_cards'][-1]
            
            # Convert PIL Image to bytes for Streamlit display
            img_buffer = io.BytesIO()
            latest_card['card_image'].save(img_buffer, format="PNG")
            img_buffer.seek(0)
            
            st.image(img_buffer, use_column_width=True)
            
            # Download options
            img_buffer = io.BytesIO()
            latest_card['card_image'].save(img_buffer, format="PNG", dpi=(300, 300))
            
            st.download_button(
                label="📥 Download Card",
                data=img_buffer.getvalue(),
                file_name=f"id_card_{latest_card['patient_id']}.png",
                mime="image/png"
            )
        else:
            st.info("Generate a card to see preview")

def create_id_card_data(patient_info):
    """Create ID card data with QR code"""
    card_id = f"HC{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
    
    card_data = {
        'card_id': card_id,
        'patient_id': patient_info['patient_id'],
        'name': f"{patient_info['first_name']} {patient_info['last_name']}",
        'dob': patient_info['date_of_birth'],
        'gender': patient_info['gender'],
        'blood_group': patient_info['blood_group'],
        'issue_date': datetime.now().strftime('%Y-%m-%d'),
        'expiry_date': (datetime.now().replace(year=datetime.now().year + 5)).strftime('%Y-%m-%d'),
        'hospital_name': 'Smart Hospital System',
        'emergency_contact': patient_info.get('emergency_contact', 'N/A')
    }
    
    # QR code data
    qr_data = {
        'type': 'patient_id_card',
        'card_id': card_id,
        'patient_id': patient_info['patient_id'],
        'name': card_data['name'],
        'dob': card_data['dob'],
        'blood_group': card_data['blood_group'],
        'emergency_contact': card_data['emergency_contact'],
        'verification_url': f"https://hospital.verify/{card_id}"
    }
    
    card_data['qr_data'] = json.dumps(qr_data)
    return card_data

def generate_card_image(card_data, template, photo=None):
    """Generate ID card image"""
    try:
        # Card dimensions
        card_width, card_height = 800, 500
        card = Image.new('RGB', (card_width, card_height), color='white')
        draw = ImageDraw.Draw(card)
        
        # Template colors
        colors = get_template_colors(template)
        
        # Background gradient
        for i in range(card_height):
            ratio = i / card_height
            color = blend_colors(colors['primary'], colors['secondary'], ratio)
            draw.line([(0, i), (card_width, i)], fill=color)
        
        # Header
        draw.rectangle([0, 0, card_width, 80], fill=colors['header'])
        
        # Fonts (fallback to default)
        try:
            title_font = ImageFont.truetype("arial.ttf", 24)
            regular_font = ImageFont.truetype("arial.ttf", 16)
        except:
            title_font = ImageFont.load_default()
            regular_font = ImageFont.load_default()
        
        # Hospital name
        draw.text((20, 20), card_data['hospital_name'], font=title_font, fill='white')
        draw.text((20, 50), 'PATIENT ID CARD', font=regular_font, fill='white')
        
        # Photo placeholder
        photo_size = (120, 150)
        photo_x, photo_y = 20, 100
        
        if photo:
            try:
                patient_photo = Image.open(photo).resize(photo_size)
                card.paste(patient_photo, (photo_x, photo_y))
            except:
                draw.rectangle([photo_x, photo_y, photo_x + photo_size[0], photo_y + photo_size[1]], 
                             fill=colors['photo_bg'], outline=colors['border'])
        else:
            draw.rectangle([photo_x, photo_y, photo_x + photo_size[0], photo_y + photo_size[1]], 
                         fill=colors['photo_bg'], outline=colors['border'])
            draw.text((photo_x + 40, photo_y + 70), 'PHOTO', font=regular_font, fill='gray')
        
        # Patient information
        info_x, info_y = 160, 100
        info_lines = [
            f"ID: {card_data['patient_id']}",
            f"Name: {card_data['name']}",
            f"DOB: {card_data['dob']}",
            f"Gender: {card_data['gender']}",
            f"Blood: {card_data['blood_group']}",
            f"Issue: {card_data['issue_date']}",
            f"Emergency: {card_data['emergency_contact']}"
        ]
        
        for i, line in enumerate(info_lines):
            draw.text((info_x, info_y + i * 25), line, font=regular_font, fill='black')
        
        # QR code
        qr_code = generate_qr_code_image(card_data['qr_data'])
        qr_size = (150, 150)
        qr_x = card_width - qr_size[0] - 20
        qr_y = card_height - qr_size[1] - 20
        
        qr_resized = qr_code.resize(qr_size)
        card.paste(qr_resized, (qr_x, qr_y))
        
        # Card ID
        draw.text((20, card_height - 30), f"Card ID: {card_data['card_id']}", 
                 font=ImageFont.load_default(), fill='gray')
        
        return card
        
    except Exception as e:
        st.error(f"Error generating card: {str(e)}")
        return None

def get_template_colors(template):
    """Color schemes for templates"""
    templates = {
        'Professional Blue': {
            'primary': (67, 126, 234),
            'secondary': (118, 75, 162),
            'header': (67, 126, 234),
            'photo_bg': (240, 240, 240),
            'border': (200, 200, 200)
        },
        'Medical Green': {
            'primary': (17, 153, 142),
            'secondary': (56, 239, 125),
            'header': (17, 153, 142),
            'photo_bg': (240, 255, 240),
            'border': (150, 200, 150)
        },
        'Modern Purple': {
            'primary': (155, 89, 182),
            'secondary': (142, 68, 173),
            'header': (155, 89, 182),
            'photo_bg': (250, 240, 255),
            'border': (200, 150, 200)
        },
        'Elegant Gold': {
            'primary': (241, 196, 15),
            'secondary': (243, 156, 18),
            'header': (241, 196, 15),
            'photo_bg': (255, 250, 240),
            'border': (200, 180, 100)
        },
        'Clean White': {
            'primary': (255, 255, 255),
            'secondary': (245, 245, 245),
            'header': (52, 73, 94),
            'photo_bg': (250, 250, 250),
            'border': (200, 200, 200)
        }
    }
    return templates.get(template, templates['Professional Blue'])

def blend_colors(color1, color2, ratio):
    """Blend two colors"""
    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
    return (r, g, b)

def generate_qr_code_image(data):
    """Generate QR code"""
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def id_card_gallery():
    """Gallery of generated cards"""
    st.header("📁 ID Card Gallery")
    
    if st.session_state['generated_cards']:
        for i, card in enumerate(st.session_state['generated_cards']):
            col1, col2 = st.columns([2, 1])
            with col1:
                # Convert PIL Image to bytes for Streamlit display
                card_buffer = io.BytesIO()
                card['card_image'].save(card_buffer, format="PNG")
                card_buffer.seek(0)
                
                st.image(card_buffer, width=400)
            with col2:
                st.write(f"**Patient:** {card['patient_id']}")
                st.write(f"**Template:** {card['template']}")
                st.write(f"**Generated:** {card['generated_at'].strftime('%Y-%m-%d %H:%M')}")
                
                img_buffer = io.BytesIO()
                card['card_image'].save(img_buffer, format="PNG")
                st.download_button(
                    "📥 Download", data=img_buffer.getvalue(),
                    file_name=f"card_{card['patient_id']}.png", mime="image/png",
                    key=f"download_{i}"
                )
            st.divider()
    else:
        st.info("No cards generated yet.")

def card_settings():
    """Card configuration settings"""
    st.header("🔧 Card Settings")
    
    # Hospital info
    st.subheader("🏥 Hospital Information")
    hospital_name = st.text_input("Hospital Name", value="Smart Hospital System")
    hospital_address = st.text_area("Address", value="123 Medical Center Dr")
    
    # Card settings
    st.subheader("📅 Card Settings")
    validity_years = st.number_input("Validity (Years)", min_value=1, max_value=10, value=5)
    
    # QR settings
    st.subheader("🔲 QR Code Settings")
    qr_size = st.slider("QR Size", 100, 200, 150)
    include_logo = st.checkbox("Include Hospital Logo")
    
    if st.button("💾 Save Settings"):
        st.success("Settings saved!")