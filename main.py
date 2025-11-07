import streamlit as st
import speech_recognition as sr
import pyttsx3
from google.generativeai import configure, GenerativeModel

# Configure Gemini 2.5 Flash
configure(api_key="YOUR_GEMINI_API_KEY")
model = GenerativeModel("gemini-2.5-flash")

# Initialize TTS engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except Exception as e:
            st.error(f"Error: {e}")
            return None

# Function to generate flashcards
def generate_flashcards(topic):
    prompt = f"Create 5 flashcards (question and answer) about {topic}. Format each as 'Q: [question]\\nA: [answer]'."
    response = model.generate_content(prompt)
    return response.text

# Function to generate practice test
def generate_practice_test(topic):
    prompt = f"Create a 5-question multiple-choice practice test about {topic}. Include the correct answer for each question."
    response = model.generate_content(prompt)
    return response.text

# Function to generate code
def generate_code(prompt):
    response = model.generate_content(f"Write Python code for: {prompt}")
    return response.text

# Streamlit UI
st.title("Jarvis Voice Assistant")

mode = st.selectbox(
    "Select Mode:",
    ["Conversation", "Code Generation", "Flashcards", "Practice Test"]
)

if st.button("Speak"):
    user_input = listen()
    if user_input:
        st.write(f"You: {user_input}")

        if mode == "Conversation":
            response = model.generate_content(user_input)
        elif mode == "Code Generation":
            response = generate_code(user_input)
        elif mode == "Flashcards":
            response = generate_flashcards(user_input)
        elif mode == "Practice Test":
            response = generate_practice_test(user_input)

        st.write(f"Jarvis: {response.text}")
        speak(response.text)
