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
        transition: transform 0.3s ease-in-out;
        overflow-y: auto;
    }
    
    /* Hide sidebar content when not shown */
    .stSidebar > div > div > div:has(.hidden-content) {
        display: none;
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
try:
    genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY")))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Gemini setup failed: {e}. Check your API key in secrets.toml.")
    model = None

# Session state for chats and user
if "user_name" not in st.session_state:
    st.session_state.user_name = "User"  # From login, e.g., st.session_state.user_name
if "chats" not in st.session_state:
    st.session_state.chats = {}  # {chat_id: [{"role": "user/ai", "content": str}]}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False

# Top-right toggle button (always visible)
col1, col2, col3 = st.columns([1, 1, 20])  # Spacer for top-right placement
with col3:
    if st.button("☰", key="toggle_sidebar", help="Toggle Sidebar"):
        st.session_state.show_sidebar = not st.session_state.show_sidebar
        # JS to force sidebar expand/collapse on toggle (smooth slide)
        expand_state = "true" if st.session_state.show_sidebar else "false"
        st.components.v1.html(f"""
            <script>
            parent.document.querySelector('section[data-testid="stSidebar"] button[kind="header"]').click();
            if (!{expand_state}) {{
                setTimeout(() => {{
                    parent.document.querySelector('section[data-testid="stSidebar"] button[kind="header"]').click();
                }}, 100);
            }}
            </script>
        """, height=0)

# Sidebar content (conditionally shown)
with st.sidebar:
    if st.session_state.show_sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)  # Wrapper for CSS
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
        
        # Previous chats list (like Grok, with timestamps)
        st.subheader("Previous Chats")
        for chat_id, messages in filtered_chats[-10:]:  # Show last 10
            timestamp = chat_id.split('_')[1] if '_' in chat_id else "Recent"
            chat_preview = messages[-1]["content"][:50] + "..." if messages else f"New Chat - {timestamp}"
            if st.button(f"{timestamp}: {chat_preview}", key=f"chat_{chat_id}"):
                st.session_state.current_chat_id = chat_id
                st.rerun()
        
        # Clear chats
        if st.button("🗑️ Clear All Chats"):
            st.session_state.chats = {}
            st.session_state.current_chat_id = None
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main chat area
if st.session_state.current_chat_id is None:
    # No chat selected, prompt to create one
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <h1>Hello, {st.session_state.user_name}! 👋</h1>
        <p>Welcome to CrypticX, your AI study companion. Upload docs for analysis, summarize notes, or chat with Gemini 1.5.</p>
        <p>Start by creating a new chat (click ☰ top-right)!</p>
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
    if uploaded_file is not None and model:
        # Handle upload: Save temporarily and analyze (placeholder for extraction)
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # TODO: Implement real extraction (e.g., with PyPDF2)
        extracted_text = "Extracted document text here..."  # Replace with actual extraction
        summary_prompt = f"Summarize this document for study purposes: {uploaded_file.name}\n\nContent: {extracted_text}"
        try:
            response = model.generate_content(summary_prompt)
            ai_response = f"📄 Document Analysis/Summary:\n{response.text}"
        except Exception as e:
            ai_response = f"Analysis error: {str(e)}"
        
        st.session_state.chats[st.session_state.current_chat_id].append({
            "role": "ai",
            "content": ai_response
        })
        os.remove(file_path)  # Clean up
        st.success("Document analyzed! Check the chat.")
        st.rerun()
    elif uploaded_file is not None:
        st.warning("Upload ready, but Gemini not configured. Add API key to secrets.toml.")
    
    # Chat input
    if prompt := st.chat_input("Type your message... (e.g., 'Summarize this' or ask Gemini)"):
        if not model:
            st.error("Gemini not set up. Add API key.")
        else:
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
