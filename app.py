import streamlit as st
from groq import Groq
import os
import json
from datetime import datetime
import logging

# Logging for debugging (optional in production)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config - must be first
st.set_page_config(
    page_title="Stephen Wolf",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'About': "Stephen Wolf v1.1 - Adaptive Intelligence Interface"}
)

# Custom futuristic CSS
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
    
    :root {
        --primary: #00d0ff;
        --secondary: #a020f0;
        --bg-dark: #0a0e27;
        --card-bg: rgba(15, 23, 42, 0.6);
        --text: #e0e0e0;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--bg-dark) 0%, #1a1f3a 100%);
        font-family: 'Rajdhani', sans-serif;
        color: var(--text);
    }
    
    /* Clean hide of Streamlit branding - keeps sidebar toggle visible */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Style the sidebar toggle button (hamburger) to match theme */
    button[kind="headerAction"] {
        background: var(--primary) !important;
        color: black !important;
        border-radius: 50% !important;
        box-shadow: 0 0 15px var(--primary);
        transition: all 0.3s ease;
    }
    
    button[kind="headerAction"]:hover {
        box-shadow: 0 0 25px var(--primary) !important;
        transform: scale(1.1);
    }
    
    h1 {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        text-align: center;
        font-size: 3rem;
        margin: 1rem 0 0.5rem;
        text-shadow: 0 0 20px rgba(0, 208, 255, 0.3);
    }
    
    .subtitle {
        text-align: center;
        color: var(--primary);
        font-size: 1.1rem;
        letter-spacing: 2px;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 14, 39, 0.95), rgba(26, 31, 58, 0.95));
        border-right: 1px solid var(--primary);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] h1, h2, h3 {
        color: var(--primary);
        font-family: 'Orbitron', sans-serif;
    }
    
    .stSelectbox > div > div {
        background-color: var(--card-bg);
        border: 1px solid var(--primary);
        border-radius: 10px;
        color: white;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-family: 'Orbitron', sans-serif;
        padding: 0.75rem 1.5rem;
        box-shadow: 0 0 15px rgba(0, 208, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 208, 255, 0.5);
    }
    
    .stChatMessage {
        background-color: rgba(15, 23, 42, 0.4);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(0, 208, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--primary), transparent);
        opacity: 0.4;
        margin: 2rem 0;
    }
    
    .stCaption {
        color: var(--primary);
        text-align: center;
        font-size: 0.9rem;
    }
    
    @media (max-width: 768px) {
        h1 {font-size: 2.2rem;}
        .subtitle {font-size: 1rem;}
        .stChatMessage {padding: 0.75rem;}
    }
    </style>
    """, unsafe_allow_html=True)

# 10 Professional Personas
PERSONALITIES = {
    "Mathematician": {"system_prompt": "You are a Mathematician. You only answer questions related to mathematics... [same as before]", "description": "Mathematics and mathematical theory"},
    "Physician": {"system_prompt": "You are a Physician...", "description": "Medicine and health"},
    "Travel Advisor": {"system_prompt": "You are a Travel Advisor...", "description": "Travel planning and destinations"},
    "Executive Chef": {"system_prompt": "You are an Executive Chef...", "description": "Cooking and culinary arts"},
    "Systems Engineer": {"system_prompt": "You are a Systems Engineer...", "description": "Technology and systems"},
    "Legal Counsel": {"system_prompt": "You are Legal Counsel...", "description": "Law and legal principles"},
    "Clinical Psychologist": {"system_prompt": "You are a Clinical Psychologist...", "description": "Psychology and mental health"},
    "Historian": {"system_prompt": "You are a Historian...", "description": "History and historical analysis"},
    "Fitness Coach": {"system_prompt": "You are a Fitness Coach...", "description": "Fitness and physical training"},
    "Financial Analyst": {"system_prompt": "You are a Financial Analyst...", "description": "Finance and economics"}
}

# Groq Models
MODELS = {
    "Llama 3.3 70B": "llama-3.3-70b-versatile",
    "Llama 3.1 8B": "llama-3.1-8b-instant",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 2 9B": "gemma2-9b-it"
}

# Safe Groq client
@st.cache_resource
def get_groq_client():
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Groq API key missing. Add to `.streamlit/secrets.toml` or environment.")
        st.stop()
    return Groq(api_key=api_key)

def generate_streaming_response(client, messages, model, system_prompt):
    try:
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        return client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=0.7,
            max_tokens=1024,
            stream=True
        )
    except Exception as e:
        logger.error(f"API Error: {e}")
        return None

# Apply CSS
inject_custom_css()

# Header
st.markdown("<h1>Stephen Wolf</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Adaptive Intelligence Interface</p>', unsafe_allow_html=True)

# Initialize state
defaults = {
    "messages": [],
    "selected_personality": next(iter(PERSONALITIES)),
    "selected_model": next(iter(MODELS)),
    "message_count": 0,
    "saved_sessions": []
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Sidebar
with st.sidebar:
    st.markdown("### Configuration")
    
    selected_model_name = st.selectbox("Model", options=list(MODELS.keys()))
    selected_model_id = MODELS[selected_model_name]
    
    selected_personality = st.selectbox("Personality", options=list(PERSONALITIES.keys()))
    
    st.info(PERSONALITIES[selected_personality]["description"])
    
    st.markdown("### Session")
    st.caption(f"Messages: {st.session_state.message_count}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear"):
            st.session_state.messages = []
            st.session_state.message_count = 0
            st.rerun()
    with col2:
        if st.button("Save"):
            if st.session_state.messages:
                entry = {
                    "timestamp": datetime.now().isoformat(),
                    "personality": selected_personality,
                    "model": selected_model_name,
                    "messages": st.session_state.messages.copy()
                }
                st.session_state.saved_sessions.append(entry)
                st.success("Saved")
            else:
                st.info("Nothing to save")
    
    if st.session_state.messages:
        export = json.dumps({
            "personality": selected_personality,
            "model": selected_model_name,
            "messages": st.session_state.messages,
            "exported": datetime.now().isoformat()
        }, indent=2)
        st.download_button("Export JSON", export, f"stephen_wolf_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "application/json")

# Reset on config change
if (st.session_state.selected_personality != selected_personality or 
    st.session_state.selected_model != selected_model_name):
    st.session_state.messages = []
    st.session_state.message_count = 0
    st.session_state.selected_personality = selected_personality
    st.session_state.selected_model = selected_model_name
    st.rerun()

# Chat Area - Fixed height issue
st.markdown("<div style='padding: 1rem 0;'></div>", unsafe_allow_html=True)

# Use a container with fixed height only when needed
if st.session_state.message_count > 8:
    chat_container = st.container(height=600)
else:
    chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.markdown(
            "<div style='text-align: center; padding: 4rem 1rem; color: #00d0ff; opacity: 0.8;'>"
            "Select a personality and send a message to begin."
            "</div>",
            unsafe_allow_html=True
        )
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Input
if prompt := st.chat_input("Enter your message"):
    if not prompt.strip():
        st.warning("Message cannot be empty.")
    else:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.message_count += 1
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            client = get_groq_client()
            stream = generate_streaming_response(
                client,
                st.session_state.messages[:-1],
                selected_model_id,
                PERSONALITIES[selected_personality]["system_prompt"]
            )
            
            if stream:
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
            else:
                full_response = "Error: Could not generate response."
                placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.message_count += 1
        st.rerun()

# Footer
st.markdown("---")
st.caption(f"Active: {selected_personality} • Model: {selected_model_name} • Messages: {st.session_state.message_count}")