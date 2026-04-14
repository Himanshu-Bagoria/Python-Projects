# Theme configurations for Smart Hospital System

# Light theme
LIGHT_THEME = {
    "primary_color": "#667eea",
    "secondary_color": "#764ba2",
    "background_color": "#f5f7fa",
    "surface_color": "#ffffff",
    "text_color": "#333333",
    "text_secondary": "#666666",
    "border_color": "#e1e5e9",
    "success_color": "#2ecc71",
    "warning_color": "#f39c12",
    "error_color": "#e74c3c",
    "info_color": "#3498db"
}

# Dark theme
DARK_THEME = {
    "primary_color": "#667eea",
    "secondary_color": "#764ba2",
    "background_color": "#1a1a2e",
    "surface_color": "#16213e",
    "text_color": "#ffffff",
    "text_secondary": "#cccccc",
    "border_color": "#2c3e50",
    "success_color": "#2ecc71",
    "warning_color": "#f39c12",
    "error_color": "#e74c3c",
    "info_color": "#3498db"
}

# Futuristic theme
FUTURISTIC_THEME = {
    "primary_color": "#00d4ff",
    "secondary_color": "#ff0080",
    "background_color": "#0a0a0a",
    "surface_color": "#1a1a1a",
    "text_color": "#ffffff",
    "text_secondary": "#00d4ff",
    "border_color": "#00d4ff",
    "success_color": "#00ff88",
    "warning_color": "#ffaa00",
    "error_color": "#ff0040",
    "info_color": "#0080ff"
}

# Medical theme
MEDICAL_THEME = {
    "primary_color": "#4ecdc4",
    "secondary_color": "#44a08d",
    "background_color": "#f8f9fa",
    "surface_color": "#ffffff",
    "text_color": "#2c3e50",
    "text_secondary": "#7f8c8d",
    "border_color": "#bdc3c7",
    "success_color": "#27ae60",
    "warning_color": "#f39c12",
    "error_color": "#e74c3c",
    "info_color": "#3498db"
}

# Get theme by name
def get_theme(theme_name):
    """Get theme configuration by name"""
    themes = {
        "light": LIGHT_THEME,
        "dark": DARK_THEME,
        "futuristic": FUTURISTIC_THEME,
        "medical": MEDICAL_THEME
    }
    return themes.get(theme_name.lower(), LIGHT_THEME)

# Apply theme to CSS
def get_theme_css(theme_name):
    """Get CSS for a specific theme"""
    theme = get_theme(theme_name)
    
    return f"""
    <style>
    :root {{
        --primary-color: {theme['primary_color']};
        --secondary-color: {theme['secondary_color']};
        --background-color: {theme['background_color']};
        --surface-color: {theme['surface_color']};
        --text-color: {theme['text_color']};
        --text-secondary: {theme['text_secondary']};
        --border-color: {theme['border_color']};
        --success-color: {theme['success_color']};
        --warning-color: {theme['warning_color']};
        --error-color: {theme['error_color']};
        --info-color: {theme['info_color']};
    }}
    
    .stApp {{
        background: var(--background-color);
        color: var(--text-color);
    }}
    
    .stButton > button {{
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }}
    
    .stTextInput > div > div > input {{
        background: var(--surface-color);
        color: var(--text-color);
        border: 2px solid var(--border-color);
        border-radius: 10px;
    }}
    
    .stSelectbox > div > div {{
        background: var(--surface-color);
        color: var(--text-color);
        border: 2px solid var(--border-color);
        border-radius: 10px;
    }}
    
    .metric-card {{
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}
    
    .module-card {{
        background: var(--surface-color);
        border: 2px solid var(--border-color);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}
    
    .module-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        border-color: var(--primary-color);
    }}
    
    .futuristic-text {{
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        text-shadow: 0 0 10px var(--primary-color);
    }}
    
    .body-text {{
        font-family: 'Rajdhani', sans-serif;
        font-weight: 400;
    }}
    
    .glow-effect {{
        animation: glow 2s ease-in-out infinite alternate;
    }}
    
    @keyframes glow {{
        from {{ box-shadow: 0 0 5px var(--primary-color); }}
        to {{ box-shadow: 0 0 20px var(--primary-color), 0 0 30px var(--primary-color); }}
    }}
    
    .pulse {{
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    
    .floating {{
        animation: floating 3s ease-in-out infinite;
    }}
    
    @keyframes floating {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
        100% {{ transform: translateY(0px); }}
    }}
    
    .sidebar .sidebar-content {{
        background: linear-gradient(180deg, var(--surface-color), var(--background-color));
    }}
    
    .stAlert {{
        background: var(--surface-color);
        border: 2px solid var(--border-color);
        border-radius: 10px;
    }}
    
    .stSuccess {{
        background: var(--success-color);
        color: white;
        border-radius: 10px;
    }}
    
    .stWarning {{
        background: var(--warning-color);
        color: white;
        border-radius: 10px;
    }}
    
    .stError {{
        background: var(--error-color);
        color: white;
        border-radius: 10px;
    }}
    
    .stInfo {{
        background: var(--info-color);
        color: white;
        border-radius: 10px;
    }}
    </style>
    """

# Theme switcher component
def create_theme_switcher():
    """Create theme switcher component"""
    import streamlit as st
    
    st.markdown("### 🎨 Theme Settings")
    
    current_theme = st.session_state.get('theme', 'light')
    
    theme_options = {
        "Light": "light",
        "Dark": "dark", 
        "Futuristic": "futuristic",
        "Medical": "medical"
    }
    
    selected_theme = st.selectbox(
        "Choose Theme",
        list(theme_options.keys()),
        index=list(theme_options.keys()).index(current_theme.title())
    )
    
    if st.button("Apply Theme"):
        st.session_state.theme = theme_options[selected_theme]
        st.success(f"✅ Theme changed to {selected_theme}")
        st.rerun()
    
    # Preview current theme
    st.markdown("#### Current Theme Preview")
    theme = get_theme(st.session_state.get('theme', 'light'))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: {theme['primary_color']}; color: white; padding: 1rem; border-radius: 10px; text-align: center;">
            Primary Color
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: {theme['secondary_color']}; color: white; padding: 1rem; border-radius: 10px; text-align: center;">
            Secondary Color
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: {theme['surface_color']}; color: {theme['text_color']}; padding: 1rem; border-radius: 10px; text-align: center; border: 2px solid {theme['border_color']};">
            Surface Color
        </div>
        """, unsafe_allow_html=True)
