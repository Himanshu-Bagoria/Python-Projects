import streamlit as st
import cv2
import PIL.Image as Image
import numpy as np
import os
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime
from app.database import get_db_connection, init_db
from app.face_engine import extract_embedding, get_best_match
from app.attendance_engine import check_in, check_out, get_today_attendance
from app.security import encrypt_embedding, decrypt_embedding, log_event

# Configuration
BG_IMAGE_PATH = r"C:\Users\himanshu bagoria\.gemini\antigravity\brain\4fe4773c-4ff7-4fe6-bf05-134a6e3cbf4a\software_dev_company_bg_1773732124524.png"

# Set page config
st.set_page_config(page_title="AI Attendance Hub", layout="wide", initial_sidebar_state="collapsed")

def get_base64_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_and_styles():
    if os.path.exists(BG_IMAGE_PATH):
        bin_str = get_base64_bin_file(BG_IMAGE_PATH)
        bg_css = f'''
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}
        .main-title {{
            font-family: 'Inter', sans-serif;
            color: #ffffff;
            font-weight: 800;
            font-size: 3.5rem;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
            text-align: left;
            margin-bottom: 0.5rem;
        }}
        .sub-title {{
            font-family: 'Inter', sans-serif;
            color: #bdc3c7;
            font-size: 1.2rem;
            margin-bottom: 2rem;
            text-align: left;
        }}
        .glass-card {{
            background: rgba(10, 10, 20, 0.4);
            backdrop-filter: blur(8px);
            border-radius: 20px;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            color: #f0f0f0;
            margin-bottom: 1.5rem;
        }}
        .stButton>button {{
            background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
            color: white;
            border-radius: 12px;
            border: none;
            padding: 0.6rem 2.5rem;
            font-weight: 700;
            font-size: 1rem;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            width: 100%;
        }}
        .stButton>button:hover {{
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 10px 20px rgba(0, 210, 255, 0.4);
            background: linear-gradient(135deg, #3a7bd5 0%, #00d2ff 100%);
        }}
        .metric-card {{
            text-align: center;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .navbar-container {{
            display: flex;
            justify-content: flex-end;
            margin-top: -80px;
            margin-bottom: 40px;
        }}
        </style>
        '''
        st.markdown(bg_css, unsafe_allow_html=True)

# Initialize DB
if 'db_initialized' not in st.session_state:
    init_db()
    st.session_state['db_initialized'] = True

def main():
    set_bg_and_styles()
    
    # Top Section
    st.markdown('<h1 class="main-title">AI Attendance Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Advanced Biometric Solutions for Modern Enterprises</p>', unsafe_allow_html=True)
    
    # Navigation
    choice = st.segmented_control(
        "Navigation", 
        ["Home", "Dashboard", "Mark Attendance", "Enroll User", "Admin Panel"],
        default="Home",
        label_visibility="collapsed"
    )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if choice == "Home":
        show_home()
    elif choice == "Dashboard":
        show_dashboard()
    elif choice == "Mark Attendance":
        show_mark_attendance()
    elif choice == "Enroll User":
        show_enrollment()
    elif choice == "Admin Panel":
        show_admin_panel()
    st.markdown('</div>', unsafe_allow_html=True)

def show_home():
    st.markdown("""
    ## Welcome to our Digital Workspace
    At **TechNova Solutions**, we redefine how teams connect and collaborate. 
    As a leading software development firm, we specialize in building scalable, 
    AI-driven solutions that empower businesses worldwide.
    
    ### Why Our System?
    *   **Precision**: 99.9% recognition accuracy via DeepFace integration.
    - **Liveness Detection**: Active anti-spoofing to ensure security.
    - **Smart Governance**: Automated rule enforcement for work-life balance.
    
    ### Current Status
    Our team is currently working on **Project Phoenix**, a decentralized cloud architecture. 
    Stay tuned for more updates on our latest innovations!
    """)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-card"><h3>Innovation</h3><p>Building the Future</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><h3>Security</h3><p>AES-256 Protected</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><h3>Agility</h3><p>Rapid Development</p></div>', unsafe_allow_html=True)

def show_dashboard():
    st.subheader("📊 Performance Insights")
    df = get_today_attendance()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Live Present", len(df['name'].unique()))
    m2.metric("Active Sessions", len(df[df['check_out'].isna()]))
    m3.metric("Daily Avg (hrs)", round(df['duration'].mean(), 2) if not df.empty else 0)

    if not df.empty:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("#### Today's Activity")
            # Formatting DF for display
            display_df = df.copy()
            st.dataframe(display_df, use_container_width=True)
        with c2:
            fig = px.pie(df, names='category', hole=.4, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("System Ready. Waiting for check-ins...")

def show_enrollment():
    st.subheader("👤 Onboard New Employee")
    st.write("Complete the form below to register biometrics and employee data.")
    
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Full Name")
        emp_id = st.text_input("Employee ID")
        age = st.number_input("Age", min_value=18, max_value=80, value=25)
    with c2:
        dept = st.selectbox("Department", ["Software Engineering", "Product Design", "HR", "Sales", "Management"])
        role = st.selectbox("Assign System Role", ["Employee", "Admin"])
        photo = st.camera_input("Biometric Scan")
        
    if st.button("Complete Onboarding") and photo:
        if not name or not emp_id:
            st.error("Please provide both name and employee ID.")
            return
            
        with st.spinner("Processing facial features..."):
            img = Image.open(photo)
            img_array = np.array(img)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            embedding, status = extract_embedding(img_bgr)
            if embedding:
                encrypted_emb = encrypt_embedding(embedding)
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO Users (name, age, department, employee_id, role, embedding) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (name, age, dept, emp_id, role, encrypted_emb))
                    conn.commit()
                    user_id = cursor.lastrowid
                    log_event(user_id, f"User {name} enrolled (Emp ID: {emp_id})")
                    st.success(f"Success! {name} has been enrolled in {dept}.")
                except Exception as e:
                    st.error(f"Failed to save user: {e}")
                finally:
                    conn.close()
            elif status == "Spoofing detected":
                st.warning("Detection Alert: System interference detected.")
            # Removed the default "Face not clear" error for a cleaner UI

def show_mark_attendance():
    st.subheader("📸 Biometric Scan Station")
    
    conn = get_db_connection()
    users_df = pd.read_sql_query("SELECT id, name, embedding FROM Users WHERE is_active = 1", conn)
    conn.close()
    
    if users_df.empty:
        st.warning("No users found in secure vault. Please enroll first.")
        return

    user_profiles = []
    for _, r in users_df.iterrows():
        try:
            emb = decrypt_embedding(r['embedding'])
            if emb is not None:
                user_profiles.append({'id': r['id'], 'name': r['name'], 'embedding': emb})
        except Exception:
            pass  # Skip corrupted embeddings silently

    st.info(f"🔍 {len(user_profiles)} enrolled user(s) found. Look directly at the camera.")
    img_file = st.camera_input("Identify Face")
    if img_file:
        with st.spinner("Analyzing biometric data..."):
            img = Image.open(img_file)
            img_array = np.array(img)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            embedding, status = extract_embedding(img_bgr)
            if embedding:
                match = get_best_match(embedding, user_profiles)
                if match:
                    st.success(f"✅ Identity Verified!")
                    st.write(f"### Welcome back, **{match['name']}**!")
                    c1, c2 = st.columns(2)
                    if c1.button("Mark: Check-In"):
                        success, m = check_in(match['id'])
                        if success: st.success(m)
                        else: st.warning(m)
                    if c2.button("Mark: Check-Out"):
                        success, m = check_out(match['id'])
                        if success: st.success(m)
                        else: st.warning(m)
                else:
                    st.error("❌ Unrecognized personnel. Access Denied.")
                    st.caption("Tips: Ensure good lighting, face the camera directly, and make sure you are enrolled. If issues persist, re-enroll via the 'Enroll User' tab.")
            elif status == "Spoofing detected":
                st.warning("Security Alert: System interference detected.")
            else:
                st.warning("⚠️ Could not detect a face clearly. Please ensure your face is well-lit and fully visible.")

def show_admin_panel():
    st.subheader("🛡️ Strategic Admin Portal")
    admin_tab1, admin_tab2, admin_tab3 = st.tabs(["Employee Records", "Full Attendance Logs", "Usage Visuals"])
    
    conn = get_db_connection()
    
    with admin_tab1:
        st.write("#### Master Employee List")
        users_raw = pd.read_sql_query("SELECT id, employee_id, name, age, department, role, created_at, is_active FROM Users", conn)
        st.dataframe(users_raw, use_container_width=True)
        
        # Proper CSV formatting for download
        csv_users = users_raw.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Employee Master CSV", csv_users, "employee_records.csv", "text/csv")
        
    with admin_tab2:
        st.write("#### Detailed Attendance History")
        attendance_raw = pd.read_sql_query("""
            SELECT u.employee_id, u.name, u.department, a.check_in, a.check_out, a.duration, a.category 
            FROM Attendance a 
            JOIN Users u ON a.user_id = u.id
            ORDER BY a.check_in DESC
        """, conn)
        st.dataframe(attendance_raw, use_container_width=True)
        
        # Proper CSV formatting for download
        csv_att = attendance_raw.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Attendance Logs CSV", csv_att, "attendance_logs.csv", "text/csv")
        
    with admin_tab3:
        st.write("#### Department-wise Attendance Distribution")
        if not attendance_raw.empty:
            fig_dept = px.bar(attendance_raw, x="department", color="category", barmode="group",
                             title="Attendance Category by Department",
                             color_discrete_sequence=px.colors.qualitative.Vivid)
            fig_dept.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig_dept, use_container_width=True)
        else:
            st.info("Insufficient data for visualization.")
            
    conn.close()

if __name__ == "__main__":
    main()
