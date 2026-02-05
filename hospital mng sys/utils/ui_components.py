import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import pandas as pd
import json

class UIComponents:
    """Advanced modular UI components library for the hospital management system"""
    
    @staticmethod
    def render_gradient_card(title, content, gradient_colors=["#667eea", "#764ba2"], icon="🔥"):
        """Render a beautiful gradient card with content"""
        gradient = f"linear-gradient(135deg, {gradient_colors[0]}, {gradient_colors[1]})"
        
        st.markdown(f"""
        <div style="
            background: {gradient};
            padding: 20px;
            border-radius: 15px;
            color: white;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            margin: 10px 0;
            transform: translateY(0);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 24px; margin-right: 10px;">{icon}</span>
                <h3 style="margin: 0; color: white;">{title}</h3>
            </div>
            <div style="font-size: 16px; line-height: 1.5;">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_metric_card(title, value, delta=None, color="primary", icon="📊"):
        """Render an animated metric card"""
        
        color_map = {
            "primary": "#667eea",
            "success": "#51cf66", 
            "warning": "#ffd43b",
            "error": "#ff6b6b",
            "info": "#4dabf7"
        }
        
        card_color = color_map.get(color, "#667eea")
        delta_color = "#51cf66" if delta and "+" in str(delta) else "#ff6b6b"
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {card_color}, {card_color}dd);
            padding: 20px;
            border-radius: 12px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 10px 0;
            transition: transform 0.3s ease;
        " onmouseover="this.style.transform='translateY(-5px)'" 
           onmouseout="this.style.transform='translateY(0)'">
            <div style="font-size: 32px; margin-bottom: 5px;">{icon}</div>
            <div style="font-size: 14px; opacity: 0.9; margin-bottom: 5px;">{title}</div>
            <div style="font-size: 28px; font-weight: bold; margin-bottom: 5px;">{value}</div>
            {f'<div style="font-size: 12px; color: {delta_color};">{delta}</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_progress_ring(percentage, title, color="#667eea", size=120):
        """Render an animated circular progress ring"""
        
        circumference = 2 * 3.14159 * 45  # radius = 45
        stroke_dasharray = circumference
        stroke_dashoffset = circumference - (percentage / 100) * circumference
        
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <svg width="{size}" height="{size}" viewBox="0 0 100 100">
                <circle
                    cx="50" cy="50" r="45"
                    fill="none"
                    stroke="#e9ecef"
                    stroke-width="8"
                />
                <circle
                    cx="50" cy="50" r="45"
                    fill="none"
                    stroke="{color}"
                    stroke-width="8"
                    stroke-linecap="round"
                    stroke-dasharray="{stroke_dasharray}"
                    stroke-dashoffset="{stroke_dashoffset}"
                    transform="rotate(-90 50 50)"
                    style="transition: stroke-dashoffset 0.5s ease-in-out;"
                />
                <text x="50" y="50" text-anchor="middle" dy="0.3em" 
                      font-size="16" font-weight="bold" fill="{color}">
                    {percentage}%
                </text>
            </svg>
            <div style="margin-top: 10px; font-weight: bold; color: #495057;">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_notification_bar(message, type="info", dismissible=True, icon=None):
        """Render a beautiful notification bar"""
        
        type_config = {
            "success": {"color": "#51cf66", "bg": "#d3f9d8", "icon": "✅"},
            "warning": {"color": "#ffd43b", "bg": "#fff3cd", "icon": "⚠️"},
            "error": {"color": "#ff6b6b", "bg": "#f8d7da", "icon": "❌"},
            "info": {"color": "#4dabf7", "bg": "#d1ecf1", "icon": "ℹ️"}
        }
        
        config = type_config.get(type, type_config["info"])
        display_icon = icon or config["icon"]
        
        dismiss_button = """
        <button onclick="this.parentElement.style.display='none'" 
                style="background: none; border: none; float: right; 
                       font-size: 18px; cursor: pointer; color: inherit;">×</button>
        """ if dismissible else ""
        
        st.markdown(f"""
        <div style="
            background: {config['bg']};
            color: {config['color']};
            padding: 15px 20px;
            border-radius: 8px;
            border-left: 4px solid {config['color']};
            margin: 10px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            animation: slideIn 0.5s ease-out;
        ">
            {dismiss_button}
            <span style="font-size: 18px; margin-right: 10px;">{display_icon}</span>
            <span style="font-weight: 500;">{message}</span>
        </div>
        <style>
        @keyframes slideIn {{
            from {{ transform: translateX(-100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_feature_showcase(features, columns=3):
        """Render a feature showcase grid"""
        
        cols = st.columns(columns)
        
        for i, feature in enumerate(features):
            with cols[i % columns]:
                UIComponents.render_gradient_card(
                    title=feature.get("title", "Feature"),
                    content=feature.get("description", "Description"),
                    gradient_colors=feature.get("colors", ["#667eea", "#764ba2"]),
                    icon=feature.get("icon", "🔥")
                )
    
    @staticmethod
    def render_stats_grid(stats_data, columns=4):
        """Render a statistics grid with animated counters"""
        
        cols = st.columns(columns)
        
        for i, stat in enumerate(stats_data):
            with cols[i % columns]:
                UIComponents.render_metric_card(
                    title=stat.get("title", "Metric"),
                    value=stat.get("value", "0"),
                    delta=stat.get("delta"),
                    color=stat.get("color", "primary"),
                    icon=stat.get("icon", "📊")
                )
    
    @staticmethod
    def render_timeline(events, title="Timeline"):
        """Render a beautiful timeline component"""
        
        st.subheader(title)
        
        for i, event in enumerate(events):
            is_last = i == len(events) - 1
            
            st.markdown(f"""
            <div style="position: relative; padding-left: 30px; margin-bottom: 20px;">
                <div style="
                    position: absolute;
                    left: 0;
                    top: 5px;
                    width: 12px;
                    height: 12px;
                    background: #667eea;
                    border-radius: 50%;
                    border: 3px solid white;
                    box-shadow: 0 0 0 3px #667eea;
                "></div>
                
                {'' if is_last else '''
                <div style="
                    position: absolute;
                    left: 5px;
                    top: 17px;
                    width: 2px;
                    height: 40px;
                    background: linear-gradient(to bottom, #667eea, #e9ecef);
                "></div>
                '''}
                
                <div style="
                    background: white;
                    padding: 15px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    border-left: 3px solid #667eea;
                ">
                    <div style="font-weight: bold; color: #667eea; margin-bottom: 5px;">
                        {event.get('date', 'Date')}
                    </div>
                    <div style="font-weight: 600; margin-bottom: 5px;">
                        {event.get('title', 'Event Title')}
                    </div>
                    <div style="color: #6c757d;">
                        {event.get('description', 'Event description')}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_modal_popup(title, content, show_modal=False, modal_key="modal"):
        """Render a modal popup dialog"""
        
        if show_modal:
            st.markdown(f"""
            <div id="{modal_key}" style="
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.5);
                animation: fadeIn 0.3s;
            ">
                <div style="
                    position: relative;
                    background-color: white;
                    margin: 5% auto;
                    padding: 30px;
                    border-radius: 15px;
                    width: 80%;
                    max-width: 600px;
                    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
                    animation: slideInDown 0.3s;
                ">
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 20px;
                        padding-bottom: 15px;
                        border-bottom: 2px solid #e9ecef;
                    ">
                        <h2 style="margin: 0; color: #667eea;">{title}</h2>
                        <span onclick="document.getElementById('{modal_key}').style.display='none'" 
                              style="
                                  font-size: 28px;
                                  font-weight: bold;
                                  cursor: pointer;
                                  color: #adb5bd;
                                  hover: color: #495057;
                              ">&times;</span>
                    </div>
                    <div>{content}</div>
                </div>
            </div>
            
            <style>
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            
            @keyframes slideInDown {{
                from {{ transform: translateY(-50px); opacity: 0; }}
                to {{ transform: translateY(0); opacity: 1; }}
            }}
            </style>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_action_buttons(buttons, layout="horizontal"):
        """Render styled action buttons"""
        
        if layout == "horizontal":
            cols = st.columns(len(buttons))
            
            for i, button in enumerate(buttons):
                with cols[i]:
                    if st.button(
                        button.get("label", "Button"),
                        key=button.get("key", f"btn_{i}"),
                        help=button.get("help"),
                        type=button.get("type", "secondary")
                    ):
                        if button.get("action"):
                            button["action"]()
        else:
            for button in buttons:
                if st.button(
                    button.get("label", "Button"),
                    key=button.get("key"),
                    help=button.get("help"),
                    type=button.get("type", "secondary"),
                    use_container_width=True
                ):
                    if button.get("action"):
                        button["action"]()
    
    @staticmethod
    def render_data_table(data, title=None, searchable=True, exportable=True, actions=None, table_key=None):
        """Render an enhanced data table with features"""
        
        # Generate unique key if not provided
        if table_key is None:
            table_key = f"table_{hash(str(title))if title else 'default'}"
        
        if title:
            st.subheader(title)
        
        if searchable:
            search_term = st.text_input("🔍 Search", key=f"search_{table_key}")
            if search_term:
                # Filter data based on search term
                data = data[data.astype(str).apply(
                    lambda x: x.str.contains(search_term, case=False, na=False)
                ).any(axis=1)]
        
        # Display data
        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )
        
        # Export functionality
        if exportable:
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("📊 Export CSV", key=f"export_csv_{table_key}"):
                    csv = data.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"{title or 'data'}_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        key=f"download_csv_{table_key}"
                    )
            
            with col2:
                if st.button("📋 Export JSON", key=f"export_json_{table_key}"):
                    json_data = data.to_json(orient="records", indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=json_data,
                        file_name=f"{title or 'data'}_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json",
                        key=f"download_json_{table_key}"
                    )
    
    @staticmethod
    def render_chart_selector(data, chart_types=["Bar", "Line", "Pie", "Scatter"]):
        """Render an interactive chart selector"""
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("📊 Chart Options")
            
            chart_type = st.selectbox("Chart Type", chart_types, key="chart_type_selector")
            
            if len(data.columns) > 1:
                x_column = st.selectbox("X-axis", data.columns, key="chart_x_axis")
                y_column = st.selectbox("Y-axis", [col for col in data.columns if col != x_column], key="chart_y_axis")
            
            color_scheme = st.selectbox("Color Scheme", 
                                      ["viridis", "blues", "reds", "greens", "purples"], key="chart_color_scheme")
        
        with col2:
            if len(data.columns) > 1:
                if chart_type == "Bar":
                    fig = px.bar(data, x=x_column, y=y_column, color_discrete_sequence=px.colors.sequential.__dict__[color_scheme])
                elif chart_type == "Line":
                    fig = px.line(data, x=x_column, y=y_column, color_discrete_sequence=px.colors.sequential.__dict__[color_scheme])
                elif chart_type == "Pie":
                    fig = px.pie(data, names=x_column, values=y_column, color_discrete_sequence=px.colors.sequential.__dict__[color_scheme])
                elif chart_type == "Scatter":
                    fig = px.scatter(data, x=x_column, y=y_column, color_discrete_sequence=px.colors.sequential.__dict__[color_scheme])
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Need at least 2 columns for charting")


class PopupCatalogs:
    """Popup catalog components for services, departments, and procedures"""
    
    @staticmethod
    def show_services_catalog():
        """Show medical services catalog popup"""
        
        services = [
            {
                "category": "Emergency Services",
                "icon": "🚨",
                "color": "#ff6b6b",
                "services": [
                    {"name": "Emergency Room", "description": "24/7 emergency medical care", "price": "₹2,000"},
                    {"name": "Trauma Care", "description": "Specialized trauma treatment", "price": "₹5,000"},
                    {"name": "Ambulance Service", "description": "Emergency transportation", "price": "₹1,500"},
                ]
            },
            {
                "category": "Diagnostic Services",
                "icon": "🔬",
                "color": "#4dabf7",
                "services": [
                    {"name": "Blood Test", "description": "Complete blood count and analysis", "price": "₹500"},
                    {"name": "X-Ray", "description": "Digital X-ray imaging", "price": "₹800"},
                    {"name": "MRI Scan", "description": "Magnetic resonance imaging", "price": "₹8,000"},
                    {"name": "CT Scan", "description": "Computed tomography scan", "price": "₹6,000"},
                ]
            },
            {
                "category": "Surgical Procedures",
                "icon": "⚕️",
                "color": "#51cf66",
                "services": [
                    {"name": "Minor Surgery", "description": "Outpatient minor procedures", "price": "₹15,000"},
                    {"name": "Major Surgery", "description": "Complex surgical procedures", "price": "₹1,50,000"},
                    {"name": "Laparoscopic Surgery", "description": "Minimally invasive surgery", "price": "₹80,000"},
                ]
            }
        ]
        
        st.markdown("## 🏥 Medical Services Catalog")
        
        for category in services:
            with st.expander(f"{category['icon']} {category['category']}", expanded=True):
                
                for service in category['services']:
                    col1, col2, col3 = st.columns([2, 3, 1])
                    
                    with col1:
                        st.markdown(f"**{service['name']}**")
                    
                    with col2:
                        st.write(service['description'])
                    
                    with col3:
                        st.markdown(f"**{service['price']}**")
                        
                        if st.button(f"Book {service['name']}", key=f"book_{service['name']}"):
                            UIComponents.render_notification_bar(
                                f"Service '{service['name']}' added to booking cart!",
                                type="success"
                            )
    
    @staticmethod
    def show_departments_catalog():
        """Show hospital departments catalog"""
        
        departments = [
            {
                "name": "Cardiology",
                "icon": "❤️",
                "description": "Heart and cardiovascular care",
                "head": "Dr. John Smith",
                "specialties": ["Heart Surgery", "Angioplasty", "ECG", "Echo"],
                "contact": "+1-234-567-8901"
            },
            {
                "name": "Neurology", 
                "icon": "🧠",
                "description": "Brain and nervous system care",
                "head": "Dr. Sarah Johnson",
                "specialties": ["Brain Surgery", "Stroke Care", "Epilepsy", "Neurology"],
                "contact": "+1-234-567-8902"
            },
            {
                "name": "Orthopedics",
                "icon": "🦴",
                "description": "Bone and joint care",
                "head": "Dr. Michael Brown",
                "specialties": ["Joint Replacement", "Fracture Care", "Sports Medicine"],
                "contact": "+1-234-567-8903"
            },
            {
                "name": "Pediatrics",
                "icon": "👶",
                "description": "Child healthcare",
                "head": "Dr. Emily Davis",
                "specialties": ["Child Care", "Vaccination", "Growth Monitoring"],
                "contact": "+1-234-567-8904"
            }
        ]
        
        st.markdown("## 🏥 Hospital Departments")
        
        cols = st.columns(2)
        
        for i, dept in enumerate(departments):
            with cols[i % 2]:
                UIComponents.render_gradient_card(
                    title=f"{dept['icon']} {dept['name']}",
                    content=f"""
                    <strong>Description:</strong> {dept['description']}<br>
                    <strong>Department Head:</strong> {dept['head']}<br>
                    <strong>Specialties:</strong> {', '.join(dept['specialties'])}<br>
                    <strong>Contact:</strong> {dept['contact']}
                    """,
                    gradient_colors=["#667eea", "#764ba2"]
                )
    
    @staticmethod
    def show_procedures_catalog():
        """Show medical procedures catalog"""
        
        procedures = {
            "Common Procedures": [
                {"name": "Health Checkup", "duration": "2 hours", "price": "₹3,000"},
                {"name": "Vaccination", "duration": "30 minutes", "price": "₹500"},
                {"name": "Blood Donation", "duration": "1 hour", "price": "Free"},
            ],
            "Diagnostic Procedures": [
                {"name": "Ultrasound", "duration": "45 minutes", "price": "₹1,500"},
                {"name": "Endoscopy", "duration": "1 hour", "price": "₹8,000"},
                {"name": "Biopsy", "duration": "2 hours", "price": "₹12,000"},
            ],
            "Therapeutic Procedures": [
                {"name": "Physiotherapy", "duration": "1 hour", "price": "₹800"},
                {"name": "Dialysis", "duration": "4 hours", "price": "₹3,500"},
                {"name": "Chemotherapy", "duration": "6 hours", "price": "₹25,000"},
            ]
        }
        
        st.markdown("## ⚕️ Medical Procedures Catalog")
        
        for category, procs in procedures.items():
            with st.expander(f"📋 {category}", expanded=True):
                
                # Create a nice table layout
                data = pd.DataFrame(procs)
                UIComponents.render_data_table(data, searchable=False, exportable=False, table_key="popup_data")


# Global instances for easy access
ui = UIComponents()
catalogs = PopupCatalogs()