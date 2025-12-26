# Stephen Wolf

**Stephen Wolf** is a sleek, futuristic web-based AI chat interface powered by Groq's ultra-fast LLMs. Switch between 10 specialized professional personas, from Mathematician to Financial Analyst, each strictly focused on its domain for precise, role-bound responses.

Built with Streamlit for a responsive, cyberpunk-inspired UI, it features real-time streaming replies, session management, JSON export, and seamless mobile/desktop experience.

## Features

- 10 strict professional personas (Mathematician, Physician, Travel Advisor, Executive Chef, Systems Engineer, Legal Counsel, Clinical Psychologist, Historian, Fitness Coach, Financial Analyst)
- Multiple Groq models (Llama 3.3 70B, Llama 3.1 8B, Mixtral, Gemma 2)
- Real-time streaming responses with typing animation
- Futuristic dark theme with neon accents and glassmorphism
- Fully responsive design (desktop & mobile)
- Sidebar configuration with model/personality selection
- Session clear, save, and JSON export
- Production-grade error handling and API key management
- Deployed for free on Streamlit Community Cloud

## Live Demo

[https://Saadajee-stephen-wolf.streamlit.app](https://Saadajee-stephen-wolf.streamlit.app) *(replace with your actual deployed URL)*

## Local Development

1. Clone the repo
2. Create `.streamlit/secrets.toml` with your Groq API key:
   ```
   GROQ_API_KEY = "gsk_your_key_here"
   ```
3. Install dependencies:
   ```
   pip install streamlit groq
   ```
   Run:
   ```
   streamlit run app.py
   ```

## Deployment
Deploy instantly on Streamlit Community Cloud:

- Connect your GitHub repo
- Set GROQ_API_KEY in app secrets
- Main file: app.py

Enjoy the adaptive intelligence!
