import streamlit as st
import hashlib
import json
from pathlib import Path

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Custom CSS for futuristic AI design
def load_css():
    st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Auth container */
    .auth-container {
        max-width: 450px;
        margin: 50px auto;
        padding: 40px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Title styling */
    .auth-title {
        font-size: 42px;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .auth-subtitle {
        font-size: 16px;
        color: rgba(255, 255, 255, 0.6);
        text-align: center;
        margin-bottom: 40px;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 15px !important;
        font-size: 16px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4a9eff !important;
        box-shadow: 0 0 20px rgba(74, 158, 255, 0.3) !important;
    }
    
    .stTextInput label {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4a9eff 0%, #3d7fd8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 30px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        margin-top: 20px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(74, 158, 255, 0.4) !important;
    }
    
    /* Link styling */
    .auth-link {
        text-align: center;
        margin-top: 25px;
        color: rgba(255, 255, 255, 0.6);
        font-size: 14px;
    }
    
    .auth-link a {
        color: #4a9eff;
        text-decoration: none;
        font-weight: 600;
        cursor: pointer;
    }
    
    .auth-link a:hover {
        color: #6bb3ff;
        text-decoration: underline;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError {
        border-radius: 12px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        margin: 30px 0;
    }
    
    /* Logo styling */
    .logo-container {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .logo-icon {
        font-size: 60px;
        color: #4a9eff;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Simple user database (in production, use proper database)
def load_users():
    users_file = Path("users.json")
    if users_file.exists():
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open("users.json", 'w') as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_page():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Logo
    st.markdown("""
        <div class="logo-container">
            <div class="logo-icon">🤖</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<div class="auth-title">Sign Up</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subtitle">Create your AI account</div>', unsafe_allow_html=True)
    
    # Form
    with st.form("signup_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        submit = st.form_submit_button("Create Account")
        
        if submit:
            if not username or not email or not password:
                st.error("❌ All fields are required")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters")
            else:
                users = load_users()
                if username in users:
                    st.error("❌ Username already exists")
                else:
                    users[username] = {
                        'email': email,
                        'password': hash_password(password)
                    }
                    save_users(users)
                    st.success("✅ Account created successfully! Please login.")
                    st.session_state.page = 'login'
                    st.rerun()
    
    # Link to login
    st.markdown("""
        <div class="auth-link">
            Already have an account? <a href="#" id="login_link">Log In</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle link click
    if st.button("Switch to Login", key="switch_login"):
        st.session_state.page = 'login'
        st.rerun()

def login_page():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Logo
    st.markdown("""
        <div class="logo-container">
            <div class="logo-icon">🤖</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<div class="auth-title">Welcome Back</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subtitle">Login to your AI account</div>', unsafe_allow_html=True)
    
    # Form
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        submit = st.form_submit_button("Log In")
        
        if submit:
            if not username or not password:
                st.error("❌ All fields are required")
            else:
                users = load_users()
                if username in users and users[username]['password'] == hash_password(password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
    
    # Link to signup
    st.markdown("""
        <div class="auth-link">
            Don't have an account? <a href="#" id="signup_link">Sign Up</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle link click
    if st.button("Switch to Sign Up", key="switch_signup"):
        st.session_state.page = 'signup'
        st.rerun()

def main_app():
    st.markdown("""
        <div style="text-align: center; padding: 50px; color: white;">
            <h1 style="font-size: 48px; margin-bottom: 20px;">🎉 Welcome to the App!</h1>
            <p style="font-size: 20px; color: rgba(255,255,255,0.7);">
                Hello, <strong>{}</strong>! You are successfully logged in.
            </p>
        </div>
    """.format(st.session_state.username), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()

# Main app logic
def main():
    st.set_page_config(
        page_title="AI Chat Bot Authentication",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    load_css()
    
    if st.session_state.authenticated:
        main_app()
    else:
        if st.session_state.page == 'login':
            login_page()
        else:
            signup_page()

if __name__ == "__main__":
    main()
