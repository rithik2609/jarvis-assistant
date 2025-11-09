"""
JARVIS - Personal AI Assistant
Streamlit UI for chatbot interface and file upload
"""
import streamlit as st
import os
from pathlib import Path
import config
from ingestion import DocumentIngestion
from rag_assistant import RAGAssistant


# Page configuration
st.set_page_config(
    page_title="JARVIS - Personal AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'assistant' not in st.session_state:
    st.session_state.assistant = None

if 'ingestion' not in st.session_state:
    st.session_state.ingestion = None


def initialize_components():
    """Initialize RAG assistant and ingestion"""
    if st.session_state.assistant is None:
        with st.spinner("Initializing JARVIS..."):
            st.session_state.assistant = RAGAssistant()
            st.session_state.ingestion = DocumentIngestion()
    return st.session_state.assistant, st.session_state.ingestion


def save_uploaded_file(uploaded_file):
    """Save uploaded file to disk"""
    upload_dir = Path(config.UPLOAD_DIR)
    upload_dir.mkdir(exist_ok=True)
    
    file_path = upload_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return str(file_path)


def main():
    # Header
    st.title("🤖 JARVIS - Personal AI Assistant")
    st.markdown("Your intelligent assistant powered by RAG and LLaMA")
    
    # Initialize components
    assistant, ingestion = initialize_components()
    
    # Sidebar for file upload and settings
    with st.sidebar:
        st.header("📁 Knowledge Base")
        
        # File upload
        st.subheader("Upload Documents")
        uploaded_files = st.file_uploader(
            "Upload your notes (PDF, DOCX, TXT)",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Upload documents to add to JARVIS's knowledge base"
        )
        
        if uploaded_files:
            if st.button("Process Files", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for idx, uploaded_file in enumerate(uploaded_files):
                    status_text.text(f"Processing {uploaded_file.name}...")
                    
                    # Save file
                    file_path = save_uploaded_file(uploaded_file)
                    
                    # Ingest file
                    ingestion.ingest_file(file_path, uploaded_file.name)
                    
                    # Update progress
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                status_text.text("✅ All files processed!")
                st.success(f"Successfully processed {len(uploaded_files)} file(s)")
        
        st.divider()
        
        # Settings
        st.subheader("⚙️ Settings")
        
        # Check Pinecone connection
        if ingestion and ingestion.index:
            st.success("✅ Pinecone Connected")
        else:
            st.warning("⚠️ Pinecone Not Connected")
        
        # Check LLM availability
        if assistant and assistant.llm_handler.is_available():
            st.success(f"✅ LLM Ready ({assistant.llm_handler.llm_type})")
        else:
            st.warning("⚠️ LLM Not Available")
            st.info("Install Ollama and run: `ollama pull llama2`")
        
        st.divider()
        
        # Clear chat history
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        
        # Information
        with st.expander("ℹ️ About JARVIS"):
            st.markdown("""
            **JARVIS** is your personal AI assistant that:
            - 📚 Learns from your uploaded documents
            - 🔍 Retrieves relevant information using vector search
            - 💬 Answers questions using AI
            - 🧠 Remembers context from your notes
            
            **How to use:**
            1. Upload your notes (PDF, DOCX, or TXT)
            2. Click "Process Files"
            3. Start chatting!
            """)
    
    # Main chat interface
    st.header("💬 Chat with JARVIS")
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message and message["sources"]:
                    with st.expander("📚 Sources"):
                        for source in set(message["sources"]):
                            st.markdown(f"- {source}")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your notes..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = assistant.chat(prompt)
                st.markdown(response['answer'])
                
                if response['sources']:
                    with st.expander("📚 Sources"):
                        for source in set(response['sources']):
                            st.markdown(f"- {source}")
        
        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response['answer'],
            "sources": response['sources']
        })
    
    # Welcome message for new users
    if len(st.session_state.messages) == 0:
        st.info("👋 Welcome! Upload your documents in the sidebar to get started, then ask me anything!")


if __name__ == "__main__":
    main()
