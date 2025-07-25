import streamlit as st
from app.ui import pdf_uploader
from app.pdf_utils import extract_text_from_pdf
from app.vectorstore_utils import create_faiss_index, retrieve_relevant_docs
from app.chat_utils import get_chat_model, ask_chat_model
from app.config import EURI_API_KEY
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time

st.set_page_config(
    page_title="DocuChat",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
}

.chat-message.user {
    background-color: #2b313e;
    color: white;
}

.chat-message.assistant {
    background-color: #f0f2f6;
    color: black;
}

.chat-message .avatar {
    width: 2rem;
}

.chat-message .message {
    flex: 1;
}

.chat-message .timestamp {
    font-size: 0.8rem;
    opacity: 0.7;
    margin-top: 0.5rem;
}

.stButton > button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 0.5rem;
    border: none;
    padding: 0.5rem 1rem;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #ff3333;
}

.upload-section {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}
.status-success {
    background-color: #d4edda;
    color: #155724;
    padding: 0.5rem;
    border-radius: 0.25rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_model" not in st.session_state:
    st.session_state.chat_model = None

st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #ff4b4b; font-size: 3rem; margin-bottom: 0.5rem;"> DocuChat Pro</h1>
    <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Your Intelligent Document Assistant</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📂 Document Upload")
    st.markdown("Upload your documents to start chatting!")

    uploaded_files = pdf_uploader()

    if uploaded_files:
        st.success(f"📄 {len(uploaded_files)} document(s) uploaded")

        # Process documents
        if st.button("Process Documents", type="primary"):
            with st.spinner("Processing your documents..."):
                # Extract text from all PDFs
                all_texts = []
                for file in uploaded_files:
                    text = extract_text_from_pdf(file)
                    all_texts.append(text)

                # Split texts into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len,
                )

                chunks = []
                for text in all_texts:
                    chunks.extend(text_splitter.split_text(text))

                # Create FAISS index
                vectorstore = create_faiss_index(chunks)
                st.session_state.vectorstore = vectorstore

                # Initialize chat model
                chat_model = get_chat_model(EURI_API_KEY)
                st.session_state.chat_model = chat_model

                st.success("Documents processed successfully!")
                st.markdown("Chat with your document")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

# Chat input
if prompt := st.chat_input("Ask about your documents..."):
    # Add user message to chat history
    timestamp = time.strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)

    # Process assistant response only if vectorstore and chat model are available
    if st.session_state.vectorstore and st.session_state.chat_model:
        with st.chat_message("assistant"):
            with st.spinner("Searching documents..."):
                relevant_docs = retrieve_relevant_docs(
                    st.session_state.vectorstore, prompt
                )

                context = "\n\n".join([doc.page_content for doc in relevant_docs])

                system_prompt = f"""You are DocuPro, an intelligent document assistant.
                Based on the following documents, provide accurate and helpful answers.
                If the information is not in the documents, clearly state that.

                Document:
                {context}

                User Question: {prompt}

                Answer:"""
            
            response = ask_chat_model(st.session_state.chat_model, system_prompt)
            st.markdown(response)
            st.caption(timestamp)


