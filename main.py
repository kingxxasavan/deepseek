# app.py - Main Streamlit app for travel login/signup/forgot password
# Run with: streamlit run app.py

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string

# Custom CSS for purple buttons (chose purple over black for a more vibrant, modern travel app feel)
st.markdown("""
<style>
div.stButton > button {
    background-color: #8B00FF;
    color: white;
    border-radius: 4px;
}
div.stButton > button:hover {
    background-color: #7D02CC;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Firebase Configuration
# Replace with your Firebase project details
# Download service account key from Firebase Console > Project Settings > Service Accounts > Generate new private key
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("path/to/your/serviceAccountKey.json")  # Update this path
        firebase_admin.initialize_app(cred)
    return firestore.client(), auth

# Email configuration (for forgot password) - Use your SMTP server (e.g., Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-sender@gmail.com"  # Update
SENDER_PASSWORD = "your-app-password"  # Use app password for Gmail

def send_verification_email(email, code):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    msg['Subject'] = "Password Reset Code"
    body = f"Your 5-digit verification code is: {code}"
    msg.attach(MimeText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, email, text)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Multi-page setup using st.tabs for simplicity (or use st_pages for separate files)
def main():
    st.set_page_config(page_title="Travel App Auth", page_icon="🌍", layout="centered")
    st.title("🌍 Personalized Travel Plans")
    
    tab1, tab2, tab3 = st.tabs(["Welcome Back!", "Create Your Account?", "Forgot Password?"])
    
    db, auth_client = init_firebase()
    
    with tab1:
        st.header("Sign In")
        email = st.text_input("Email address*", placeholder="example@gmail.com")
        password = st.text_input("Password*", type="password")
        remember_me = st.checkbox("Remember me")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Sign In", use_container_width=True):
                if email and password:
                    try:
                        user = auth_client.sign_in_with_email_and_password(email, password)
                        st.success("Signed in successfully!")
                        # Redirect or set session state
                        st.session_state.user = user
                    except Exception as e:
                        st.error(f"Sign in failed: {e}")
                else:
                    st.warning("Please fill in all fields.")
        
        with col2:
            st.markdown("---")
            if st.button("Continue with Google", use_container_width=True):
                st.info("Google OAuth integration placeholder - Implement with firebase_auth.")
            if st.button("Continue with Apple", use_container_width=True):
                st.info("Apple OAuth integration placeholder - Implement with firebase_auth.")
        
        st.markdown("[Forgot Password?](#tab3)")  # Link to tab
    
    with tab2:
        st.header("Create Your Account")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email address*", placeholder="example@gmail.com")
        password = st.text_input("Password*", type="password", help="At least 6 characters")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Register", use_container_width=True):
                if full_name and email and password:
                    try:
                        # Create user in Firebase Auth
                        user = auth_client.create_user_with_email_and_password(email, password)
                        # Save additional info to Firestore
                        user_doc = {
                            "full_name": full_name,
                            "email": email,
                            "created_at": datetime.now(),
                            "is_active": True
                        }
                        db.collection("users").document(user["localId"]).set(user_doc)
                        st.success("Account created successfully! Please sign in.")
                    except Exception as e:
                        st.error(f"Registration failed: {e}")
                else:
                    st.warning("Please fill in all fields.")
        
        with col2:
            st.markdown("---")
            if st.button("Continue with Google", use_container_width=True):
                st.info("Google OAuth integration placeholder.")
            if st.button("Continue with Apple", use_container_width=True):
                st.info("Apple OAuth integration placeholder.")
    
    with tab3:
        st.header("Forgot Password?")
        email = st.text_input("Email address*", placeholder="example@gmail.com")
        
        if st.button("Send Code", use_container_width=True):
            if email:
                # Generate 5-digit code
                code = ''.join(secrets.choice(string.digits) for _ in range(5))
                st.session_state.reset_code = code  # Store in session for verification
                st.session_state.reset_email = email
                
                if send_verification_email(email, code):
                    st.success("Verification code sent to your email!")
                    # Next step: Input code and new password
                    entered_code = st.text_input("Enter 5-digit code")
                    new_password = st.text_input("New Password", type="password")
                    
                    if st.button("Reset Password", use_container_width=True):
                        if entered_code == code and new_password:
                            try:
                                auth_client.reset_password(email, new_password)
                                st.success("Password reset successfully!")
                                del st.session_state.reset_code
                                del st.session_state.reset_email
                            except Exception as e:
                                st.error(f"Reset failed: {e}")
                        else:
                            st.warning("Invalid code or password.")
                else:
                    st.error("Failed to send code.")
            else:
                st.warning("Please enter your email.")

if __name__ == "__main__":
    main()
