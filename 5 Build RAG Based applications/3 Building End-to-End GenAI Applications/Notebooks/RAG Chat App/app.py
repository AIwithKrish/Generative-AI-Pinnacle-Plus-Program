"""Streamlit App for RAG Chat

A web application for interacting with documents using Retrieval-Augmented Generation (RAG).
Users can upload PDF or text files and ask questions about their content.
"""

import os
import streamlit as st
from pathlib import Path
import tempfile
from rag_pipeline import RAGPipeline


# Page configuration
st.set_page_config(
    page_title="RAG Chat App",
    page_icon="RAG",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        color: #1f77b4;
        text-align: center;
        padding: 20px 0;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #1f77b4;
        padding: 12px;
        margin-bottom: 20px;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 12px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False


def initialize_rag_pipeline():
    """Initialize the RAG pipeline with API key."""
    api_key = st.session_state.get("api_key", "").strip() or os.getenv("OPENAI_API_KEY")

    if not api_key:
        st.error("OpenAI API Key is required. Please enter it in the sidebar.")
        return False

    try:
        if st.session_state.rag_pipeline is None:
            st.session_state.rag_pipeline = RAGPipeline(openai_api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error initializing RAG pipeline: {str(e)}")
        return False


def load_documents(uploaded_files):
    """Load and process uploaded documents."""
    if not uploaded_files:
        st.warning("No files selected.")
        return False

    try:
        with st.spinner("Processing documents..."):
            rag = st.session_state.rag_pipeline

            for uploaded_file in uploaded_files:
                # Create a temporary file to store the upload
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_path = tmp_file.name

                try:
                    # Load based on file type
                    if uploaded_file.type == "application/pdf":
                        rag.load_pdf(tmp_path)
                        st.success(f"Loaded PDF: {uploaded_file.name}")
                    elif uploaded_file.type == "text/plain":
                        rag.load_text_file(tmp_path)
                        st.success(f"Loaded Text: {uploaded_file.name}")
                    else:
                        st.warning(f"Unsupported file type: {uploaded_file.name}")
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(tmp_path)
                    except:
                        pass

            # Process documents
            with st.spinner("Splitting documents and creating embeddings..."):
                rag.split_documents(chunk_size=1000, chunk_overlap=200)
                rag.create_vector_store()
                rag.setup_chain(model_name="gpt-3.5-turbo", temperature=0.7)

            st.session_state.documents_loaded = True
            st.success("Documents processed successfully!")
            return True

    except Exception as e:
        st.error(f"Error loading documents: {str(e)}")
        return False


def chat_interface():
    """Display the chat interface."""
    st.subheader("Ask Questions About Your Documents")

    # Chat history display
    if st.session_state.chat_history:
        st.markdown("### Conversation History")
        for i, msg in enumerate(st.session_state.chat_history):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Input area
    user_input = st.chat_input("Ask a question about your documents...")

    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response
        try:
            with st.spinner("Thinking..."):
                response = st.session_state.rag_pipeline.query(user_input)
                answer = response.get("answer", "No answer generated")

                # Add assistant message to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

                # Display assistant message
                with st.chat_message("assistant"):
                    st.markdown(answer)

                    # Show context sources
                    with st.expander("View Source Context"):
                        context = response.get("context", [])
                        if context:
                            for i, doc in enumerate(context, 1):
                                st.markdown(f"**Source {i}:**")
                                st.markdown(doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content)
                                st.divider()
                        else:
                            st.info("No source context available")

        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            # Remove the user message if there was an error
            st.session_state.chat_history.pop()


def main():
    """Main application function."""
    # Header
    st.markdown('<h1 class="main-header">RAG Chat Application</h1>', unsafe_allow_html=True)
    st.markdown("**Chat with your documents using AI-powered RAG (Retrieval-Augmented Generation)**")

    # Sidebar
    with st.sidebar:
        st.markdown("### Configuration")

        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Enter your OpenAI API key. You can get one from https://platform.openai.com/api-keys"
        )

        if api_key:
            st.session_state.api_key = api_key

        st.divider()

        st.markdown("### Upload Documents")
        st.markdown("""
        Upload PDF or text files containing the information you want to ask questions about.
        The app will process and index them for quick retrieval.
        """)

        uploaded_files = st.file_uploader(
            "Choose files",
            type=["pdf", "txt"],
            accept_multiple_files=True,
            help="Supported formats: PDF and TXT"
        )

        if st.button("Load Documents", use_container_width=True):
            if not api_key:
                st.error("Please enter your OpenAI API Key first")
            elif initialize_rag_pipeline():
                load_documents(uploaded_files)

        st.divider()

        # Settings
        st.markdown("### Advanced Settings")

        model_choice = st.selectbox(
            "Select Model",
            ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            help="Choose the OpenAI model to use"
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Higher values = more creative, Lower values = more accurate"
        )

        # Display status
        st.divider()
        st.markdown("### Status")

        if st.session_state.documents_loaded:
            st.markdown('<div class="success-box">Documents loaded and indexed</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">Upload documents to get started</div>', unsafe_allow_html=True)

        # Clear chat history button
        if st.button("Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()

    # Main content area
    if not st.session_state.documents_loaded:
        st.info("**Get started:** Upload your documents in the sidebar to begin")

        # Show sample information
        with st.expander("How to use this app"):
            st.markdown("""
            1. **Enter API Key:** Add your OpenAI API key in the sidebar
            2. **Upload Documents:** Select PDF or TXT files containing your data
            3. **Load Documents:** Click "Load Documents" to process and index them
            4. **Ask Questions:** Use the chat interface to ask questions about your documents
            5. **View Sources:** Check the source context to see which parts of documents were used

            ### Features:
            - Support for PDF and TXT files
            - Intelligent document retrieval
            - Natural conversation interface
            - Source attribution for answers
            - Configurable AI model and creativity settings
            """)
    else:
        # Show chat interface
        chat_interface()


if __name__ == "__main__":
    main()
