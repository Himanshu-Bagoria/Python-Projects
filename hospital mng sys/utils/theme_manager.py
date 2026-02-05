import streamlit as st
import json
import os

class ThemeManager:
    def __init__(self):
        self.themes = {
            'light': {
                'primary_color': '#667eea',
                'background_color': '#ffffff',
                'secondary_background_color': '#f8f9fc',
                'text_color': '#2d3748',
                'accent_color': '#764ba2',
                'success_color': '#38ef7d',
                'warning_color': '#f093fb',
                'error_color': '#ff9a9e',
                'border_color': '#e2e8f0',
                'shadow': '0 4px 20px rgba(0,0,0,0.08)',
                'hover_bg': '#f1f5f9'
            },
            'dark': {
                'primary_color': '#667eea',
                'background_color': '#1a202c',
                'secondary_background_color': '#2d3748',
                'text_color': '#f7fafc',
                'accent_color': '#764ba2',
                'success_color': '#38ef7d',
                'warning_color': '#f093fb',
                'error_color': '#ff9a9e',
                'border_color': '#4a5568',
                'shadow': '0 8px 30px rgba(0,0,0,0.3)',
                'hover_bg': '#4a5568'
            }
        }
    
    def get_theme_css(self, theme_name='light'):
        """Generate CSS for the selected theme"""
        theme = self.themes.get(theme_name, self.themes['light'])
        
        css = f"""
        <style>
        /* CSS Variables for Theme */
        :root {{
            --primary-color: {theme['primary_color']};
            --background-color: {theme['background_color']};
            --secondary-bg: {theme['secondary_background_color']};
            --text-color: {theme['text_color']};
            --accent-color: {theme['accent_color']};
            --success-color: {theme['success_color']};
            --warning-color: {theme['warning_color']};
            --error-color: {theme['error_color']};
            --border-color: {theme['border_color']};
            --shadow: {theme['shadow']};
            --hover-bg: {theme['hover_bg']};
            --selected-text: #ffffff;
            
            /* Gradient Variables */
            --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-success: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            --gradient-warning: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --gradient-error: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            --gradient-info: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-cool: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            --gradient-warm: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
            --gradient-ocean: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-sunset: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            --gradient-forest: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
            
            /* Animation Variables */
            --animation-fast: 0.2s;
            --animation-normal: 0.3s;
            --animation-slow: 0.5s;
        }}
        
        /* Main container styling with animated background */
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 100%;
            background: linear-gradient(45deg, 
                #667eea 0%, 
                #764ba2 15%, 
                #f093fb 30%, 
                #f5576c 45%, 
                #4facfe 60%, 
                #00f2fe 75%, 
                #42e695 90%, 
                #3bb2b8 100%
            );
            background-size: 400% 400%;
            animation: gradientAnimation 15s ease infinite;
            min-height: 100vh;
            position: relative;
        }}
        
        @keyframes gradientAnimation {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        /* Subtle overlay to maintain readability */
        .main .block-container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.85);
            pointer-events: none;
            z-index: -1;
        }}
        
        /* Enhanced Logo container with vibrant animations */
        .logo-container {{
            text-align: center;
            padding: 3rem 0;
            background: linear-gradient(45deg, 
                #ff9a9e 0%, 
                #fad0c4 25%, 
                #a1c4fd 50%, 
                #c2e9fb 75%, 
                #d4fc79 100%
            );
            background-size: 400% 400%;
            border-radius: 20px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            animation: logoGradientShift 8s ease infinite, pulseGlow 3s ease-in-out infinite alternate;
        }}
                
        @keyframes logoGradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
                
        @keyframes pulseGlow {{
            0% {{ box-shadow: 0 20px 40px rgba(0,0,0,0.2); }}
            100% {{ box-shadow: 0 25px 50px rgba(0,0,0,0.3), 0 0 30px rgba(255,255,255,0.4); }}
        }}
        
        @keyframes gradientShift {{
            0%, 100% {{ background: var(--gradient-primary); }}
            25% {{ background: var(--gradient-cool); }}
            50% {{ background: var(--gradient-warm); }}
            75% {{ background: var(--gradient-ocean); }}
        }}
                
        /* Additional vibrant animations for other elements */
        @keyframes vibrantShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        .main-title {{
            color: white;
            font-size: 3.5rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
            font-family: 'Arial', sans-serif;
            animation: titleGlow 3s ease-in-out infinite alternate;
            letter-spacing: 2px;
        }}
        
        @keyframes titleGlow {{
            from {{ text-shadow: 3px 3px 6px rgba(0,0,0,0.4), 0 0 20px rgba(255,255,255,0.3); }}
            to {{ text-shadow: 3px 3px 6px rgba(0,0,0,0.4), 0 0 30px rgba(255,255,255,0.6); }}
        }}
        
        .pulse-effect {{
            position: absolute;
            top: 50%;
            left: 50%;
            width: 120px;
            height: 120px;
            background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 70%, transparent 100%);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            animation: advancedPulse 3s infinite;
        }}
        
        .pulse-effect::before {{
            content: '';
            position: absolute;
            top: 20px;
            left: 20px;
            right: 20px;
            bottom: 20px;
            background: radial-gradient(circle, rgba(255,255,255,0.4) 0%, transparent 70%);
            border-radius: 50%;
            animation: advancedPulse 3s infinite 0.5s;
        }}
        
        @keyframes advancedPulse {{
            0%, 100% {{ transform: translate(-50%, -50%) scale(0.8); opacity: 0.8; }}
            50% {{ transform: translate(-50%, -50%) scale(1.5); opacity: 0.2; }}
        }}
        
        /* Enhanced Sidebar styling with gradient background */
        section[data-testid="stSidebar"] > div:first-child {{
            background: linear-gradient(160deg, 
                rgba(102, 126, 234, 0.9) 0%, 
                rgba(118, 75, 162, 0.85) 100%
            );
            background-blend-mode: overlay;
        }}
                
        .sidebar-header {{
            color: white;
            font-size: 1.5rem;
            font-weight: 600;
            padding: 1rem 0;
            margin-bottom: 1rem;
            text-align: center;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
            background: linear-gradient(to right, #ffffff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
                
        /* Enhanced sidebar content */
        [data-testid="stSidebar"] {{
            background: rgba(102, 126, 234, 0.1) !important;
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: inset -1px 0 10px rgba(0,0,0,0.1);
        }}
        
        .theme-label, .lang-label {{
            color: var(--text-color);
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        /* Enhanced Card styling with gradients */
        .metric-card {{
            background: linear-gradient(135deg, var(--secondary-bg) 0%, rgba(255,255,255,0.9) 100%);
            padding: 2rem;
            border-radius: 20px;
            border: none;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
            transition: all var(--animation-normal) ease;
            position: relative;
            overflow: hidden;
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-primary);
            animation: shimmer 2s infinite;
        }}
        
        .metric-card:hover {{
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }}
        
        @keyframes shimmer {{
            0% {{ background: var(--gradient-primary); }}
            25% {{ background: var(--gradient-success); }}
            50% {{ background: var(--gradient-warning); }}
            75% {{ background: var(--gradient-info); }}
            100% {{ background: var(--gradient-primary); }}
        }}
        
        .metric-title {{
            color: var(--text-color);
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
            opacity: 0.8;
        }}
        
        .metric-value {{
            color: var(--accent-color);
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
        }}
        
        /* Form styling */
        .stTextInput > div > div > input {{
            background-color: var(--secondary-bg);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
        }}
        
        .stSelectbox > div > div > select {{
            background-color: var(--secondary-bg);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
        }}
        
        .stTextArea > div > div > textarea {{
            background-color: var(--secondary-bg);
            color: var(--text-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
        }}
        
        /* Enhanced Button styling with gradients and animations */
        .stButton > button {{
            background: var(--gradient-primary);
            color: white;
            border: none;
            border-radius: 15px;
            padding: 1rem 2rem;
            font-weight: 700;
            font-size: 1rem;
            transition: all var(--animation-normal) ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            letter-spacing: 0.5px;
        }}
        
        .stButton > button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left var(--animation-slow) ease;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            background: var(--gradient-cool);
        }}
        
        .stButton > button:hover::before {{
            left: 100%;
        }}
        
        .stButton > button:active {{
            transform: translateY(-1px) scale(1.02);
            transition: all 0.1s ease;
        }}
        
        /* Specialized gradient buttons */
        .success-btn {{
            background: var(--gradient-success) !important;
            color: white !important;
        }}
        
        .warning-btn {{
            background: var(--gradient-warning) !important;
            color: white !important;
        }}
        
        .error-btn {{
            background: var(--gradient-error) !important;
            color: white !important;
        }}
        
        .info-btn {{
            background: var(--gradient-info) !important;
            color: white !important;
        }}
        
        .ocean-btn {{
            background: var(--gradient-ocean) !important;
            color: white !important;
        }}
        
        .sunset-btn {{
            background: var(--gradient-sunset) !important;
            color: white !important;
        }}
        
        .forest-btn {{
            background: var(--gradient-forest) !important;
            color: white !important;
        }}
        
        /* Enhanced Info boxes with gradients and animations */
        .info-box {{
            background: linear-gradient(135deg, var(--secondary-bg) 0%, rgba(255,255,255,0.8) 100%);
            border: none;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1.5rem 0;
            position: relative;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: all var(--animation-normal) ease;
        }}
        
        .info-box::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: var(--gradient-info);
            border-radius: 15px 15px 0 0;
        }}
        
        .info-box:hover {{
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }}
        
        .success-box {{
            background: linear-gradient(135deg, rgba(17, 153, 142, 0.1) 0%, rgba(56, 239, 125, 0.1) 100%);
            border: none;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1.5rem 0;
            position: relative;
            box-shadow: 0 8px 25px rgba(17, 153, 142, 0.1);
        }}
        
        .success-box::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: var(--gradient-success);
            border-radius: 15px 15px 0 0;
        }}
        
        .warning-box {{
            background: linear-gradient(135deg, rgba(240, 147, 251, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%);
            border: none;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1.5rem 0;
            position: relative;
            box-shadow: 0 8px 25px rgba(240, 147, 251, 0.1);
        }}
        
        .warning-box::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: var(--gradient-warning);
            border-radius: 15px 15px 0 0;
        }}
        
        .error-box {{
            background: linear-gradient(135deg, rgba(255, 154, 158, 0.1) 0%, rgba(254, 207, 239, 0.1) 100%);
            border: none;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1.5rem 0;
            position: relative;
            box-shadow: 0 8px 25px rgba(255, 154, 158, 0.1);
        }}
        
        .error-box::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: var(--gradient-error);
            border-radius: 15px 15px 0 0;
        }}
        
        /* Table styling */
        .dataframe {{
            background: var(--secondary-bg) !important;
            color: var(--text-color) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px !important;
        }}
        
        .dataframe th {{
            background: var(--primary-color) !important;
            color: white !important;
            font-weight: 600 !important;
        }}
        
        .dataframe td {{
            border-bottom: 1px solid var(--border-color) !important;
        }}
        
        /* Progress bar */
        .stProgress > div > div > div > div {{
            background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
        }}
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: var(--secondary-bg);
            color: var(--text-color);
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}
        
        .stTabs [aria-selected="true"] {{
            background: var(--accent-color) !important;
            color: white !important;
        }}
        
        /* Expander styling */
        .streamlit-expanderHeader {{
            background: var(--secondary-bg);
            color: var(--text-color);
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}
        
        /* Charts and plots */
        .js-plotly-plot {{
            background: var(--secondary-bg) !important;
            border-radius: 8px !important;
        }}
        
        /* Custom animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.5s ease-out;
        }}
        
        /* Mobile responsive */
        @media (max-width: 768px) {{
            .main-title {{
                font-size: 2rem;
            }}
            
            .metric-card {{
                padding: 1rem;
            }}
            
            .metric-value {{
                font-size: 1.5rem;
            }}
        }}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--secondary-bg);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--accent-color);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--primary-color);
        }}
        
        /* Enhanced Loading spinner with gradient */
        .loading-spinner {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: conic-gradient(from 0deg, var(--primary-color), var(--accent-color), var(--primary-color));
            animation: gradientSpin 1.5s linear infinite;
            margin: 20px auto;
            position: relative;
        }}
        
        .loading-spinner::before {{
            content: '';
            position: absolute;
            top: 3px;
            left: 3px;
            right: 3px;
            bottom: 3px;
            background: var(--background-color);
            border-radius: 50%;
        }}
        
        @keyframes gradientSpin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* Enhanced Status badges with gradients */
        .status-badge {{
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all var(--animation-normal) ease;
        }}
        
        .status-active {{
            background: var(--gradient-success);
            color: white;
        }}
        
        .status-pending {{
            background: var(--gradient-warning);
            color: white;
        }}
        
        .status-inactive {{
            background: var(--gradient-error);
            color: white;
        }}
        
        .status-badge:hover {{
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        
        /* Additional animated elements */
        .floating-element {{
            animation: float 3s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        .bounce-in {{
            animation: bounceIn 0.6s ease-out;
        }}
        
        @keyframes bounceIn {{
            0% {{ transform: scale(0.3); opacity: 0; }}
            50% {{ transform: scale(1.05); opacity: 0.8; }}
            70% {{ transform: scale(0.9); opacity: 1; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        
        .slide-in-left {{
            animation: slideInLeft 0.5s ease-out;
        }}
        
        @keyframes slideInLeft {{
            from {{ transform: translateX(-100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        .slide-in-right {{
            animation: slideInRight 0.5s ease-out;
        }}
        
        @keyframes slideInRight {{
            from {{ transform: translateX(100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        /* Gradient text effect */
        .gradient-text {{
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: bold;
        }}
        
        /* Glassmorphism effect */
        .glass-card {{
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }}
        
        /* Neon glow effect */
        .neon-glow {{
            box-shadow: 0 0 20px var(--accent-color),
                        0 0 40px var(--accent-color),
                        0 0 60px var(--accent-color);
            animation: neonPulse 2s ease-in-out infinite alternate;
        }}
        
        @keyframes neonPulse {{
            from {{ box-shadow: 0 0 20px var(--accent-color), 0 0 40px var(--accent-color), 0 0 60px var(--accent-color); }}
            to {{ box-shadow: 0 0 30px var(--accent-color), 0 0 60px var(--accent-color), 0 0 90px var(--accent-color); }}
        }}
        
        /* Decorative floating elements */
        .floating-shape {{
            position: fixed;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
            z-index: -1;
            animation: floatShape 8s infinite ease-in-out;
        }}
                
        .floating-shape:nth-child(1) {{
            top: 10%;
            left: 5%;
            animation-delay: 0s;
        }}
                
        .floating-shape:nth-child(2) {{
            top: 20%;
            right: 10%;
            width: 120px;
            height: 120px;
            animation-delay: 1s;
        }}
                
        .floating-shape:nth-child(3) {{
            bottom: 30%;
            left: 15%;
            width: 60px;
            height: 60px;
            animation-delay: 2s;
        }}
                
        .floating-shape:nth-child(4) {{
            bottom: 15%;
            right: 20%;
            width: 100px;
            height: 100px;
            animation-delay: 3s;
        }}
                
        @keyframes floatShape {{
            0%, 100% {{
                transform: translate(0, 0) rotate(0deg);
            }}
            25% {{
                transform: translate(20px, 20px) rotate(10deg);
            }}
            50% {{
                transform: translate(0, 40px) rotate(0deg);
            }}
            75% {{
                transform: translate(-20px, 20px) rotate(-10deg);
            }}
        }}
                
        /* Custom scrollbar enhancements */
        ::-webkit-scrollbar {{
            width: 12px;
        }}
                
        ::-webkit-scrollbar-track {{
            background: var(--secondary-bg);
            border-radius: 10px;
        }}
                
        ::-webkit-scrollbar-thumb {{
            background: var(--gradient-primary);
            border-radius: 10px;
            border: 2px solid var(--secondary-bg);
        }}
                
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--gradient-cool);
        }}
                
        /* Vibrant hover effects for interactive elements */
        .stButton > button:hover {{
            background: var(--gradient-warm) !important;
        }}
                
        .stSelectbox > div > div > select:hover {{
            border: 1px solid var(--accent-color);
            box-shadow: 0 0 15px rgba(118, 75, 162, 0.3);
        }}
                
        .stTextInput > div > div > input:hover {{
            border: 1px solid var(--accent-color);
            box-shadow: 0 0 15px rgba(102, 126, 234, 0.3);
        }}
                
        /* Colorful borders for containers */
        .st-emotion-cache-13ln4jf {{
            border: 2px solid transparent;
            border-radius: 15px;
            background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #f5576c) !important;
            background-size: 400% 400% !important;
            animation: colorfulBorder 10s ease infinite;
            position: relative;
        }}
        
        @keyframes colorfulBorder {{
            0% {{ background-position: 0% 50%; }}
            25% {{ background-position: 100% 50%; }}
            50% {{ background-position: 100% 100%; }}
            75% {{ background-position: 0% 100%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        /* Responsive enhancements */
        @media (max-width: 768px) {{
            .main-title {{
                font-size: 2.5rem;
            }}
            
            .metric-card {{
                padding: 1rem;
            }}
            
            .logo-container {{
                padding: 2rem 0;
            }}
        }}
        
        @media (max-width: 480px) {{
            .main-title {{
                font-size: 2rem;
            }}
            
            .stButton > button {{
                padding: 0.8rem 1.5rem;
                font-size: 0.9rem;
            }}
        }}
        
        </style>
        """
        
        return css
    
    def set_theme(self, theme_name):
        """Set the current theme"""
        if 'current_theme' not in st.session_state:
            st.session_state['current_theme'] = theme_name
        else:
            st.session_state['current_theme'] = theme_name
    
    def get_current_theme(self):
        """Get current theme name"""
        return st.session_state.get('current_theme', 'light')

# Global theme manager instance
theme_manager = ThemeManager()

def get_theme_css():
    """Get CSS for current theme"""
    current_theme = theme_manager.get_current_theme()
    return theme_manager.get_theme_css(current_theme)

def set_theme(theme_name):
    """Set theme"""
    theme_manager.set_theme(theme_name)