import streamlit as st
import google.generativeai as genai
from datetime import datetime
import json
import os

# Page config
st.set_page_config(
    page_title="CrypticX Dashboard - AI Study Tool",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start collapsed for sliding effect
)

# Custom CSS for transparent blue background and sliding sidebar
st.markdown("""
    <style>
    /* Transparent blue background */
    .main .block-container {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 2rem;
    }
    
    /* Sliding sidebar animation */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(30, 58, 138, 0.1) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(59, 130, 246, 0.3);
        animation: slideIn 0.3s ease-out;
        overflow-y: auto;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }
    
    /* Hover effect for sidebar */
    section[data-testid="stSidebar"] {
        transition: transform 0.3s ease-in-out;
    }
    
    /* Chat message styling like Grok */
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: linear-gradient(135deg, #3B82F6, #1E40AF);
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .ai-message {
        background: rgba(255, 255, 255, 0.1);
        color: #1F2937;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    /* Upload pin icon styling */
    [data-testid="stFileUploader"] {
        position: relative;
    }
    
    [data-testid="stFileUploader"]::before {
        content: "📎";
        position: absolute;
        left: -2rem;
        top: 0.5rem;
        font-size: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Configure Gemini (use your API key via st.secrets or env)
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY")))
model = genai.GenerativeModel('gemini-1.5-flash')

# Session state for chats and user
if "user_name" not in st.session_state:
    st.session_state.user_name = "User"  # From login, e.g., st.session_state.user_name
if "chats" not in st.session_state:
    st.session_state.chats = {}  # {chat_id: [{"role": "user/ai", "content": str}]}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False

# Sidebar toggle button (for mobile/desktop hover/slide)
if st.sidebar.button("☰ Menu", key="toggle_sidebar"):
    st.session_state.show_sidebar = not st.session_state.show_sidebar

# Sidebar content (only show if toggled or expanded)
with st.sidebar:
    if st.session_state.show_sidebar or st.sidebar.get_state() == "expanded":
        st.header("📚 CrypticX Chats")
        
        # Create new chat
        if st.button("➕ Create New Chat"):
            new_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state.chats[new_id] = []
            st.session_state.current_chat_id = new_id
            st.rerun()
        
        # Search chats
        search_query = st.text_input("🔍 Search Chats")
        filtered_chats = []
        if search_query:
            for chat_id, messages in st.session_state.chats.items():
                if any(search_query.lower() in msg["content"].lower() for msg in messages):
                    filtered_chats.append((chat_id, messages))
        else:
            filtered_chats = list(st.session_state.chats.items())
        
        # Previous chats list (like Grok's chat history)
        st.subheader("Previous Chats")
        for chat_id, messages in filtered_chats[-10:]:  # Show last 10
            chat_preview = messages[-1]["content"][:50] + "..." if messages else "New Chat"
            if st.button(f"Chat {chat_id.split('_')[0]}: {chat_preview}", key=f"chat_{chat_id}"):
                st.session_state.current_chat_id = chat_id
                st.rerun()
        
        # Clear chats
        if st.button("🗑️ Clear All Chats"):
            st.session_state.chats = {}
            st.session_state.current_chat_id = None
            st.rerun()

# Main chat area
if st.session_state.current_chat_id is None:
    # No chat selected, prompt to create one
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <h1>Hello, {st.session_state.user_name}! 👋</h1>
        <p>Welcome to CrypticX, your AI study companion. Upload docs for analysis, summarize notes, or chat with Gemini 1.5.</p>
        <p>Start by creating a new chat in the sidebar!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Load current chat
    current_chat = st.session_state.chats[st.session_state.current_chat_id]
    
    # Display chat history (like Grok)
    st.header(f"Chat: {st.session_state.current_chat_id.split('_')[0]}")
    chat_container = st.container()
    with chat_container:
        for msg in current_chat:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message ai-message">{msg["content"]}</div>', unsafe_allow_html=True)
    
    # File upload for documents (pin-like)
    uploaded_file = st.file_uploader("📎 Upload Document (PDF/DOC for analysis)", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        # Handle upload: Save temporarily and analyze
        with open("temp_upload", "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Example: Summarize with Gemini (adapt for full analysis)
        summary_prompt = f"Summarize this document for study: {uploaded_file.name}"
        # For real impl, use PyPDF2 or docx to extract text first
        extracted_text = "Extracted text here"  # Placeholder: Implement text extraction
        response = model.generate_content([summary_prompt, extracted_text])
        st.session_state.chats[st.session_state.current_chat_id].append({
            "role": "ai",
            "content": f"📄 Document Analysis/Summary:\n{response.text}"
        })
        os.remove("temp_upload")  # Clean up
        st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Type your message... (e.g., 'Summarize this' or ask Gemini)"):
        # Add user message
        st.session_state.chats[st.session_state.current_chat_id].append({"role": "user", "content": prompt})
        with chat_container:
            st.markdown(f'<div class="chat-message user-message">{prompt}</div>', unsafe_allow_html=True)
        
        # Generate AI response with Gemini (context-aware, continues chat)
        chat_history = [{"role": m["role"], "parts": [m["content"]]} for m in current_chat]
        full_prompt = chat_history + [{"role": "user", "parts": [prompt]}]
        try:
            response = model.generate_content(full_prompt)
            ai_msg = response.text
        except Exception as e:
            ai_msg = f"Oops! Error: {str(e)}. Check your API key."
        
        st.session_state.chats[st.session_state.current_chat_id].append({"role": "ai", "content": ai_msg})
        
        # Rerun to show new message
        st.rerun()

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: rgba(59, 130, 246, 0.7);'>Powered by Gemini 1.5 | Document Analysis & Summarization Ready 🚀</p>", unsafe_allow_html=True)
