import streamlit as st
from pathlib import Path

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Cryptic - AI Chat Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# ============================================================================
# CUSTOM CSS - MATCHING AUTH.PY DESIGN WITH LANDING PAGE ENHANCEMENTS
# ============================================================================
def load_css():
    st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling - Same gradient as auth */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        min-height: 100vh;
    }
    
    /* ============================================
       NAVIGATION BAR
       ============================================ */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: rgba(26, 26, 46, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px 50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .navbar-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .navbar-logo-icon {
        font-size: 36px;
    }
    
    .navbar-logo-text {
        background: linear-gradient(135deg, #4a9eff 0%, #6bb3ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .navbar-menu {
        display: flex;
        gap: 30px;
        align-items: center;
    }
    
    .nav-link {
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        position: relative;
        padding: 8px 0;
    }
    
    .nav-link:hover {
        color: #4a9eff;
    }
    
    .nav-link::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 0;
        height: 2px;
        background: linear-gradient(135deg, #4a9eff 0%, #6bb3ff 100%);
        transition: width 0.3s ease;
    }
    
    .nav-link:hover::after {
        width: 100%;
    }
    
    /* Navigation buttons */
    .nav-buttons {
        display: flex;
        gap: 15px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #4a9eff 0%, #3d7fd8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(74, 158, 255, 0.4) !important;
    }
    
    /* Secondary button style */
    .secondary-btn button {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .secondary-btn button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: #4a9eff !important;
    }
    
    /* ============================================
       HERO SECTION
       ============================================ */
    .hero-section {
        padding: 180px 50px 100px 50px;
        text-align: center;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .hero-title {
        font-size: 72px;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 25px;
        text-transform: uppercase;
        letter-spacing: 4px;
        line-height: 1.2;
        animation: fadeInUp 0.8s ease;
    }
    
    .hero-title-gradient {
        background: linear-gradient(135deg, #4a9eff 0%, #6bb3ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 24px;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 50px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
        animation: fadeInUp 0.8s ease 0.2s backwards;
    }
    
    .hero-cta {
        display: flex;
        gap: 20px;
        justify-content: center;
        margin-top: 50px;
        animation: fadeInUp 0.8s ease 0.4s backwards;
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
    
    /* ============================================
       FEATURES SECTION
       ============================================ */
    .features-section {
        padding: 100px 50px;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .section-title {
        font-size: 48px;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    .section-subtitle {
        font-size: 18px;
        color: rgba(255, 255, 255, 0.6);
        text-align: center;
        margin-bottom: 70px;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 40px;
        margin-top: 50px;
    }
    
    .feature-card {
        padding: 45px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.4s ease;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        border-color: rgba(74, 158, 255, 0.3);
        box-shadow: 0 15px 50px rgba(74, 158, 255, 0.3);
    }
    
    .feature-icon {
        font-size: 60px;
        margin-bottom: 25px;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }
    
    .feature-title {
        font-size: 26px;
        font-weight: 700;
        color: #4a9eff;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .feature-description {
        font-size: 16px;
        color: rgba(255, 255, 255, 0.7);
        line-height: 1.8;
    }
    
    /* ============================================
       WHY CHOOSE US SECTION
       ============================================ */
    .why-choose-section {
        padding: 100px 50px;
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .benefits-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 35px;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .benefit-card {
        padding: 35px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }
    
    .benefit-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(74, 158, 255, 0.2);
        transform: translateX(10px);
    }
    
    .benefit-number {
        font-size: 48px;
        font-weight: 800;
        color: #4a9eff;
        opacity: 0.3;
        margin-bottom: 15px;
    }
    
    .benefit-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
    }
    
    .benefit-text {
        font-size: 15px;
        color: rgba(255, 255, 255, 0.6);
        line-height: 1.7;
    }
    
    /* ============================================
       STATS SECTION
       ============================================ */
    .stats-section {
        padding: 80px 50px;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 40px;
    }
    
    .stat-card {
        text-align: center;
        padding: 30px;
        background: rgba(74, 158, 255, 0.05);
        border: 1px solid rgba(74, 158, 255, 0.2);
        border-radius: 15px;
        backdrop-filter: blur(5px);
    }
    
    .stat-number {
        font-size: 56px;
        font-weight: 900;
        color: #4a9eff;
        margin-bottom: 10px;
    }
    
    .stat-label {
        font-size: 18px;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* ============================================
       CTA SECTION
       ============================================ */
    .cta-section {
        padding: 100px 50px;
        text-align: center;
        background: linear-gradient(135deg, rgba(74, 158, 255, 0.1) 0%, rgba(107, 179, 255, 0.05) 100%);
        backdrop-filter: blur(10px);
    }
    
    .cta-title {
        font-size: 52px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 25px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .cta-text {
        font-size: 20px;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 50px;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .cta-buttons {
        display: flex;
        gap: 20px;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    /* ============================================
       FOOTER
       ============================================ */
    .footer {
        padding: 50px;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 50px;
    }
    
    .footer-text {
        color: rgba(255, 255, 255, 0.5);
        font-size: 14px;
        margin-bottom: 20px;
    }
    
    .footer-links {
        display: flex;
        gap: 30px;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 20px;
    }
    
    .footer-link {
        color: rgba(255, 255, 255, 0.6);
        text-decoration: none;
        font-size: 14px;
        transition: color 0.3s ease;
    }
    
    .footer-link:hover {
        color: #4a9eff;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .navbar {
            padding: 15px 20px;
            flex-direction: column;
            gap: 20px;
        }
        
        .navbar-menu {
            flex-direction: column;
            gap: 15px;
        }
        
        .hero-title {
            font-size: 42px;
        }
        
        .hero-subtitle {
            font-size: 18px;
        }
        
        .section-title {
            font-size: 36px;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .hero-cta, .cta-buttons {
            flex-direction: column;
            align-items: center;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# NAVIGATION BAR
# ============================================================================
def navigation_bar():
    # Create navbar
    st.markdown("""
        <div class="navbar">
            <div class="navbar-logo">
                <span class="navbar-logo-icon">🤖</span>
                <span class="navbar-logo-text">CRYPTIC</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons in columns (positioned in top right via CSS)
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
    
    with col3:
        if st.button("💳 Pricing", key="nav_pricing"):
            st.switch_page("pricing.py")
    
    with col4:
        if st.button("📧 Contact", key="nav_contact"):
            st.switch_page("contact.py")
    
    with col5:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.session_state.authenticated:
            if st.button("🚀 Dashboard", key="nav_dashboard"):
                st.switch_page("app.py")
        else:
            if st.button("🔐 Login", key="nav_login"):
                st.switch_page("auth.py")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        if not st.session_state.authenticated:
            if st.button("✨ Sign Up", key="nav_signup"):
                st.session_state.page = 'signup'
                st.switch_page("auth.py")

# ============================================================================
# HERO SECTION
# ============================================================================
def hero_section():
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">
                WELCOME TO <span class="hero-title-gradient">CRYPTIC</span>
            </h1>
            <p class="hero-subtitle">
                The Next Generation AI Chat Bot Platform. Unlock limitless conversations 
                with cutting-edge artificial intelligence technology. Experience the future of 
                communication today.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        cta_col1, cta_col2 = st.columns(2)
        with cta_col1:
            if st.button("🚀 Get Started Free", key="hero_cta_start", use_container_width=True):
                st.session_state.page = 'signup'
                st.switch_page("auth.py")
        with cta_col2:
            st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
            if st.button("📖 Learn More", key="hero_cta_learn", use_container_width=True):
                st.markdown('<script>document.querySelector(".features-section").scrollIntoView({behavior: "smooth"});</script>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FEATURES SECTION
# ============================================================================
def features_section():
    st.markdown("""
        <div class="features-section">
            <h2 class="section-title">Powerful Features</h2>
            <p class="section-subtitle">
                Experience the most advanced AI chat technology with features designed 
                to revolutionize your communication
            </p>
            
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🧠</div>
                    <h3 class="feature-title">Advanced AI</h3>
                    <p class="feature-description">
                        Powered by state-of-the-art language models that understand context, 
                        nuance, and deliver human-like conversations with unprecedented accuracy.
                    </p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3 class="feature-title">Lightning Fast</h3>
                    <p class="feature-description">
                        Get instant responses with our optimized infrastructure. No waiting, 
                        no delays - just seamless real-time conversations at the speed of thought.
                    </p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3 class="feature-title">Secure & Private</h3>
                    <p class="feature-description">
                        Your data is protected with enterprise-grade encryption. We prioritize 
                        your privacy and never share your conversations with third parties.
                    </p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🎨</div>
                    <h3 class="feature-title">Customizable</h3>
                    <p class="feature-description">
                        Tailor the AI to your specific needs. From tone and style to specialized 
                        knowledge domains, make it truly yours.
                    </p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🌐</div>
                    <h3 class="feature-title">Multi-Platform</h3>
                    <p class="feature-description">
                        Access Cryptic anywhere, anytime. Seamlessly sync across all your devices 
                        with our cloud-based platform.
                    </p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">💎</div>
                    <h3 class="feature-title">Premium Quality</h3>
                    <p class="feature-description">
                        Experience the highest quality AI responses with advanced reasoning, 
                        creative thinking, and problem-solving capabilities.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# WHY CHOOSE US SECTION
# ============================================================================
def why_choose_section():
    st.markdown("""
        <div class="why-choose-section">
            <h2 class="section-title">Why Choose Cryptic?</h2>
            <p class="section-subtitle">
                We're not just another AI chat bot. We're your intelligent partner 
                in productivity, creativity, and innovation.
            </p>
            
            <div class="benefits-grid">
                <div class="benefit-card">
                    <div class="benefit-number">01</div>
                    <h3 class="benefit-title">Cutting-Edge Technology</h3>
                    <p class="benefit-text">
                        Built on the latest AI breakthroughs, continuously updated to deliver 
                        the best performance and most accurate responses.
                    </p>
                </div>
                
                <div class="benefit-card">
                    <div class="benefit-number">02</div>
                    <h3 class="benefit-title">24/7 Availability</h3>
                    <p class="benefit-text">
                        Never wait for support. Cryptic is always ready to assist you, 
                        day or night, across all time zones.
                    </p>
                </div>
                
                <div class="benefit-card">
                    <div class="benefit-number">03</div>
                    <h3 class="benefit-title">Continuous Learning</h3>
                    <p class="benefit-text">
                        Our AI evolves with every interaction, getting smarter and more 
                        personalized to your needs over time.
                    </p>
                </div>
                
                <div class="benefit-card">
                    <div class="benefit-number">04</div>
                    <h3 class="benefit-title">Affordable Plans</h3>
                    <p class="benefit-text">
                        Premium AI technology at a fraction of the cost. Flexible pricing 
                        that scales with your needs.
                    </p>
                </div>
                
                <div class="benefit-card">
                    <div class="benefit-number">05</div>
                    <h3 class="benefit-title">Expert Support</h3>
                    <p class="benefit-text">
                        Our dedicated team is here to help you get the most out of Cryptic 
                        with responsive, knowledgeable support.
                    </p>
                </div>
                
                <div class="benefit-card">
                    <div class="benefit-number">06</div>
                    <h3 class="benefit-title">No Commitment</h3>
                    <p class="benefit-text">
                        Try Cryptic risk-free. Cancel anytime with no hidden fees or 
                        long-term contracts required.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# STATS SECTION
# ============================================================================
def stats_section():
    st.markdown("""
        <div class="stats-section">
            <h2 class="section-title">Trusted by Thousands</h2>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">50K+</div>
                    <div class="stat-label">Active Users</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-number">1M+</div>
                    <div class="stat-label">Conversations</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-number">99.9%</div>
                    <div class="stat-label">Uptime</div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-number">4.9★</div>
                    <div class="stat-label">User Rating</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FINAL CTA SECTION
# ============================================================================
def cta_section():
    st.markdown("""
        <div class="cta-section">
            <h2 class="cta-title">Ready to Transform Your Workflow?</h2>
            <p class="cta-text">
                Join thousands of users who are already experiencing the future of AI communication. 
                Start your journey with Cryptic today - no credit card required.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        cta_btn_col1, cta_btn_col2, cta_btn_col3 = st.columns(3)
        with cta_btn_col1:
            if st.button("🚀 Start Free Trial", key="cta_trial", use_container_width=True):
                st.session_state.page = 'signup'
                st.switch_page("auth.py")
        with cta_btn_col2:
            if st.button("💳 View Pricing", key="cta_pricing", use_container_width=True):
                st.switch_page("pricing.py")
        with cta_btn_col3:
            st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
            if st.button("📧 Contact Sales", key="cta_contact", use_container_width=True):
                st.switch_page("contact.py")
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
def footer():
    st.markdown("""
        <div class="footer">
            <p class="footer-text">
                © 2025 Cryptic AI. All rights reserved.
            </p>
            <div class="footer-links">
                <a href="#" class="footer-link">Privacy Policy</a>
                <a href="#" class="footer-link">Terms of Service</a>
                <a href="#" class="footer-link">Documentation</a>
                <a href="#" class="footer-link">API</a>
                <a href="#" class="footer-link">Blog</a>
            </div>
            <p class="footer-text" style="margin-top: 20px; font-size: 12px;">
                🤖 Powered by Advanced AI Technology
            </p>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN LANDING PAGE
# ============================================================================
def main():
    load_css()
    navigation_bar()
    hero_section()
    features_section()
    why_choose_section()
    stats_section()
    cta_section()
    footer()

if __name__ == "__main__":
    main()
