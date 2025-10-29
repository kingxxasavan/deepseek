import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
import io
import pandas as pd
from PIL import Image
import base64

# Configure page
st.set_page_config(
    page_title="CrypticX",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for purple glass design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
    }
    
    .glass {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .purple-glass {
        background: rgba(147, 51, 234, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(147, 51, 234, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(147, 51, 234, 0.2);
    }
    
    .green-glass {
        background: rgba(34, 197, 94, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(34, 197, 94, 0.2);
    }
    
    .nav-bar {
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 1000;
        background: rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(20px);
        padding: 1rem 0;
    }
    
    .nav-link {
        color: white !important;
        text-decoration: none;
        margin: 0 1rem;
        font-weight: 500;
    }
    
    .nav-link:hover {
        color: #a855f7 !important;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #a855f7, #9333ea);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .btn-secondary {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .centered-form {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .pricing-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
    }
    
    .pricing-card.pro {
        background: rgba(168, 85, 247, 0.2);
        border: 1px solid rgba(168, 85, 247, 0.4);
        position: relative;
    }
    
    .pricing-card.pro::before {
        content: 'MOST POPULAR';
        position: absolute;
        top: -10px;
        left: 50%;
        transform: translateX(-50%);
        background: #a855f7;
        color: white;
        padding: 0.25rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .feature-list {
        list-style: none;
        padding: 0;
    }
    
    .feature-list li {
        padding: 0.5rem 0;
        color: rgba(255, 255, 255, 0.8);
    }
    
    .feature-list li::before {
        content: '✓ ';
        color: #a855f7;
        font-weight: bold;
    }
    
    h1, h2, h3 {
        color: white;
        font-weight: 700;
    }
    
    /* Hide nav on scroll - approximate with JS */
    <script>
    let lastScrollTop = 0;
    const nav = document.querySelector('.nav-bar');
    window.addEventListener('scroll', () => {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            nav.style.transform = 'translateY(-100%)';
        } else {
            nav.style.transform = 'translateY(0)';
        }
        lastScrollTop = scrollTop;
    });
    </script>
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_right_panel' not in st.session_state:
    st.session_state.show_right_panel = True
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {'flashcards': [], 'quizzes': [], 'documents': []}

# Gemini setup - assume API key in secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.95,
            "max_output_tokens": 2048,
        },
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
    )
except:
    st.warning("Gemini API key not found. Please add to secrets.toml")
    model = None

# Navigation Bar
def render_nav():
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col1:
        if st.button("Home", key="nav_home"):
            st.session_state.page = 'home'
    with col2:
        if st.button("Pricing", key="nav_pricing"):
            st.session_state.page = 'pricing'
    with col3:
        if st.button("Contact", key="nav_contact"):
            st.session_state.page = 'contact'
    with col4:
        if st.button("Dashboard", key="nav_dashboard"):
            if st.session_state.user:
                st.session_state.page = 'dashboard'
            else:
                st.session_state.page = 'login'
    with col5:
        if st.session_state.user:
            if st.button("Logout", key="nav_logout"):
                st.session_state.user = None
                st.rerun()
        else:
            if st.button("Login", key="nav_login"):
                st.session_state.page = 'login'

st.markdown('<div class="nav-bar"><div style="display: flex; justify-content: center; align-items: center;">', unsafe_allow_html=True)
render_nav()
st.markdown('</div></div>', unsafe_allow_html=True)
st.markdown('<div style="height: 70px;"></div>', unsafe_allow_html=True)  # Spacer for fixed nav

# Page Router
def main():
    if st.session_state.page == 'home':
        render_home()
    elif st.session_state.page == 'pricing':
        render_pricing()
    elif st.session_state.page == 'login':
        render_login()
    elif st.session_state.page == 'signup':
        render_signup()
    elif st.session_state.page == 'forgot':
        render_forgot()
    elif st.session_state.page == 'dashboard':
        if not st.session_state.user:
            st.session_state.page = 'login'
            st.rerun()
        else:
            render_dashboard()
    elif st.session_state.page == 'contact':
        render_contact()

def render_home():
    st.markdown('<div style="height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">', unsafe_allow_html=True)
    st.markdown('<h1>Welcome to CrypticX</h1><p style="font-size: 1.2rem; color: rgba(255,255,255,0.8);">Your AI-powered study companion. Unlock the power of generative AI to master any subject.</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown('<button class="btn-primary" onclick="st.session_state.page = \'signup\'">Get Started for Free</button>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Why Choose Us
    st.markdown('<div class="glass" style="margin: 4rem 2rem; padding: 3rem; text-align: center;">', unsafe_allow_html=True)
    st.markdown('<h2>Why Choose CrypticX?</h2><p>Revolutionize your learning with cutting-edge AI tools designed for students and professionals.</p>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown('<h3>🔮 AI Magic</h3><p>Generate flashcards and quizzes instantly.</p>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<h3>📚 Document Analysis</h3><p>Upload PDFs and get smart summaries.</p>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('<h3>🚀 Easy to Use</h3><p>Intuitive interface, start in seconds.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Features
    st.markdown('<div style="margin: 4rem 2rem; text-align: center;">', unsafe_allow_html=True)
    st.markdown('<h2>Features</h2>', unsafe_allow_html=True)
    cols = st.columns(2)
    with cols[0]:
        st.markdown("""
        <ul class="feature-list">
            <li>Flashcard Generation</li>
            <li>Interactive Quizzes</li>
            <li>PDF Upload & Analysis</li>
            <li>Progress Tracking</li>
        </ul>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
        <ul class="feature-list">
            <li>Advanced Summaries</li>
            <li>Team Collaboration</li>
            <li>Custom Integrations</li>
            <li>Priority Support</li>
        </ul>
        """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown('<button class="btn-primary" onclick="st.session_state.page = \'pricing\'">Get Started for Free</button>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_pricing():
    st.markdown('<div style="padding: 4rem 2rem; text-align: center;">', unsafe_allow_html=True)
    st.markdown('<h1 style="color: white;">Choose Your Plan</h1><p style="color: rgba(255,255,255,0.8);">Start free, upgrade when you\'re ready</p>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        <div class="pricing-card">
            <h3>Free</h3>
            <h2>$0<span style="font-size: 1rem;">/mo</span></h2>
            <ul class="feature-list">
                <li>10 AI questions/day</li>
                <li>Basic summaries</li>
                <li>5 quizzes/week</li>
                <li>Community support</li>
            </ul>
            <button class="btn-secondary" onclick="st.session_state.page = 'signup'">Start Free</button>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
        <div class="pricing-card pro">
            <h3>Pro</h3>
            <h2>$15<span style="font-size: 1rem;">/mo</span></h2>
            <ul class="feature-list">
                <li>Unlimited AI questions</li>
                <li>Advanced summaries</li>
                <li>Unlimited quizzes</li>
                <li>PDF upload (100MB)</li>
                <li>Priority support</li>
                <li>Progress analytics</li>
            </ul>
            <button class="btn-primary" onclick="st.session_state.page = 'signup'">Get Pro</button>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown("""
        <div class="pricing-card">
            <h3>Enterprise</h3>
            <h2>$35<span style="font-size: 1rem;">/mo</span></h2>
            <ul class="feature-list">
                <li>Everything in Pro</li>
                <li>Team accounts</li>
                <li>Advanced analytics</li>
                <li>Custom integrations</li>
                <li>Dedicated support</li>
                <li>Unlimited storage</li>
            </ul>
            <button class="btn-secondary">Contact Us</button>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_login():
    st.markdown('<div style="height: 100vh; display: flex; justify-content: center; align-items: center;">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass centered-form">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: white;">Login</h2>', unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.button("Login", key="login_btn"):
            # Mock login
            if email and password:
                st.session_state.user = {"email": email}
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.error("Please enter email and password")
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("Forgot Password?", key="forgot_link"):
                st.session_state.page = 'forgot'
                st.rerun()
        st.markdown('<p style="text-align: center; color: rgba(255,255,255,0.8);">Don\'t have an account? <a href="#" onclick="st.session_state.page = \'signup\'" style="color: #a855f7;">Sign up</a></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_signup():
    st.markdown('<div style="height: 100vh; display: flex; justify-content: center; align-items: center;">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass centered-form">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: white;">Sign Up</h2>', unsafe_allow_html=True)
        name = st.text_input("Full Name", placeholder="Enter your name")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        if st.button("Sign Up", key="signup_btn"):
            # Mock signup
            if name and email and password:
                st.session_state.user = {"name": name, "email": email}
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.error("Please fill all fields")
        st.markdown('<p style="text-align: center; color: rgba(255,255,255,0.8);">Already have an account? <a href="#" onclick="st.session_state.page = \'login\'" style="color: #a855f7;">Login</a></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_forgot():
    st.markdown('<div style="height: 100vh; display: flex; justify-content: center; align-items: center;">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass centered-form">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: white;">Forgot Password</h2>', unsafe_allow_html=True)
        email = st.text_input("Email", placeholder="Enter your email to reset")
        if st.button("Send Reset Link", key="reset_btn"):
            if email:
                st.success("Reset link sent to your email!")
                st.session_state.page = 'login'
                st.rerun()
            else:
                st.error("Please enter your email")
        if st.button("Back to Login", key="back_login"):
            st.session_state.page = 'login'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_contact():
    st.markdown('<div style="padding: 4rem 2rem;">', unsafe_allow_html=True)
    st.markdown('<div class="glass" style="max-width: 600px; margin: 0 auto;">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: white;">Contact Us</h2>', unsafe_allow_html=True)
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    if st.button("Send Message", key="contact_btn"):
        st.success("Message sent! We'll get back to you soon.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_dashboard():
    # Full width layout
    if 'chat_input' not in st.session_state:
        st.session_state.chat_input = ""
    
    # Left sidebar - Purple glass side panel
    with st.sidebar:
        st.markdown('<div class="purple-glass" style="height: 100vh; overflow-y: auto;">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white;">Study Tools</h3>', unsafe_allow_html=True)
        tool = st.selectbox("Select Tool", ["Chat with AI", "Generate Flashcards", "Create Quiz", "Analyze Document"])
        if tool == "Analyze Document":
            uploaded_file = st.file_uploader("Upload PDF", type="pdf")
            if uploaded_file:
                # Mock analysis
                st.session_state.generated_content['documents'].append("Analyzed: " + uploaded_file.name)
        elif tool == "Generate Flashcards":
            topic = st.text_input("Topic")
            if st.button("Generate", key="gen_flash"):
                if model:
                    response = model.generate_content(f"Generate 5 flashcards on {topic}")
                    st.session_state.generated_content['flashcards'].append(response.text)
                else:
                    st.session_state.generated_content['flashcards'].append(f"Mock flashcards on {topic}")
        elif tool == "Create Quiz":
            topic = st.text_input("Quiz Topic")
            if st.button("Create", key="gen_quiz"):
                if model:
                    response = model.generate_content(f"Create a 10-question quiz on {topic}")
                    st.session_state.generated_content['quizzes'].append(response.text)
                else:
                    st.session_state.generated_content['quizzes'].append(f"Mock quiz on {topic}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chat area
    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.markdown('<div class="glass" style="height: 80vh; overflow-y: auto; padding: 1rem;">', unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask anything about your studies..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Auto-hide right panel when chatting
            st.session_state.show_right_panel = False
            
            if model:
                response = model.generate_content(prompt)
                full_response = response.text
            else:
                full_response = "Mock response: This is a generated answer using Gemini 1.5 Flash."
            
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            with st.chat_message("assistant"):
                st.markdown(full_response)
        
        # Show right panel after chat (manual toggle for simplicity)
        if st.button("Show Outputs"):
            st.session_state.show_right_panel = True
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Right panel - Green glass, conditional
    if st.session_state.show_right_panel:
        with col_right:
            st.markdown('<div class="green-glass" style="height: 80vh; overflow-y: auto;">', unsafe_allow_html=True)
            st.markdown('<h3 style="color: white;">Generated Content</h3>', unsafe_allow_html=True)
            
            if st.session_state.generated_content['flashcards']:
                st.markdown("### Flashcards")
                for card in st.session_state.generated_content['flashcards'][-3:]:  # Last 3
                    st.markdown(card)
            
            if st.session_state.generated_content['quizzes']:
                st.markdown("### Quizzes")
                for quiz in st.session_state.generated_content['quizzes'][-3:]:
                    st.markdown(quiz)
            
            if st.session_state.generated_content['documents']:
                st.markdown("### Documents")
                for doc in st.session_state.generated_content['documents'][-3:]:
                    st.markdown(doc)
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
