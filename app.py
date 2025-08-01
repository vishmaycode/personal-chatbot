import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

load_dotenv()

st.set_page_config(page_title="Vishmay Info", page_icon="😎")
st.title("Know more about me!")


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

        Relevant information:
        {profile_text}"""
    )
    response = llm([system_msg, HumanMessage(content=query)])
    st.session_state.messages.append(response)
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

