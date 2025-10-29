
import streamlit as st
import json
import os

# Page configuration
st.set_page_config(
    page_title="Cryptix - Modern Learning Tool",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import utilities
from utils.auth import load_users, save_users, authenticate, register_user
from utils.styles import apply_custom_styles

# Apply custom styles
apply_custom_styles()

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Custom header
def render_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown('<div class="logo">🔷 CRYPTIX</div>', unsafe_allow_html=True)
    
    with col2:
        menu_col1, menu_col2, menu_col3, menu_col4, menu_col5 = st.columns(5)
        
        with menu_col1:
            if st.button("Home", key="nav_home", use_container_width=True):
                st.switch_page("app.py")
        with menu_col2:
            if st.button("Dashboard", key="nav_dashboard", use_container_width=True):
                st.switch_page("pages/dashboard.py")
        with menu_col3:
            if st.button("Pricing", key="nav_pricing", use_container_width=True):
                st.switch_page("pages/pricing.py")
        with menu_col4:
            if st.button("Contact", key="nav_contact", use_container_width=True):
                st.switch_page("pages/contact.py")
        with menu_col5:
            if st.button("About", key="nav_about", use_container_width=True):
                st.switch_page("pages/about.py")
    
    with col3:
        if st.session_state.authenticated:
            col_user, col_logout = st.columns(2)
            with col_user:
                st.markdown(f'<p style="color: white; margin: 0;">👤 {st.session_state.username}</p>', unsafe_allow_html=True)
            with col_logout:
                if st.button("Logout", key="logout_btn"):
                    st.session_state.authenticated = False
                    st.session_state.username = None
                    st.rerun()
        else:
            col_login, col_signup = st.columns(2)
            with col_login:
                if st.button("Log In", key="login_btn"):
                    st.switch_page("pages/login.py")
            with col_signup:
                if st.button("Sign Up", key="signup_btn"):
                    st.switch_page("pages/signup.py")

# Render header
render_header()

# Home Page Content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<p class="hero-title">INTRODUCING</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-main">WELCOME TO<br>CRYPTIX</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-description">The new modern learning tool revolutionizing education. Cryptix combines AI-powered conversations with interactive learning experiences to help you master any subject efficiently.</p>', unsafe_allow_html=True)
    if st.button("Get Started", key="hero_cta", type="primary"):
        st.switch_page("pages/signup.py")

with col2:
    st.markdown('''
    <div style="text-align: center; padding: 2rem;">
        <div style="font-size: 200px; filter: drop-shadow(0 0 30px rgba(65, 105, 225, 0.5));">
            🤖
        </div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Features Section
st.markdown('<h2 class="section-title">Why Choose Cryptix?</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <h3 class="feature-title">Personalized Learning</h3>
        <p class="feature-text">AI-powered adaptive learning paths tailored to your unique needs and learning style.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <h3 class="feature-title">Interactive Conversations</h3>
        <p class="feature-text">Engage in meaningful dialogues with our AI to deepen your understanding of complex topics.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3 class="feature-title">Progress Tracking</h3>
        <p class="feature-text">Monitor your learning journey with detailed analytics and insights into your progress.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🚀</div>
        <h3 class="feature-title">Fast & Efficient</h3>
        <p class="feature-text">Learn at your own pace with our optimized learning algorithms that save you time.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔒</div>
        <h3 class="feature-title">Secure & Private</h3>
        <p class="feature-text">Your data is encrypted and protected with industry-leading security standards.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🌐</div>
        <h3 class="feature-title">Access Anywhere</h3>
        <p class="feature-text">Learn from any device, anywhere in the world with our cloud-based platform.</p>
    </div>
    """, unsafe_allow_html=True)
