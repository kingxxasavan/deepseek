import streamlit as st

st.set_page_config(
    page_title="Login - CrypticX",
    page_icon="🔐",
    layout="centered"
)

def auth_page():
    # Custom CSS for auth pages
    st.markdown("""
    <style>
        .main {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .auth-container {
            background: rgba(42, 49, 62, 0.8);
            padding: 3rem;
            border-radius: 15px;
            border: 1px solid #2d3746;
            width: 100%;
            max-width: 450px;
            backdrop-filter: blur(10px);
        }
        .tab-content {
            margin-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #00d4ff;'>🧠 CrypticX</h1>
        <p style='color: #a0aec0;'>Your AI Study Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for Login/Signup
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            st.markdown("### Welcome Back!")
            
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                remember = st.checkbox("Remember me")
            with col2:
                st.markdown("[Forgot password?](#)")
            
            login_button = st.form_submit_button("Login", use_container_width=True)
            
            if login_button:
                if email and password:
                    st.success("Login successful! Redirecting...")
                    st.switch_page("pages/1_Dashboard.py")
                else:
                    st.error("Please fill in all fields.")
    
    with tab2:
        with st.form("signup_form"):
            st.markdown("### Create Your Account")
            
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name")
            with col2:
                last_name = st.text_input("Last Name")
            
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            user_type = st.selectbox("I am a...", ["Student", "Teacher", "Parent", "Institution"])
            
            agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            signup_button = st.form_submit_button("Create Account", use_container_width=True)
            
            if signup_button:
                if not all([first_name, last_name, email, password, confirm_password]):
                    st.error("Please fill in all fields.")
                elif password != confirm_password:
                    st.error("Passwords don't match!")
                elif not agree_terms:
                    st.error("Please agree to the terms and conditions.")
                else:
                    st.success("Account created successfully! Welcome to CrypticX!")
                    st.switch_page("pages/1_Dashboard.py")
    
    # Back to home
    st.markdown("""
    <div style='text-align: center; margin-top: 2rem;'>
        <a href='#' onclick='window.history.back()' style='color: #00d4ff; text-decoration: none;'>← Back to Home</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    auth_page()
