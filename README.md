# Vishmay Info Chatbot

A Streamlit-based chatbot that answers questions about Vishmay Karbotkar using information from a profile document. Powered by OpenRouter and LangChain.

## Features
- Friendly chatbot interface using Streamlit
- Answers only about Vishmay Karbotkar
- Uses profile.txt for all responses

## Setup

1. **Clone the repository**
   ```bash
   git clone git@github.com:vishmaycode/personal-chatbot.git
   cd personal-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   - Copy `.env.example` to `.env` and add your OpenRouter API key:
     ```bash
     cp .env.example .env
     # Edit .env and set OPENROUTER_API_KEY
     ```

4. **Add your profile**
   - Edit `profile.txt` with information about Vishmay Karbotkar.

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Usage
- Ask questions about Vishmay's experience or skills.
- The chatbot will only answer using information from `profile.txt`.
- Greetings will receive a short, friendly 5-word reply.

## Environment Variables
- `OPENROUTER_API_KEY`: Your OpenRouter API key (see `.env.example`).
