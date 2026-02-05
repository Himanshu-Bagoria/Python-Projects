import streamlit as st
import pandas as pd
from datetime import datetime
from utils.auth import login_required
from utils.ui_components import UIComponents

@login_required
def popup_catalogs():
    """Interactive popup catalogs for hospital services and procedures"""
    st.title("🏥 Hospital Services & Procedures Catalog")
    
    # Create colorful header
    st.markdown("""
    <div class="gradient-text" style="text-align: center; font-size: 1.2em; margin-bottom: 2rem;">
        Browse our comprehensive catalog of medical services, departments, and procedures
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs with icons
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🩺 Medical Services", "🏥 Departments", "👨‍⚕️ Attending Doctors", "⚕️ Procedures", 
        "💰 Pricing", "📋 Service Requests"
    ])
    
    with tab1:
        medical_services_catalog()
    
    with tab2:
        departments_catalog()
    
    with tab3:
        attending_doctors_catalog()
    
    with tab4:
        procedures_catalog()
    
    with tab5:
        pricing_catalog()
    
    with tab6:
        service_requests()

def medical_services_catalog():
    """Medical services catalog with interactive cards"""
    st.header("🩺 Medical Services Catalog")
    
    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_service = st.text_input("🔍 Search Services", placeholder="Search by service name or category...")
    
    with col2:
        category_filter = st.selectbox("Filter by Category", [
            "All", "Emergency", "Diagnostic", "Surgical", "Therapeutic", "Preventive"
        ])
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Name", "Price", "Duration", "Popularity"])
    
    # Services data
    services_data = get_medical_services_data()
    
    # Apply filters
    filtered_services = apply_service_filters(services_data, search_service, category_filter)
    
    # Display services in interactive cards
    if not filtered_services.empty:
        st.subheader(f"📊 Found {len(filtered_services)} services")
        
        # Create grid layout
        cols = st.columns(2)
        
        for idx, service in filtered_services.iterrows():
            with cols[idx % 2]:
                render_service_card(service, idx)
    else:
        st.info("No services found matching your criteria.")
    
    # Quick action buttons
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    
    action_buttons = [
        {
            "label": "📞 Emergency Services",
            "action": lambda: show_emergency_popup(),
            "key": "emergency_btn",
            "type": "primary"
        },
        {
            "label": "🩺 Book Health Checkup",
            "action": lambda: show_health_checkup_popup(),
            "key": "checkup_btn"
        },
        {
            "label": "💊 Pharmacy Services",
            "action": lambda: show_pharmacy_popup(),
            "key": "pharmacy_btn"
        },
        {
            "label": "🚑 Ambulance Service",
            "action": lambda: show_ambulance_popup(),
            "key": "ambulance_btn"
        }
    ]
    
    UIComponents.render_action_buttons(action_buttons, layout="horizontal")

def departments_catalog():
    """Interactive departments catalog"""
    st.header("🏥 Hospital Departments")
    
    # Department data
    departments = get_departments_data()
    
    # Display departments in showcase format
    st.subheader("🎯 Our Specialized Departments")
    
    UIComponents.render_feature_showcase(departments, columns=3)
    
    # Department details in expandable cards
    st.subheader("📋 Detailed Department Information")
    
    for dept in departments:
        with st.expander(f"{dept['icon']} {dept['title']}", expanded=False):
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {dept['description']}")
                st.markdown(f"**Services Offered:**")
                
                services = dept.get('services', [])
                for service in services:
                    st.markdown(f"• {service}")
                
                st.markdown(f"**Specialties:**")
                specialties = dept.get('specialties', [])
                for specialty in specialties:
                    st.markdown(f"• {specialty}")
            
            with col2:
                st.markdown("**Department Head:**")
                st.info(dept.get('head', 'TBD'))
                
                st.markdown("**Contact:**")
                st.info(dept.get('contact', 'Available 24/7'))
                
                st.markdown("**Location:**")
                st.info(dept.get('location', 'Ground Floor'))
                
                # Action buttons for each department
                if st.button(f"🔍 View Details", key=f"view_{dept['title']}"):
                    show_department_details_popup(dept)
                
                if st.button(f"📅 Book Appointment", key=f"book_{dept['title']}"):
                    show_appointment_booking_popup(dept)

def attending_doctors_catalog():
    """Interactive attending doctors catalog"""
    st.header("👨‍⚕️ Attending Doctors Catalog")
    
    # Search and filter section
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_doctor = st.text_input("🔍 Search Doctors", placeholder="Search by name, specialization, or department...")
    
    with col2:
        specialty_filter = st.selectbox("Filter by Specialty", [
            "All", "Cardiology", "Neurology", "Orthopedics", "Pediatrics", 
            "General Medicine", "Emergency Medicine", "Surgery", "Gynecology"
        ])
    
    with col3:
        availability_filter = st.selectbox("Availability", ["All", "Available Today", "Available This Week"])
    
    # Get attending doctors data
    doctors_data = get_attending_doctors_data()
    
    # Apply filters
    filtered_doctors = apply_doctor_filters(doctors_data, search_doctor, specialty_filter, availability_filter)
    
    if not filtered_doctors.empty:
        st.subheader(f"📊 Found {len(filtered_doctors)} attending doctors")
        
        # Display doctors in cards
        cols = st.columns(2)
        
        for idx, doctor in filtered_doctors.iterrows():
            with cols[idx % 2]:
                render_doctor_card(doctor, idx)
    else:
        st.info("No doctors found matching your criteria.")
    
    # Quick actions for doctor booking
    st.markdown("---")
    st.subheader("🚀 Quick Doctor Actions")
    
    quick_actions = [
        {
            "label": "🚑 Emergency Doctor",
            "action": lambda: show_emergency_doctor_popup(),
            "key": "emergency_doctor_btn",
            "type": "primary"
        },
        {
            "label": "👨‍⚕️ Book Consultation",
            "action": lambda: show_consultation_booking_popup(),
            "key": "consultation_btn"
        },
        {
            "label": "📞 Telemedicine",
            "action": lambda: show_telemedicine_popup(),
            "key": "telemedicine_btn"
        },
        {
            "label": "🔍 Find Specialist",
            "action": lambda: show_specialist_finder_popup(),
            "key": "specialist_btn"
        }
    ]
    
    UIComponents.render_action_buttons(quick_actions, layout="horizontal")

def procedures_catalog():
    """Medical procedures catalog with detailed information"""
    st.header("⚕️ Medical Procedures Catalog")
    
    # Procedure categories
    procedure_categories = get_procedures_data()
    
    # Category navigation
    selected_category = st.selectbox(
        "📂 Select Procedure Category",
        list(procedure_categories.keys())
    )
    
    if selected_category:
        procedures = procedure_categories[selected_category]
        
        st.subheader(f"📋 {selected_category}")
        
        # Display procedures in a data table
        procedures_df = pd.DataFrame(procedures)
        
        # Enhanced table with search and export
        UIComponents.render_data_table(
            procedures_df,
            title=f"{selected_category} Procedures",
            searchable=True,
            exportable=True,
            table_key="procedures_catalog"
        )
        
        # Procedure comparison tool
        st.subheader("⚖️ Compare Procedures")
        
        selected_procedures = st.multiselect(
            "Select procedures to compare",
            procedures_df['Name'].tolist(),
            max_selections=3
        )
        
        if selected_procedures:
            comparison_data = procedures_df[procedures_df['Name'].isin(selected_procedures)]
            
            # Create comparison chart
            UIComponents.render_chart_selector(comparison_data)

def pricing_catalog():
    """Pricing catalog with interactive pricing tool"""
    st.header("💰 Pricing Information")
    
    # Pricing calculator
    st.subheader("🧮 Pricing Calculator")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Service Selection**")
        
        service_type = st.selectbox("Service Type", [
            "Consultation", "Diagnostic Test", "Surgical Procedure", "Emergency Service"
        ])
        
        if service_type == "Consultation":
            specialty = st.selectbox("Specialty", [
                "General Medicine", "Cardiology", "Neurology", "Orthopedics"
            ])
            doctor_level = st.selectbox("Doctor Level", [
                "Junior Doctor", "Senior Doctor", "Consultant", "HOD"
            ])
        
        elif service_type == "Diagnostic Test":
            test_category = st.selectbox("Test Category", [
                "Blood Tests", "Imaging", "Specialized Tests"
            ])
            urgency = st.selectbox("Urgency", ["Routine", "Urgent", "Emergency"])
        
        insurance_coverage = st.number_input("Insurance Coverage (%)", 0, 100, 70)
        
        if st.button("💰 Calculate Price", type="primary"):
            calculated_price = calculate_service_price(service_type, locals())
            display_pricing_results(calculated_price, insurance_coverage)
    
    with col2:
        st.markdown("**Pricing Breakdown**")
        
        # Sample pricing data
        pricing_data = get_pricing_data()
        
        # Display pricing in metric cards
        UIComponents.render_stats_grid(pricing_data, columns=2)
    
    # Insurance information
    st.subheader("🏥 Insurance Information")
    
    insurance_info = [
        {
            "title": "Accepted Insurance Plans",
            "description": "We accept all major insurance providers including government schemes",
            "colors": ["#11998e", "#38ef7d"],
            "icon": "🏥"
        },
        {
            "title": "Cashless Treatment",
            "description": "Direct billing available for approved insurance policies",
            "colors": ["#667eea", "#764ba2"],
            "icon": "💳"
        },
        {
            "title": "Payment Plans",
            "description": "Flexible payment options and EMI facilities available",
            "colors": ["#fa709a", "#fee140"],
            "icon": "💰"
        }
    ]
    
    UIComponents.render_feature_showcase(insurance_info, columns=3)

def service_requests():
    """Service request system"""
    st.header("📋 Service Requests")
    
    # Request new service
    st.subheader("➕ Request New Service")
    
    with st.form("service_request"):
        col1, col2 = st.columns(2)
        
        with col1:
            service_name = st.text_input("Service Name*")
            service_category = st.selectbox("Category", [
                "Medical Service", "Administrative", "Support Service", "Emergency"
            ])
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
        
        with col2:
            requested_date = st.date_input("Preferred Date")
            requested_time = st.time_input("Preferred Time")
            contact_phone = st.text_input("Contact Phone")
        
        description = st.text_area("Service Description*", 
                                 placeholder="Describe the service you need...")
        
        special_requirements = st.text_area("Special Requirements", 
                                          placeholder="Any special needs or requirements...")
        
        # Submit button
        if st.form_submit_button("📤 Submit Request", type="primary"):
            if service_name and description:
                # Save request (simplified for demo)
                request_id = f"REQ{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                UIComponents.render_notification_bar(
                    f"Service request submitted successfully! Request ID: {request_id}",
                    type="success"
                )
                
                # Show confirmation details
                st.markdown("---")
                st.subheader("✅ Request Confirmation")
                
                confirmation_data = {
                    "Request ID": request_id,
                    "Service": service_name,
                    "Category": service_category,
                    "Priority": priority,
                    "Requested Date": requested_date,
                    "Status": "Pending Review"
                }
                
                for key, value in confirmation_data.items():
                    st.write(f"**{key}:** {value}")
            
            else:
                UIComponents.render_notification_bar(
                    "Please fill in all required fields",
                    type="error"
                )
    
    # View existing requests
    st.subheader("📊 Your Service Requests")
    
    # Sample request data
    requests_data = get_sample_requests()
    
    if not requests_data.empty:
        UIComponents.render_data_table(
            requests_data,
            title="Service Requests History",
            searchable=True,
            exportable=True,
            table_key="service_requests"
        )
    else:
        st.info("No service requests found.")

# Helper Functions

def render_service_card(service, idx):
    """Render individual service card"""
    
    # Determine gradient colors based on category
    color_mapping = {
        "Emergency": ["#ff6b6b", "#ee5a52"],
        "Diagnostic": ["#4dabf7", "#339af0"],
        "Surgical": ["#51cf66", "#40c057"],
        "Therapeutic": ["#ffd43b", "#fab005"],
        "Preventive": ["#9775fa", "#845ef7"]
    }
    
    colors = color_mapping.get(service['Category'], ["#667eea", "#764ba2"])
    
    UIComponents.render_gradient_card(
        title=f"{service['Icon']} {service['Name']}",
        content=f"""
        <div style="margin-bottom: 10px;">
            <strong>Category:</strong> {service['Category']}<br>
            <strong>Duration:</strong> {service['Duration']}<br>
            <strong>Price:</strong> <span style="font-size: 1.2em; font-weight: bold;">{service['Price']}</span><br>
            <strong>Description:</strong> {service['Description']}
        </div>
        """,
        gradient_colors=colors,
        icon=service['Icon']
    )
    
    # Add action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"📞 Book Now", key=f"book_service_{idx}"):
            show_service_booking_popup(service)
    
    with col2:
        if st.button(f"ℹ️ Details", key=f"details_service_{idx}"):
            show_service_details_popup(service)

def get_medical_services_data():
    """Get medical services data"""
    return pd.DataFrame({
        'Name': [
            'General Consultation', 'Emergency Care', 'Blood Test', 'X-Ray',
            'MRI Scan', 'Surgery Consultation', 'Health Checkup', 'Vaccination'
        ],
        'Category': [
            'Diagnostic', 'Emergency', 'Diagnostic', 'Diagnostic',
            'Diagnostic', 'Surgical', 'Preventive', 'Preventive'
        ],
        'Price': [
            '₹500', '₹2,000', '₹300', '₹800',
            '₹8,000', '₹1,000', '₹2,500', '₹200'
        ],
        'Duration': [
            '30 min', '24/7', '15 min', '20 min',
            '45 min', '45 min', '2 hours', '10 min'
        ],
        'Description': [
            'Basic medical consultation', 'Emergency medical care', 'Complete blood analysis',
            'Digital X-ray imaging', 'High-resolution MRI scan', 'Pre-surgery consultation',
            'Comprehensive health screening', 'Immunization services'
        ],
        'Icon': ['🩺', '🚨', '🩸', '📱', '🔍', '⚕️', '❤️', '💉']
    })

def get_departments_data():
    """Get departments showcase data"""
    return [
        {
            "title": "Cardiology",
            "description": "Expert heart and cardiovascular care with state-of-the-art facilities",
            "colors": ["#ff6b6b", "#ee5a52"],
            "icon": "❤️",
            "services": ["Heart Surgery", "Angioplasty", "ECG", "Echocardiogram"],
            "specialties": ["Interventional Cardiology", "Cardiac Surgery", "Heart Failure"],
            "head": "Dr. John Smith",
            "contact": "+1-234-567-8901",
            "location": "2nd Floor, East Wing"
        },
        {
            "title": "Neurology", 
            "description": "Advanced brain and nervous system treatment center",
            "colors": ["#4dabf7", "#339af0"],
            "icon": "🧠",
            "services": ["Brain Surgery", "Stroke Care", "Epilepsy Treatment"],
            "specialties": ["Neurosurgery", "Stroke Medicine", "Movement Disorders"],
            "head": "Dr. Sarah Johnson",
            "contact": "+1-234-567-8902",
            "location": "3rd Floor, North Wing"
        },
        {
            "title": "Emergency",
            "description": "24/7 emergency care with rapid response team",
            "colors": ["#51cf66", "#40c057"],
            "icon": "🚨",
            "services": ["Emergency Room", "Trauma Care", "Critical Care"],
            "specialties": ["Emergency Medicine", "Trauma Surgery", "Critical Care"],
            "head": "Dr. Michael Brown",
            "contact": "911",
            "location": "Ground Floor"
        }
    ]

def get_procedures_data():
    """Get procedures data by category"""
    return {
        "Diagnostic Procedures": [
            {"Name": "Blood Test", "Duration": "15 min", "Price": "₹300", "Preparation": "Fasting 12 hours"},
            {"Name": "X-Ray", "Duration": "20 min", "Price": "₹800", "Preparation": "Remove metal objects"},
            {"Name": "MRI Scan", "Duration": "45 min", "Price": "₹8,000", "Preparation": "No metal implants"},
            {"Name": "CT Scan", "Duration": "30 min", "Price": "₹6,000", "Preparation": "Contrast may be used"},
        ],
        "Surgical Procedures": [
            {"Name": "Appendectomy", "Duration": "2 hours", "Price": "₹50,000", "Preparation": "Pre-operative tests"},
            {"Name": "Cataract Surgery", "Duration": "1 hour", "Price": "₹30,000", "Preparation": "Eye drops required"},
            {"Name": "Knee Replacement", "Duration": "3 hours", "Price": "₹2,00,000", "Preparation": "Physical therapy"},
        ],
        "Therapeutic Procedures": [
            {"Name": "Physiotherapy", "Duration": "1 hour", "Price": "₹800", "Preparation": "Comfortable clothing"},
            {"Name": "Chemotherapy", "Duration": "4 hours", "Price": "₹25,000", "Preparation": "Pre-medications"},
            {"Name": "Dialysis", "Duration": "4 hours", "Price": "₹3,500", "Preparation": "Fluid restrictions"},
        ]
    }

def get_pricing_data():
    """Get pricing statistics"""
    return [
        {"title": "Average Consultation", "value": "₹750", "delta": "+5%", "color": "primary", "icon": "💰"},
        {"title": "Emergency Care", "value": "₹2,500", "delta": "24/7", "color": "error", "icon": "🚨"},
        {"title": "Diagnostic Tests", "value": "₹1,200", "delta": "+8%", "color": "info", "icon": "🔬"},
        {"title": "Insurance Coverage", "value": "85%", "delta": "+12%", "color": "success", "icon": "🏥"}
    ]

def get_sample_requests():
    """Get sample service requests"""
    return pd.DataFrame({
        'Request ID': ['REQ001', 'REQ002', 'REQ003'],
        'Service': ['Home Nursing', 'Ambulance Service', 'Lab Test at Home'],
        'Date Requested': ['2025-08-25', '2025-08-24', '2025-08-23'],
        'Priority': ['Medium', 'High', 'Low'],
        'Status': ['In Progress', 'Completed', 'Pending']
    })

def apply_service_filters(data, search_term, category_filter):
    """Apply filters to services data"""
    filtered_data = data.copy()
    
    if search_term:
        filtered_data = filtered_data[
            filtered_data['Name'].str.contains(search_term, case=False) |
            filtered_data['Description'].str.contains(search_term, case=False)
        ]
    
    if category_filter != "All":
        filtered_data = filtered_data[filtered_data['Category'] == category_filter]
    
    return filtered_data

def calculate_service_price(service_type, params):
    """Calculate service price based on parameters"""
    base_prices = {
        "Consultation": 500,
        "Diagnostic Test": 1000,
        "Surgical Procedure": 50000,
        "Emergency Service": 2500
    }
    
    base_price = base_prices.get(service_type, 500)
    
    # Add modifiers based on parameters
    if service_type == "Consultation":
        multipliers = {
            "Junior Doctor": 1.0,
            "Senior Doctor": 1.5,
            "Consultant": 2.0,
            "HOD": 2.5
        }
        base_price *= multipliers.get(params.get('doctor_level', 'Junior Doctor'), 1.0)
    
    return base_price

def get_attending_doctors_data():
    """Get attending doctors data"""
    return pd.DataFrame({
        'Name': [
            'Dr. John Smith', 'Dr. Sarah Johnson', 'Dr. Michael Brown', 'Dr. Emily Davis',
            'Dr. David Wilson', 'Dr. Lisa Garcia', 'Dr. Robert Taylor', 'Dr. Jennifer Lee'
        ],
        'Specialization': [
            'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics',
            'General Medicine', 'Emergency Medicine', 'Surgery', 'Gynecology'
        ],
        'Department': [
            'Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics',
            'General Medicine', 'Emergency', 'Surgery', 'Gynecology'
        ],
        'Experience': [15, 12, 8, 10, 20, 7, 18, 14],
        'Consultation_Fee': [800, 900, 700, 600, 500, 850, 1200, 750],
        'Rating': [4.8, 4.9, 4.7, 4.6, 4.5, 4.8, 4.9, 4.7],
        'Availability': [
            'Available Today', 'Available This Week', 'Available Today', 'Available Today',
            'Available This Week', 'Available Today', 'Available This Week', 'Available Today'
        ],
        'Next_Available': [
            '2025-08-26 2:00 PM', '2025-08-27 10:00 AM', '2025-08-26 3:30 PM', '2025-08-26 11:00 AM',
            '2025-08-28 9:00 AM', '2025-08-26 4:00 PM', '2025-08-27 2:30 PM', '2025-08-26 1:00 PM'
        ],
        'Phone': [
            '+1-234-567-8901', '+1-234-567-8902', '+1-234-567-8903', '+1-234-567-8904',
            '+1-234-567-8905', '+1-234-567-8906', '+1-234-567-8907', '+1-234-567-8908'
        ],
        'Education': [
            'MBBS, MD (Cardiology)', 'MBBS, DM (Neurology)', 'MBBS, MS (Orthopedics)', 'MBBS, MD (Pediatrics)',
            'MBBS, MD (General Medicine)', 'MBBS, DNB (Emergency)', 'MBBS, MS, MCh (Surgery)', 'MBBS, MD (Gynecology)'
        ],
        'Languages': [
            'English, Hindi', 'English, Spanish', 'English, French', 'English, Hindi, Punjabi',
            'English, Hindi', 'English, Spanish, Hindi', 'English, German', 'English, Mandarin'
        ]
    })

def apply_doctor_filters(data, search_term, specialty_filter, availability_filter):
    """Apply filters to doctors data"""
    filtered_data = data.copy()
    
    if search_term:
        filtered_data = filtered_data[
            filtered_data['Name'].str.contains(search_term, case=False) |
            filtered_data['Specialization'].str.contains(search_term, case=False) |
            filtered_data['Department'].str.contains(search_term, case=False)
        ]
    
    if specialty_filter != "All":
        filtered_data = filtered_data[filtered_data['Specialization'] == specialty_filter]
    
    if availability_filter != "All":
        filtered_data = filtered_data[filtered_data['Availability'] == availability_filter]
    
    return filtered_data

def render_doctor_card(doctor, idx):
    """Render individual doctor card"""
    # Specialty color mapping
    color_mapping = {
        "Cardiology": ["#ff6b6b", "#ee5a52"],
        "Neurology": ["#4dabf7", "#339af0"],
        "Orthopedics": ["#51cf66", "#40c057"],
        "Pediatrics": ["#ffd43b", "#fab005"],
        "General Medicine": ["#9775fa", "#845ef7"],
        "Emergency Medicine": ["#ff8cc8", "#fd79a8"],
        "Surgery": ["#00b894", "#00a085"],
        "Gynecology": ["#fd79a8", "#e84393"]
    }
    
    colors = color_mapping.get(doctor['Specialization'], ["#667eea", "#764ba2"])
    
    # Create star rating display
    stars = "⭐" * int(doctor['Rating']) + "☆" * (5 - int(doctor['Rating']))
    
    UIComponents.render_gradient_card(
        title=f"👨‍⚕️ {doctor['Name']}",
        content=f"""
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <strong>🏥 {doctor['Specialization']}</strong>
                <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 12px; font-size: 0.9em;">
                    {doctor['Availability']}
                </span>
            </div>
            <div style="margin-bottom: 8px;">
                <strong>📅 Next Available:</strong> {doctor['Next_Available']}<br>
                <strong>💰 Fee:</strong> ₹{doctor['Consultation_Fee']}<br>
                <strong>🎓 Experience:</strong> {doctor['Experience']} years<br>
                <strong>⭐ Rating:</strong> {stars} ({doctor['Rating']}/5)
            </div>
            <div style="font-size: 0.9em; color: rgba(255,255,255,0.9);">
                <strong>🎓 Education:</strong> {doctor['Education']}<br>
                <strong>🌐 Languages:</strong> {doctor['Languages']}
            </div>
        </div>
        """,
        gradient_colors=colors,
        icon="👨‍⚕️"
    )
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"📞 Call", key=f"call_doctor_{idx}"):
            show_doctor_call_popup(doctor)
    
    with col2:
        if st.button(f"📅 Book", key=f"book_doctor_{idx}"):
            show_doctor_booking_popup(doctor)
    
    with col3:
        if st.button(f"ℹ️ Profile", key=f"profile_doctor_{idx}"):
            show_doctor_profile_popup(doctor)

def display_pricing_results(price, insurance_coverage):
    """Display pricing calculation results"""
    insurance_amount = price * (insurance_coverage / 100)
    patient_amount = price - insurance_amount
    
    st.markdown("### 💰 Pricing Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        UIComponents.render_metric_card(
            "Total Cost", f"₹{price:,.0f}", color="primary", icon="💰"
        )
    
    with col2:
        UIComponents.render_metric_card(
            "Insurance Covers", f"₹{insurance_amount:,.0f}", color="success", icon="🏥"
        )
    
    with col3:
        UIComponents.render_metric_card(
            "You Pay", f"₹{patient_amount:,.0f}", color="info", icon="💳"
        )

# Popup functions (simplified for demo)
def show_emergency_doctor_popup():
    st.error("🚑 Emergency doctor contacted! Please wait for immediate assistance.")

def show_consultation_booking_popup():
    st.success("👨‍⚕️ Consultation booking initiated! Please select your preferred doctor.")

def show_telemedicine_popup():
    st.info("📞 Telemedicine consultation available 24/7. Video call setup in progress...")

def show_specialist_finder_popup():
    st.info("🔍 Specialist finder activated! Browse our expert doctors above.")

def show_doctor_call_popup(doctor):
    st.success(f"📞 Calling {doctor['Name']} at {doctor['Phone']}")

def show_doctor_booking_popup(doctor):
    st.success(f"📅 Booking appointment with {doctor['Name']} - {doctor['Next_Available']}")

def show_doctor_profile_popup(doctor):
    st.info(f"👨‍⚕️ Viewing detailed profile for {doctor['Name']} - {doctor['Specialization']} specialist")

def show_emergency_popup():
    st.info("🚨 Emergency services contacted! Help is on the way.")

def show_health_checkup_popup():
    st.success("🩺 Health checkup booking initiated!")

def show_pharmacy_popup():
    st.info("💊 Pharmacy services are available 24/7")

def show_ambulance_popup():
    st.warning("🚑 Ambulance service requested!")

def show_department_details_popup(dept):
    st.info(f"📋 Detailed information for {dept['title']} department")

def show_appointment_booking_popup(dept):
    st.success(f"📅 Appointment booking for {dept['title']} initiated")

def show_service_booking_popup(service):
    st.success(f"📞 Booking {service['Name']} - Please call our helpline")

def show_service_details_popup(service):
    st.info(f"ℹ️ Detailed information for {service['Name']}")