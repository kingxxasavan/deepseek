import streamlit as st
import time
from datetime import datetime

# Page configuration

st.set_page_config(
page_title=“AI Learning Assistant”,
page_icon=“🤖”,
layout=“wide”,
initial_sidebar_state=“collapsed”
)

# Custom CSS for glassmorphism and animations

st.markdown(”””

<style>
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 10px 0;
        animation: slideIn 0.5s ease-out;
    }
    
    /* Sliding panel animation */
    @keyframes slideIn {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Chat container */
    .chat-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Greeting text */
    .greeting {
        color: white;
        text-align: center;
        font-size: 2.5em;
        font-weight: 600;
        margin: 30px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        animation: fadeInDown 1s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            transform: translateY(-50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    .subgreeting {
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 40px;
        animation: fadeInUp 1.2s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            transform: translateY(50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 20px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        color: white;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.5);
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Side panels */
    .side-panel-left {
        animation: slideIn 0.6s ease-out;
    }
    
    .side-panel-right {
        animation: slideInRight 0.6s ease-out;
    }
    
    /* Message bubbles */
    .user-message {
        background: rgba(102, 126, 234, 0.6);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 5px 18px;
        margin: 8px 0;
        max-width: 70%;
        float: right;
        clear: both;
        backdrop-filter: blur(5px);
    }
    
    .ai-message {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 5px;
        margin: 8px 0;
        max-width: 70%;
        float: left;
        clear: both;
        backdrop-filter: blur(5px);
    }
    
    /* Button styling */
    .stButton>button {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 10px 20px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.05);
    }
    
    /* Text input styling */
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    /* Icon styling */
    .feature-icon {
        font-size: 2em;
        margin-bottom: 10px;
    }
</style>

“””, unsafe_allow_html=True)

# Initialize session state

if ‘chat_history’ not in st.session_state:
st.session_state.chat_history = []
if ‘show_greeting’ not in st.session_state:
st.session_state.show_greeting = True
if ‘selected_feature’ not in st.session_state:
st.session_state.selected_feature = None

# Functions for AI features

def generate_flashcards(topic, num_cards=5):
“”“Simulate AI flashcard generation”””
return [
{“front”: f”Question {i+1} about {topic}”, “back”: f”Answer {i+1} for {topic}”}
for i in range(num_cards)
]

def generate_quiz(topic, num_questions=5):
“”“Simulate AI quiz generation”””
return [
{
“question”: f”Question {i+1} about {topic}?”,
“options”: [“Option A”, “Option B”, “Option C”, “Option D”],
“correct”: 0
}
for i in range(num_questions)
]

def summarize_document(text):
“”“Simulate AI document summarization”””
return f”Summary: This document discusses key points about {text[:50]}… The main findings include comprehensive analysis and detailed insights.”

# Main layout

col_left, col_center, col_right = st.columns([1, 2, 1])

# Left Panel - Feature Selection

with col_left:
st.markdown(’<div class="side-panel-left">’, unsafe_allow_html=True)
st.markdown(”””
<div class="glass-card">
<h3 style="color: white; text-align: center;">✨ AI Features</h3>
</div>
“””, unsafe_allow_html=True)

```
# Feature buttons
features = [
    {"name": "💳 Flashcards", "icon": "💳", "key": "flashcards"},
    {"name": "📝 Quiz Generator", "icon": "📝", "key": "quiz"},
    {"name": "📄 Summarize", "icon": "📄", "key": "summarize"},
    {"name": "💬 Chat", "icon": "💬", "key": "chat"}
]

for feature in features:
    if st.button(feature['name'], key=feature['key'], use_container_width=True):
        st.session_state.selected_feature = feature['key']
        st.session_state.show_greeting = False
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
```

# Center Panel - Main Chat/Content Area

with col_center:
# Greeting message
if st.session_state.show_greeting:
current_hour = datetime.now().hour
if current_hour < 12:
greeting = “Good Morning! ☀️”
elif current_hour < 18:
greeting = “Good Afternoon! 🌤️”
else:
greeting = “Good Evening! 🌙”

```
    st.markdown(f'<div class="greeting">{greeting}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subgreeting">Welcome to your AI Learning Assistant. How can I help you today?</div>',
        unsafe_allow_html=True
    )
    
    # Quick action cards
    st.markdown("""
    <div class="glass-card">
        <h4 style="color: white; margin-bottom: 20px;">🚀 Quick Start</h4>
        <p style="color: rgba(255,255,255,0.9);">
            Select a feature from the left panel to get started, or use the chat to ask me anything!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Feature-specific content
else:
    feature = st.session_state.selected_feature
    
    if feature == "flashcards":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white;">💳 AI Flashcard Generator</h3>', unsafe_allow_html=True)
        
        topic = st.text_input("Enter a topic:", key="flashcard_topic")
        num_cards = st.slider("Number of cards:", 3, 10, 5)
        
        if st.button("Generate Flashcards"):
            with st.spinner("Generating flashcards..."):
                time.sleep(1)
                cards = generate_flashcards(topic, num_cards)
                
                for i, card in enumerate(cards):
                    st.markdown(f"""
                    <div class="feature-card">
                        <strong>Card {i+1}</strong><br>
                        <strong>Q:</strong> {card['front']}<br>
                        <strong>A:</strong> {card['back']}
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif feature == "quiz":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white;">📝 AI Quiz Generator</h3>', unsafe_allow_html=True)
        
        topic = st.text_input("Enter a topic:", key="quiz_topic")
        num_questions = st.slider("Number of questions:", 3, 10, 5)
        
        if st.button("Generate Quiz"):
            with st.spinner("Generating quiz..."):
                time.sleep(1)
                quiz = generate_quiz(topic, num_questions)
                
                for i, q in enumerate(quiz):
                    st.markdown(f"""
                    <div class="feature-card">
                        <strong>Question {i+1}:</strong> {q['question']}<br>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for opt in q['options']:
                        st.radio(f"Q{i+1}", q['options'], key=f"q{i}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif feature == "summarize":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white;">📄 Document Summarizer</h3>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload a document", type=['txt', 'pdf', 'docx'])
        text_input = st.text_area("Or paste text here:", height=200)
        
        if st.button("Summarize"):
            with st.spinner("Analyzing document..."):
                time.sleep(1)
                content = text_input if text_input else "Sample document content"
                summary = summarize_document(content)
                
                st.markdown(f"""
                <div class="feature-card">
                    <strong>Summary:</strong><br>{summary}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif feature == "chat":
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat history
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-message">{msg["content"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_input("Type your message...", key="chat_input")
        if st.button("Send") and user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Simulate AI response
            ai_response = f"I understand you're asking about: {user_input}. Let me help you with that!"
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
```

# Right Panel - Info/Stats

with col_right:
st.markdown(’<div class="side-panel-right">’, unsafe_allow_html=True)
st.markdown(”””
<div class="glass-card">
<h3 style="color: white; text-align: center;">📊 Stats</h3>
</div>
“””, unsafe_allow_html=True)

```
st.markdown("""
<div class="feature-card">
    <div class="feature-icon">🎯</div>
    <strong style="color: white;">Study Streak</strong><br>
    <span style="color: rgba(255,255,255,0.9);">5 days</span>
</div>

<div class="feature-card">
    <div class="feature-icon">📚</div>
    <strong style="color: white;">Cards Reviewed</strong><br>
    <span style="color: rgba(255,255,255,0.9);">124 cards</span>
</div>

<div class="feature-card">
    <div class="feature-icon">✅</div>
    <strong style="color: white;">Quizzes Completed</strong><br>
    <span style="color: rgba(255,255,255,0.9);">12 quizzes</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
```
