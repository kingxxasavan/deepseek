import streamlit as st
import stripe
import json
from pathlib import Path

# ============================================================================
# STRIPE CONFIGURATION - Using Streamlit Secrets
# ============================================================================
# Access keys from st.secrets (stored in .streamlit/secrets.toml)
try:
    stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]
    STRIPE_PUBLISHABLE_KEY = st.secrets["STRIPE_PUBLISHABLE_KEY"]
    
    # Stripe Price IDs for each plan
    PRICE_IDS = {
        "starter": st.secrets.get("STRIPE_PRICE_STARTER", "price_starter_id"),
        "professional": st.secrets.get("STRIPE_PRICE_PRO", "price_pro_id"),
        "enterprise": st.secrets.get("STRIPE_PRICE_ENTERPRISE", "price_enterprise_id")
    }
except Exception as e:
    st.error("⚠️ Stripe configuration missing. Please set up your secrets.toml file.")
    STRIPE_PUBLISHABLE_KEY = None
    PRICE_IDS = {}

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Pricing Plans - AI Chat Bot",
    page_icon="💳",
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
# CUSTOM CSS - MATCHING AUTH.PY DESIGN
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
    
    /* Page title */
    .pricing-header {
        text-align: center;
        padding: 60px 20px 40px 20px;
    }
    
    .pricing-title {
        font-size: 52px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 3px;
        background: linear-gradient(135deg, #4a9eff 0%, #6bb3ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .pricing-subtitle {
        font-size: 18px;
        color: rgba(255, 255, 255, 0.6);
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Pricing cards container */
    .pricing-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        padding: 40px 20px;
        flex-wrap: wrap;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Individual pricing card - Matching auth container style */
    .pricing-card {
        width: 380px;
        padding: 40px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .pricing-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 50px rgba(74, 158, 255, 0.3);
        border-color: rgba(74, 158, 255, 0.3);
    }
    
    /* Popular badge */
    .popular-badge {
        position: absolute;
        top: 20px;
        right: -35px;
        background: linear-gradient(135deg, #4a9eff 0%, #3d7fd8 100%);
        color: white;
        padding: 8px 45px;
        transform: rotate(45deg);
        font-size: 12px;
        font-weight: 700;
        text-align: center;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(74, 158, 255, 0.4);
    }
    
    /* Plan icon */
    .plan-icon {
        font-size: 50px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Plan name */
    .plan-name {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Plan description */
    .plan-description {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.5);
        text-align: center;
        margin-bottom: 30px;
        line-height: 1.5;
    }
    
    /* Price */
    .price-container {
        text-align: center;
        margin: 30px 0;
        padding: 20px 0;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .price {
        font-size: 56px;
        font-weight: 800;
        color: #4a9eff;
        line-height: 1;
    }
    
    .price-currency {
        font-size: 28px;
        vertical-align: super;
    }
    
    .price-period {
        font-size: 16px;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 5px;
    }
    
    /* Features list */
    .features-list {
        margin: 30px 0;
        padding: 0;
        list-style: none;
    }
    
    .feature-item {
        padding: 12px 0;
        color: rgba(255, 255, 255, 0.8);
        font-size: 15px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .feature-item:last-child {
        border-bottom: none;
    }
    
    .feature-icon {
        color: #4a9eff;
        margin-right: 12px;
        font-size: 18px;
        font-weight: bold;
    }
    
    .feature-icon-disabled {
        color: rgba(255, 255, 255, 0.2);
        margin-right: 12px;
        font-size: 18px;
    }
    
    /* Button styling - Matching auth button */
    .stButton > button {
        background: linear-gradient(135deg, #4a9eff 0%, #3d7fd8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 18px 30px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        margin-top: 25px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(74, 158, 255, 0.4) !important;
    }
    
    /* Back button */
    .back-button {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
    }
    
    .back-button button {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 12px 24px !important;
        width: auto !important;
    }
    
    .back-button button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: #4a9eff !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background: rgba(74, 158, 255, 0.1) !important;
        border: 1px solid rgba(74, 158, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #6bb3ff !important;
    }
    
    /* Info box */
    .info-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 30px;
        margin: 40px auto;
        max-width: 800px;
        text-align: center;
    }
    
    .info-title {
        font-size: 24px;
        font-weight: 700;
        color: #4a9eff;
        margin-bottom: 15px;
    }
    
    .info-text {
        color: rgba(255, 255, 255, 0.7);
        line-height: 1.6;
        font-size: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# STRIPE CHECKOUT SESSION CREATION
# ============================================================================
def create_checkout_session(price_id, plan_name):
    """Create a Stripe Checkout session"""
    try:
        # Get current user info
        username = st.session_state.get('username', 'guest')
        
        # Create checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=st.secrets.get("STRIPE_SUCCESS_URL", "https://yourdomain.com/success"),
            cancel_url=st.secrets.get("STRIPE_CANCEL_URL", "https://yourdomain.com/cancel"),
            client_reference_id=username,
            customer_email=None,  # Can be populated if you have user email
            metadata={
                'username': username,
                'plan': plan_name
            }
        )
        return checkout_session.url
    except Exception as e:
        st.error(f"Error creating checkout session: {str(e)}")
        return None

# ============================================================================
# SAVE SUBSCRIPTION INFO
# ============================================================================
def save_subscription(username, plan, session_id):
    """Save subscription information locally"""
    subscriptions_file = Path("subscriptions.json")
    
    if subscriptions_file.exists():
        with open(subscriptions_file, 'r') as f:
            subscriptions = json.load(f)
    else:
        subscriptions = {}
    
    subscriptions[username] = {
        'plan': plan,
        'session_id': session_id,
        'timestamp': str(datetime.now())
    }
    
    with open(subscriptions_file, 'w') as f:
        json.dump(subscriptions, f)

# ============================================================================
# PRICING PAGE UI
# ============================================================================
def pricing_page():
    load_css()
    
    # Back button (if coming from main app)
    if st.session_state.authenticated:
        st.markdown('<div class="back-button">', unsafe_allow_html=True)
        if st.button("← Back to App"):
            st.switch_page("app.py")  # Change to your main app page
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="pricing-header">
            <div class="pricing-title">🚀 Choose Your Plan</div>
            <div class="pricing-subtitle">
                Unlock the full potential of AI-powered conversations with our flexible pricing plans
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Pricing cards
    col1, col2, col3 = st.columns(3)
    
    # ========== STARTER PLAN ==========
    with col1:
        st.markdown("""
            <div class="pricing-card">
                <div class="plan-icon">🌱</div>
                <div class="plan-name">Starter</div>
                <div class="plan-description">Perfect for individuals getting started</div>
                
                <div class="price-container">
                    <div class="price">
                        <span class="price-currency">$</span>9
                    </div>
                    <div class="price-period">per month</div>
                </div>
                
                <ul class="features-list">
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        100 AI conversations/month
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        Basic AI models
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        Email support
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        Standard response time
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon-disabled">✗</span>
                        Advanced analytics
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon-disabled">✗</span>
                        Priority support
                    </li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Get Started", key="starter", use_container_width=True):
            if PRICE_IDS.get("starter"):
                checkout_url = create_checkout_session(PRICE_IDS["starter"], "Starter")
                if checkout_url:
                    st.markdown(f'<meta http-equiv="refresh" content="0;url={checkout_url}">', unsafe_allow_html=True)
                    st.success("Redirecting to checkout...")
            else:
                st.error("Stripe configuration incomplete")
    
    # ========== PROFESSIONAL PLAN ==========
    with col2:
        st.markdown("""
            <div class="pricing-card">
                <div class="popular-badge">POPULAR</div>
                <div class="plan-icon">⚡</div>
                <div class="plan-name">Professional</div>
                <div class="plan-description">Best for professionals and power users</div>
                
                <div class="price-container">
                    <div class="price">
                        <span class="price-currency">$</span>29
                    </div>
                    <div class="price-period">per month</div>
                </div>
                
                <ul class="features-list">
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        Unlimited conversations
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        Advanced AI models
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        Priority email support
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        Faster response time
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        Advanced analytics
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        API access
                    </li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Get Professional", key="professional", use_container_width=True):
            if PRICE_IDS.get("professional"):
                checkout_url = create_checkout_session(PRICE_IDS["professional"], "Professional")
                if checkout_url:
                    st.markdown(f'<meta http-equiv="refresh" content="0;url={checkout_url}">', unsafe_allow_html=True)
                    st.success("Redirecting to checkout...")
            else:
                st.error("Stripe configuration incomplete")
    
    # ========== ENTERPRISE PLAN ==========
    with col3:
        st.markdown("""
            <div class="pricing-card">
                <div class="plan-icon">🏢</div>
                <div class="plan-name">Enterprise</div>
                <div class="plan-description">For teams and organizations</div>
                
                <div class="price-container">
                    <div class="price">
                        <span class="price-currency">$</span>99
                    </div>
                    <div class="price-period">per month</div>
                </div>
                
                <ul class="features-list">
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        Everything in Professional
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        Multi-user accounts
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        24/7 dedicated support
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        Custom AI training
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        Custom integrations
                    </li>
                    <li class="feature-item">
                        <span class="feature-icon">✓</span>
                        SLA guarantee
                    </li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Get Enterprise", key="enterprise", use_container_width=True):
            if PRICE_IDS.get("enterprise"):
                checkout_url = create_checkout_session(PRICE_IDS["enterprise"], "Enterprise")
                if checkout_url:
                    st.markdown(f'<meta http-equiv="refresh" content="0;url={checkout_url}">', unsafe_allow_html=True)
                    st.success("Redirecting to checkout...")
            else:
                st.error("Stripe configuration incomplete")
    
    # Info box
    st.markdown("""
        <div class="info-box">
            <div class="info-title">💳 Secure Payment Processing</div>
            <div class="info-text">
                All payments are processed securely through Stripe. We never store your payment information.<br>
                Cancel anytime with no hidden fees or commitments.
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN FUNCTION
# ============================================================================
def main():
    pricing_page()

if __name__ == "__main__":
    main()
