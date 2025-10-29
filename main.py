import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="CrypticX - AI Study Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    .hero-section {
        background: linear-gradient(135deg, #0e1117 0%, #1a1d29 100%);
        padding: 4rem 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #2d3746;
    }
    .feature-card {
        background: rgba(42, 49, 62, 0.7);
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #2d3746;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    .review-card {
        background: rgba(42, 49, 62, 0.5);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #00d4ff;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Navigation
    col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])
    with col1:
        st.markdown("### 🧠 CrypticX")
    with col2:
        if st.button("Dashboard"):
            st.switch_page("pages/1_Dashboard.py")
    with col3:
        if st.button("Pricing"):
            st.switch_page("pages/2_Pricing.py")
    with col4:
        if st.button("Contact"):
            st.switch_page("pages/3_Contact.py")
    with col5:
        if st.button("Login"):
            st.switch_page("pages/4_Auth.py")

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 style='text-align: center; color: #00d4ff; font-size: 3.5rem; margin-bottom: 1rem;'>
            Welcome to CrypticX
        </h1>
        <p style='text-align: center; font-size: 1.5rem; color: #a0aec0;'>
            The ultimate tool for school. Master complex concepts, ace your exams, and unlock your full academic potential with cutting-edge AI technology.
        </p>
        <div style='text-align: center; margin-top: 2rem;'>
            <button style='
                background: linear-gradient(45deg, #00d4ff, #0099cc);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 25px;
                font-size: 1.2rem;
                cursor: pointer;
                margin: 0 10px;
            '>Get Started Free</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Why Choose CrypticX Section
    st.markdown("## 🚀 Why Choose CrypticX?")
    st.markdown("### The ultimate AI study companion for modern students")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 Smart AI Tutor</h3>
            <p>24/7 personalized learning assistant that adapts to your study style and pace.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Comprehensive Coverage</h3>
            <p>From mathematics to literature, science to history - we've got all subjects covered.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Exam Focused</h3>
            <p>Specialized tools for test preparation, practice exams, and performance analytics.</p>
        </div>
        """, unsafe_allow_html=True)

    # Reviews Section
    st.markdown("## ⭐ What Students Say")
    
    reviews = [
        {"name": "Sarah M.", "course": "Computer Science", "text": "CrypticX helped me understand complex algorithms that I struggled with for months!", "rating": "★★★★★"},
        {"name": "James L.", "course": "Medicine", "text": "The medical terminology helper is incredible. My exam scores improved by 30%!", "rating": "★★★★★"},
        {"name": "Emma K.", "course": "Engineering", "text": "Finally an AI that actually explains engineering concepts in a way I can understand.", "rating": "★★★★☆"}
    ]
    
    for review in reviews:
        st.markdown(f"""
        <div class="review-card">
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <h4>{review['name']} - {review['course']}</h4>
                <span style='color: #ffd700;'>{review['rating']}</span>
            </div>
            <p style='color: #a0aec0; margin-top: 0.5rem;'>{review['text']}</p>
        </div>
        """, unsafe_allow_html=True)

    # CTA Section
    st.markdown("""
    <div style='text-align: center; margin: 3rem 0;'>
        <h2>Ready to Transform Your Learning?</h2>
        <p style='color: #a0aec0; font-size: 1.2rem;'>Join thousands of students already achieving academic excellence</p>
        <button style='
            background: linear-gradient(45deg, #00d4ff, #0099cc);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 25px;
            font-size: 1.2rem;
            cursor: pointer;
            margin-top: 1rem;
        '>Start Your Free Trial</button>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
