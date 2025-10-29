import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Dashboard - CrypticX",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for dashboard
st.markdown("""
<style>
    .metric-card {
        background: rgba(42, 49, 62, 0.7);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #2d3746;
        margin: 0.5rem 0;
    }
    .study-session {
        background: rgba(42, 49, 62, 0.5);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

def dashboard_page():
    st.title("📊 Study Dashboard")
    
    # Navigation
    col1, col2, col3, col4 = st.columns([2,1,1,1])
    with col1:
        st.markdown("### 🧠 CrypticX Dashboard")
    with col2:
        if st.button("🏠 Home"):
            st.switch_page("main.py")
    with col3:
        if st.button("💰 Pricing"):
            st.switch_page("pages/2_Pricing.py")
    with col4:
        if st.button("📞 Contact"):
            st.switch_page("pages/3_Contact.py")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style='color: #00d4ff; margin: 0;'>Study Hours</h3>
            <h1 style='color: white; margin: 0;'>24.5</h1>
            <p style='color: #a0aec0; margin: 0;'>This Week</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style='color: #00d4ff; margin: 0;'>Subjects</h3>
            <h1 style='color: white; margin: 0;'>8</h1>
            <p style='color: #a0aec0; margin: 0;'>Active</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style='color: #00d4ff; margin: 0;'>Progress</h3>
            <h1 style='color: white; margin: 0;'>78%</h1>
            <p style='color: #a0aec0; margin: 0;'>Overall</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style='color: #00d4ff; margin: 0;'>Quizzes</h3>
            <h1 style='color: white; margin: 0;'>42</h1>
            <p style='color: #a0aec0; margin: 0;'>Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts and Data
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Study Time Distribution")
        subjects = ['Math', 'Science', 'History', 'Literature', 'Programming']
        hours = [12, 8, 6, 4, 10]
        fig = px.pie(values=hours, names=subjects, 
                    color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Weekly Progress")
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        progress = [65, 70, 68, 75, 82, 85, 78]
        fig = go.Figure(data=go.Scatter(x=days, y=progress, 
                                      mode='lines+markers',
                                      line=dict(color='#00d4ff', width=3),
                                      marker=dict(size=8)))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                         paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Study Sessions
    st.subheader("Recent Study Sessions")
    sessions = [
        {"subject": "Advanced Calculus", "duration": "2h 15m", "date": "2024-01-15", "score": "92%"},
        {"subject": "Organic Chemistry", "duration": "1h 45m", "date": "2024-01-14", "score": "85%"},
        {"subject": "World History", "duration": "1h 30m", "date": "2024-01-14", "score": "88%"},
        {"subject": "Python Programming", "duration": "3h 00m", "date": "2024-01-13", "score": "95%"}
    ]
    
    for session in sessions:
        st.markdown(f"""
        <div class="study-session">
            <div style='display: flex; justify-content: space-between;'>
                <h4>{session['subject']}</h4>
                <span style='color: #00d4ff;'>{session['score']}</span>
            </div>
            <div style='display: flex; justify-content: space-between; color: #a0aec0;'>
                <span>⏱️ {session['duration']}</span>
                <span>📅 {session['date']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    dashboard_page()
