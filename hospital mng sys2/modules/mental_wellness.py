import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication
from utils.database import db
from utils.ui_components import create_metric_card, create_alert_box, create_progress_bar
from utils.voice_utils import voice_assistant
from config.themes import get_theme_css

class MentalWellnessCompanion:
    def __init__(self):
        self.mood_options = [
            "😊 Very Happy", "🙂 Happy", "😐 Neutral", "😔 Sad", "😢 Very Sad",
            "😤 Stressed", "😴 Tired", "😡 Angry", "😰 Anxious", "😌 Calm"
        ]
        
        self.stress_levels = ["Low", "Moderate", "High", "Very High"]
        
        self.meditation_types = [
            "Mindfulness", "Breathing", "Body Scan", "Loving-Kindness",
            "Walking", "Sleep", "Anxiety Relief", "Focus"
        ]
        
    def track_mood(self, patient_id, mood, stress_level, notes=""):
        """Track patient's mood and stress level"""
        mood_entry = {
            'id': f"mood_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'patient_id': patient_id,
            'date': datetime.now().isoformat(),
            'mood': mood,
            'stress_level': stress_level,
            'notes': notes
        }
        
        # Add to database (simulate)
        return mood_entry
    
    def get_mood_history(self, patient_id, days=30):
        """Get patient's mood history"""
        # Simulate mood history data
        mood_history = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            mood_history.append({
                'date': date.isoformat(),
                'mood': np.random.choice(self.mood_options),
                'stress_level': np.random.choice(self.stress_levels),
                'notes': f"Day {i+1} mood entry"
            })
        
        return mood_history
    
    def analyze_mood_trends(self, mood_history):
        """Analyze mood and stress trends"""
        if not mood_history:
            return None
        
        df = pd.DataFrame(mood_history)
        df['date'] = pd.to_datetime(df['date'])
        
        # Mood distribution
        mood_distribution = df['mood'].value_counts()
        
        # Stress level trends
        stress_trend = df.groupby(df['date'].dt.to_period('D'))['stress_level'].value_counts().unstack(fill_value=0)
        
        # Weekly mood average
        weekly_mood = df.groupby(df['date'].dt.to_period('W')).size()
        
        return {
            'mood_distribution': mood_distribution,
            'stress_trend': stress_trend,
            'weekly_mood': weekly_mood
        }
    
    def get_meditation_guide(self, meditation_type):
        """Get meditation guide for specific type"""
        guides = {
            "Mindfulness": {
                "duration": "10 minutes",
                "steps": [
                    "Find a comfortable sitting position",
                    "Close your eyes and take deep breaths",
                    "Focus on your breath - inhale and exhale",
                    "When thoughts arise, gently return to breath",
                    "Continue for 10 minutes"
                ],
                "benefits": ["Reduces stress", "Improves focus", "Enhances self-awareness"]
            },
            "Breathing": {
                "duration": "5 minutes",
                "steps": [
                    "Sit comfortably with your back straight",
                    "Place one hand on your chest, one on your belly",
                    "Breathe in for 4 counts",
                    "Hold for 4 counts",
                    "Breathe out for 6 counts",
                    "Repeat the cycle"
                ],
                "benefits": ["Calms nervous system", "Reduces anxiety", "Improves sleep"]
            },
            "Body Scan": {
                "duration": "15 minutes",
                "steps": [
                    "Lie down in a comfortable position",
                    "Start from your toes, notice any sensations",
                    "Move attention up through your body",
                    "Scan each part: legs, torso, arms, head",
                    "Release tension as you go"
                ],
                "benefits": ["Reduces body tension", "Improves body awareness", "Promotes relaxation"]
            }
        }
        
        return guides.get(meditation_type, guides["Mindfulness"])
    
    def assess_stress_level(self, responses):
        """Assess stress level based on questionnaire responses"""
        # Simple stress assessment
        stress_score = sum(responses.values())
        
        if stress_score <= 5:
            return "Low", "You're managing stress well!"
        elif stress_score <= 10:
            return "Moderate", "Consider stress management techniques"
        elif stress_score <= 15:
            return "High", "Please consider professional help"
        else:
            return "Very High", "Immediate professional support recommended"
    
    def get_wellness_resources(self):
        """Get wellness resources and tips"""
        resources = {
            "Daily Tips": [
                "Practice gratitude - write 3 things you're thankful for",
                "Take regular breaks from screens",
                "Connect with loved ones daily",
                "Get adequate sleep (7-9 hours)",
                "Exercise regularly, even just a short walk"
            ],
            "Coping Strategies": [
                "Deep breathing exercises",
                "Progressive muscle relaxation",
                "Mindful walking",
                "Journaling your thoughts",
                "Listening to calming music"
            ],
            "Professional Help": [
                "Talk to your doctor about mental health",
                "Consider therapy or counseling",
                "Join support groups",
                "Use crisis helplines if needed",
                "Practice self-compassion"
            ]
        }
        
        return resources

def main():
    """Main function for Mental Wellness Companion module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the Mental Wellness Companion")
        return
    
    # Initialize companion
    companion = MentalWellnessCompanion()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">🧘 Mental Wellness Companion</h1>
        <p class="body-text">Your personal mental health and wellness guide</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "😊 Mood Tracker", "🧘‍♀️ Meditation", "📊 Wellness Analytics", 
        "📝 Stress Assessment", "💡 Resources"
    ])
    
    with tab1:
        st.markdown("### 😊 Daily Mood Tracker")
        
        # Mood tracking form
        with st.form("mood_tracker"):
            col1, col2 = st.columns(2)
            
            with col1:
                mood = st.selectbox("How are you feeling today?", companion.mood_options)
                stress_level = st.selectbox("Stress Level", companion.stress_levels)
            
            with col2:
                notes = st.text_area("Any notes about your mood? (optional)")
                
                if st.form_submit_button("📝 Log Mood"):
                    # Track mood
                    mood_entry = companion.track_mood(
                        st.session_state.get('user', {}).get('id', 'patient_001'),
                        mood, stress_level, notes
                    )
                    st.success("✅ Mood logged successfully!")
        
        # Recent mood history
        st.markdown("### 📅 Recent Mood History")
        
        patient_id = st.session_state.get('user', {}).get('id', 'patient_001')
        mood_history = companion.get_mood_history(patient_id, days=7)
        
        if mood_history:
            # Display recent entries
            for entry in mood_history[:5]:
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    st.markdown(f"**{entry['date'][:10]}**")
                with col2:
                    st.markdown(entry['mood'])
                with col3:
                    st.markdown(f"Stress: {entry['stress_level']}")
                st.markdown("---")
    
    with tab2:
        st.markdown("### 🧘‍♀️ Meditation & Relaxation")
        
        # Meditation selection
        meditation_type = st.selectbox("Choose Meditation Type", companion.meditation_types)
        
        if meditation_type:
            guide = companion.get_meditation_guide(meditation_type)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"#### {meditation_type} Meditation")
                st.markdown(f"**Duration:** {guide['duration']}")
                
                st.markdown("**Steps:**")
                for i, step in enumerate(guide['steps'], 1):
                    st.markdown(f"{i}. {step}")
                
                st.markdown("**Benefits:**")
                for benefit in guide['benefits']:
                    st.markdown(f"• {benefit}")
            
            with col2:
                # Meditation timer
                st.markdown("#### ⏱️ Meditation Timer")
                
                duration_minutes = int(guide['duration'].split()[0])
                
                if st.button("🎵 Start Meditation"):
                    st.info(f"🧘‍♀️ Starting {meditation_type} meditation for {duration_minutes} minutes...")
                    st.success("✅ Meditation session completed!")
                
                # Voice guidance
                if st.button("🎤 Voice Guidance"):
                    voice_assistant.speak(f"Let's begin {meditation_type} meditation. {guide['steps'][0]}")
        
        # Quick relaxation techniques
        st.markdown("### 🍃 Quick Relaxation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🫁 Deep Breathing"):
                st.info("Inhale for 4, hold for 4, exhale for 6...")
        
        with col2:
            if st.button("🫂 Progressive Relaxation"):
                st.info("Tense and release each muscle group...")
        
        with col3:
            if st.button("🚶‍♀️ Mindful Walking"):
                st.info("Focus on each step and your surroundings...")
    
    with tab3:
        st.markdown("### 📊 Wellness Analytics")
        
        # Get mood analytics
        patient_id = st.session_state.get('user', {}).get('id', 'patient_001')
        mood_history = companion.get_mood_history(patient_id, days=30)
        trends = companion.analyze_mood_trends(mood_history)
        
        if trends:
            col1, col2 = st.columns(2)
            
            with col1:
                # Mood distribution
                fig = px.pie(
                    values=trends['mood_distribution'].values,
                    names=trends['mood_distribution'].index,
                    title="Mood Distribution (30 days)"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Weekly mood trend
                fig2 = px.line(
                    x=trends['weekly_mood'].index.astype(str),
                    y=trends['weekly_mood'].values,
                    title="Weekly Mood Entries"
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            # Wellness score
            st.markdown("### 🎯 Wellness Score")
            
            # Calculate wellness score (simplified)
            positive_moods = sum(1 for entry in mood_history if "Happy" in entry['mood'] or "Calm" in entry['mood'])
            total_entries = len(mood_history)
            wellness_score = (positive_moods / total_entries) * 100 if total_entries > 0 else 0
            
            create_progress_bar(wellness_score, 100, f"Wellness Score: {wellness_score:.1f}%")
            
            if wellness_score >= 70:
                create_alert_box("Great job! You're maintaining good mental wellness.", "success")
            elif wellness_score >= 50:
                create_alert_box("You're doing okay. Consider more self-care activities.", "warning")
            else:
                create_alert_box("Consider reaching out for support or professional help.", "error")
    
    with tab4:
        st.markdown("### 📝 Stress Assessment")
        
        # Stress assessment questionnaire
        st.markdown("#### How often do you experience the following?")
        
        questions = {
            "Feeling overwhelmed": "How often do you feel overwhelmed?",
            "Sleep problems": "Do you have trouble sleeping?",
            "Irritability": "Do you feel irritable or easily frustrated?",
            "Concentration issues": "Do you have trouble concentrating?",
            "Physical tension": "Do you experience muscle tension or headaches?"
        }
        
        responses = {}
        
        for key, question in questions.items():
            responses[key] = st.selectbox(
                question,
                ["Never", "Rarely", "Sometimes", "Often", "Always"],
                key=f"stress_{key}"
            )
        
        # Calculate stress score
        score_mapping = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4}
        stress_responses = {k: score_mapping[v] for k, v in responses.items()}
        
        if st.button("📊 Assess Stress Level"):
            stress_level, message = companion.assess_stress_level(stress_responses)
            
            st.markdown(f"### Assessment Result")
            create_metric_card("Stress Level", stress_level, "📊")
            create_alert_box(message, "info" if stress_level == "Low" else "warning")
            
            # Recommendations based on stress level
            if stress_level in ["High", "Very High"]:
                st.markdown("**Immediate Recommendations:**")
                st.markdown("• Practice deep breathing exercises")
                st.markdown("• Take short breaks throughout the day")
                st.markdown("• Consider talking to a mental health professional")
                st.markdown("• Engage in physical activity")
    
    with tab5:
        st.markdown("### 💡 Wellness Resources")
        
        resources = companion.get_wellness_resources()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🌟 Daily Tips")
            for tip in resources["Daily Tips"]:
                st.markdown(f"• {tip}")
        
        with col2:
            st.markdown("#### 🛠️ Coping Strategies")
            for strategy in resources["Coping Strategies"]:
                st.markdown(f"• {strategy}")
        
        with col3:
            st.markdown("#### 🆘 Professional Help")
            for help_option in resources["Professional Help"]:
                st.markdown(f"• {help_option}")
        
        # Crisis resources
        st.markdown("### 🆘 Crisis Resources")
        
        crisis_resources = [
            "National Suicide Prevention Lifeline: 988",
            "Crisis Text Line: Text HOME to 741741",
            "Emergency Services: 911",
            "Your local mental health crisis line"
        ]
        
        for resource in crisis_resources:
            st.markdown(f"**{resource}**")
        
        st.markdown("> *Remember: It's okay to ask for help. You don't have to go through difficult times alone.*")

if __name__ == "__main__":
    main()
