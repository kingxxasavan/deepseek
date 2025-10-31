import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import base64

# Page config
st.set_page_config(
    page_title="Crptic AI - AI-Powered Learning Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_chat' not in st.session_state:
    st.session_state.current_chat = []
if 'plan' not in st.session_state:
    st.session_state.plan = 'Free'

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main {
        padding: 0;
    }
    
    /* Landing Page Styles */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 100px 50px;
        text-align: center;
        color: white;
        border-radius: 0 0 50px 50px;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        margin-bottom: 20px;
        background: linear-gradient(to right, #fff, #e0e0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeInUp 1s ease;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 40px;
        opacity: 0.95;
        animation: fadeInUp 1.2s ease;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .cta-button {
        background: white;
        color: #667eea;
        padding: 18px 50px;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: 700;
        border: none;
        cursor: pointer;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        display: inline-block;
        text-decoration: none;
    }
    
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    .features-section {
        padding: 80px 50px;
        background: white;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 40px;
        margin: 20px;
        text-align: center;
        transition: transform 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.2);
    }
    
    .feature-icon {
        font-size: 3.5rem;
        margin-bottom: 20px;
    }
    
    .feature-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 15px;
    }
    
    .feature-desc {
        font-size: 1.1rem;
        color: #666;
        line-height: 1.6;
    }
    
    /* Pricing Cards */
    .pricing-section {
        padding: 80px 50px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .pricing-card {
        background: white;
        border-radius: 24px;
        padding: 45px 35px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .pricing-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    }
    
    .pricing-card.featured {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: scale(1.05);
    }
    
    .pricing-card.featured:hover {
        transform: scale(1.08) translateY(-10px);
    }
    
    .featured-badge {
        position: absolute;
        top: 20px;
        right: -30px;
        background: #ffd700;
        color: #333;
        padding: 5px 40px;
        transform: rotate(45deg);
        font-weight: 700;
        font-size: 0.8rem;
    }
    
    .price {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 20px 0;
    }
    
    .price-period {
        font-size: 1.2rem;
        opacity: 0.8;
    }
    
    .plan-name {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .plan-desc {
        margin-bottom: 30px;
        opacity: 0.9;
    }
    
    .feature-list {
        text-align: left;
        margin: 30px 0;
    }
    
    .feature-item {
        padding: 12px 0;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    
    .pricing-card.featured .feature-item {
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Chat Interface */
    .chat-container {
        height: calc(100vh - 100px);
        display: flex;
        flex-direction: column;
        background: white;
        border-radius: 20px;
        margin: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 20px 20px 0 0;
        color: white;
    }
    
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 30px;
        background: #f8f9fa;
    }
    
    .message {
        margin: 15px 0;
        padding: 15px 20px;
        border-radius: 18px;
        max-width: 70%;
        animation: messageSlide 0.3s ease;
    }
    
    @keyframes messageSlide {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .ai-message {
        background: white;
        color: #333;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .chat-input-container {
        padding: 25px;
        background: white;
        border-radius: 0 0 20px 20px;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Sidebar Chat */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .chat-item {
        padding: 12px 15px;
        margin: 8px 0;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .chat-item:hover {
        background: rgba(255,255,255,0.2);
        transform: translateX(5px);
    }
    
    .new-chat-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        font-weight: 600;
        cursor: pointer;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .new-chat-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .user-profile {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .avatar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    /* Auth Container */
    .auth-container {
        max-width: 450px;
        margin: 80px auto;
        background: white;
        border-radius: 24px;
        padding: 50px 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .auth-header {
        text-align: center;
        margin-bottom: 40px;
    }
    
    .auth-logo {
        font-size: 4rem;
        margin-bottom: 20px;
    }
    
    .auth-title {
        color: #667eea;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px 30px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 15px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 30px;
        background: #f8f9fa;
    }
    
    .section-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 60px;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Navigation functions
def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

def login_user(username):
    st.session_state.authenticated = True
    st.session_state.username = username
    go_to_page('chat')

# Landing Page
def landing_page():
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🧠 Crptic AI</div>
        <div class="hero-subtitle">
            Your AI-Powered Learning Assistant<br>
            Upload Documents, Images, PDFs - Learn Smarter with Gemini 2.5 Flash
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Get Started Free", use_container_width=True):
            go_to_page('signup')
        if st.button("🔑 Sign In", use_container_width=True):
            go_to_page('login')
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Features Section
    st.markdown('<div class="features-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Why Choose Crptic AI?</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-title">Multi-Format Support</div>
            <div class="feature-desc">
                Upload PDFs, Word docs, images, spreadsheets, and more. 
                Our AI understands them all.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Powered by Gemini 2.5</div>
            <div class="feature-desc">
                Lightning-fast responses with Google's most advanced 
                AI model for accurate learning assistance.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure & Private</div>
            <div class="feature-desc">
                Your documents are processed securely. We never store 
                your data longer than necessary.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Pricing Section
    if st.button("💰 View Pricing", use_container_width=True, key="view_pricing"):
        go_to_page('pricing')

# Pricing Page
def pricing_page():
    st.markdown("""
    <div class="hero-section" style="padding: 60px 50px;">
        <div class="hero-title" style="font-size: 3.5rem;">Choose Your Plan</div>
        <div class="hero-subtitle">Start free, upgrade anytime. No credit card required.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="pricing-section">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <div class="plan-name">Free</div>
            <div class="price">$0<span class="price-period">/mo</span></div>
            <div class="plan-desc">Perfect for trying out</div>
            <div class="feature-list">
                <div class="feature-item">✓ 10 messages/day</div>
                <div class="feature-item">✓ Basic document upload</div>
                <div class="feature-item">✓ Image analysis</div>
                <div class="feature-item">✓ Community support</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Free", key="free_plan", use_container_width=True):
            go_to_page('signup')
    
    with col2:
        st.markdown("""
        <div class="pricing-card">
            <div class="plan-name">Starter</div>
            <div class="price">$15<span class="price-period">/mo</span></div>
            <div class="plan-desc">For regular learners</div>
            <div class="feature-list">
                <div class="feature-item">✓ 100 messages/day</div>
                <div class="feature-item">✓ All document formats</div>
                <div class="feature-item">✓ Priority processing</div>
                <div class="feature-item">✓ Email support</div>
                <div class="feature-item">✓ Chat history</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Choose Starter", key="starter_plan", use_container_width=True):
            go_to_page('signup')
    
    with col3:
        st.markdown("""
        <div class="pricing-card">
            <div class="plan-name">Pro</div>
            <div class="price">$35<span class="price-period">/mo</span></div>
            <div class="plan-desc">For power users</div>
            <div class="feature-list">
                <div class="feature-item">✓ Unlimited messages</div>
                <div class="feature-item">✓ Batch processing</div>
                <div class="feature-item">✓ API access</div>
                <div class="feature-item">✓ Priority support</div>
                <div class="feature-item">✓ Advanced analytics</div>
                <div class="feature-item">✓ Custom integrations</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Choose Pro", key="pro_plan", use_container_width=True):
            go_to_page('signup')
    
    with col4:
        st.markdown("""
        <div class="pricing-card featured">
            <div class="featured-badge">LIMITED</div>
            <div class="plan-name">Founder's Pass</div>
            <div class="price">$50<span class="price-period">/3mo</span></div>
            <div class="plan-desc">First 500 Only!</div>
            <div class="feature-list">
                <div class="feature-item">✓ EVERYTHING in Pro</div>
                <div class="feature-item">✓ Lifetime premium features</div>
                <div class="feature-item">✓ Early access to new features</div>
                <div class="feature-item">✓ Founder badge</div>
                <div class="feature-item">✓ Direct founder support</div>
                <div class="feature-item">✓ Exclusive community</div>
                <div class="feature-item">🎁 One-time payment!</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Claim Founder Pass", key="founder_plan", use_container_width=True):
            st.session_state.plan = 'Founder'
            go_to_page('signup')
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Home", use_container_width=True):
        go_to_page('landing')

# Login Page
def login_page():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 50px;">
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-container">
        <div class="auth-header">
            <div class="auth-logo">🧠</div>
            <div class="auth-title">Welcome Back</div>
            <p style="color: #666;">Sign in to continue your learning journey</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Email or Username", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔐 Sign In", use_container_width=True):
            if username and password:
                login_user(username)
            else:
                st.error("Please enter both username and password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Don't have an account?", use_container_width=True):
                go_to_page('signup')
        with col_b:
            if st.button("← Back to Home", use_container_width=True):
                go_to_page('landing')
    
    st.markdown("</div>", unsafe_allow_html=True)

# Signup Page
def signup_page():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 50px;">
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-container">
        <div class="auth-header">
            <div class="auth-logo">🧠</div>
            <div class="auth-title">Join Crptic AI</div>
            <p style="color: #666;">Create your account and start learning smarter</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        full_name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••")
        
        plan_display = st.session_state.get('plan', 'Free')
        st.info(f"📦 Selected Plan: **{plan_display}**")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✨ Create Account", use_container_width=True):
            if full_name and email and password and confirm_password:
                if password == confirm_password:
                    login_user(email)
                else:
                    st.error("Passwords don't match!")
            else:
                st.error("Please fill in all fields")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Already have an account?", use_container_width=True):
                go_to_page('login')
        with col_b:
            if st.button("← Back to Home", use_container_width=True):
                go_to_page('landing')
    
    st.markdown("</div>", unsafe_allow_html=True)

# Chat Interface
def chat_page():
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 2.5rem;">🧠</div>
            <div style="font-size: 1.5rem; font-weight: 700; margin-top: 10px;">Crptic AI</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="new-chat-btn">➕ New Chat</div>', unsafe_allow_html=True)
        if st.button("New Chat", use_container_width=True, key="new_chat_btn"):
            st.session_state.current_chat = []
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💬 Recent Chats")
        
        # Sample chat history
        chats = [
            "📚 Study Guide for Biology",
            "📊 Data Analysis Help",
            "🖼️ Image Analysis Task",
            "📄 Document Summary",
            "🧮 Math Problem Solving"
        ]
        
        for chat in chats:
            if st.button(chat, use_container_width=True, key=f"chat_{chat}"):
                st.info(f"Loading {chat}...")
        
        st.markdown("---")
        st.markdown("### 🛠️ Tools")
        if st.button("📁 Document Manager", use_container_width=True):
            st.info("Document manager coming soon!")
        if st.button("⚙️ Settings", use_container_width=True):
            st.info("Settings coming soon!")
        if st.button("💰 Upgrade Plan", use_container_width=True):
            go_to_page('pricing')
        
        # User profile at bottom
        st.markdown(f"""
        <div class="user-profile">
            <div class="avatar">{st.session_state.username[0].upper()}</div>
            <div>
                <div style="font-weight: 600;">{st.session_state.username}</div>
                <div style="font-size: 0.85rem; opacity: 0.7;">{st.session_state.plan} Plan</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            st.session_state.authenticated = False
            go_to_page('landing')
    
    # Main Chat Area
    st.markdown("""
    <div class="chat-header">
        <h2 style="margin: 0;">💬 Chat with Crptic AI</h2>
        <p style="margin: 5px 0 0 0; opacity: 0.9;">Powered by Gemini 2.5 Flash</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "📎 Upload Documents (PDF, DOCX, Images, etc.)",
            accept_multiple_files=True,
            type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'xlsx', 'csv']
        )
        
        if uploaded_files:
            st.success(f"✓ {len(uploaded_files)} file(s) uploaded successfully!")
            for file in uploaded_files:
                st.write(f"• {file.name}")
    
    with col2:
        st.info("**Supported Formats:**\n- PDF Documents\n- Word Files\n- Images\n- Spreadsheets\n- Text Files")
    
    # Chat messages
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    if len(st.session_state.current_chat) == 0:
        st.markdown("""
        <div style="text-align: center; padding: 100px 20px; color: #999;">
            <div style="font-size: 4rem; margin-bottom: 20px;">🧠</div>
            <h3>How can I help you learn today?</h3>
            <p>Upload documents, ask questions, or start a conversation!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.current_chat:
            if msg['role'] == 'user':
                st.markdown(f'<div class="message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message ai-message">🧠 {msg["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    st.markdown('<div class="chat-input-container">', unsafe_allow_html
