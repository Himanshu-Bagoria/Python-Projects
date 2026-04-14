import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import io

# Import custom modules
from components.data_manager import DataManager
from components.viz import VisualizationManager
from utils.alerts import AlertSystem
from utils.reports import ReportGenerator
from utils.productivity import ProductivityAnalyzer

# Optional face recognition import
try:
    from components.face_recognition import FaceRecognitionSystem
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    # Silent fallback - no warnings shown
    class FaceRecognitionSystem:
        def __init__(self):
            pass
        def add_employee_face(self, *args, **kwargs):
            return False, "Face recognition feature requires additional setup"
        def capture_and_recognize(self, *args, **kwargs):
            return None, "Face recognition feature requires additional setup"
        def get_registered_faces(self, *args, **kwargs):
            return []
        def remove_employee_face(self, *args, **kwargs):
            return False, "Face recognition feature requires additional setup"

# Set page configuration
st.set_page_config(
    page_title="Employee Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #6a0dad 0%, #8a2be2 50%, #4b0082 100%) !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4b0082 0%, #6a0dad 100%) !important;
        color: white !important;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Sidebar radio buttons */
    [data-testid="stSidebar"] .stRadio > label {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        margin: 5px 0 !important;
        padding: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(5px) !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label[data-checked="true"] {
        background: #4caf50 !important;
        color: white !important;
        font-weight: bold !important;
    }
    
    /* Main header styling */
    h1 {
        background: linear-gradient(90deg, #1a237e, #4caf50) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-size: 2.5rem !important;
        font-weight: bold !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(90deg, #e3f2fd, #e8f5e8) !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #bbdefb !important;
        color: #1a237e !important;
        border-radius: 8px !important;
        margin: 0 5px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #90caf9 !important;
        transform: translateY(-2px) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: #4caf50 !important;
        color: white !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #1a237e, #4caf50) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    
    /* Metric cards styling */
    [data-testid="stMetricValue"] {
        color: #1a237e !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4caf50 !important;
        font-weight: bold !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    
    /* Form styling */
    [data-testid="stForm"] {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 8px 25px rgba(138, 43, 226, 0.3) !important;
        border: 2px solid #8a2be2 !important;
    }
    
    /* Input field styling */
    input[type="text"], input[type="email"], input[type="number"], select, textarea {
        background: #2d2d2d !important;
        border: 2px solid #8a2be2 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-size: 16px !important;
        color: #ffffff !important;
        margin: 8px 0 !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    
    input[type="text"]:focus, input[type="email"]:focus, input[type="number"]:focus, select:focus, textarea:focus {
        outline: none !important;
        border-color: #ff69b4 !important;
        box-shadow: 0 0 0 3px rgba(255, 105, 180, 0.3) !important;
        background: #3d3d3d !important;
    }
    
    /* Placeholder text */
    input::placeholder, textarea::placeholder {
        color: #aaaaaa !important;
    }
    
    /* Required field labels */
    [data-testid="stMarkdownContainer"] label {
        color: #ff69b4 !important;
        font-weight: bold !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.7) !important;
    }
    
    /* Required asterisk */
    [data-testid="stMarkdownContainer"] label:after {
        content: " *";
        color: #f44336 !important;
        font-weight: bold !important;
        font-size: 18px !important;
        vertical-align: top !important;
    }
    
    /* All labels styling */
    label {
        color: #e0b0ff !important;
        font-weight: bold !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.7) !important;
    }
    
    /* Specific input labels */
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label, .stDateInput label, .stTimeInput label {
        color: #ff69b4 !important;
        font-weight: bold !important;
        font-size: 16px !important;
        background: linear-gradient(135deg, #4b0082, #6a0dad) !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        display: inline-block !important;
        margin-bottom: 8px !important;
        border: 2px solid #8a2be2 !important;
        box-shadow: 0 2px 8px rgba(138, 43, 226, 0.3) !important;
    }
    
    /* Required field styling */
    .stTextInput label:after, .stNumberInput label:after, .stSelectbox label:after, .stTextArea label:after {
        content: " *";
        color: #d32f2f !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background: #2d2d2d !important;
        border: 2px solid #8a2be2 !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    /* Date and time pickers */
    .stDateInput > div > div, .stTimeInput > div > div {
        background: #2d2d2d !important;
        border: 2px solid #8a2be2 !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    /* Heading pop and hover effects */
    h1, h2, h3 {
        animation: popIn 0.8s ease-out;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    h1:hover, h2:hover, h3:hover {
        transform: scale(1.05);
        text-shadow: 3px 3px 8px rgba(138, 43, 226, 0.7);
        color: #ff69b4 !important;
    }
    
    @keyframes popIn {
        0% {
            transform: scale(0.8);
            opacity: 0;
        }
        70% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Additional hover effects for section headers */
    .section-header:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 30px rgba(138, 43, 226, 0.6) !important;
    }
    
    /* Tab hover effects */
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 5px 15px rgba(138, 43, 226, 0.4) !important;
    }
    
    /* Button hover effects */
    .stButton > button:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 6px 12px rgba(138, 43, 226, 0.5) !important;
        background: linear-gradient(45deg, #ff69b4, #8a2be2) !important;
    }
    
    /* Metric card hover effects */
    .metric-card:hover {
        transform: translateY(-8px) scale(1.05) !important;
        box-shadow: 0 12px 25px rgba(138, 43, 226, 0.6) !important;
    }
    
    /* Additional text hover effects */
    p:hover {
        color: #ff69b4 !important;
        transition: color 0.3s ease;
    }
    
    /* Main title styling */
    h1 {
        background: linear-gradient(90deg, #ff69b4, #8a2be2, #4169e1) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-size: 2.8rem !important;
        font-weight: bold !important;
        text-align: center !important;
        margin: 20px 0 !important;
        padding: 10px !important;
        border-radius: 15px !important;
        background-color: rgba(255,255,255,0.1) !important;
        backdrop-filter: blur(10px) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Initialize components
data_manager = DataManager()
face_recognition = FaceRecognitionSystem()
viz_manager = VisualizationManager()
alert_system = AlertSystem(data_manager)
report_generator = ReportGenerator(data_manager)
productivity_analyzer = ProductivityAnalyzer(data_manager)

# Face recognition availability handled silently
# No sidebar warning to maintain clean UI

def apply_theme():
    """Apply theme styling"""
    if st.session_state.theme == 'dark':
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stSidebar {
            background-color: #1e1e1e;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: #000000;
        }
        .stSidebar {
            background-color: #f0f2f6;
        }
        </style>
        """, unsafe_allow_html=True)

def main():
    # Apply theme
    apply_theme()
    
    # Theme toggle
    with st.sidebar:
        st.markdown("### Theme")
        if st.button("🌙 Dark" if st.session_state.theme == 'light' else "☀️ Light"):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
            st.rerun()
    
    # App title
    st.title("📊 Employee Performance Dashboard")
    st.markdown("---")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### Navigation")
        page = st.radio(
            "Go to:",
            ["Dashboard", "Employee Management", "Attendance", "Performance Tracking", 
             "Reports", "Analytics"]
        )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Employee Management":
        show_employee_management()
    elif page == "Attendance":
        show_attendance()
    elif page == "Performance Tracking":
        show_performance_tracking()
    elif page == "Reports":
        show_reports()
    elif page == "Analytics":
        show_analytics()

def show_dashboard():
    st.header("🎯 Executive Dashboard")
    
    # Add decorative header
    st.markdown("""
    <div class="section-header" style="background: linear-gradient(135deg, #8a2be2 0%, #4b0082 100%); 
                padding: 25px; border-radius: 20px; margin-bottom: 25px; 
                text-align: center; box-shadow: 0 8px 25px rgba(138, 43, 226, 0.4);
                border: 3px solid #ff69b4; animation: popIn 1s ease-out; 
                transition: all 0.3s ease;">
        <h2 style="color: white; margin: 0; font-size: 2.2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">📊 Performance Overview</h2>
        <p style="color: #e0b0ff; margin: 15px 0 0 0; font-size: 1.1rem;">Real-time insights and analytics for your team</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    employees_df = data_manager.load_employees()
    attendance_df = data_manager.load_attendance()
    performance_df = data_manager.load_performance()
    
    # Key metrics with enhanced styling
    st.markdown("""
    <div class="kpi-header" style="background: linear-gradient(90deg, #8a2be2 0%, #4b0082 100%); 
                padding: 20px; border-radius: 20px; margin: 25px 0; 
                text-align: center; box-shadow: 0 8px 25px rgba(138, 43, 226, 0.4);
                border: 3px solid #ff69b4; animation: popIn 1s ease-out;
                transition: all 0.3s ease; cursor: pointer;">
        <h3 style="text-align: center; color: white; margin: 0; font-size: 1.8rem; 
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">🔑 Key Performance Indicators</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); 
                    padding: 25px; border-radius: 20px; text-align: center; 
                    box-shadow: 0 6px 15px rgba(76, 175, 80, 0.3); 
                    transition: all 0.3s ease; cursor: pointer;
                    border: 2px solid #81c784; hover-effect: true;">
            <h3 style="color: white; margin: 0; font-size: 2.5rem; transition: all 0.3s ease;">👥</h3>
            <h2 style="color: white; margin: 15px 0 0 0; font-size: 2.2rem; font-weight: bold; transition: all 0.3s ease;">{len(employees_df)}</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 1.1rem; transition: all 0.3s ease;">Total Employees</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if not attendance_df.empty:
            present_today = len(attendance_df[
                (attendance_df['date'] == datetime.now().strftime('%Y-%m-%d')) & 
                (attendance_df['status'] == 'Present')
            ])
        else:
            present_today = 0
        
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #2196f3 0%, #0d47a1 100%); 
                    padding: 25px; border-radius: 20px; text-align: center; 
                    box-shadow: 0 6px 15px rgba(33, 150, 243, 0.3); 
                    transition: all 0.3s ease; cursor: pointer;
                    border: 2px solid #64b5f6; hover-effect: true;">
            <h3 style="color: white; margin: 0; font-size: 2.5rem; transition: all 0.3s ease;">📅</h3>
            <h2 style="color: white; margin: 15px 0 0 0; font-size: 2.2rem; font-weight: bold; transition: all 0.3s ease;">{present_today}</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 1.1rem; transition: all 0.3s ease;">Present Today</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if not performance_df.empty:
            avg_productivity = performance_df['productivity_score'].mean()
        else:
            avg_productivity = 0.0
        
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #ff9800 0%, #e65100 100%); 
                    padding: 25px; border-radius: 20px; text-align: center; 
                    box-shadow: 0 6px 15px rgba(255, 152, 0, 0.3); 
                    transition: all 0.3s ease; cursor: pointer;
                    border: 2px solid #ffb74d; hover-effect: true;">
            <h3 style="color: white; margin: 0; font-size: 2.5rem; transition: all 0.3s ease;">📈</h3>
            <h2 style="color: white; margin: 15px 0 0 0; font-size: 2.2rem; font-weight: bold; transition: all 0.3s ease;">{avg_productivity:.1f}</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 1.1rem; transition: all 0.3s ease;">Avg Productivity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        departments = employees_df['department'].nunique() if not employees_df.empty else 0
        
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #9c27b0 0%, #4a148c 100%); 
                    padding: 25px; border-radius: 20px; text-align: center; 
                    box-shadow: 0 6px 15px rgba(156, 39, 176, 0.3); 
                    transition: all 0.3s ease; cursor: pointer;
                    border: 2px solid #ba68c8; hover-effect: true;">
            <h3 style="color: white; margin: 0; font-size: 2.5rem; transition: all 0.3s ease;">🏢</h3>
            <h2 style="color: white; margin: 15px 0 0 0; font-size: 2.2rem; font-weight: bold; transition: all 0.3s ease;">{departments}</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 1.1rem; transition: all 0.3s ease;">Departments</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Department distribution
        if not employees_df.empty:
            dept_counts = employees_df['department'].value_counts()
            fig = px.pie(values=dept_counts.values, names=dept_counts.index,
                        title="Employee Distribution by Department")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Attendance trend
        if not attendance_df.empty:
            attendance_trend = attendance_df.groupby('date').agg({
                'status': lambda x: (x == 'Present').sum()
            }).reset_index()
            attendance_trend.columns = ['date', 'present_count']
            
            fig = px.line(attendance_trend, x='date', y='present_count',
                         title="Daily Attendance Trend")
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("Recent Activity")
    if not attendance_df.empty:
        recent_attendance = attendance_df.tail(10)
        st.dataframe(recent_attendance)

def show_employee_management():
    st.header("👥 Employee Management")
    
    # Add decorative header
    st.markdown("""
    <div class="section-header" style="background: linear-gradient(135deg, #4b0082 0%, #8a2be2 100%); 
                padding: 25px; border-radius: 20px; margin-bottom: 25px; 
                text-align: center; box-shadow: 0 8px 25px rgba(138, 43, 226, 0.4);
                border: 3px solid #ff69b4; animation: popIn 1s ease-out; 
                transition: all 0.3s ease;">
        <h2 style="color: white; margin: 0; font-size: 2.2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">📋 Employee Management</h2>
        <p style="color: #e0b0ff; margin: 15px 0 0 0; font-size: 1.1rem;">Add, update, and manage your team members</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["View Employees", "Add Employee", "Upload Data"])
    
    with tab1:
        st.subheader("Employee List")
        employees_df = data_manager.load_employees()
        
        if not employees_df.empty:
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                dept_filter = st.selectbox("Filter by Department", 
                                         ["All"] + list(employees_df['department'].unique()))
            with col2:
                search = st.text_input("Search by Name or ID")
            
            # Apply filters
            filtered_df = employees_df.copy()
            if dept_filter != "All":
                filtered_df = filtered_df[filtered_df['department'] == dept_filter]
            if search:
                filtered_df = filtered_df[
                    filtered_df['name'].str.contains(search, case=False) |
                    filtered_df['employee_id'].str.contains(search, case=False)
                ]
            
            st.dataframe(filtered_df, use_container_width=True)
            
            # Employee details
            if st.checkbox("Show Employee Details"):
                selected_id = st.selectbox("Select Employee", filtered_df['employee_id'].tolist())
                if selected_id:
                    employee = filtered_df[filtered_df['employee_id'] == selected_id].iloc[0]
                    st.write(f"**Name:** {employee['name']}")
                    st.write(f"**Department:** {employee['department']}")
                    st.write(f"**Role:** {employee['role']}")
                    st.write(f"**Email:** {employee['email']}")
                    st.write(f"**Hire Date:** {employee['hire_date']}")
        else:
            st.info("No employees found. Add employees using the tabs above.")
    
    with tab2:
        st.subheader("Add New Employee")
        
        with st.form("add_employee_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                employee_id = st.text_input("Employee ID *")
                name = st.text_input("Full Name *")
                email = st.text_input("Email *")
                department = st.selectbox("Department", 
                                        ["Engineering", "Marketing", "Sales", "HR", "Finance"])
            
            with col2:
                role = st.text_input("Role *")
                hire_date = st.date_input("Hire Date", date.today())
                salary = st.number_input("Salary", min_value=0)
                phone = st.text_input("Phone")
                address = st.text_area("Address")
            
            submitted = st.form_submit_button("Add Employee")
            
            if submitted:
                if employee_id and name and email and role:
                    employee_data = {
                        'employee_id': employee_id,
                        'name': name,
                        'email': email,
                        'department': department,
                        'role': role,
                        'hire_date': hire_date.strftime('%Y-%m-%d'),
                        'salary': salary,
                        'phone': phone,
                        'address': address
                    }
                    
                    success, message = data_manager.add_employee(employee_data)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all required fields (*)")
    
    with tab3:
        st.subheader("Upload Employee Data")
        uploaded_file = st.file_uploader("Choose CSV or Excel file", 
                                       type=['csv', 'xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.write("Preview of uploaded data:")
                st.dataframe(df.head())
                
                if st.button("Import Data"):
                    employees_df = data_manager.load_employees()
                    # Merge with existing data
                    combined_df = pd.concat([employees_df, df], ignore_index=True)
                    # Remove duplicates
                    combined_df = combined_df.drop_duplicates(subset=['employee_id'], keep='last')
                    
                    if data_manager.save_employees(combined_df):
                        st.success(f"Successfully imported {len(df)} employees")
                    else:
                        st.error("Error importing data")
                        
            except Exception as e:
                st.error(f"Error reading file: {e}")

def show_attendance():
    st.header("📋 Attendance Management")
    
    # Add decorative header
    st.markdown("""
    <div class="section-header" style="background: linear-gradient(135deg, #4b0082 0%, #8a2be2 100%); 
                padding: 25px; border-radius: 20px; margin-bottom: 25px; 
                text-align: center; box-shadow: 0 8px 25px rgba(138, 43, 226, 0.4);
                border: 3px solid #ff69b4; animation: popIn 1s ease-out; 
                transition: all 0.3s ease;">
        <h2 style="color: white; margin: 0; font-size: 2.2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">📅 Attendance Tracking</h2>
        <p style="color: #e0b0ff; margin: 15px 0 0 0; font-size: 1.1rem;">Monitor and manage employee attendance</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Log Attendance", "View Records", "Face Recognition"])
    
    with tab1:
        st.subheader("Manual Attendance Logging")
        
        employees_df = data_manager.load_employees()
        if not employees_df.empty:
            employee_ids = employees_df['employee_id'].tolist()
            selected_employee = st.selectbox("Select Employee", employee_ids)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                status = st.selectbox("Status", ["Present", "Absent"])
            with col2:
                time_in = st.time_input("Time In", datetime.now().time())
            with col3:
                time_out = st.time_input("Time Out")
            
            if st.button("Log Attendance"):
                time_in_str = time_in.strftime('%H:%M:%S')
                time_out_str = time_out.strftime('%H:%M:%S') if time_out else None
                
                success, message = data_manager.log_attendance(
                    selected_employee, status, time_in_str, time_out_str
                )
                if success:
                    st.success(message)
                else:
                    st.error(message)
        else:
            st.info("No employees found. Please add employees first.")
    
    with tab2:
        st.subheader("Attendance Records")
        
        attendance_df = data_manager.load_attendance()
        if not attendance_df.empty:
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                start_date = st.date_input("Start Date", 
                                         datetime.now().date().replace(day=1))
            with col2:
                end_date = st.date_input("End Date", datetime.now().date())
            with col3:
                dept_filter = st.selectbox("Department", 
                                         ["All"] + list(data_manager.load_employees()['department'].unique()))
            
            # Apply filters
            filtered_attendance = attendance_df.copy()
            filtered_attendance['date'] = pd.to_datetime(filtered_attendance['date'])
            
            filtered_attendance = filtered_attendance[
                (filtered_attendance['date'].dt.date >= start_date) &
                (filtered_attendance['date'].dt.date <= end_date)
            ]
            
            if dept_filter != "All":
                employee_ids = data_manager.load_employees()[
                    data_manager.load_employees()['department'] == dept_filter
                ]['employee_id'].tolist()
                filtered_attendance = filtered_attendance[
                    filtered_attendance['employee_id'].isin(employee_ids)
                ]
            
            st.dataframe(filtered_attendance, use_container_width=True)
            
            # Attendance statistics
            if not filtered_attendance.empty:
                total_records = len(filtered_attendance)
                present_records = len(filtered_attendance[filtered_attendance['status'] == 'Present'])
                attendance_rate = (present_records / total_records) * 100
                
                st.metric("Attendance Rate", f"{attendance_rate:.1f}%")
        else:
            st.info("No attendance records found.")
    
    with tab3:
        show_face_recognition()

def show_face_recognition():
    st.subheader("Face Recognition Attendance")
    
    if not FACE_RECOGNITION_AVAILABLE:
        st.info("📸 Face Recognition Feature")
        st.success("""
        **This feature requires additional setup:**
        
        🔧 **Installation Steps:**
        1. Install Visual Studio Build Tools (Windows)
        2. Run: `pip install face-recognition`
        
        📝 **Alternative:** Use manual attendance logging in the Attendance section above.
        
        This is an optional feature - all other dashboard functionality works perfectly!
        """)
        return
    
    tab1, tab2 = st.tabs(["Register Face", "Recognize Face"])
    
    with tab1:
        st.write("Register employee face for recognition")
        employees_df = data_manager.load_employees()
        
        if not employees_df.empty:
            employee_ids = employees_df['employee_id'].tolist()
            selected_employee = st.selectbox("Select Employee", employee_ids, key="register_employee")
            
            uploaded_file = st.file_uploader("Upload employee photo", type=['jpg', 'jpeg', 'png'])
            
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", width=200)
                
                if st.button("Register Face"):
                    employee_name = employees_df[employees_df['employee_id'] == selected_employee]['name'].iloc[0]
                    success, message = face_recognition.add_employee_face(
                        selected_employee, employee_name, image
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        else:
            st.info("No employees found. Please add employees first.")
    
    with tab2:
        st.write("Recognize employee face for attendance")
        
        if st.button("Start Face Recognition"):
            with st.spinner("Starting webcam..."):
                recognized_faces, message = face_recognition.capture_and_recognize()
                
                if recognized_faces:
                    st.success(f"Recognized: {recognized_faces[0]['name']}")
                    # Auto-log attendance
                    success, log_message = data_manager.log_attendance(
                        recognized_faces[0]['employee_id'], "Present"
                    )
                    if success:
                        st.success("Attendance logged automatically!")
                    else:
                        st.warning(f"Could not log attendance: {log_message}")
                else:
                    st.error("No faces recognized")

def show_performance_tracking():
    st.header("📈 Performance Tracking")
    
    # Add decorative header
    st.markdown("""
    <div class="section-header" style="background: linear-gradient(135deg, #4b0082 0%, #8a2be2 100%); 
                padding: 25px; border-radius: 20px; margin-bottom: 25px; 
                text-align: center; box-shadow: 0 8px 25px rgba(138, 43, 226, 0.4);
                border: 3px solid #ff69b4; animation: popIn 1s ease-out; 
                transition: all 0.3s ease;">
        <h2 style="color: white; margin: 0; font-size: 2.2rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">📊 Performance Monitoring</h2>
        <p style="color: #e0b0ff; margin: 15px 0 0 0; font-size: 1.1rem;">Track KPIs and analyze employee performance</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Add Performance Record", "View Performance", "Productivity Analysis"])
    
    with tab1:
        st.subheader("Add Performance Record")
        
        employees_df = data_manager.load_employees()
        if not employees_df.empty:
            employee_ids = employees_df['employee_id'].tolist()
            selected_employee = st.selectbox("Select Employee", employee_ids, key="perf_employee")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                date_record = st.date_input("Date", datetime.now().date())
            with col2:
                tasks_completed = st.number_input("Tasks Completed", min_value=0, max_value=20, value=5)
            with col3:
                quality_score = st.slider("Quality Score", 0.0, 10.0, 7.0, 0.5)
            
            productivity_score = st.slider("Productivity Score", 0.0, 10.0, 7.0, 0.5)
            comments = st.text_area("Comments")
            
            if st.button("Add Performance Record"):
                performance_data = {
                    'employee_id': selected_employee,
                    'date': date_record.strftime('%Y-%m-%d'),
                    'tasks_completed': tasks_completed,
                    'quality_score': quality_score,
                    'productivity_score': productivity_score,
                    'comments': comments
                }
                
                success, message = data_manager.add_performance_record(performance_data)
                if success:
                    st.success(message)
                else:
                    st.error(message)
        else:
            st.info("No employees found. Please add employees first.")
    
    with tab2:
        st.subheader("Performance Records")
        
        performance_df = data_manager.load_performance()
        if not performance_df.empty:
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", 
                                         datetime.now().date().replace(day=1), key="perf_start")
            with col2:
                end_date = st.date_input("End Date", datetime.now().date(), key="perf_end")
            
            # Apply filters
            filtered_performance = performance_df.copy()
            filtered_performance['date'] = pd.to_datetime(filtered_performance['date'])
            
            filtered_performance = filtered_performance[
                (filtered_performance['date'].dt.date >= start_date) &
                (filtered_performance['date'].dt.date <= end_date)
            ]
            
            st.dataframe(filtered_performance, use_container_width=True)
        else:
            st.info("No performance records found.")
    
    with tab3:
        st.subheader("Productivity Analysis")
        
        employee_id = st.selectbox("Select Employee for Analysis", 
                                 ["All"] + data_manager.load_employees()['employee_id'].tolist())
        
        if st.button("Analyze Productivity"):
            if employee_id == "All":
                # Overall productivity analysis
                performance_df = data_manager.load_performance()
                if not performance_df.empty:
                    # Create productivity trend chart
                    fig = viz_manager.create_performance_trend(performance_df)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            else:
                # Individual employee analysis
                analysis, message = productivity_analyzer.analyze_productivity_trends(employee_id)
                if analysis:
                    st.write(f"**Average Productivity:** {analysis['statistics']['average_productivity']:.2f}")
                    st.write(f"**Trend:** {analysis['statistics']['trend_direction']}")
                    
                    # Show trend chart
                    fig = viz_manager.create_performance_trend(data_manager.load_performance(), employee_id)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Show recommendations
                    recommendations = productivity_analyzer.generate_productivity_recommendations(employee_id)
                    st.subheader("Recommendations")
                    for rec in recommendations:
                        st.write(f"• {rec}")

def show_reports():
    st.header("📋 Reports")
    
    tab1, tab2 = st.tabs(["Generate Report", "Export Data"])
    
    with tab1:
        st.subheader("Generate Performance Report")
        
        report_type = st.radio("Report Type", ["Employee", "Department"])
        
        if report_type == "Employee":
            employee_id = st.selectbox("Select Employee", 
                                     data_manager.load_employees()['employee_id'].tolist())
            start_date = st.date_input("Start Date", datetime.now().date().replace(day=1))
            end_date = st.date_input("End Date", datetime.now().date())
            
            if st.button("Generate Employee Report"):
                report_data, message = report_generator.generate_employee_report(
                    employee_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
                )
                
                if report_data:
                    st.success(message)
                    st.subheader("Report Preview")
                    st.write(f"**Employee:** {report_data['employee_info']['Name']}")
                    st.write(f"**Department:** {report_data['employee_info']['Department']}")
                    st.write(f"**Attendance Rate:** {report_data['statistics']['attendance_rate']:.1f}%")
                    st.write(f"**Average Productivity:** {report_data['statistics']['avg_productivity_score']:.1f}")
                    
                    # Generate PDF
                    pdf_data = report_generator.generate_pdf_report(report_data, "employee")
                    if pdf_data:
                        st.download_button(
                            "Download PDF Report",
                            data=pdf_data,
                            file_name=f"employee_report_{employee_id}.pdf",
                            mime="application/pdf"
                        )
        
        else:  # Department report
            department = st.selectbox("Select Department", 
                                    data_manager.load_employees()['department'].unique())
            start_date = st.date_input("Start Date", datetime.now().date().replace(day=1))
            end_date = st.date_input("End Date", datetime.now().date())
            
            if st.button("Generate Department Report"):
                report_data, message = report_generator.generate_department_report(
                    department, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
                )
                
                if report_data:
                    st.success(message)
                    st.subheader("Report Preview")
                    st.write(f"**Department:** {report_data['department']}")
                    st.write(f"**Employee Count:** {report_data['employee_count']}")
                    st.write(f"**Average Attendance Rate:** {report_data['statistics'].get('attendance_rate', 0):.1f}%")
                    
                    # Generate PDF
                    pdf_data = report_generator.generate_pdf_report(report_data, "department")
                    if pdf_data:
                        st.download_button(
                            "Download PDF Report",
                            data=pdf_data,
                            file_name=f"department_report_{department}.pdf",
                            mime="application/pdf"
                        )
    
    with tab2:
        st.subheader("Export Data")
        
        data_type = st.selectbox("Data Type", ["Employees", "Attendance", "Performance"])
        export_format = st.radio("Format", ["CSV", "Excel"])
        
        if st.button("Export Data"):
            if data_type == "Employees":
                data = data_manager.load_employees()
            elif data_type == "Attendance":
                data = data_manager.load_attendance()
            else:
                data = data_manager.load_performance()
            
            if not data.empty:
                csv = data.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    data=csv,
                    file_name=f"{data_type.lower()}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No data to export")

def show_alerts():
    st.header("⚠️ Alerts & Notifications")
    
    # Get all alerts
    alerts = alert_system.get_all_alerts()
    alert_system.display_alerts(alerts)
    
    # Alert settings
    st.subheader("Alert Settings")
    with st.form("alert_settings"):
        attendance_threshold = st.slider("Attendance Alert Threshold (%)", 0, 100, 80)
        performance_threshold = st.slider("Performance Alert Threshold", 0.0, 10.0, 7.0)
        inactivity_threshold = st.slider("Inactivity Alert Threshold (days)", 1, 30, 7)
        
        if st.form_submit_button("Update Settings"):
            st.success("Alert settings updated!")

def show_analytics():
    st.header("🔍 Advanced Analytics")
    
    # Load data
    attendance_df = data_manager.load_attendance()
    performance_df = data_manager.load_performance()
    employees_df = data_manager.load_employees()
    
    # Merge data for analysis
    if not attendance_df.empty and not performance_df.empty and not employees_df.empty:
        merged_df = attendance_df.merge(performance_df, on=['employee_id', 'date'], how='outer')
        merged_df = merged_df.merge(employees_df[['employee_id', 'department', 'name']], 
                                  on='employee_id', how='left')
        
        # Department performance comparison
        st.subheader("Department Performance Comparison")
        dept_stats = data_manager.get_department_stats()
        if not dept_stats.empty:
            fig = viz_manager.create_department_pie_chart(dept_stats)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # Performance leaderboard
        st.subheader("Top Performers Leaderboard")
        fig = viz_manager.create_leaderboard(performance_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Productivity heatmap
        st.subheader("Productivity Heatmap")
        fig = viz_manager.create_productivity_heatmap(performance_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient data for analytics. Please add more employee data.")

if __name__ == "__main__":
    main()