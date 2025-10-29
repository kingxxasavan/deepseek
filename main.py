import streamlit as st
from streamlit_option_menu import streamlit_option_menu
import json
import os

# Page configuration
st.set_page_config(
    page_title="Cryptix - Modern Learning Tool",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS based on the design
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #1a1642 0%, #2d1b69 50%, #4a1a5c 100%);
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header styling */
    .custom-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 3rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Logo */
    .logo {
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Navigation links */
    .nav-links {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-link {
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        font-size: 1rem;
        transition: color 0.3s;
    }
    
    .nav-link:hover {
        color: white;
    }
    
    /* Buttons */
    .btn-login {
        padding: 0.5rem 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 25px;
        color: white;
        background: transparent;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .btn-signup {
        padding: 0.5rem 1.5rem;
        border: none;
        border-radius: 25px;
        color: white;
        background: linear-gradient(135deg, #4169E1, #6495ED);
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .btn-login:hover, .btn-signup:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(65, 105, 225, 0.4);
    }
    
    /* Hero section */
    .hero-section {
        padding: 4rem 3rem;
        text-align: left;
    }
    
    .hero-title {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.7);
        letter-spacing: 3px;
        margin-bottom: 1rem;
    }
    
    .hero-main {
        font-size: 4rem;
        font-weight: bold;
        color: white;
        line-height: 1.2;
        margin-bottom: 1.5rem;
        text-transform: uppercase;
    }
    
    .hero-description {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.7);
        max-width: 600px;
        line-height: 1.8;
        margin-bottom: 2rem;
    }
    
    .btn-get-started {
        padding: 1rem 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 30px;
        color: white;
        background: transparent;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .btn-get-started:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-2px);
    }
    
    /* Features section */
    .features-section {
        padding: 4rem 3rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        margin: 3rem 0;
    }
    
    .section-title {
        font-size: 2.5rem;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px rgba(65, 105, 225, 0.3);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        color: white;
        margin-bottom: 1rem;
    }
    
    .feature-text {
        color: rgba(255, 255, 255, 0.7);
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# User data file
USER_DATA_FILE = 'users.json'

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

def authenticate(username, password):
    users = load_users()
    if username in users and users[username] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
        return True
    return False

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = password
    save_users(users)
    return True

# Custom header
def render_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown('<div class="logo">🔷 CRYPTIX</div>', unsafe_allow_html=True)
    
    with col2:
        selected = st.radio(
            "",
            ["Home", "Dashboard", "Pricing", "Contact", "About"],
            horizontal=True,
            key="nav_menu",
            label_visibility="collapsed"
        )
        st.session_state.page = selected
    
    with col3:
        if st.session_state.authenticated:
            col_user, col_logout = st.columns(2)
            with col_user:
                st.markdown(f'<p style="color: white;">👤 {st.session_state.username}</p>', unsafe_allow_html=True)
            with col_logout:
                if st.button("Logout", key="logout_btn"):
                    st.session_state.authenticated = False
                    st.session_state.username = None
                    st.session_state.page = 'Home'
                    st.rerun()
        else:
            col_login, col_signup = st.columns(2)
            with col_login:
                if st.button("Log In", key="login_btn"):
                    st.session_state.page = 'Login'
                    st.rerun()
            with col_signup:
                if st.button("Sign Up", key="signup_btn"):
                    st.session_state.page = 'Signup'
                    st.rerun()

# Render header
render_header()

# Page routing
if st.session_state.page == 'Home':
    # Hero Section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<p class="hero-title">INTRODUCING</p>', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-main">WELCOME TO<br>CRYPTIX</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-description">The new modern learning tool revolutionizing education. Cryptix combines AI-powered conversations with interactive learning experiences to help you master any subject efficiently.</p>', unsafe_allow_html=True)
        if st.button("Get Started", key="hero_cta"):
            st.session_state.page = 'Signup'
            st.rerun()
    
    with col2:
        st.markdown('<div style="text-align: center; padding: 2rem;">🤖</div>', unsafe_allow_html=True)
    
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

elif st.session_state.page == 'Dashboard':
    if not st.session_state.authenticated:
        st.warning("⚠️ Please log in to access the Dashboard")
        if st.button("Go to Login"):
            st.session_state.page = 'Login'
            st.rerun()
    else:
        st.markdown(f'<h1 style="color: white;">Welcome back, {st.session_state.username}! 👋</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: rgba(255,255,255,0.7); font-size: 1.2rem;">Your personalized learning dashboard</p>', unsafe_allow_html=True)
        
        # Dashboard content
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3 style="color: white;">📚 Courses</h3>
                <h2 style="color: #4169E1; font-size: 3rem;">12</h2>
                <p style="color: rgba(255,255,255,0.7);">Active courses</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3 style="color: white;">⏱️ Study Time</h3>
                <h2 style="color: #4169E1; font-size: 3rem;">48h</h2>
                <p style="color: rgba(255,255,255,0.7);">This month</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h3 style="color: white;">🎯 Progress</h3>
                <h2 style="color: #4169E1; font-size: 3rem;">78%</h2>
                <p style="color: rgba(255,255,255,0.7);">Overall completion</p>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.page == 'Login':
    st.markdown('<h1 style="color: white; text-align: center;">Log In to Cryptix</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Log In", use_container_width=True)
            
            if submit:
                if authenticate(username, password):
                    st.success("✅ Login successful!")
                    st.session_state.page = 'Dashboard'
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        if st.button("Don't have an account? Sign Up"):
            st.session_state.page = 'Signup'
            st.rerun()

elif st.session_state.page == 'Signup':
    st.markdown('<h1 style="color: white; text-align: center;">Create Your Account</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("signup_form"):
            username = st.text_input("Username", placeholder="Choose a username")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            submit = st.form_submit_button("Sign Up", use_container_width=True)
            
            if submit:
                if password != confirm_password:
                    st.error("❌ Passwords don't match")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                elif register_user(username, password):
                    st.success("✅ Account created successfully!")
                    authenticate(username, password)
                    st.session_state.page = 'Dashboard'
                    st.rerun()
                else:
                    st.error("❌ Username already exists")
        
        if st.button("Already have an account? Log In"):
            st.session_state.page = 'Login'
            st.rerun()

elif st.session_state.page == 'Pricing':
    st.markdown('<h1 style="color: white; text-align: center;">Choose Your Plan</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: rgba(255,255,255,0.7); text-align: center; font-size: 1.2rem; margin-bottom: 3rem;">Select the perfect plan for your learning journey</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: white; text-align: center;">Free</h3>
            <h2 style="color: #4169E1; font-size: 3rem; text-align: center;">$0</h2>
            <p style="color: rgba(255,255,255,0.7); text-align: center; margin-bottom: 2rem;">per month</p>
            <ul style="color: rgba(255,255,255,0.7); list-style: none; padding: 0;">
                <li>✓ 5 courses access</li>
                <li>✓ Basic AI chat</li>
                <li>✓ Progress tracking</li>
                <li>✗ Advanced analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="border: 2px solid #4169E1;">
            <h3 style="color: white; text-align: center;">Pro</h3>
            <h2 style="color: #4169E1; font-size: 3rem; text-align: center;">$19</h2>
            <p style="color: rgba(255,255,255,0.7); text-align: center; margin-bottom: 2rem;">per month</p>
            <ul style="color: rgba(255,255,255,0.7); list-style: none; padding: 0;">
                <li>✓ Unlimited courses</li>
                <li>✓ Advanced AI chat</li>
                <li>✓ Full analytics</li>
                <li>✓ Priority support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: white; text-align: center;">Enterprise</h3>
            <h2 style="color: #4169E1; font-size: 3rem; text-align: center;">Custom</h2>
            <p style="color: rgba(255,255,255,0.7); text-align: center; margin-bottom: 2rem;">contact us</p>
            <ul style="color: rgba(255,255,255,0.7); list-style: none; padding: 0;">
                <li>✓ Everything in Pro</li>
                <li>✓ Custom integration</li>
                <li>✓ Dedicated support</li>
                <li>✓ Team management</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == 'Contact':
    st.markdown('<h1 style="color: white; text-align: center;">Get In Touch</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: rgba(255,255,255,0.7); text-align: center; font-size: 1.2rem; margin-bottom: 3rem;">We\'d love to hear from you</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("contact_form"):
            name = st.text_input("Name", placeholder="Your name")
            email = st.text_input("Email", placeholder="your.email@example.com")
            message = st.text_area("Message", placeholder="Your message here...", height=150)
            submit = st.form_submit_button("Send Message", use_container_width=True)
            
            if submit:
                if name and email and message:
                    st.success("✅ Message sent successfully! We'll get back to you soon.")
                else:
                    st.error("❌ Please fill in all fields")

elif st.session_state.page == 'About':
    st.markdown('<h1 style="color: white; text-align: center;">About Cryptix</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: rgba(255,255,255,0.7); text-align: center; font-size: 1.2rem; margin-bottom: 3rem;">Revolutionizing education with AI-powered learning</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2 style="color: white;">Our Mission</h2>
            <p style="color: rgba(255,255,255,0.7); line-height: 1.8;">
                At Cryptix, we believe that learning should be accessible, engaging, and personalized. 
                Our AI-powered platform adapts to your unique learning style, helping you master 
                any subject at your own pace.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2 style="color: white;">Our Vision</h2>
            <p style="color: rgba(255,255,255,0.7); line-height: 1.8;">
                We envision a world where everyone has access to world-class education, 
                powered by cutting-edge AI technology that makes learning more effective 
                and enjoyable than ever before.
            </p>
        </div>
        """, unsafe_allow_html=True)
