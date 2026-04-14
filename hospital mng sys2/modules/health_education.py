import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.auth import check_authentication
from utils.database import db
from utils.ui_components import create_metric_card, create_alert_box, create_progress_bar
from utils.image_utils import create_image_display
from config.themes import get_theme_css

class HealthEducationHub:
    def __init__(self):
        self.health_topics = {
            "Cardiovascular Health": {
                "description": "Learn about heart health, blood pressure, and cardiovascular diseases",
                "articles": [
                    "Understanding Blood Pressure",
                    "Heart-Healthy Diet Tips",
                    "Exercise for Heart Health",
                    "Signs of Heart Attack"
                ],
                "image_url": "https://example.com/heart-health.jpg"
            },
            "Diabetes Management": {
                "description": "Comprehensive guide to diabetes care and management",
                "articles": [
                    "Understanding Diabetes Types",
                    "Blood Sugar Monitoring",
                    "Diabetes-Friendly Diet",
                    "Exercise and Diabetes"
                ],
                "image_url": "https://example.com/diabetes.jpg"
            },
            "Mental Health": {
                "description": "Resources for mental wellness and psychological health",
                "articles": [
                    "Stress Management Techniques",
                    "Anxiety and Depression",
                    "Mindfulness Practices",
                    "Getting Help for Mental Health"
                ],
                "image_url": "https://example.com/mental-health.jpg"
            },
            "Nutrition": {
                "description": "Healthy eating guidelines and nutritional information",
                "articles": [
                    "Balanced Diet Basics",
                    "Vitamins and Minerals",
                    "Healthy Meal Planning",
                    "Food Safety Guidelines"
                ],
                "image_url": "https://example.com/nutrition.jpg"
            },
            "Exercise & Fitness": {
                "description": "Physical activity guidelines and fitness tips",
                "articles": [
                    "Getting Started with Exercise",
                    "Strength Training Basics",
                    "Cardiovascular Exercise",
                    "Exercise Safety Tips"
                ],
                "image_url": "https://example.com/fitness.jpg"
            }
        }
        
        self.health_quizzes = {
            "Heart Health Quiz": {
                "questions": [
                    {
                        "question": "What is a normal blood pressure reading?",
                        "options": ["120/80", "140/90", "160/100", "180/110"],
                        "correct": 0
                    },
                    {
                        "question": "Which exercise is best for heart health?",
                        "options": ["Walking", "Weight lifting", "Yoga", "All of the above"],
                        "correct": 3
                    }
                ]
            },
            "Diabetes Awareness Quiz": {
                "questions": [
                    {
                        "question": "What is the main symptom of diabetes?",
                        "options": ["Fever", "Increased thirst", "Headache", "Cough"],
                        "correct": 1
                    },
                    {
                        "question": "Which food should diabetics avoid?",
                        "options": ["Vegetables", "Fruits", "Sugary drinks", "Lean protein"],
                        "correct": 2
                    }
                ]
            }
        }
    
    def get_health_tips(self, category=None):
        """Get health tips by category"""
        tips = {
            "General": [
                "Drink 8 glasses of water daily",
                "Get 7-9 hours of sleep each night",
                "Wash your hands frequently",
                "Take regular breaks from screens"
            ],
            "Cardiovascular": [
                "Exercise for at least 30 minutes daily",
                "Limit salt intake to 2,300mg per day",
                "Quit smoking and avoid secondhand smoke",
                "Monitor your blood pressure regularly"
            ],
            "Mental Health": [
                "Practice mindfulness or meditation",
                "Stay connected with friends and family",
                "Seek professional help when needed",
                "Maintain a regular sleep schedule"
            ],
            "Nutrition": [
                "Eat a variety of colorful fruits and vegetables",
                "Choose whole grains over refined grains",
                "Limit processed foods and added sugars",
                "Include lean protein in every meal"
            ]
        }
        
        if category and category in tips:
            return tips[category]
        return tips["General"]
    
    def get_article_content(self, article_title):
        """Get content for a specific article"""
        articles = {
            "Understanding Blood Pressure": {
                "content": """
                Blood pressure is the force of blood pushing against the walls of your arteries. 
                Normal blood pressure is less than 120/80 mmHg. High blood pressure (hypertension) 
                can lead to serious health problems like heart disease and stroke.
                
                **Key Points:**
                - Systolic pressure (top number) should be under 120
                - Diastolic pressure (bottom number) should be under 80
                - Regular monitoring is important
                - Lifestyle changes can help manage blood pressure
                """,
                "image_url": "https://example.com/blood-pressure.jpg"
            },
            "Heart-Healthy Diet Tips": {
                "content": """
                A heart-healthy diet focuses on whole foods, lean proteins, and healthy fats.
                
                **Recommended Foods:**
                - Fruits and vegetables (5 servings daily)
                - Whole grains (brown rice, quinoa, oats)
                - Lean proteins (fish, chicken, beans)
                - Healthy fats (olive oil, nuts, avocados)
                
                **Foods to Limit:**
                - Saturated and trans fats
                - Added sugars and salt
                - Processed foods
                - Red meat
                """,
                "image_url": "https://example.com/heart-diet.jpg"
            }
        }
        
        return articles.get(article_title, {
            "content": "Article content coming soon...",
            "image_url": None
        })
    
    def calculate_quiz_score(self, quiz_name, answers):
        """Calculate quiz score"""
        if quiz_name not in self.health_quizzes:
            return 0
        
        quiz = self.health_quizzes[quiz_name]
        correct_answers = 0
        
        for i, answer in enumerate(answers):
            if i < len(quiz["questions"]) and answer == quiz["questions"][i]["correct"]:
                correct_answers += 1
        
        return (correct_answers / len(quiz["questions"])) * 100

def main():
    """Main function for Health Education Hub module"""
    
    # Apply theme CSS
    st.markdown(get_theme_css(st.session_state.get('theme', 'light')), unsafe_allow_html=True)
    
    # Check authentication
    if not check_authentication():
        st.error("🔒 Please log in to access the Health Education Hub")
        return
    
    # Initialize education hub
    education_hub = HealthEducationHub()
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1 class="futuristic-text">📚 Health Education Hub</h1>
        <p class="body-text">Your comprehensive health education resource</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 Health Topics", "💡 Daily Tips", "🧠 Health Quizzes", 
        "📋 Learning Progress", "🔍 Search Resources"
    ])
    
    with tab1:
        st.markdown("### 📖 Health Topics")
        
        # Topic selection
        topic_options = list(education_hub.health_topics.keys())
        selected_topic = st.selectbox("Select Health Topic", topic_options)
        
        if selected_topic:
            topic_info = education_hub.health_topics[selected_topic]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"#### {selected_topic}")
                st.markdown(topic_info["description"])
                
                st.markdown("**Available Articles:**")
                for article in topic_info["articles"]:
                    if st.button(f"📄 {article}", key=f"article_{article}"):
                        st.session_state.selected_article = article
            
            with col2:
                if topic_info.get("image_url"):
                    create_image_display(topic_info["image_url"], selected_topic)
            
            # Display selected article
            if hasattr(st.session_state, 'selected_article'):
                article_content = education_hub.get_article_content(st.session_state.selected_article)
                
                st.markdown("---")
                st.markdown(f"### 📄 {st.session_state.selected_article}")
                
                if article_content.get("image_url"):
                    create_image_display(article_content["image_url"], st.session_state.selected_article)
                
                st.markdown(article_content["content"])
                
                # Article actions
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📱 Save Article"):
                        st.success("✅ Article saved to your library!")
                
                with col2:
                    if st.button("📤 Share Article"):
                        st.info("📤 Sharing article...")
                
                with col3:
                    if st.button("📝 Take Notes"):
                        st.text_area("Your Notes:", placeholder="Add your personal notes here...")
    
    with tab2:
        st.markdown("### 💡 Daily Health Tips")
        
        # Tip category selection
        tip_categories = ["General", "Cardiovascular", "Mental Health", "Nutrition"]
        selected_category = st.selectbox("Select Tip Category", tip_categories)
        
        tips = education_hub.get_health_tips(selected_category)
        
        st.markdown(f"#### {selected_category} Health Tips")
        
        for i, tip in enumerate(tips, 1):
            with st.expander(f"💡 Tip {i}"):
                st.markdown(tip)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"✅ Mark as Done", key=f"done_{i}"):
                        st.success("✅ Tip completed!")
                
                with col2:
                    if st.button(f"📅 Set Reminder", key=f"reminder_{i}"):
                        st.info("📅 Reminder set for tomorrow!")
        
        # Tip of the day
        st.markdown("### 🌟 Tip of the Day")
        
        daily_tip = np.random.choice(tips)
        
        create_alert_box(f"**Today's Tip:** {daily_tip}", "info")
        
        if st.button("🎯 Get Another Tip"):
            st.rerun()
    
    with tab3:
        st.markdown("### 🧠 Health Quizzes")
        
        # Quiz selection
        quiz_options = list(education_hub.health_quizzes.keys())
        selected_quiz = st.selectbox("Select Quiz", quiz_options)
        
        if selected_quiz:
            quiz = education_hub.health_quizzes[selected_quiz]
            
            st.markdown(f"#### {selected_quiz}")
            st.markdown(f"**Questions:** {len(quiz['questions'])}")
            
            # Quiz interface
            if 'quiz_answers' not in st.session_state:
                st.session_state.quiz_answers = {}
            
            if 'quiz_submitted' not in st.session_state:
                st.session_state.quiz_submitted = False
            
            if not st.session_state.quiz_submitted:
                # Display questions
                for i, question_data in enumerate(quiz['questions']):
                    st.markdown(f"**Question {i+1}:** {question_data['question']}")
                    
                    answer = st.radio(
                        "Select your answer:",
                        question_data['options'],
                        key=f"quiz_q_{i}",
                        label_visibility="collapsed"
                    )
                    
                    st.session_state.quiz_answers[i] = question_data['options'].index(answer)
                
                if st.button("📝 Submit Quiz"):
                    st.session_state.quiz_submitted = True
                    st.rerun()
            
            else:
                # Show results
                score = education_hub.calculate_quiz_score(selected_quiz, st.session_state.quiz_answers.values())
                
                st.markdown("### 📊 Quiz Results")
                
                create_progress_bar(score, 100, f"Your Score: {score:.1f}%")
                
                if score >= 80:
                    create_alert_box("🎉 Excellent! You have a great understanding of this topic.", "success")
                elif score >= 60:
                    create_alert_box("👍 Good job! You have a good understanding.", "info")
                else:
                    create_alert_box("📚 Keep learning! Review the materials and try again.", "warning")
                
                # Show correct answers
                st.markdown("### ✅ Correct Answers")
                
                for i, question_data in enumerate(quiz['questions']):
                    user_answer = st.session_state.quiz_answers.get(i, -1)
                    correct_answer = question_data['correct']
                    
                    if user_answer == correct_answer:
                        st.markdown(f"✅ **Q{i+1}:** {question_data['question']}")
                        st.markdown(f"   Your answer: {question_data['options'][user_answer]} (Correct!)")
                    else:
                        st.markdown(f"❌ **Q{i+1}:** {question_data['question']}")
                        st.markdown(f"   Your answer: {question_data['options'][user_answer]}")
                        st.markdown(f"   Correct answer: {question_data['options'][correct_answer]}")
                
                # Reset quiz
                if st.button("🔄 Take Quiz Again"):
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.rerun()
    
    with tab4:
        st.markdown("### 📋 Learning Progress")
        
        # Simulate learning progress
        progress_data = {
            "Articles Read": 15,
            "Quizzes Completed": 8,
            "Average Quiz Score": 85,
            "Topics Explored": 5,
            "Tips Completed": 23,
            "Days Active": 12
        }
        
        # Progress metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            create_metric_card("Articles Read", progress_data["Articles Read"], "📖")
            create_metric_card("Quizzes Completed", progress_data["Quizzes Completed"], "🧠")
        
        with col2:
            create_metric_card("Avg. Quiz Score", f"{progress_data['Average Quiz Score']}%", "📊")
            create_metric_card("Topics Explored", progress_data["Topics Explored"], "📚")
        
        with col3:
            create_metric_card("Tips Completed", progress_data["Tips Completed"], "💡")
            create_metric_card("Days Active", progress_data["Days Active"], "📅")
        
        # Learning streak
        st.markdown("### 🔥 Learning Streak")
        
        streak_days = 5
        create_progress_bar(streak_days, 7, f"Current Streak: {streak_days} days")
        
        if streak_days >= 7:
            create_alert_box("🎉 Amazing! You've maintained a 7-day learning streak!", "success")
        elif streak_days >= 3:
            create_alert_box("🔥 Great! Keep up the learning momentum!", "info")
        else:
            create_alert_box("💪 Start building your learning streak today!", "warning")
        
        # Recommended next steps
        st.markdown("### 🎯 Recommended Next Steps")
        
        recommendations = [
            "Complete the Heart Health Quiz",
            "Read 'Understanding Blood Pressure' article",
            "Try the daily meditation tip",
            "Explore the Nutrition topic"
        ]
        
        for rec in recommendations:
            st.markdown(f"• {rec}")
    
    with tab5:
        st.markdown("### 🔍 Search Health Resources")
        
        # Search interface
        search_term = st.text_input("Search for health topics, articles, or tips:")
        
        if search_term:
            st.markdown(f"**Search results for '{search_term}':**")
            
            # Search in topics
            for topic, info in education_hub.health_topics.items():
                if search_term.lower() in topic.lower() or search_term.lower() in info["description"].lower():
                    with st.expander(f"📚 {topic}"):
                        st.markdown(info["description"])
                        st.markdown("**Articles:**")
                        for article in info["articles"]:
                            st.markdown(f"• {article}")
            
            # Search in tips
            all_tips = []
            for category in ["General", "Cardiovascular", "Mental Health", "Nutrition"]:
                tips = education_hub.get_health_tips(category)
                for tip in tips:
                    if search_term.lower() in tip.lower():
                        all_tips.append((category, tip))
            
            if all_tips:
                st.markdown("**💡 Related Tips:**")
                for category, tip in all_tips:
                    st.markdown(f"• **{category}:** {tip}")
        
        # Popular searches
        st.markdown("### 🔥 Popular Searches")
        
        popular_searches = [
            "blood pressure", "diabetes", "exercise", "nutrition",
            "mental health", "heart disease", "weight loss", "sleep"
        ]
        
        cols = st.columns(4)
        for i, search in enumerate(popular_searches):
            with cols[i % 4]:
                if st.button(f"🔍 {search.title()}", key=f"pop_{i}"):
                    st.info(f"Searching for '{search}'...")

if __name__ == "__main__":
    main()
