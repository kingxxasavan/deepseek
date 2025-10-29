import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
from pathlib import Path

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Contact Us - AI Chat Bot",
    page_icon="📧",
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
# EMAIL CONFIGURATION - Using Streamlit Secrets
# ============================================================================
try:
    # SMTP Configuration
    SMTP_SERVER = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = st.secrets.get("SMTP_PORT", 587)
    SMTP_EMAIL = st.secrets["SMTP_EMAIL"]  # Your sending email
    SMTP_PASSWORD = st.secrets["SMTP_PASSWORD"]  # App password or email password
    BUSINESS_EMAIL = st.secrets["BUSINESS_EMAIL"]  # Where you receive messages
except Exception as e:
    st.error("⚠️ Email configuration missing. Please set up your secrets.toml file.")
    SMTP_EMAIL = None
    BUSINESS_EMAIL = None

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
    
    /* Page header */
    .contact-header {
        text-align: center;
        padding: 60px 20px 40px 20px;
    }
    
    .contact-title {
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
    
    .contact-subtitle {
        font-size: 18px;
        color: rgba(255, 255, 255, 0.6);
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Contact container - Matching auth container */
    .contact-container {
        max-width: 700px;
        margin: 50px auto;
        padding: 50px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Form icon */
    .form-icon {
        text-align: center;
        font-size: 60px;
        margin-bottom: 30px;
    }
    
    /* Input styling - Matching auth inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 15px !important;
        font-size: 16px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #4a9eff !important;
        box-shadow: 0 0 20px rgba(74, 158, 255, 0.3) !important;
    }
    
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label {
        color: rgba(255, 255, 255, 0.8) !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
    }
    
    /* Textarea specific */
    .stTextArea > div > div > textarea {
        min-height: 150px !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #4a9eff !important;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
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
    
    /* Success/Error messages - Matching auth */
    .stSuccess {
        background: rgba(74, 158, 255, 0.1) !important;
        border: 1px solid rgba(74, 158, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #6bb3ff !important;
        padding: 20px !important;
    }
    
    .stError {
        background: rgba(255, 74, 74, 0.1) !important;
        border: 1px solid rgba(255, 74, 74, 0.3) !important;
        border-radius: 12px !important;
        color: #ff6b6b !important;
        padding: 20px !important;
    }
    
    /* Info boxes */
    .info-cards {
        display: flex;
        gap: 20px;
        margin: 50px auto;
        max-width: 1200px;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .info-card {
        flex: 1;
        min-width: 280px;
        padding: 30px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        border-color: rgba(74, 158, 255, 0.3);
        box-shadow: 0 10px 30px rgba(74, 158, 255, 0.2);
    }
    
    .info-card-icon {
        font-size: 40px;
        margin-bottom: 15px;
    }
    
    .info-card-title {
        font-size: 20px;
        font-weight: 700;
        color: #4a9eff;
        margin-bottom: 10px;
    }
    
    .info-card-text {
        color: rgba(255, 255, 255, 0.7);
        font-size: 14px;
        line-height: 1.6;
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
    
    /* Character counter */
    .char-counter {
        text-align: right;
        color: rgba(255, 255, 255, 0.4);
        font-size: 12px;
        margin-top: -15px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# EMAIL SENDING FUNCTION
# ============================================================================
def send_email(name, email, subject, message, issue_type):
    """Send email using SMTP"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = SMTP_EMAIL
        msg['To'] = BUSINESS_EMAIL
        msg['Subject'] = f"[{issue_type}] {subject}"
        
        # Create email body
        email_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #4a9eff; border-bottom: 3px solid #4a9eff; padding-bottom: 10px;">New Contact Form Submission</h2>
                    
                    <div style="margin: 20px 0;">
                        <p style="margin: 10px 0;"><strong style="color: #333;">Issue Type:</strong> <span style="background: #4a9eff; color: white; padding: 4px 12px; border-radius: 5px; font-size: 12px;">{issue_type}</span></p>
                        <p style="margin: 10px 0;"><strong style="color: #333;">Name:</strong> {name}</p>
                        <p style="margin: 10px 0;"><strong style="color: #333;">Email:</strong> <a href="mailto:{email}" style="color: #4a9eff;">{email}</a></p>
                        <p style="margin: 10px 0;"><strong style="color: #333;">Subject:</strong> {subject}</p>
                    </div>
                    
                    <div style="background: #f9f9f9; border-left: 4px solid #4a9eff; padding: 15px; margin: 20px 0; border-radius: 5px;">
                        <h3 style="color: #333; margin-top: 0;">Message:</h3>
                        <p style="color: #555; line-height: 1.6; white-space: pre-wrap;">{message}</p>
                    </div>
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #888; font-size: 12px;">
                        <p>Sent from: AI Chat Bot Contact Form</p>
                        <p>Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Attach HTML body
        msg.attach(MIMEText(email_body, 'html'))
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        
        # Save to local file as backup
        save_contact_submission(name, email, subject, message, issue_type)
        
        return True
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False

# ============================================================================
# SAVE CONTACT SUBMISSIONS LOCALLY
# ============================================================================
def save_contact_submission(name, email, subject, message, issue_type):
    """Save contact form submissions to local JSON file"""
    contacts_file = Path("contacts.json")
    
    if contacts_file.exists():
        with open(contacts_file, 'r') as f:
            contacts = json.load(f)
    else:
        contacts = []
    
    submission = {
        'timestamp': str(datetime.now()),
        'name': name,
        'email': email,
        'subject': subject,
        'message': message,
        'issue_type': issue_type,
        'username': st.session_state.get('username', 'guest')
    }
    
    contacts.append(submission)
    
    with open(contacts_file, 'w') as f:
        json.dump(contacts, f, indent=2)

# ============================================================================
# CONTACT PAGE UI
# ============================================================================
def contact_page():
    load_css()
    
    # Back button (if coming from main app)
    if st.session_state.authenticated:
        st.markdown('<div class="back-button">', unsafe_allow_html=True)
        if st.button("← Back to App"):
            st.switch_page("app.py")  # Change to your main app page
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="contact-header">
            <div class="contact-title">📧 Contact Us</div>
            <div class="contact-subtitle">
                Have questions or issues? We're here to help. Send us a message and we'll get back to you as soon as possible.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Info cards
    st.markdown("""
        <div class="info-cards">
            <div class="info-card">
                <div class="info-card-icon">⚡</div>
                <div class="info-card-title">Fast Response</div>
                <div class="info-card-text">We typically respond within 24 hours during business days</div>
            </div>
            <div class="info-card">
                <div class="info-card-icon">🔒</div>
                <div class="info-card-title">Secure & Private</div>
                <div class="info-card-text">Your information is kept confidential and secure</div>
            </div>
            <div class="info-card">
                <div class="info-card-icon">💬</div>
                <div class="info-card-title">Dedicated Support</div>
                <div class="info-card-text">Our team is committed to helping you succeed</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Contact form container
    st.markdown('<div class="contact-container">', unsafe_allow_html=True)
    
    # Form icon
    st.markdown("""
        <div class="form-icon">✉️</div>
    """, unsafe_allow_html=True)
    
    # Contact form
    with st.form("contact_form", clear_on_submit=True):
        # Name and Email in columns
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Your Name *",
                placeholder="John Doe",
                help="Enter your full name"
            )
        
        with col2:
            email = st.text_input(
                "Your Email *",
                placeholder="john@example.com",
                help="We'll use this to respond to you"
            )
        
        # Issue type
        issue_type = st.selectbox(
            "Issue Type *",
            [
                "General Inquiry",
                "Technical Support",
                "Billing Question",
                "Feature Request",
                "Bug Report",
                "Account Issue",
                "Partnership/Business",
                "Other"
            ],
            help="Select the category that best describes your inquiry"
        )
        
        # Subject
        subject = st.text_input(
            "Subject *",
            placeholder="Brief description of your issue",
            help="A short summary of your message"
        )
        
        # Message
        message = st.text_area(
            "Message *",
            placeholder="Please describe your issue or question in detail...",
            help="Provide as much detail as possible to help us assist you better",
            max_chars=2000
        )
        
        # Character counter
        if message:
            char_count = len(message)
            st.markdown(f'<div class="char-counter">{char_count}/2000 characters</div>', unsafe_allow_html=True)
        
        # Submit button
        submit = st.form_submit_button("📤 Send Message")
        
        if submit:
            # Validation
            if not name or not email or not subject or not message:
                st.error("❌ Please fill in all required fields")
            elif "@" not in email or "." not in email:
                st.error("❌ Please enter a valid email address")
            elif len(message) < 10:
                st.error("❌ Message must be at least 10 characters long")
            else:
                # Send email
                if SMTP_EMAIL and BUSINESS_EMAIL:
                    with st.spinner("Sending your message..."):
                        if send_email(name, email, subject, message, issue_type):
                            st.success("✅ Message sent successfully! We'll get back to you soon.")
                            st.balloons()
                        else:
                            st.error("❌ Failed to send message. Please try again or email us directly.")
                else:
                    # Save locally even if email config is missing
                    save_contact_submission(name, email, subject, message, issue_type)
                    st.warning("⚠️ Email configuration incomplete. Your message has been saved locally.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional contact info
    st.markdown("""
        <div style="text-align: center; margin-top: 50px; color: rgba(255,255,255,0.6);">
            <p style="font-size: 16px; margin-bottom: 10px;">
                <strong style="color: #4a9eff;">Alternative Contact Methods:</strong>
            </p>
            <p style="font-size: 14px;">
                📧 Email: <a href="mailto:support@example.com" style="color: #4a9eff; text-decoration: none;">support@example.com</a><br>
                💼 Business Inquiries: <a href="mailto:business@example.com" style="color: #4a9eff; text-decoration: none;">business@example.com</a>
            </p>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN FUNCTION
# ============================================================================
def main():
    contact_page()

if __name__ == "__main__":
    main()
