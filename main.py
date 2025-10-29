import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json

# Page config

st.set_page_config(
page_title=“Cryptic AI Study Tool”,
page_icon=“🔮”,
layout=“wide”,
initial_sidebar_state=“collapsed”
)

# Custom CSS for purple glass design

st.markdown(”””

<style>
    /* Global Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    .main {
        padding: 0 !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1a0033 0%, #2d1b4e 50%, #1a0033 100%);
        background-attachment: fixed;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Glass morphism styles */
    .glass {
        background: rgba(139, 92, 246, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(139, 92, 246, 0.15);
    }
    
    .green-glass {
        background: rgba(74, 222, 128, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(74, 222, 128, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(74, 222, 128, 0.15);
    }
    
    /* Navigation Bar */
    .nav-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: rgba(26, 0, 51, 0.9);
        backdrop-filter: blur(20px);
        padding: 1rem 3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(139, 92, 246, 0.3);
        transition: transform 0.3s ease;
    }
    
    .nav-hidden {
        transform: translateY(-100%);
    }
    
    .nav-logo {
        font-size: 1.8rem;
        font-weight: bold;
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-link {
        color: #c4b5fd;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
        cursor: pointer;
    }
    
    .nav-link:hover {
        color: #a78bfa;
    }
    
    /* Hero Section */
    .hero {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 8rem 2rem 4rem;
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #c4b5fd;
        margin-bottom: 2rem;
    }
    
    /* Button Styles */
    .cta-button {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        color: white;
        padding: 1rem 3rem;
        border: none;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: bold;
        cursor: pointer;
        transition: transform 0.3s, box-shadow 0.3s;
        display: inline-block;
        text-decoration: none;
        margin: 1rem;
    }
    
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.4);
    }
    
    /* Section Styles */
    .section {
        min-height: 100vh;
        padding: 6rem 3rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .section-title {
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 3rem;
    }
    
    /* Feature Cards */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: rgba(139, 92, 246, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: transform 0.3s;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        color: #a78bfa;
        margin-bottom: 1rem;
    }
    
    .feature-desc {
        color: #c4b5fd;
        line-height: 1.6;
    }
    
    /* Pricing Cards */
    .pricing-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem auto;
        max-width: 1200px;
    }
    
    .pricing-card {
        background: rgba(139, 92, 246, 0.1);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        transition: transform 0.3s, border-color 0.3s;
    }
    
    .pricing-card:hover {
        transform: scale(1.05);
        border-color: rgba(139, 92, 246, 0.6);
    }
    
    .pricing-card.featured {
        border-color: #a78bfa;
        border-width: 3px;
    }
    
    .pricing-plan {
        font-size: 1.8rem;
        color: #a78bfa;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    .pricing-price {
        font-size: 3rem;
        color: white;
        margin: 1rem 0;
    }
    
    .pricing-features {
        text-align: left;
        margin: 2rem 0;
        color: #c4b5fd;
        line-height: 2;
    }
    
    /* Auth Container */
    .auth-container {
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .auth-box {
        background: rgba(139, 92, 246, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 20px;
        padding: 3rem;
        width: 100%;
        max-width: 450px;
        box-shadow: 0 8px 32px 0 rgba(139, 92, 246, 0.15);
    }
    
    .auth-title {
        font-size: 2.5rem;
        text-align: center;
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    /* Input Styles */
    .stTextInput input, .stTextArea textarea {
        background: rgba(139, 92, 246, 0.1) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 0.8rem !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.2) !important;
    }
    
    /* Dashboard Styles */
    .dashboard {
        display: grid;
        grid-template-columns: 300px 1fr 400px;
        height: 100vh;
        gap: 0;
    }
    
    .sidebar {
        background: rgba(26, 0, 51, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(139, 92, 246, 0.2);
        padding: 2rem 1rem;
        overflow-y: auto;
        transition: transform 0.3s ease;
    }
    
    .sidebar-hidden {
        transform: translateX(-100%);
    }
    
    .main-content {
        padding: 2rem;
        overflow-y: auto;
        background: rgba(26, 0, 51, 0.3);
    }
    
    .right-panel {
        background: rgba(26, 51, 26, 0.95);
        backdrop-filter: blur(20px);
        border-left: 1px solid rgba(74, 222, 128, 0.2);
        padding: 2rem 1rem;
        overflow-y: auto;
        transition: transform 0.3s ease;
    }
    
    .right-panel-hidden {
        transform: translateX(100%);
    }
    
    .tool-button {
        width: 100%;
        padding: 1rem;
        margin: 0.5rem 0;
        background: rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 10px;
        color: #c4b5fd;
        cursor: pointer;
        transition: all 0.3s;
        text-align: left;
        font-size: 1rem;
    }
    
    .tool-button:hover {
        background: rgba(139, 92, 246, 0.3);
        border-color: #a78bfa;
        transform: translateX(5px);
    }
    
    .generated-item {
        background: rgba(74, 222, 128, 0.1);
        border: 1px solid rgba(74, 222, 128, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #86efac;
    }
    
    /* Scrollbar Styles */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(139, 92, 246, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(139, 92, 246, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(139, 92, 246, 0.7);
    }
    
    /* Contact Form */
    .contact-section {
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Labels */
    label {
        color: #c4b5fd !important;
        font-weight: 500 !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 2rem;
        font-weight: bold;
        width: 100%;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(139, 92, 246, 0.4);
    }
</style>

“””, unsafe_allow_html=True)

# Initialize session state

if ‘page’ not in st.session_state:
st.session_state.page = ‘landing’
if ‘logged_in’ not in st.session_state:
st.session_state.logged_in = False
if ‘flashcards’ not in st.session_state:
st.session_state.flashcards = []
if ‘quizzes’ not in st.session_state:
st.session_state.quizzes = []
if ‘documents’ not in st.session_state:
st.session_state.documents = []
if ‘show_sidebar’ not in st.session_state:
st.session_state.show_sidebar = True
if ‘show_right_panel’ not in st.session_state:
st.session_state.show_right_panel = True

# Navigation function

def navigate_to(page):
st.session_state.page = page
st.rerun()

# Landing Page

def landing_page():
# Navigation Bar
st.markdown(”””
<div class="nav-bar" id="navbar">
<div class="nav-logo">🔮 Cryptic AI</div>
<div class="nav-links">
<a class="nav-link" onclick="scrollToSection('why')">Why Choose Us</a>
<a class="nav-link" onclick="scrollToSection('features')">Features</a>
<a class="nav-link" onclick="scrollToSection('pricing')">Pricing</a>
<a class="nav-link" onclick="scrollToSection('contact')">Contact</a>
</div>
</div>

```
<script>
    let lastScroll = 0;
    const navbar = document.getElementById('navbar');
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > lastScroll && currentScroll > 100) {
            navbar.classList.add('nav-hidden');
        } else {
            navbar.classList.remove('nav-hidden');
        }
        
        lastScroll = currentScroll;
    });
    
    function scrollToSection(id) {
        document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
    }
</script>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <div class="hero-title">Welcome to Cryptic AI</div>
    <div class="hero-subtitle">Transform Your Learning with AI-Powered Study Tools</div>
    <p style="color: #c4b5fd; font-size: 1.2rem; max-width: 800px; margin-bottom: 2rem;">
        Harness the power of artificial intelligence to create flashcards, quizzes, 
        and analyze documents instantly. Study smarter, not harder.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Get Started For Free", key="hero_cta", use_container_width=True):
        navigate_to('signup')

# Why Choose Us Section
st.markdown('<div id="why" class="section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Why Choose Cryptic AI?</h2>', unsafe_allow_html=True)

cols = st.columns(3)
reasons = [
    ("⚡", "Lightning Fast", "Generate study materials in seconds with our advanced AI technology"),
    ("🎯", "Personalized Learning", "Adaptive content tailored to your learning style and pace"),
    ("🔒", "Secure & Private", "Your data is encrypted and never shared with third parties")
]

for col, (icon, title, desc) in zip(cols, reasons):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Features Section
st.markdown('<div id="features" class="section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Powerful Features</h2>', unsafe_allow_html=True)

cols = st.columns(2)
features = [
    ("🗃️", "AI Flashcards", "Automatically generate flashcards from any text or document"),
    ("📝", "Smart Quizzes", "Create custom quizzes with multiple question types"),
    ("📄", "Document Analysis", "Deep analysis and summarization of your study materials"),
    ("🤖", "Gemini AI Integration", "Powered by Google's cutting-edge Gemini 1.5 Flash model")
]

for i, (icon, title, desc) in enumerate(features):
    with cols[i % 2]:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# CTA Section
st.markdown('<div class="section" style="min-height: 50vh;">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Start Learning Now", key="features_cta", use_container_width=True):
        navigate_to('signup')
st.markdown('</div>', unsafe_allow_html=True)

# Pricing Section
st.markdown('<div id="pricing" class="section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Choose Your Plan</h2>', unsafe_allow_html=True)

pricing_cols = st.columns(3)
plans = [
    ("Free", "$0", ["10 flashcards/month", "5 quizzes/month", "Basic document analysis", "Community support"], False),
    ("Pro", "$9.99", ["Unlimited flashcards", "Unlimited quizzes", "Advanced AI analysis", "Priority support", "Export features"], True),
    ("Team", "$29.99", ["Everything in Pro", "Team collaboration", "Admin dashboard", "API access", "24/7 support"], False)
]

for col, (plan, price, features_list, featured) in zip(pricing_cols, plans):
    with col:
        featured_class = "featured" if featured else ""
        features_html = "".join([f"<div>✓ {feature}</div>" for feature in features_list])
        st.markdown(f"""
        <div class="pricing-card {featured_class}">
            <div class="pricing-plan">{plan}</div>
            <div class="pricing-price">{price}<span style="font-size: 1rem;">/month</span></div>
            <div class="pricing-features">{features_html}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Choose {plan}", key=f"pricing_{plan}", use_container_width=True):
            navigate_to('signup')
st.markdown('</div>', unsafe_allow_html=True)

# Contact Section
st.markdown('<div id="contact" class="section">', unsafe_allow_html=True)
st.markdown('<div class="contact-section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">Get In Touch</h2>', unsafe_allow_html=True)

with st.form("contact_form"):
    st.text_input("Name", placeholder="Your name")
    st.text_input("Email", placeholder="your@email.com")
    st.text_area("Message", placeholder="How can we help you?", height=150)
    submitted = st.form_submit_button("Send Message")
    if submitted:
        st.success("✅ Message sent! We'll get back to you soon.")

st.markdown('</div></div>', unsafe_allow_html=True)
```

# Login Page

def login_page():
st.markdown(’<div class="auth-container">’, unsafe_allow_html=True)
st.markdown(’<div class="auth-box">’, unsafe_allow_html=True)
st.markdown(’<div class="auth-title">Welcome Back</div>’, unsafe_allow_html=True)

```
with st.form("login_form"):
    email = st.text_input("Email", placeholder="your@email.com")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    col1, col2 = st.columns(2)
    with col1:
        login_button = st.form_submit_button("Login", use_container_width=True)
    with col2:
        if st.form_submit_button("Back", use_container_width=True):
            navigate_to('landing')
    
    if login_button:
        if email and password:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            navigate_to('dashboard')
        else:
            st.error("Please fill in all fields")

col1, col2 = st.columns(2)
with col1:
    if st.button("Forgot Password?", use_container_width=True):
        navigate_to('forgot')
with col2:
    if st.button("Sign Up", use_container_width=True):
        navigate_to('signup')

st.markdown('</div></div>', unsafe_allow_html=True)
```

# Signup Page

def signup_page():
st.markdown(’<div class="auth-container">’, unsafe_allow_html=True)
st.markdown(’<div class="auth-box">’, unsafe_allow_html=True)
st.markdown(’<div class="auth-title">Create Account</div>’, unsafe_allow_html=True)

```
with st.form("signup_form"):
    name = st.text_input("Full Name", placeholder="John Doe")
    email = st.text_input("Email", placeholder="your@email.com")
    password = st.text_input("Password", type="password", placeholder="Create a password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
    
    col1, col2 = st.columns(2)
    with col1:
        signup_button = st.form_submit_button("Sign Up", use_container_width=True)
    with col2:
        if st.form_submit_button("Back", use_container_width=True):
            navigate_to('landing')
    
    if signup_button:
        if name and email and password and confirm_password:
            if password == confirm_password:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_name = name
                navigate_to('dashboard')
            else:
                st.error("Passwords don't match")
        else:
            st.error("Please fill in all fields")

if st.button("Already have an account? Login", use_container_width=True):
    navigate_to('login')

st.markdown('</div></div>', unsafe_allow_html=True)
```

# Forgot Password Page

def forgot_page():
st.markdown(’<div class="auth-container">’, unsafe_allow_html=True)
st.markdown(’<div class="auth-box">’, unsafe_allow_html=True)
st.markdown(’<div class="auth-title">Reset Password</div>’, unsafe_allow_html=True)

```
st.markdown('<p style="text-align: center; color: #c4b5fd; margin-bottom: 2rem;">Enter your email to receive a password reset link</p>', unsafe_allow_html=True)

with st.form("forgot_form"):
    email = st.text_input("Email", placeholder="your@email.com")
    
    col1, col2 = st.columns(2)
    with col1:
        reset_button = st.form_submit_button("Send Reset Link", use_container_width=True)
    with col2:
        if st.form_submit_button("Back", use_container_width=True):
            navigate_to('login')
    
    if reset_button:
        if email:
            st.success("✅ Reset link sent! Check your email.")
        else:
            st.error("Please enter your email")

st.markdown('</div></div>', unsafe_allow_html=True)
```

# Dashboard

def dashboard_page():
sidebar_class = “” if st.session_state.show_sidebar else “sidebar-hidden”
right_panel_class = “” if st.session_state.show_right_panel else “right-panel-hidden”

```
# Create three columns for dashboard layout
col1, col2, col3 = st.columns([1, 3, 1.5])

# Left Sidebar
with col1:
    st.markdown(f'<div class="sidebar {sidebar_class}">', unsafe_allow_html=True)
    st.markdown('<h2 style="color: #a78bfa; margin-bottom: 2rem;">🔮 Cryptic AI</h2>', unsafe_allow_html=True)
    
    if st.button("🗃️ Generate Flashcards", key="flashcard_btn", use_container_width=True):
        st.session_state.current_tool = "flashcards"
    
    if st.button("📝 Create Quiz", key="quiz_btn", use_container_width=True):
        st.session_state.current_tool = "quiz"
    
    if st.button("📄 Analyze Document", key="doc_btn", use_container_width=True):
        st.session_state.current_tool = "document"
    
    if st.button("🤖 Chat with Gemini", key="chat_btn", use_container_width=True):
        st.session_state.current_tool = "chat"
        st.session_state.show_right_panel = False
    
    st.markdown("<hr style='border-color: rgba(139, 92, 246, 0.3); margin: 2rem 0;'>", unsafe_allow_html=True)
    
    if st.button("⚙️ Settings", key="settings_btn", use_container_width=True):
        pass
    
    if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        navigate_to('landing')
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main Content
with col2:
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    tool = st.session_state.get('current_tool', 'flashcards')
    
    if tool == "flashcards":
        st.markdown('<h1 style="color: #a78bfa;">🗃️ AI Flashcard Generator</h1>', unsafe_allow_html=True)
        st.markdown('<div class="glass" style="margin-top: 2rem;">', unsafe_allow_html=True)
        
        topic = st.text_input("Enter a topic:", placeholder="e.g., Python Programming, World War II, Calculus")
        num_cards = st.slider("Number of flashcards:", 5, 20, 10)
        
        if st.button("Generate Flashcards", use_container_width=True):
            with st.spinner("🔮 Creating flashcards..."):
                # Simulated flashcard generation
                new_cards = [
                    {"front": f"Question {i+1} about {topic}", "back": f"Answer {i+1} with detailed explanation"}
                    for i in range(num_cards)
                ]
                st.session_state.flashcards.extend(new_cards)
                st.session_state.show_right_panel = True
                st.success(f"✅ Generated {num_cards} flashcards!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif tool == "quiz":
        st.markdown('<h1 style="color: #a78bfa;">📝 Smart Quiz Creator</h1>', unsafe_allow_html=True)
```
