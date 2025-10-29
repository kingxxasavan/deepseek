import streamlit as st

st.set_page_config(
    page_title="Contact - CrypticX",
    page_icon="📞",
    layout="wide"
)

def contact_page():
    st.title("📞 Contact Us")
    
    # Navigation
    col1, col2, col3, col4 = st.columns([2,1,1,1])
    with col1:
        st.markdown("### 🧠 CrypticX Contact")
    with col2:
        if st.button("🏠 Home"):
            st.switch_page("main.py")
    with col3:
        if st.button("📊 Dashboard"):
            st.switch_page("pages/1_Dashboard.py")
    with col4:
        if st.button("💰 Pricing"):
            st.switch_page("pages/2_Pricing.py")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='
            background: rgba(42, 49, 62, 0.7);
            padding: 2rem;
            border-radius: 15px;
            border: 1px solid #2d3746;
            margin-bottom: 2rem;
        '>
            <h3 style='color: #00d4ff;'>Get in Touch</h3>
            <p style='color: #a0aec0;'>We'd love to hear from you! Send us a message and we'll respond as soon as possible.</p>
            
            <div style='margin: 1.5rem 0;'>
                <h4 style='color: #00d4ff;'>📧 Email</h4>
                <p style='color: #a0aec0;'>support@crypticx.com</p>
            </div>
            
            <div style='margin: 1.5rem 0;'>
                <h4 style='color: #00d4ff;'>📞 Phone</h4>
                <p style='color: #a0aec0;'>+1 (555) 123-LEARN</p>
            </div>
            
            <div style='margin: 1.5rem 0;'>
                <h4 style='color: #00d4ff;'>📍 Address</h4>
                <p style='color: #a0aec0;'>123 Education Street<br>Tech City, TC 12345</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.form("contact_form"):
            st.markdown("### Send us a Message")
            
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name*")
            with col2:
                last_name = st.text_input("Last Name*")
            
            email = st.text_input("Email Address*")
            subject = st.selectbox("Subject*", 
                                 ["General Inquiry", "Technical Support", "Billing", "Partnership", "Other"])
            
            message = st.text_area("Message*", height=150)
            
            submitted = st.form_submit_button("Send Message", use_container_width=True)
            
            if submitted:
                if first_name and last_name and email and message:
                    st.success("🎉 Thank you for your message! We'll get back to you within 24 hours.")
                else:
                    st.error("Please fill in all required fields (*).")
    
    # Social Media & Additional Info
    st.markdown("""
    <div style='
        background: rgba(42, 49, 62, 0.5);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #2d3746;
        text-align: center;
        margin-top: 2rem;
    '>
        <h3 style='color: #00d4ff;'>Follow Us</h3>
        <div style='display: flex; justify-content: center; gap: 2rem; margin: 1rem 0;'>
            <span style='color: #a0aec0;'>📘 Facebook</span>
            <span style='color: #a0aec0;'>🐦 Twitter</span>
            <span style='color: #a0aec0;'>📸 Instagram</span>
            <span style='color: #a0aec0;'>💼 LinkedIn</span>
        </div>
        
        <div style='margin-top: 2rem;'>
            <h4 style='color: #00d4ff;'>🕒 Support Hours</h4>
            <p style='color: #a0aec0;'>Monday - Friday: 9:00 AM - 6:00 PM EST<br>Weekend: Emergency support only</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    contact_page()
