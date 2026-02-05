import streamlit as st
from utils.auth import login_required

@login_required
def health_education():
    st.title("📚 Health Education Center")
    
    tabs = st.tabs(["📖 Articles", "🎥 Videos", "📊 Health Tips"])
    
    with tabs[0]:
        st.header("Health Articles")
        articles = [
            "Understanding Diabetes",
            "Heart Health Basics", 
            "Mental Health Awareness",
            "Nutrition Guidelines"
        ]
        for article in articles:
            if st.button(article):
                st.info(f"Reading: {article}")
    
    with tabs[1]:
        st.header("Educational Videos")
        st.info("Health education videos would be embedded here")
    
    with tabs[2]:
        st.header("Daily Health Tips")
        tips = [
            "Drink 8 glasses of water daily",
            "Exercise for 30 minutes", 
            "Get 7-8 hours of sleep",
            "Eat 5 servings of fruits/vegetables"
        ]
        for tip in tips:
            st.success(f"💡 {tip}")