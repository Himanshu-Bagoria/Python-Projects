import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import qrcode
from PIL import Image
import io
import base64

def create_glow_button(text, key=None, on_click=None):
    """Create a glowing button with futuristic design"""
    return st.button(
        text,
        key=key,
        on_click=on_click,
        help="Click to proceed"
    )

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """Create a metric card with animated design"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{title}</h3>
            <h2>{value}</h2>
            {f'<p style="color: {"green" if delta_color == "normal" else "red"}">{delta}</p>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)

def create_animated_chart(data, chart_type="line", title="Chart"):
    """Create animated charts with Plotly"""
    if chart_type == "line":
        fig = px.line(data, x=data.index, y=data.values, title=title)
    elif chart_type == "bar":
        fig = px.bar(data, x=data.index, y=data.values, title=title)
    elif chart_type == "scatter":
        fig = px.scatter(data, x=data.index, y=data.values, title=title)
    
    fig.update_layout(
        template="plotly_dark" if st.session_state.get('theme') == 'dark' else "plotly_white",
        title_font_size=20,
        showlegend=True,
        height=400
    )
    
    return fig

def create_vital_signs_chart():
    """Create real-time vital signs chart"""
    # Simulate real-time data
    time_points = pd.date_range(start=datetime.now() - timedelta(minutes=30), 
                               end=datetime.now(), freq='1min')
    
    heart_rate = np.random.normal(75, 10, len(time_points))
    oxygen_sat = np.random.normal(98, 2, len(time_points))
    temperature = np.random.normal(37, 0.5, len(time_points))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=time_points,
        y=heart_rate,
        name='Heart Rate (BPM)',
        line=dict(color='#ff6b6b', width=3),
        fill='tonexty'
    ))
    
    fig.add_trace(go.Scatter(
        x=time_points,
        y=oxygen_sat,
        name='Oxygen Saturation (%)',
        line=dict(color='#4ecdc4', width=3),
        yaxis='y2'
    ))
    
    fig.add_trace(go.Scatter(
        x=time_points,
        y=temperature,
        name='Temperature (°C)',
        line=dict(color='#45b7d1', width=3),
        yaxis='y3'
    ))
    
    fig.update_layout(
        title="Real-Time Vital Signs",
        xaxis_title="Time",
        yaxis=dict(title="Heart Rate (BPM)", side="left"),
        yaxis2=dict(title="Oxygen Saturation (%)", side="right", overlaying="y"),
        yaxis3=dict(title="Temperature (°C)", side="right", overlaying="y", position=0.95),
        height=400,
        showlegend=True,
        template="plotly_dark" if st.session_state.get('theme') == 'dark' else "plotly_white"
    )
    
    return fig

def create_qr_code(data, size=200):
    """Create QR code for prescriptions, payments, etc."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for display
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str

def display_qr_code(data, title="QR Code"):
    """Display QR code in Streamlit"""
    img_str = create_qr_code(data)
    st.markdown(f"""
    <div style="text-align: center;">
        <h4>{title}</h4>
        <img src="data:image/png;base64,{img_str}" style="width: 200px; height: 200px;">
    </div>
    """, unsafe_allow_html=True)

def create_progress_bar(value, max_value, title="Progress"):
    """Create animated progress bar"""
    progress = value / max_value
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <h4>{title}</h4>
        <div style="background: #f0f0f0; border-radius: 10px; height: 20px; overflow: hidden;">
            <div style="background: linear-gradient(45deg, #667eea, #764ba2); 
                        height: 100%; width: {progress * 100}%; 
                        transition: width 0.5s ease; border-radius: 10px;"></div>
        </div>
        <p style="text-align: center; margin-top: 0.5rem;">{value}/{max_value} ({progress*100:.1f}%)</p>
    </div>
    """, unsafe_allow_html=True)

def create_alert_box(message, alert_type="info"):
    """Create styled alert boxes"""
    colors = {
        "info": "#3498db",
        "success": "#2ecc71",
        "warning": "#f39c12",
        "error": "#e74c3c"
    }
    
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    st.markdown(f"""
    <div style="background: {colors[alert_type]}; color: white; padding: 1rem; 
                border-radius: 10px; margin: 1rem 0; display: flex; align-items: center;">
        <span style="font-size: 1.5rem; margin-right: 1rem;">{icons[alert_type]}</span>
        <span>{message}</span>
    </div>
    """, unsafe_allow_html=True)

def create_body_map():
    """Create interactive body map for symptom selection"""
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h3>Select Affected Body Area</h3>
        <div style="position: relative; display: inline-block;">
            <svg width="300" height="400" viewBox="0 0 300 400">
                <!-- Head -->
                <circle cx="150" cy="50" r="30" fill="#ff6b6b" opacity="0.7" 
                        style="cursor: pointer;" onclick="selectArea('head')"/>
                <text x="150" y="55" text-anchor="middle" fill="white" font-weight="bold">Head</text>
                
                <!-- Chest -->
                <rect x="120" y="80" width="60" height="80" fill="#4ecdc4" opacity="0.7"
                      style="cursor: pointer;" onclick="selectArea('chest')"/>
                <text x="150" y="125" text-anchor="middle" fill="white" font-weight="bold">Chest</text>
                
                <!-- Arms -->
                <rect x="50" y="100" width="30" height="100" fill="#45b7d1" opacity="0.7"
                      style="cursor: pointer;" onclick="selectArea('left_arm')"/>
                <rect x="220" y="100" width="30" height="100" fill="#45b7d1" opacity="0.7"
                      style="cursor: pointer;" onclick="selectArea('right_arm')"/>
                <text x="85" y="150" text-anchor="middle" fill="white" font-weight="bold">Arms</text>
                
                <!-- Abdomen -->
                <rect x="120" y="160" width="60" height="60" fill="#f39c12" opacity="0.7"
                      style="cursor: pointer;" onclick="selectArea('abdomen')"/>
                <text x="150" y="195" text-anchor="middle" fill="white" font-weight="bold">Abdomen</text>
                
                <!-- Legs -->
                <rect x="100" y="220" width="25" height="120" fill="#9b59b6" opacity="0.7"
                      style="cursor: pointer;" onclick="selectArea('left_leg')"/>
                <rect x="175" y="220" width="25" height="120" fill="#9b59b6" opacity="0.7"
                      style="cursor: pointer;" onclick="selectArea('right_leg')"/>
                <text x="150" y="280" text-anchor="middle" fill="white" font-weight="bold">Legs</text>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_voice_button(text="🎤 Voice Input"):
    """Create voice input button"""
    return st.button(text, key="voice_input")

def create_image_display(image_url, title="Image", width=300):
    """Display image from URL with error handling"""
    try:
        st.markdown(f"""
        <div style="text-align: center; margin: 1rem 0;">
            <h4>{title}</h4>
            <img src="{image_url}" style="width: {width}px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.2);">
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading image: {e}")

def create_timeline_chart(data):
    """Create timeline chart for medical history"""
    fig = go.Figure()
    
    for i, (date, event, category) in enumerate(data):
        fig.add_trace(go.Scatter(
            x=[date],
            y=[i],
            mode='markers+text',
            marker=dict(size=15, color='#667eea'),
            text=[event],
            textposition="middle right",
            name=category
        ))
    
    fig.update_layout(
        title="Medical History Timeline",
        xaxis_title="Date",
        yaxis_title="Events",
        height=400,
        showlegend=False,
        template="plotly_dark" if st.session_state.get('theme') == 'dark' else "plotly_white"
    )
    
    return fig

def create_radar_chart(categories, values, title="Health Metrics"):
    """Create radar chart for health metrics"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current',
        line_color='#667eea'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title=title,
        height=400
    )
    
    return fig

def create_animated_counter(target_value, duration=2000):
    """Create animated counter for statistics"""
    st.markdown(f"""
    <div style="text-align: center;">
        <div class="counter" data-target="{target_value}" data-duration="{duration}">
            <span class="counter-value">0</span>
        </div>
    </div>
    <script>
        function animateCounter(element, target, duration) {{
            let start = 0;
            const increment = target / (duration / 16);
            
            function updateCounter() {{
                start += increment;
                if (start < target) {{
                    element.textContent = Math.floor(start);
                    requestAnimationFrame(updateCounter);
                }} else {{
                    element.textContent = target;
                }}
            }}
            
            updateCounter();
        }}
        
        document.querySelectorAll('.counter').forEach(counter => {{
            const target = parseInt(counter.dataset.target);
            const duration = parseInt(counter.dataset.duration);
            const valueElement = counter.querySelector('.counter-value');
            animateCounter(valueElement, target, duration);
        }});
    </script>
    """, unsafe_allow_html=True)
