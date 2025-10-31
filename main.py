import streamlit as st
import base64
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Crptic AI - AI Study Tool",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'selected_plan' not in st.session_state:
    st.session_state.selected_plan = None
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'signup'
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'current_chat' not in st.session_state:
    st.session_state.current_chat = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Global navigation handling via query params
query_params = st.query_params
if 'action' in query_params:
    action = query_params['action'][0] if isinstance(query_params['action'], list) else query_params['action']
    handled = False
    if action == 'home':
        st.session_state.current_page = 'home'
        handled = True
    elif action == 'dashboard':
        if st.session_state.logged_in:
            st.session_state.current_page = 'dashboard'
            handled = True
        else:
            st.session_state.current_page = 'home'
            handled = True
    elif action == 'auth':
        st.session_state.current_page = 'auth'
        handled = True
    elif action == 'contact':
        st.session_state.current_page = 'contact'
        handled = True
    if handled:
        del st.query_params['action']
        st.rerun()

if 'plan' in query_params:
    plan = query_params['plan'][0] if isinstance(query_params['plan'], list) else query_params['plan']
    st.session_state.selected_plan = plan
    del st.query_params['plan']
    st.rerun()

# Full CSS
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    .stDecoration {display: none !important;}
    
    /* Force hide sidebar completely */
    section[data-testid="stSidebar"] {display: none !important;}
    .stSidebar {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
    
    /* Reset padding */
    .block-container {padding: 0 !important; margin: 0 !important;}
    .main .block-container {max-width: 100% !important; padding: 0 !important;}
    .stApp {margin: 0 !important; padding: 0 !important;}
    section.main > div {padding: 0 !important;}
    div[data-testid="stAppViewContainer"] {padding: 0 !important; margin: 0 !important;}
    
    /* Hide all Streamlit buttons completely */
    .stButton {display: none !important; visibility: hidden !important; position: absolute !important; width: 0 !important; height: 0 !important; opacity: 0 !important;}
    
    /* Base styles */
    * {margin: 0; padding: 0; box-sizing: border-box;}
    html, body {margin: 0 !important; padding: 0 !important; overflow-x: hidden; scroll-behavior: smooth;}
    
    .stApp {background: #0a0a0f; color: #fff; font-family: 'Inter', 'Segoe UI', sans-serif;}
    
    /* Grid background */
    .grid-background {position: fixed; inset: 0; background-image: linear-gradient(rgba(139, 92, 246, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(139, 92, 246, 0.03) 1px, transparent 1px); background-size: 50px 50px; z-index: 0;}
    
    /* Animated glow effects */
    .glow-orb {position: fixed; width: 800px; height: 800px; border-radius: 50%; filter: blur(120px); opacity: 0.3; z-index: 1; pointer-events: none;}
    .glow-orb.purple {background: radial-gradient(circle, rgba(139, 92, 246, 0.6), transparent); top: -200px; left: 50%; transform: translateX(-50%); animation: float 20s ease-in-out infinite;}
    .glow-orb.pink {background: radial-gradient(circle, rgba(236, 72, 153, 0.4), transparent); bottom: -300px; right: -200px; animation: float 25s ease-in-out infinite reverse;}
    
    @keyframes float {0%, 100% { transform: translate(-50%, 0) scale(1); } 50% { transform: translate(-50%, -50px) scale(1.1); } }
    @keyframes fadeInUp {from {opacity: 0; transform: translateY(30px);} to {opacity: 1; transform: translateY(0);} }
    .fade-in-up {animation: fadeInUp 0.6s ease-out forwards;}
    
    /* Navigation */
    .nav-container {position: fixed; top: 0; left: 0; right: 0; z-index: 1000; background: transparent; backdrop-filter: blur(20px); border-bottom: 1px solid rgba(139, 92, 246, 0.1); transition: all 0.3s ease;}
    nav {position: relative; z-index: 100; display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 4rem; max-width: 1400px; margin: 0 auto;}
    .logo {display: flex; align-items: center; gap: 0.75rem; font-size: 1.5rem; font-weight: 700; color: #8b5cf6; cursor: pointer; letter-spacing: 0.5px;}
    .logo-icon {font-size: 1.8rem; filter: drop-shadow(0 0 10px rgba(139, 92, 246, 0.8)); animation: pulse 2s ease-in-out infinite;}
    @keyframes pulse {0%, 100% { filter: drop-shadow(0 0 10px rgba(139, 92, 246, 0.8)); } 50% { filter: drop-shadow(0 0 20px rgba(139, 92, 246, 1)); } }
    .nav-links {display: flex; gap: 2.5rem; align-items: center;}
    .nav-link {color: rgba(255, 255, 255, 0.7); text-decoration: none; font-size: 0.95rem; font-weight: 500; transition: all 0.3s; cursor: pointer; padding: 0.5rem 0; border-bottom: 2px solid transparent; position: relative;}
    .nav-link:hover {color: #fff; border-bottom-color: #8b5cf6;}
    .nav-link.active {color: #fff; border-bottom-color: #8b5cf6;}
    .nav-cta {padding: 0.7rem 1.8rem !important; border-radius: 50px; background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); color: #fff; font-weight: 600; cursor: pointer; transition: all 0.3s; border: none; font-size: 0.9rem; box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);}
    .nav-cta:hover {transform: translateY(-2px); box-shadow: 0 6px 25px rgba(139, 92, 246, 0.6);}
    .user-greeting {color: #8b5cf6; font-weight: 600;}
    
    /* Main content */
    .content-wrapper {position: relative; z-index: 10; padding-top: 80px;}
    
    /* Hero section */
    .hero-section {min-height: calc(100vh - 80px); display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 4rem 2rem; position: relative;}
    .welcome-badge {display: inline-flex; align-items: center; gap: 0.5rem; background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); padding: 0.6rem 1.5rem; border-radius: 50px; font-size: 0.9rem; color: #fff; font-weight: 500; margin-bottom: 2rem; backdrop-filter: blur(10px); animation: fadeInUp 0.6s ease-out;}
    .hero-title {font-size: 5rem; font-weight: 800; line-height: 1.1; margin-bottom: 1.5rem; background: linear-gradient(135deg, #ffffff 0%, #8b5cf6 50%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; max-width: 1000px; animation: fadeInUp 0.8s ease-out 0.2s backwards;}
    .hero-subtitle {font-size: 1.25rem; color: rgba(255, 255, 255, 0.6); margin-bottom: 3rem; max-width: 700px; line-height: 1.7; animation: fadeInUp 1s ease-out 0.4s backwards;}
    .hero-cta {padding: 1rem 2.5rem; border-radius: 50px; background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); color: #fff; font-weight: 600; cursor: pointer; transition: all 0.3s; border: none; font-size: 1.1rem; box-shadow: 0 8px 30px rgba(139, 92, 246, 0.4); animation: fadeInUp 1.2s ease-out 0.6s backwards;}
    .hero-cta:hover {transform: translateY(-3px); box-shadow: 0 12px 40px rgba(139, 92, 246, 0.6);}
    
    /* Stats section */
    .stats-section {display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; max-width: 900px; margin: 4rem auto 0; padding: 0 2rem;}
    .stat-item {text-align: center;}
    .stat-number {font-size: 3rem; font-weight: 800; background: linear-gradient(135deg, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;}
    .stat-label {color: rgba(255, 255, 255, 0.6); font-size: 0.95rem;}
    
    /* Section styling */
    .section {position: relative; z-index: 10; max-width: 1200px; margin: 0 auto; padding: 6rem 2rem; width: 100%; display: flex; flex-direction: column; align-items: center;}
    .section-title {font-size: 3rem; font-weight: 700; text-align: center; margin-bottom: 1rem; color: #fff;}
    .section-subtitle {font-size: 1.15rem; color: rgba(255, 255, 255, 0.5); text-align: center; margin-bottom: 4rem;}
    
    /* Feature cards */
    .features-grid {display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-top: 3rem; width: 100%;}
    .feature-card {background: rgba(139, 92, 246, 0.05); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 24px; padding: 2.5rem; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); backdrop-filter: blur(10px); cursor: pointer; height: 100%; display: flex; flex-direction: column; align-items: center; text-align: center;}
    .feature-card:hover {transform: translateY(-10px); background: rgba(139, 92, 246, 0.1); border-color: rgba(139, 92, 246, 0.5); box-shadow: 0 20px 60px rgba(139, 92, 246, 0.2);}
    .feature-icon {font-size: 3rem; margin-bottom: 1.5rem; display: block; transition: transform 0.3s;}
    .feature-card:hover .feature-icon {transform: scale(1.1);}
    .feature-card h3 {font-size: 1.5rem; margin-bottom: 1rem; color: #fff; font-weight: 600;}
    .feature-card p {color: rgba(255, 255, 255, 0.6); line-height: 1.7; font-size: 0.95rem; flex-grow: 1;}
    
    /* Pricing cards */
    .pricing-grid {display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-top: 3rem; width: 100%;}
    .pricing-card {background: rgba(139, 92, 246, 0.05); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 24px; padding: 3rem 2.5rem; text-align: center; transition: all 0.4s; position: relative;}
    .pricing-card.featured {background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(236, 72, 153, 0.15)); border: 2px solid #8b5cf6; transform: scale(1.05);}
    .pricing-card:hover {transform: translateY(-10px) scale(1.02); box-shadow: 0 20px 60px rgba(139, 92, 246, 0.3);}
    .pricing-card.featured:hover {transform: translateY(-10px) scale(1.07);}
    .pricing-badge {position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: linear-gradient(135deg, #8b5cf6, #ec4899); color: white; padding: 0.4rem 1.2rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;}
    .pricing-card h3 {font-size: 1.5rem; margin-bottom: 1rem; color: #fff;}
    .price {font-size: 3.5rem; font-weight: 800; margin: 1.5rem 0; background: linear-gradient(135deg, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
    .price-period {font-size: 1rem; color: rgba(255, 255, 255, 0.5);}
    .feature-list {text-align: left; margin: 2rem 0; color: rgba(255, 255, 255, 0.7); line-height: 2.2; font-size: 0.95rem;}
    .pricing-button {width: 100%; padding: 0.9rem; border-radius: 12px; background: rgba(139, 92, 246, 0.2); border: 1px solid rgba(139, 92, 246, 0.3); color: #fff; font-weight: 600; cursor: pointer; transition: all 0.3s; margin-top: 1rem;}
    .pricing-button:hover {background: rgba(139, 92, 246, 0.3); border-color: #8b5cf6; transform: translateY(-2px);}
    .pricing-card.featured .pricing-button {background: linear-gradient(135deg, #8b5cf6, #ec4899); border: none;}
    
    /* Auth styles */
    .auth-container {min-height: calc(100vh - 80px); display: flex; justify-content: center; align-items: center; padding: 2rem;}
    .auth-box {background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; padding: 3rem; max-width: 400px; width: 100%; backdrop-filter: blur(20px);}
    .auth-header {text-align: center; margin-bottom: 2rem;}
    .auth-title {font-size: 2.5rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem;}
    .auth-subtitle {color: rgba(255, 255, 255, 0.6); font-size: 1.1rem;}
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 12px; color: #fff; padding: 1rem;}
    .stTextInput > div > div > input::placeholder, .stTextArea > div > div > textarea::placeholder {color: rgba(255, 255, 255, 0.5);}
    
    /* Contact Page */
    .contact-section {min-height: calc(100vh - 80px); display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 4rem 2rem;}
    .contact-form {max-width: 600px; width: 100%; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; padding: 3rem; backdrop-filter: blur(20px);}
    
    /* Dashboard Sidebar */
    .dashboard-wrapper {display: flex; min-height: calc(100vh - 80px); position: relative;}
    .dashboard-sidebar {width: 280px; background: rgba(10, 10, 15, 0.8); border-right: 1px solid rgba(139, 92, 246, 0.2); padding: 2rem 1.5rem; position: fixed; height: calc(100vh - 80px); overflow-y: auto; backdrop-filter: blur(20px);}
    .dashboard-main {margin-left: 280px; flex: 1; padding: 2rem; width: calc(100% - 280px);}
    
    .sidebar-section {margin-bottom: 2rem;}
    .sidebar-title {color: rgba(255, 255, 255, 0.5); font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;}
    .new-chat-btn {background: linear-gradient(135deg, #8b5cf6, #ec4899); color: white; padding: 0.9rem; border-radius: 12px; text-align: center; font-weight: 600; cursor: pointer; margin-bottom: 1.5rem; transition: all 0.3s;}
    .new-chat-btn:hover {transform: translateY(-2px); box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);}
    .chat-item {padding: 0.8rem 1rem; margin: 0.5rem 0; background: rgba(255, 255, 255, 0.05); border-radius: 10px; cursor: pointer; transition: all 0.3s; color: rgba(255, 255, 255, 0.7); font-size: 0.9rem;}
    .chat-item:hover {background: rgba(139, 92, 246, 0.2); transform: translateX(5px);}
    .user-profile {position: absolute; bottom: 0; left: 0; right: 0; background: rgba(255, 255, 255, 0.05); padding: 1.2rem; border-top: 1px solid rgba(139, 92, 246, 0.2); display: flex; align-items: center; gap: 0.8rem;}
    .avatar {width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #8b5cf6, #ec4899); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.2rem;}
    
    /* Chat Interface */
    .chat-header {background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 20px; padding: 1.5rem 2rem; margin-bottom: 2rem;}
    .chat-messages {min-height: 400px; max-height: 600px; overflow-y: auto; padding: 1.5rem; background: rgba(255, 255, 255, 0.02); border-radius: 20px; margin-bottom: 2rem;}
    .message {margin: 1rem 0; padding: 1rem 1.5rem; border-radius: 18px; max-width: 75%; animation: messageSlide 0.3s ease;}
    @keyframes messageSlide {from {opacity: 0; transform: translateY(10px);} to {opacity: 1; transform: translateY(0);}}
    .user-message {background: linear-gradient(135deg, #8b5cf6, #ec4899); color: white; margin-left: auto; text-align: right;}
    .ai-message {background: rgba(139, 92, 246, 0.1); color: #fff; border: 1px solid rgba(139, 92, 246, 0.2);}
    .chat-input-area {background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 1.5rem;}
    
    /* File Upload */
    [data-testid="stFileUploader"] {border: 2px dashed rgba(139, 92, 246, 0.5); border-radius: 12px; padding: 2rem; background: rgba(139, 92, 246, 0.05);}
    
    /* Footer */
    .custom-footer {position: relative; z-index: 10; border-top: 1px solid rgba(139, 92, 246, 0.1); margin-top: 5rem; padding: 3rem 2rem; text-align: center; color: rgba(255, 255, 255, 0.4); background: rgba(10, 10, 15, 0.5);}
    .footer-links {display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;}
    .footer-link {color: rgba(255, 255, 255, 0.5); text-decoration: none; font-size: 0.9rem; transition: color 0.3s; cursor: pointer;}
    .footer-link:hover {color: #8b5cf6;}
    
    /* Responsive */
    @media (max-width: 1024px) {
        .features-grid, .pricing-grid {grid-template-columns: repeat(2, 1fr);}
        .dashboard-sidebar {width: 240px;}
        .dashboard-main {margin-left: 240px; width: calc(100% - 240px);}
    }
    @media (max-width: 768px) {
        nav {padding: 1rem 1.5rem;}
        .nav-links {display: none;}
        .hero-title {font-size: 2.5rem;}
        .hero-subtitle {font-size: 1.1rem;}
        .features-grid, .pricing-grid, .stats-section {grid-template-columns: 1fr;}
        .section-title {font-size: 2rem;}
        .pricing-card.featured {transform: scale(1);}
        .dashboard-sidebar {display: none;}
        .dashboard-main {margin-left: 0; width: 100%;}
    }
    
    /* Unhide specific buttons */
    .hero-cta, [key="hero_start"], [key="plan_free"], [key="plan_starter"], [key="plan_pro"], [key="back_home"], [key="login_submit"], [key="signup_submit"], [key="toggle_login"], [key="toggle_signup"], [key="logout"], [key="new_chat_btn"], [key="send_message"], [key="contact_submit"] {
        display: inline-block !important;
        visibility: visible !important;
        position: relative !important;
        width: auto !important;
        height: auto !important;
        opacity: 1 !important;
    }
</style>
""", unsafe_allow_html=True)

# Background elements
st.markdown('<div class="grid-background"></div><div class="glow-orb purple"></div><div class="glow-orb pink"></div>', unsafe_allow_html=True)

# Pages
def landing_page():
    st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)
    st.markdown('<div id="home" class="hero-section"><div class="welcome-badge">✨ Welcome to Crptic AI - AI-Powered Learning Assistant</div><h1 class="hero-title">Master Your Studies with AI-Powered Learning</h1><p class="hero-subtitle">Upload documents, images, PDFs and chat with Gemini 2.5 Flash. Transform the way you learn with intelligent tools designed for students.</p><button class="hero-cta" onclick="window.location.href=\'?action=auth&plan=Free\'">Start Learning Free</button></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="stats-section"><div class="stat-item"><div class="stat-number">50K+</div><div class="stat-label">Active Students</div></div><div class="stat-item"><div class="stat-number">95%</div><div class="stat-label">Satisfaction Rate</div></div><div class="stat-item"><div class="stat-number">1M+</div><div class="stat-label">Questions Answered</div></div></div></div>', unsafe_allow_html=True)
    
    st.markdown('<div id="features" class="section"><h2 class="section-title">Why Choose Crptic AI</h2><p class="section-subtitle">The smartest way to study in 2025</p><div class="features-grid">', unsafe_allow_html=True)
    st.markdown('<div class="feature-card"><span class="feature-icon">📚</span><h3>Multi-Format Support</h3><p>Upload PDFs, Word docs, images, spreadsheets. Our AI understands them all with Gemini 2.5 Flash.</p></div><div class="feature-card"><span class="feature-icon">⚡</span><h3>Lightning Fast</h3><p>Get instant answers powered by Google\'s most advanced AI model. No more waiting hours for responses.</p></div><div class="feature-card"><span class="feature-icon">🔒</span><h3>Secure & Private</h3><p>Your documents are processed securely with API keys stored safely. We never store your data.</p></div><div class="feature-card"><span class="feature-icon">🎯</span><h3>Smart Learning</h3><p>AI adapts to your learning style, providing customized explanations that make sense to you.</p></div><div class="feature-card"><span class="feature-icon">💡</span><h3>Document Analysis</h3><p>Extract insights from any document format. Summarize, explain, and get answers from your materials.</p></div><div class="feature-card"><span class="feature-icon">🌟</span><h3>Student Success</h3><p>Join thousands who\'ve improved grades with our intelligent AI-powered study assistant.</p></div></div></div>', unsafe_allow_html=True)
    
    st.markdown('<div id="pricing" class="section"><h2 class="section-title">Choose Your Plan</h2><p class="section-subtitle">Start free, upgrade when you\'re ready</p><div class="pricing-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="pricing-card"><h3>Free</h3><div class="price">$0<span class="price-period">/mo</span></div><div class="feature-list">✓ 10 messages/day<br>✓ Basic document upload<br>✓ Image analysis<br>✓ Community support</div><button class="pricing-button" onclick="window.location.href=\'?action=auth&plan=Free\'">Start Free</button></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pricing-card featured"><div class="pricing-badge">⭐ MOST POPULAR</div><h3>Starter</h3><div class="price">$15<span class="price-period">/mo</span></div><div class="feature-list">✓ 100 messages/day<br>✓ All document formats<br>✓ Priority processing<br>✓ Email support<br>✓ Chat history</div><button class="pricing-button" onclick="window.location.href=\'?action=auth&plan=Starter\'">Get Starter</button></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="pricing-card"><h3>Pro</h3><div class="price">$35<span class="price-period">/mo</span></div><div class="feature-list">✓ Unlimited messages<br>✓ Batch processing<br>✓ API access<br>✓ Priority support<br>✓ Advanced analytics<br>✓ Custom integrations</div><button class="pricing-button" onclick="window.location.href=\'?action=auth&plan=Pro\'">Get Pro</button></div>', unsafe_allow_html=True)
    
    st.markdown('</div></div></div>', unsafe_allow_html=True)

def auth_page():
    st.markdown('<div class="content-wrapper"><div class="auth-container"><div class="auth-box">', unsafe_allow_html=True)
    
    if st.button("← Back to Home", key="back_home"):
        st.session_state.current_page = 'home'
        st.session_state.selected_plan = None
        st.rerun()
    
    if st.session_state.selected_plan:
        st.markdown(f'<div class="welcome-badge" style="margin-bottom: 1.5rem;">Selected Plan: {st.session_state.selected_plan}</div>', unsafe_allow_html=True)
    
    if st.session_state.auth_mode == 'login':
        st.markdown('<div class="auth-header"><h1 class="auth-title">Welcome Back</h1><p class="auth-subtitle">Sign in to access your dashboard</p></div>', unsafe_allow_html=True)
        email = st.text_input("Email", key="login_email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
        
        if st.button("Sign In", key="login_submit"):
            if email and password:
                st.session_state.logged_in = True
                st.session_state.user_name = email.split('@')[0]
                st.session_state.current_page = 'dashboard'
                st.session_state.auth_mode = 'signup'
                st.rerun()
            else:
                st.error("⚠ Please fill all fields")
        
        if st.button("Don't have an account? Create one", key="toggle_signup"):
            st.session_state.auth_mode = 'signup'
            st.rerun()
    else:
        st.markdown('<div class="auth-header"><h1 class="auth-title">Create Account</h1><p class="auth-subtitle">Join and start your AI learning journey</p></div>', unsafe_allow_html=True)
        name = st.text_input("Full Name", key="signup_name", placeholder="Enter your name")
        email = st.text_input("Email", key="signup_email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", key="signup_password", placeholder="Create a password")
        
        if st.button("Create Account", key="signup_submit"):
            if name and email and password:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.session_state.current_page = 'dashboard'
                st.session_state.auth_mode = 'signup'
                st.rerun()
            else:
                st.error("⚠ Please fill all fields")
        
        if st.button("Already have an account? Sign In", key="toggle_login"):
            st.session_state.auth_mode = 'login'
            st.rerun()
    
    st.markdown('</div></div></div>', unsafe_allow_html=True)

def contact_page():
    st.markdown('<div class="content-wrapper"><div class="contact-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title" style="font-size: 3.5rem; margin-bottom: 1rem;">Get in Touch</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle" style="margin-bottom: 3rem;">Have questions? We\'d love to hear from you.</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    name = st.text_input("Your Name", placeholder="John Doe")
    email = st.text_input("Email Address", placeholder="your@email.com")
    message = st.text_area("Message", placeholder="Tell us what you need help with...", height=150)
    
    if st.button("Send Message", key="contact_submit"):
        if name and email and message:
            st.success("✓ Message sent! We'll get back to you soon.")
        else:
            st.error("⚠ Please fill all fields")
    
    st.markdown('</div></div></div>', unsafe_allow_html=True)

def dashboard_page():
    st.markdown('<div class="content-wrapper"><div class="dashboard-wrapper">', unsafe_allow_html=True)
    
    # Sidebar
    st.markdown(f'''
    <div class="dashboard-sidebar">
        <div class="sidebar-section">
            <div class="new-chat-btn" onclick="window.location.reload()">➕ New Chat</div>
        </div>
        
        <div class="sidebar-section">
            <div class="sidebar-title">Recent Chats</div>
            <div class="chat-item">📚 Study Guide for Biology</div>
            <div class="chat-item">📊 Data Analysis Help</div>
            <div class="chat-item">🖼️ Image Analysis Task</div>
            <div class="chat-item">📄 Document Summary</div>
            <div class="chat-item">🧮 Math Problem Solving</div>
        </div>
        
        <div class="sidebar-section">
            <div class="sidebar-title">Tools</div>
            <div class="chat-item">📁 Document Manager</div>
            <div class="chat-item">⚙️ Settings</div>
            <div class="chat-item" onclick="window.location.href='?action=home#pricing'">💰 Upgrade Plan</div>
        </div>
        
        <div class="user-profile">
            <div class="avatar">{st.session_state.user_name[0].upper()}</div>
            <div>
                <div style="font-weight: 600; color: #fff;">{st.session_state.user_name}</div>
                <div style="font-size: 0.85rem; color: rgba(255, 255, 255, 0.6);">{st.session_state.selected_plan or 'Free'} Plan</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Main Content
    st.markdown('<div class="dashboard-main">', unsafe_allow_html=True)
    
    # Chat Header
    st.markdown('''
    <div class="chat-header">
        <h2 style="margin: 0; font-size: 1.8rem;">💬 Chat with Crptic AI</h2>
        <p style="margin: 5px 0 0 0; color: rgba(255, 255, 255, 0.6);">Powered by Gemini 2.5 Flash</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # File Upload
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
    
    # Chat Messages
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    if len(st.session_state.current_chat) == 0:
        st.markdown('''
        <div style="text-align: center; padding: 80px 20px; color: rgba(255, 255, 255, 0.4);">
            <div style="font-size: 4rem; margin-bottom: 20px;">⚡</div>
            <h3 style="color: #fff; margin-bottom: 10px;">How can I help you learn today?</h3>
            <p>Upload documents, ask questions, or start a conversation!</p>
        </div>
        ''', unsafe_allow_html=True)
    else:
        for msg in st.session_state.current_chat:
            if msg['role'] == 'user':
                st.markdown(f'<div class="message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message ai-message">⚡ {msg["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat Input
    st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_area(
            "Type your message...",
            placeholder="Ask me anything about your documents, or ask for help with learning...",
            height=100,
            key="user_input",
            label_visibility="collapsed"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        send_button = st.button("Send 🚀", use_container_width=True, key="send_message")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle message sending
    if send_button and user_input:
        st.session_state.current_chat.append({
            'role': 'user',
            'content': user_input
        })
        
        ai_response = f"I understand you're asking about: '{user_input[:50]}...'. "
        ai_response += "I'm processing your request with Gemini 2.5 Flash. "
        
        if uploaded_files:
            ai_response += f"I've also analyzed your {len(uploaded_files)} uploaded file(s). "
        
        ai_response += "Here's what I found: [This is where the actual AI response would appear. In production, this connects to Gemini 2.5 Flash API using your Streamlit secrets for secure authentication.]"
        
        st.session_state.current_chat.append({
            'role': 'assistant',
            'content': ai_response
        })
        
        st.rerun()
    
    st.markdown('</div></div></div>', unsafe_allow_html=True)

# Main Router
if not st.session_state.logged_in:
    # Navigation for logged out users
    if st.session_state.current_page == 'auth':
        st.markdown('<div class="nav-container"><nav><div class="logo" onclick="window.location.href=\'?action=home\'"><span class="logo-icon">⚡</span><span>Crptic AI</span></div></nav></div>', unsafe_allow_html=True)
        auth_page()
    elif st.session_state.current_page == 'contact':
        st.markdown('<div class="nav-container"><nav><div class="logo" onclick="window.location.href=\'?action=home\'"><span class="logo-icon">⚡</span><span>Crptic AI</span></div><div class="nav-links"><span class="nav-link" onclick="window.location.href=\'?action=home\'">Home</span><span class="nav-link" onclick="window.location.href=\'?action=home#pricing\'">Pricing</span><span class="nav-link active">Contact</span><span class="nav-link" onclick="window.location.href=\'?action=auth\'">Login</span><button class="nav-cta" onclick="window.location.href=\'?action=auth\'">Sign Up</button></div></nav></div>', unsafe_allow_html=True)
        contact_page()
    else:
        st.markdown('<div class="nav-container"><nav><div class="logo" onclick="window.location.href=\'?action=home\'"><span class="logo-icon">⚡</span><span>Crptic AI</span></div><div class="nav-links"><span class="nav-link active" onclick="window.location.href=\'?action=home\'">Home</span><span class="nav-link" onclick="window.location.href=\'?action=home#pricing\'">Pricing</span><span class="nav-link" onclick="window.location.href=\'?action=contact\'">Contact</span><span class="nav-link" onclick="window.location.href=\'?action=auth\'">Login</span><button class="nav-cta" onclick="window.location.href=\'?action=auth\'">Sign Up</button></div></nav></div>', unsafe_allow_html=True)
        landing_page()
else:
    # Navigation for logged in users
    st.markdown(f'<div class="nav-container"><nav><div class="logo" onclick="window.location.href=\'?action=home\'"><span class="logo-icon">⚡</span><span>Crptic AI</span></div><div class="nav-links"><span class="nav-link" onclick="window.location.href=\'?action=home\'">Home</span><span class="nav-link" onclick="window.location.href=\'?action=home#pricing\'">Pricing</span><span class="nav-link" onclick="window.location.href=\'?action=contact\'">Contact</span><span class="nav-link active" onclick="window.location.href=\'?action=dashboard\'">Dashboard</span><span class="user-greeting">Hi, {st.session_state.user_name}</span></div></nav></div>', unsafe_allow_html=True)
    
    # Logout button (only visible when logged in)
    col_logout, _ = st.columns([1, 5])
    with col_logout:
        if st.button("Logout", key="logout"):
            for key in list(st.session_state.keys()):
                if key not in ['current_page', 'logged_in']:
                    del st.session_state[key]
            st.session_state.current_page = 'home'
            st.session_state.logged_in = False
            st.rerun()
    
    if st.session_state.current_page == 'dashboard':
        dashboard_page()
    elif st.session_state.current_page == 'contact':
        contact_page()
    else:
        st.session_state.current_page = 'dashboard'
        st.rerun()

# Footer
st.markdown('<div class="custom-footer"><p>&copy; 2025 Crptic AI. All rights reserved.</p><div class="footer-links"><span class="footer-link" onclick="window.location.href=\'?action=home\'">Privacy</span><span class="footer-link" onclick="window.location.href=\'?action=home\'">Terms</span><span class="footer-link" onclick="window.location.href=\'?action=contact\'">Contact</span></div></div>', unsafe_allow_html=True)
