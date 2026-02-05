import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from utils.database import db
from utils.auth import auth_manager, login_required

@login_required
def digital_prescription():
    """Digital prescription management"""
    st.title("💊 Digital Prescription System")
    
    tabs = st.tabs(["📝 Create Prescription", "📋 View Prescriptions", "🔍 Search Medications", "➕ Add Medicine", "📊 Medicine Inventory"])
    
    with tabs[0]:
        create_prescription()
    with tabs[1]:
        view_prescriptions()
    with tabs[2]:
        medication_search()
    with tabs[3]:
        add_medicine()
    with tabs[4]:
        medicine_inventory()

def create_prescription():
    """Create new prescription"""
    st.header("Create New Prescription")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Patient selection
        patients_df = db.get_patients()
        if not patients_df.empty:
            patient_options = [f"{row['patient_id']} - {row['first_name']} {row['last_name']}" 
                             for _, row in patients_df.iterrows()]
            selected_patient = st.selectbox("Select Patient", patient_options)
            patient_id = selected_patient.split(' - ')[0] if selected_patient else None
        
        # Diagnosis
        diagnosis = st.text_area("Diagnosis", placeholder="Enter diagnosis...")
        
        # Prescription date
        prescription_date = st.date_input("Prescription Date", value=date.today())
    
    with col2:
        # Doctor info (auto-filled based on current user)
        user = auth_manager.get_current_user()
        st.text_input("Prescribing Doctor", value=f"Dr. {user['username']}", disabled=True)
        
        # Valid until
        valid_until = st.date_input("Valid Until", value=date.today() + timedelta(days=30))
    
    # Medications
    st.subheader("Medications")
    
    if 'medications' not in st.session_state:
        st.session_state.medications = []
    
    # Add medication form
    with st.expander("Add Medication", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            med_name = st.text_input("Medication Name")
        with col2:
            dosage = st.text_input("Dosage", placeholder="e.g., 500mg")
        with col3:
            frequency = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "Four times daily", "As needed"])
        with col4:
            duration = st.text_input("Duration", placeholder="e.g., 7 days")
        
        instructions = st.text_area("Special Instructions", placeholder="Take with food, etc.")
        
        if st.button("Add Medication"):
            if med_name and dosage:
                st.session_state.medications.append({
                    'name': med_name,
                    'dosage': dosage,
                    'frequency': frequency,
                    'duration': duration,
                    'instructions': instructions
                })
                st.success("Medication added!")
                st.rerun()
    
    # Display added medications
    if st.session_state.medications:
        st.subheader("Added Medications")
        for i, med in enumerate(st.session_state.medications):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{med['name']}** - {med['dosage']} - {med['frequency']} - {med['duration']}")
                if med['instructions']:
                    st.write(f"*Instructions: {med['instructions']}*")
            with col2:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.medications.pop(i)
                    st.rerun()
    
    # Generate prescription
    if st.button("Generate Prescription", type="primary"):
        if patient_id and diagnosis and st.session_state.medications:
            prescription_id = generate_prescription(patient_id, diagnosis, st.session_state.medications)
            st.success(f"Prescription generated successfully! ID: {prescription_id}")
            st.session_state.medications = []
        else:
            st.error("Please fill in all required fields and add at least one medication.")

def generate_prescription(patient_id, diagnosis, medications):
    """Generate prescription ID and save to database"""
    from datetime import datetime, timedelta
    
    user = auth_manager.get_current_user()
    doctor_id = f"DR{user['id']:03d}"  # Generate doctor ID from user ID
    
    prescription_data = {
        'patient_id': patient_id,
        'doctor_id': doctor_id,
        'medications': medications,
        'issued_date': datetime.now().date(),
        'expiry_date': datetime.now().date() + timedelta(days=30),
        'instructions': diagnosis
    }
    
    prescription_id = db.create_prescription(prescription_data)
    
    # Log the action
    db.log_action(user['id'], 'create_prescription', 'prescriptions', prescription_id)
    
    return prescription_id

def view_prescriptions():
    """View existing prescriptions"""
    st.header("📋 View Prescriptions")
    
    user = auth_manager.get_current_user()
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if user['role'] == 'admin':
            view_type = st.selectbox("View Type", ["All Prescriptions", "My Prescriptions", "By Patient", "By Doctor"], key="prescription_view_type")
        elif user['role'] == 'doctor':
            view_type = st.selectbox("View Type", ["My Prescriptions", "By Patient"], key="prescription_view_type_doctor")
        else:
            view_type = "My Prescriptions"
    
    with col2:
        if view_type in ["By Patient", "All Prescriptions"]:
            # Get patients for dropdown
            patients_df = db.get_patients()
            if not patients_df.empty:
                patient_options = ["All"] + [f"{row['patient_id']} - {row['first_name']} {row['last_name']}" 
                                           for _, row in patients_df.iterrows()]
                selected_patient = st.selectbox("Select Patient", patient_options, key="prescription_patient_filter")
                patient_filter = None if selected_patient == "All" else selected_patient.split(' - ')[0]
            else:
                patient_filter = None
        else:
            patient_filter = None
    
    with col3:
        date_filter = st.date_input("From Date", value=None)
    
    # Get prescriptions based on filters
    if view_type == "My Prescriptions" and user['role'] in ['doctor', 'patient']:
        if user['role'] == 'doctor':
            doctor_id = f"DR{user['id']:03d}"
            prescriptions_df = db.get_prescriptions(doctor_id=doctor_id)
        else:  # patient
            patient_id = f"PAT{user['id']:03d}"
            prescriptions_df = db.get_prescriptions(patient_id=patient_id)
    elif view_type == "By Patient" and patient_filter:
        prescriptions_df = db.get_prescriptions(patient_id=patient_filter)
    else:
        prescriptions_df = db.get_prescriptions()
    
    if not prescriptions_df.empty:
        st.subheader(f"📊 Found {len(prescriptions_df)} prescriptions")
        
        # Display prescriptions
        for idx, prescription in prescriptions_df.iterrows():
            with st.expander(f"📝 {prescription['prescription_id']} - {prescription['issued_date']}", expanded=False):
                
                col_a, col_b = st.columns([2, 1])
                
                with col_a:
                    st.markdown(f"**Prescription ID:** {prescription['prescription_id']}")
                    st.markdown(f"**Patient ID:** {prescription['patient_id']}")
                    st.markdown(f"**Doctor ID:** {prescription['doctor_id']}")
                    st.markdown(f"**Issued Date:** {prescription['issued_date']}")
                    st.markdown(f"**Expiry Date:** {prescription['expiry_date']}")
                    st.markdown(f"**Status:** {prescription['status'].title()}")
                    
                    if prescription['instructions']:
                        st.markdown(f"**Instructions:** {prescription['instructions']}")
                
                with col_b:
                    # Action buttons
                    if st.button(f"📜 View Details", key=f"view_{prescription['prescription_id']}"):
                        show_prescription_details(prescription)
                    
                    if user['role'] in ['admin', 'doctor'] and prescription['status'] == 'active':
                        if st.button(f"❌ Cancel", key=f"cancel_{prescription['prescription_id']}"):
                            # Update prescription status to cancelled
                            st.success("Prescription cancelled")
                
                # Show medications if available
                if prescription['medications']:
                    try:
                        import json
                        medications = json.loads(prescription['medications']) if isinstance(prescription['medications'], str) else prescription['medications']
                        st.markdown("**Medications:**")
                        for med in medications:
                            if isinstance(med, dict):
                                st.write(f"• {med.get('name', 'Unknown')} - {med.get('dosage', 'N/A')} - {med.get('frequency', 'N/A')} - {med.get('duration', 'N/A')}")
                            else:
                                st.write(f"• {med}")
                    except:
                        st.write(f"• {prescription['medications']}")
    
    else:
        st.info("📝 No prescriptions found matching your criteria.")

def show_prescription_details(prescription):
    """Show detailed prescription information"""
    st.markdown("---")
    st.subheader(f"📜 Prescription Details - {prescription['prescription_id']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Prescription ID:** {prescription['prescription_id']}")
        st.markdown(f"**Patient ID:** {prescription['patient_id']}")
        st.markdown(f"**Doctor ID:** {prescription['doctor_id']}")
        st.markdown(f"**Issued Date:** {prescription['issued_date']}")
        st.markdown(f"**Expiry Date:** {prescription['expiry_date']}")
        st.markdown(f"**Status:** {prescription['status'].title()}")
        
        if prescription['instructions']:
            st.markdown(f"**Instructions/Diagnosis:** {prescription['instructions']}")
    
    with col2:
        st.markdown("**Actions:**")
        if st.button("🖨️ Print Prescription"):
            st.success("Prescription sent to printer!")
        
        if st.button("📧 Email to Patient"):
            st.success("Prescription emailed to patient!")
    
    # Show detailed medications
    if prescription['medications']:
        st.markdown("**Prescribed Medications:**")
        try:
            import json
            medications = json.loads(prescription['medications']) if isinstance(prescription['medications'], str) else prescription['medications']
            
            for i, med in enumerate(medications, 1):
                st.markdown(f"**{i}. {med.get('name', 'Unknown Medicine')}**")
                if isinstance(med, dict):
                    if med.get('dosage'):
                        st.write(f"   • Dosage: {med['dosage']}")
                    if med.get('frequency'):
                        st.write(f"   • Frequency: {med['frequency']}")
                    if med.get('duration'):
                        st.write(f"   • Duration: {med['duration']}")
                    if med.get('instructions'):
                        st.write(f"   • Instructions: {med['instructions']}")
        except:
            st.write(prescription['medications'])

def medication_search():
    """Search medication database"""
    st.header("🔍 Medication Search & Information")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search medications...", placeholder="Enter medicine name, indication, or symptom")
    
    with col2:
        category_filter = st.selectbox("Category", ["All"] + db.get_medicine_categories(), key="search_category_filter")
    
    with col3:
        prescription_filter = st.selectbox("Prescription Type", ["All", "Prescription Required", "Over-the-Counter"], key="search_prescription_filter")
    
    # Get medicines from database
    if search_term or category_filter != "All":
        category = None if category_filter == "All" else category_filter
        medicines_df = db.get_medicines(search_term=search_term, category=category)
        
        # Apply prescription filter
        if prescription_filter == "Prescription Required":
            medicines_df = medicines_df[medicines_df['prescription_required'] == 1]
        elif prescription_filter == "Over-the-Counter":
            medicines_df = medicines_df[medicines_df['prescription_required'] == 0]
        
        if not medicines_df.empty:
            st.subheader(f"📋 Found {len(medicines_df)} medications")
            
            # Display medicines in cards
            for idx, medicine in medicines_df.iterrows():
                with st.expander(f"💊 {medicine['name']} ({medicine['strength']}) - {medicine['category']}", expanded=False):
                    
                    col_a, col_b, col_c = st.columns([2, 2, 1])
                    
                    with col_a:
                        st.markdown(f"**Generic Name:** {medicine['generic_name'] or 'N/A'}")
                        st.markdown(f"**Brand Name:** {medicine['brand_name'] or 'N/A'}")
                        st.markdown(f"**Category:** {medicine['category']}")
                        st.markdown(f"**Type:** {medicine['type']}")
                        st.markdown(f"**Strength:** {medicine['strength']} {medicine['unit'] or ''}")
                        st.markdown(f"**Manufacturer:** {medicine['manufacturer'] or 'N/A'}")
                    
                    with col_b:
                        st.markdown(f"**Indications:** {medicine['indications'] or 'N/A'}")
                        st.markdown(f"**Dosage Form:** {medicine['dosage_form'] or 'N/A'}")
                        st.markdown(f"**Route:** {medicine['route_of_administration'] or 'N/A'}")
                        st.markdown(f"**Price:** ₹{medicine['price']:.2f}")
                        prescription_status = "🔒 Prescription Required" if medicine['prescription_required'] else "🛍️ Over-the-Counter"
                        st.markdown(f"**Type:** {prescription_status}")
                    
                    with col_c:
                        stock_color = "green" if medicine['stock_quantity'] > medicine['minimum_stock'] else "red"
                        st.markdown(f"**Stock:** <span style='color: {stock_color}'>{medicine['stock_quantity']}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Min Stock:** {medicine['minimum_stock']}")
                        
                        if st.button(f"➕ Add to Prescription", key=f"add_{medicine['medicine_id']}"):
                            if 'prescription_medicines' not in st.session_state:
                                st.session_state.prescription_medicines = []
                            
                            medicine_info = {
                                'id': medicine['medicine_id'],
                                'name': medicine['name'],
                                'strength': medicine['strength'],
                                'type': medicine['type']
                            }
                            
                            if medicine_info not in st.session_state.prescription_medicines:
                                st.session_state.prescription_medicines.append(medicine_info)
                                st.success(f"Added {medicine['name']} to prescription!")
                            else:
                                st.warning("Medicine already in prescription")
                    
                    # Detailed information
                    if medicine['description']:
                        st.markdown(f"**Description:** {medicine['description']}")
                    
                    if medicine['contraindications']:
                        st.warning(f"⚠️ **Contraindications:** {medicine['contraindications']}")
                    
                    if medicine['side_effects']:
                        st.info(f"📊 **Side Effects:** {medicine['side_effects']}")
                    
                    if medicine['storage_conditions']:
                        st.info(f"🌡️ **Storage:** {medicine['storage_conditions']}")
        else:
            st.info("🔍 No medications found matching your search criteria.")
    
    else:
        # Show popular medicines or recent searches
        st.subheader("🔥 Popular Medications")
        
        popular_medicines = [
            {
                'name': 'Paracetamol',
                'indication': 'Fever, Headache, Body Pain',
                'strength': '500mg',
                'type': 'Tablet'
            },
            {
                'name': 'Ibuprofen', 
                'indication': 'Pain, Inflammation',
                'strength': '400mg',
                'type': 'Tablet'
            },
            {
                'name': 'Cetirizine',
                'indication': 'Allergies, Cold symptoms',
                'strength': '10mg',
                'type': 'Tablet'
            },
            {
                'name': 'Amoxicillin',
                'indication': 'Bacterial infections',
                'strength': '250mg',
                'type': 'Capsule'
            }
        ]
        
        cols = st.columns(4)
        for i, med in enumerate(popular_medicines):
            with cols[i]:
                with st.container():
                    st.markdown(f"**{med['name']}**")
                    st.markdown(f"*{med['indication']}*")
                    st.markdown(f"{med['strength']} {med['type']}")
                    if st.button(f"🔍 Search", key=f"search_{med['name']}"):
                        st.session_state.search_term = med['name']
                        st.rerun()
    
    # Show selected medicines for prescription
    if 'prescription_medicines' in st.session_state and st.session_state.prescription_medicines:
        st.markdown("---")
        st.subheader("📜 Selected Medicines for Prescription")
        
        for i, med in enumerate(st.session_state.prescription_medicines):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{med['name']}** - {med['strength']} {med['type']}")
            with col2:
                if st.button("❌ Remove", key=f"remove_selected_{i}"):
                    st.session_state.prescription_medicines.pop(i)
                    st.rerun()

def add_medicine():
    """Add new medicine to the database"""
    st.header("➕ Add New Medicine")
    
    # Check permissions
    user = auth_manager.get_current_user()
    if user['role'] not in ['admin', 'doctor']:
        st.error("🚫 Access Denied: Only administrators and doctors can add new medicines.")
        return
    
    st.markdown("👨‍⚕️ **Add medicines to help patients with their treatment**")
    
    with st.form("add_medicine_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Basic Information")
            medicine_name = st.text_input("Medicine Name*", placeholder="e.g., Paracetamol")
            generic_name = st.text_input("Generic Name", placeholder="e.g., Acetaminophen")
            brand_name = st.text_input("Brand Name", placeholder="e.g., Tylenol")
            
            category = st.selectbox("Category*", [
                "Analgesic", "Antibiotic", "Antiviral", "Antifungal", "NSAID", 
                "Antihistamine", "Antidiabetic", "Antihypertensive", "Cardiovascular",
                "Respiratory", "Gastrointestinal", "Neurological", "Psychiatric",
                "Dermatological", "Ophthalmological", "Other"
            ], key="add_medicine_category")
            
            medicine_type = st.selectbox("Type*", [
                "Tablet", "Capsule", "Syrup", "Injection", "Cream", "Ointment",
                "Drops", "Inhaler", "Patch", "Suppository", "Other"
            ], key="add_medicine_type")
            
            strength = st.text_input("Strength", placeholder="e.g., 500mg, 10ml")
            unit = st.selectbox("Unit", ["mg", "g", "ml", "mcg", "IU", "%", "Other"], key="add_medicine_unit")
        
        with col2:
            st.subheader("🏢 Manufacturer & Details")
            manufacturer = st.text_input("Manufacturer", placeholder="e.g., Generic Pharma Ltd.")
            
            dosage_form = st.selectbox("Dosage Form", [
                "Oral", "Topical", "Injectable", "Inhalable", "Sublingual", 
                "Rectal", "Ophthalmic", "Otic", "Nasal", "Other"
            ], key="add_medicine_dosage_form")
            
            route_admin = st.selectbox("Route of Administration", [
                "Oral", "Intravenous", "Intramuscular", "Subcutaneous", "Topical",
                "Inhalation", "Sublingual", "Rectal", "Ophthalmic", "Other"
            ], key="add_medicine_route")
            
            price = st.number_input("Price per Unit (₹)", min_value=0.0, value=0.0, step=0.01)
            
            prescription_required = st.checkbox("Prescription Required", value=False)
        
        st.subheader("📝 Medical Information")
        
        col3, col4 = st.columns(2)
        
        with col3:
            description = st.text_area("Description", placeholder="Brief description of the medicine")
            indications = st.text_area("Indications", placeholder="What conditions this medicine treats")
            contraindications = st.text_area("Contraindications", placeholder="When not to use this medicine")
        
        with col4:
            side_effects = st.text_area("Side Effects", placeholder="Possible side effects")
            storage_conditions = st.text_area("Storage Conditions", placeholder="How to store this medicine")
            shelf_life = st.text_input("Shelf Life", placeholder="e.g., 3 years, 24 months")
        
        st.subheader("📦 Inventory Information")
        
        col5, col6 = st.columns(2)
        
        with col5:
            stock_quantity = st.number_input("Initial Stock Quantity", min_value=0, value=0)
        
        with col6:
            minimum_stock = st.number_input("Minimum Stock Level", min_value=1, value=10)
        
        # Submit button
        st.markdown("---")
        submitted = st.form_submit_button("➕ Add Medicine", type="primary", use_container_width=True)
        
        if submitted:
            if not medicine_name or not category or not medicine_type:
                st.error("❌ Please fill in all required fields marked with *")
            else:
                medicine_data = {
                    'name': medicine_name,
                    'generic_name': generic_name,
                    'brand_name': brand_name,
                    'category': category,
                    'type': medicine_type,
                    'strength': strength,
                    'unit': unit,
                    'manufacturer': manufacturer,
                    'description': description,
                    'indications': indications,
                    'contraindications': contraindications,
                    'side_effects': side_effects,
                    'dosage_form': dosage_form,
                    'route_of_administration': route_admin,
                    'storage_conditions': storage_conditions,
                    'shelf_life': shelf_life,
                    'price': price,
                    'stock_quantity': stock_quantity,
                    'minimum_stock': minimum_stock,
                    'prescription_required': prescription_required
                }
                
                medicine_id = db.add_medicine(medicine_data)
                
                if medicine_id:
                    st.success(f"✓ Medicine '{medicine_name}' has been successfully added!")
                    st.info(f"🏷️ Medicine ID: {medicine_id}")
                    
                    # Log the action
                    db.log_action(user['id'], 'add_medicine', 'medicines', medicine_id)
                else:
                    st.error("❌ Failed to add medicine. Medicine name might already exist.")

def medicine_inventory():
    """Medicine inventory management"""
    st.header("📊 Medicine Inventory Management")
    
    # Check permissions
    user = auth_manager.get_current_user()
    if user['role'] not in ['admin', 'doctor', 'nurse']:
        st.error("🚫 Access Denied: Only administrators, doctors, and nurses can view inventory.")
        return
    
    # Get all medicines
    medicines_df = db.get_medicines()
    
    if not medicines_df.empty:
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_medicines = len(medicines_df)
            st.metric("📊 Total Medicines", total_medicines)
        
        with col2:
            low_stock = len(medicines_df[medicines_df['stock_quantity'] <= medicines_df['minimum_stock']])
            st.metric("⚠️ Low Stock Items", low_stock, delta=f"-{low_stock}" if low_stock > 0 else "0")
        
        with col3:
            total_value = (medicines_df['stock_quantity'] * medicines_df['price']).sum()
            st.metric("💰 Total Inventory Value", f"₹{total_value:,.2f}")
        
        with col4:
            prescription_medicines = len(medicines_df[medicines_df['prescription_required'] == 1])
            st.metric("🔒 Prescription Medicines", prescription_medicines)
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_filter = st.selectbox("Filter by Category", ["All"] + list(medicines_df['category'].unique()), key="inventory_category_filter")
        
        with col2:
            stock_filter = st.selectbox("Stock Status", ["All", "Low Stock", "Out of Stock", "In Stock"], key="inventory_stock_filter")
        
        with col3:
            prescription_filter = st.selectbox("Prescription Type", ["All", "Prescription Required", "Over-the-Counter"], key="inventory_prescription_filter")
        
        # Apply filters
        filtered_df = medicines_df.copy()
        
        if category_filter != "All":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
        
        if stock_filter == "Low Stock":
            filtered_df = filtered_df[filtered_df['stock_quantity'] <= filtered_df['minimum_stock']]
        elif stock_filter == "Out of Stock":
            filtered_df = filtered_df[filtered_df['stock_quantity'] == 0]
        elif stock_filter == "In Stock":
            filtered_df = filtered_df[filtered_df['stock_quantity'] > 0]
        
        if prescription_filter == "Prescription Required":
            filtered_df = filtered_df[filtered_df['prescription_required'] == 1]
        elif prescription_filter == "Over-the-Counter":
            filtered_df = filtered_df[filtered_df['prescription_required'] == 0]
        
        # Display results
        st.subheader(f"📋 Inventory List ({len(filtered_df)} items)")
        
        if not filtered_df.empty:
            # Display as expandable cards
            for idx, medicine in filtered_df.iterrows():
                # Determine stock status color
                if medicine['stock_quantity'] == 0:
                    stock_status = "🔴 Out of Stock"
                    stock_color = "red"
                elif medicine['stock_quantity'] <= medicine['minimum_stock']:
                    stock_status = "🟡 Low Stock"
                    stock_color = "orange"
                else:
                    stock_status = "🟢 In Stock"
                    stock_color = "green"
                
                with st.expander(f"💊 {medicine['name']} ({medicine['strength']}) - {stock_status}", expanded=False):
                    
                    col_a, col_b, col_c = st.columns([2, 2, 1])
                    
                    with col_a:
                        st.markdown(f"**Medicine ID:** {medicine['medicine_id']}")
                        st.markdown(f"**Generic Name:** {medicine['generic_name'] or 'N/A'}")
                        st.markdown(f"**Category:** {medicine['category']}")
                        st.markdown(f"**Type:** {medicine['type']}")
                        st.markdown(f"**Manufacturer:** {medicine['manufacturer'] or 'N/A'}")
                    
                    with col_b:
                        st.markdown(f"**Current Stock:** <span style='color: {stock_color}'>{medicine['stock_quantity']}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Minimum Stock:** {medicine['minimum_stock']}")
                        st.markdown(f"**Price per Unit:** ₹{medicine['price']:.2f}")
                        st.markdown(f"**Total Value:** ₹{(medicine['stock_quantity'] * medicine['price']):.2f}")
                        prescription_status = "🔒 Prescription Required" if medicine['prescription_required'] else "🛍️ Over-the-Counter"
                        st.markdown(f"**Type:** {prescription_status}")
                    
                    with col_c:
                        if user['role'] in ['admin']:
                            new_stock = st.number_input(f"Update Stock", min_value=0, value=int(medicine['stock_quantity']), key=f"stock_{medicine['medicine_id']}")
                            
                            if st.button(f"💾 Update", key=f"update_{medicine['medicine_id']}"):
                                # Update stock in database
                                update_data = dict(medicine)
                                update_data['stock_quantity'] = new_stock
                                
                                if db.update_medicine(medicine['medicine_id'], update_data):
                                    st.success("✓ Stock updated!")
                                    st.rerun()
                                else:
                                    st.error("❌ Update failed")
                    
                    # Show additional details if available
                    if medicine['indications']:
                        st.markdown(f"**Indications:** {medicine['indications']}")
        else:
            st.info("🔍 No medicines found matching the selected criteria.")
    
    else:
        st.warning("📦 No medicines found in inventory. Add some medicines to get started!")