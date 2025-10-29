import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os

# Page config: Wide layout, favicon
st.set_page_config(
    page_title="CrypticX - AI Study Sky",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Theme config for base sky colors (light mode)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #87CEEB 0%, #E0F6FF 50%, #FFFFFF 100%);
        min-height: 100vh;
    }
    </style>
""", unsafe_allow_html=True)

# Custom CSS: Sky transparent + Grok-like
st.markdown("""
    <style>
    /* Sky body */
    .stApp {
        background: transparent !important;
    }
    .main .block-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(135, 206, 235, 0.3);
        border-radius: 20px;
        padding: 1rem;
    }
    
    /* Top header like Grok */
    .header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background: rgba(135, 206, 235, 0.2);
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    .header-title { color: #1E3A8A; font-size: 1.5rem; font-weight: bold; }
    .header-actions { display: flex; gap: 1rem; }
    .header-btn { background: rgba(30, 58, 138, 0.2); border: none; border-radius: 50%; padding: 0.5rem; color: #1E3A8A; cursor: pointer; }
    
    /* Sliding sidebar: Slim, sky-transparent */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(135, 206, 235, 0.3) 0%, rgba(224, 246, 255, 0.2) 100%);
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(135, 206, 235, 0.4);
        width: 250px !important;
        transition: transform 0.4s ease, opacity 0.3s;
        opacity: 0.95;
    }
    section[data-testid="stSidebar"]:hover { transform: translateX(0) scale(1.02); }
    @keyframes slideSky { from { transform: translateX(-100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
    .sidebar-content { animation: slideSky 0.4s ease-out; }
    
    /* Chat messages: Bubbly, transparent */
    .chat-message { padding: 1rem; margin: 0.5rem 0; border-radius: 18px; max-width: 70%; word-wrap: break-word; }
    .user-message { background: linear-gradient(135deg, #87CEEB, #1E3A8A); color: white; margin-left: auto; text-align: right; }
    .ai-message { background: rgba(255, 255, 255, 0.7); color: #1E3A8A; backdrop-filter: blur(10px); border: 1px solid rgba(135, 206, 235, 0.3); }
    
    /* Chat input: Bottom sticky, placeholder */
    [data-testid="stChatInput"] { background: rgba(255, 255, 255, 0.2); border-radius: 25px; border: 1px solid #87CEEB; }
    [data-testid="stChatInput"] input::placeholder { color: #1E3A8A; opacity: 0.7; }
    
    /* Upload pin */
    [data-testid="stFileUploader"]::before { content: "📎"; position: absolute; left: -2rem; top: 0.5rem; font-size: 1.5rem; }
    
    /* Responsive zoom/close */
    @media (max-width: 768px) { section[data-testid="stSidebar"] { transform: translateX(-100%); } }
    @media (min-zoom: 1.25) { .chat-message { font-size: 1.1em; } .header-bar { padding: 0.5rem; } }
    
    /* Hide footer on zoom/small */
    .powered-footer { opacity: 0.7; transition: opacity 0.3s; }
    @media (max-width: 600px), (min-zoom: 1.5) { .powered-footer { display: none; } }
    </style>
""", unsafe_allow_html=True)

# Gemini setup
try:
    genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY")))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Gemini error: {e}. Add API key.")
    model = None

# Session state
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")  # Auto-default chat
    st.session_state.chats[st.session_state.current_chat_id] = []
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = False

# Simple Login (Grok-like: Quick name entry)
if not st.session_state.logged_in:
    st.markdown('<div class="header-bar"><div class="header-title">Welcome to CrypticX Sky</div></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        name = st.text_input("Enter your name to start chatting ☁️")
    with col2:
        if st.button("Login", type="primary"):
            if name:
                st.session_state.user_name = name
                st.session_state.logged_in = True
                st.rerun()
    st.stop()

# Top header (post-login, like Grok)
st.markdown(f"""
    <div class="header-bar">
        <div class="header-title">CrypticX - Study in the Sky {chr(9731)}</div>
        <div class="header-actions">
            <button class="header-btn" onclick="window.open('https://x.com', '_blank')">📤</button>
            <button class="header-btn">⭐</button>
            <button class="header-btn">⚙️</button>
            <span style="color: #1E3A8A; font-weight: bold;">Hi, {st.session_state.user_name}!</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Toggle sidebar (top-right, always visible)
if st.button("☰", key="toggle_sidebar"):
    st.session_state.show_sidebar = not st.session_state.show_sidebar
    st.rerun()

# Sidebar (Grok-style: Chats + Tools)
with st.sidebar:
    if st.session_state.show_sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.header("☁️ Chats")
        
        # New chat
        if st.button("➕ New Chat"):
            new_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state.chats[new_id] = []
            st.session_state.current_chat_id = new_id
            st.rerun()
        
        # Search
        search = st.text_input("🔍 Search Chats")
        filtered = [(k, v) for k, v in st.session_state.chats.items() 
                    if not search or any(search.lower() in m["content"].lower() for m in v)]
        
        # Previous chats
        for cid, msgs in filtered[-5:]:  # Top 5
            preview = msgs[-1]["content"][:40] + "..." if msgs else "Fresh chat"
            if st.button(f"{cid.split('_')[1]}: {preview}", key=f"sel_{cid}"):
                st.session_state.current_chat_id = cid
                st.rerun()
        
        # Study Tools expander (your features)
        with st.expander("🛠️ Study Tools"):
            st.info("Upload docs here for analysis/summary.")
        
        # Clear
        if st.button("🗑️ Clear All"):
            st.session_state.chats = {}
            st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state.chats[st.session_state.current_chat_id] = []
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main chat (always ready, like Grok)
current_chat = st.session_state.chats[st.session_state.current_chat_id]
st.header(f"Chat in the Sky ☁️")

# Messages container
chat_cont = st.container()
with chat_cont:
    # Greeting on first load/continue
    if not current_chat:
        greeting = f"Hello, {st.session_state.user_name}! Ready to dive into studies? Upload a doc or ask away."
        st.markdown(f'<div class="chat-message ai-message">{greeting}</div>', unsafe_allow_html=True)
        current_chat.append({"role": "ai", "content": greeting})
    
    # Render history
    for msg in current_chat:
        cls = "user-message" if msg["role"] == "user" else "ai-message"
        st.markdown(f'<div class="chat-message {cls}">{msg["content"]}</div>', unsafe_allow_html=True)

# Upload (tools integration)
uploaded = st.file_uploader("📎 Upload Doc for Analysis", type=["pdf", "txt", "docx"])
if uploaded and model:
    # Placeholder extraction
    text = "Extracted text..."  # Add PyPDF2/docx logic here
    resp = model.generate_content(f"Summarize for study: {text}")
    ai_msg = f"📄 Analysis: {resp.text}"
    current_chat.append({"role": "ai", "content": ai_msg})
    with chat_cont:
        st.markdown(f'<div class="chat-message ai-message">{ai_msg}</div>', unsafe_allow_html=True)
    st.rerun()

# Chat input (always there, placeholder)
if prompt := st.chat_input("Chat about your studies... (e.g., 'Explain quantum basics')"):
    if model:
        current_chat.append({"role": "user", "content": prompt})
        with chat_cont:
            st.markdown(f'<div class="chat-message user-message">{prompt}</div>', unsafe_allow_html=True)
        
        # Gemini response (contextual)
        history = [{"role": m["role"], "parts": [m["content"]]} for m in current_chat]
        resp = model.generate_content(history + [{"role": "user", "parts": [prompt]}])
        ai_msg = resp.text
        current_chat.append({"role": "ai", "content": ai_msg})
        st.rerun()
    else:
        st.warning("Add Gemini key for chat.")

# Subtle footer (no ---)
st.markdown('<div class="powered-footer" style="text-align: center; padding: 1rem; color: rgba(30, 58, 138, 0.6);">Powered by Gemini 1.5 ☁️</div>', unsafe_allow_html=True)
