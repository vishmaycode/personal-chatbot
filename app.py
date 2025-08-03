import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

load_dotenv()

st.set_page_config(page_title="Vishmay Info", page_icon="😎")

# Set your 6-digit PIN here (you can change this)
CORRECT_PIN = os.getenv("ACCESS_KEY")

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# PIN Authentication Screen
if not st.session_state.authenticated:
    st.title("Access Control")
    st.write("Please enter the 6-digit PIN to access the chatbot:")
    st.write("In case you dont have the pin, please speak with the website owner to get the 6 digit PIN:")
    
    # Create a form to handle Enter key submission
    with st.form(key="pin_form"):
        pin_input = st.text_input("PIN:", type="password", max_chars=6, placeholder="Enter 6-digit PIN")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button("Enter", use_container_width=True)
        
        # Check PIN when form is submitted (either by button click or Enter key)
        if submit_button:
            if pin_input == CORRECT_PIN:
                st.session_state.authenticated = True
                st.success("Access granted!")
                st.rerun()
            else:
                st.error("Incorrect PIN. Please try again.")
    
    st.stop()  # Stop execution here if not authenticated

# Main Chatbot (only shown after authentication)
st.title("Know me!")

# Load profile text directly
@st.cache_resource
def get_profile_text():
    docs = load_profile()
    return "\n".join([doc.page_content for doc in docs])

def load_profile(path="profile.txt"):
    loader = TextLoader(path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(docs)

profile_text = get_profile_text()

llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    model_name="mistralai/mistral-7b-instruct"
)

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial assistant message
    st.session_state.messages.append(SystemMessage(content="Hi, I am Vishmay."))

query = st.chat_input("Ask about my experience or skills...")

if query:
    st.session_state.messages.append(HumanMessage(content=query))
    system_msg = SystemMessage(
        content=f"""You are a chatbot that answers questions only about Vishmay Karbotkar, using information from the provided document.
        If the user greets you (e.g., 'hi', 'hello'), reply ONLY with a short, friendly greeting of exactly 5 words. Do not share any details unless the user asks for specific information.
        When answering questions, respond naturally and concisely, focusing only on what is asked. Never make up information or go beyond the document. If a question is unclear, politely ask for clarification.
        If the user asks any irrelevant question which is not in the provided information then kindly tell the user that you dont have the information in 5 words, do not talk about myself in this case.

        Relevant information:
        {profile_text}"""
    )
    response = llm([system_msg, HumanMessage(content=query)])
    st.session_state.messages.append(response)

for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)