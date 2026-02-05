import streamlit as st
from utils.auth import login_required

@login_required
def mental_wellness():
    st.title("🧠 Mental Wellness Center")
    
    tabs = st.tabs(["🧘 Wellness Tools", "📊 Mood Tracking", "📞 Support"])
    
    with tabs[0]:
        st.header("Wellness Tools")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Breathing Exercise")
            if st.button("Start 5-min Breathing"):
                st.info("Breathing exercise would start here")
        with col2:
            st.subheader("Meditation")
            if st.button("Guided Meditation"):
                st.info("Meditation session would start here")
    
    with tabs[1]:
        st.header("Mood Tracking")
        mood = st.slider("Rate your mood today (1-10)", 1, 10, 7)
        notes = st.text_area("How are you feeling?")
        if st.button("Save Mood Entry"):
            st.success("Mood entry saved!")
    
    with tabs[2]:
        st.header("Mental Health Support")
        st.info("Crisis Helpline: 1-800-CRISIS")
        st.info("Schedule appointment with counselor")