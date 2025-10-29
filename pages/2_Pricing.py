import streamlit as st

st.set_page_config(
    page_title="Pricing - CrypticX",
    page_icon="💰",
    layout="wide"
)

def pricing_page():
    st.title("💰 Pricing Plans")
    
    # Navigation
    col1, col2, col3, col4 = st.columns([2,1,1,1])
    with col1:
        st.markdown("### 🧠 CrypticX Pricing")
    with col2:
        if st.button("🏠 Home"):
            st.switch_page("main.py")
    with col3:
        if st.button("📊 Dashboard"):
            st.switch_page("pages/1_Dashboard.py")
    with col4:
        if st.button("📞 Contact"):
            st.switch_page("pages/3_Contact.py")
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem;'>
        <h2>Choose Your Perfect Plan</h2>
        <p style='color: #a0aec0; font-size: 1.2rem;'>Flexible pricing for every student's needs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Pricing Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='
            background: rgba(42, 49, 62, 0.7);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #2d3746;
            text-align: center;
            height: 100%;
        '>
            <h3 style='color: #00d4ff;'>Free</h3>
            <h1 style='color: white;'>$0</h1>
            <p style='color: #a0aec0;'>/month</p>
            <ul style='text-align: left; color: #a0aec0; margin: 2rem 0;'>
                <li>Basic AI Tutor Access</li>
                <li>3 Study Subjects</li>
                <li>5 Quizzes per Month</li>
                <li>Community Support</li>
            </ul>
            <button style='
                background: #2d3746;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 20px;
                width: 100%;
                cursor: pointer;
            '>Get Started</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(0,212,255,0.1) 0%, rgba(42,49,62,0.8) 100%);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #00d4ff;
            text-align: center;
            height: 100%;
            transform: scale(1.05);
        '>
            <div style='background: #00d4ff; color: black; padding: 0.5rem; border-radius: 5px; margin: -2rem -2rem 1rem -2rem;'>
                <strong>MOST POPULAR</strong>
            </div>
            <h3 style='color: #00d4ff;'>Pro Student</h3>
            <h1 style='color: white;'>$19.99</h1>
            <p style='color: #a0aec0;'>/month</p>
            <ul style='text-align: left; color: #a0aec0; margin: 2rem 0;'>
                <li>Full AI Tutor Access</li>
                <li>Unlimited Subjects</li>
                <li>Unlimited Quizzes</li>
                <li>Advanced Analytics</li>
                <li>Priority Support</li>
                <li>Exam Preparation Tools</li>
            </ul>
            <button style='
                background: linear-gradient(45deg, #00d4ff, #0099cc);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 20px;
                width: 100%;
                cursor: pointer;
            '>Start Free Trial</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='
            background: rgba(42, 49, 62, 0.7);
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #2d3746;
            text-align: center;
            height: 100%;
        '>
            <h3 style='color: #00d4ff;'>Institution</h3>
            <h1 style='color: white;'>Custom</h1>
            <p style='color: #a0aec0;'>/year</p>
            <ul style='text-align: left; color: #a0aec0; margin: 2rem 0;'>
                <li>Everything in Pro</li>
                <li>Multi-User Management</li>
                <li>Custom Integration</li>
                <li>Dedicated Support</li>
                <li>Progress Reporting</li>
                <li>API Access</li>
            </ul>
            <button style='
                background: #2d3746;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 20px;
                width: 100%;
                cursor: pointer;
            '>Contact Sales</button>
        </div>
        """, unsafe_allow_html=True)
    
    # FAQ Section
    st.markdown("## ❓ Frequently Asked Questions")
    
    faqs = [
        {"question": "Can I change plans anytime?", "answer": "Yes, you can upgrade or downgrade your plan at any time."},
        {"question": "Is there a student discount?", "answer": "All our plans are already student-friendly priced!"},
        {"question": "What payment methods do you accept?", "answer": "We accept all major credit cards, PayPal, and bank transfers."},
        {"question": "Can I get a refund?", "answer": "We offer a 14-day money-back guarantee for all paid plans."}
    ]
    
    for faq in faqs:
        with st.expander(faq["question"]):
            st.write(faq["answer"])

if __name__ == "__main__":
    pricing_page()
