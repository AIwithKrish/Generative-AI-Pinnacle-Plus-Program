# RAG Chat App with LangChain + Streamlit

A modern, production-ready Retrieval-Augmented Generation (RAG) chat application built with LangChain and Streamlit. Ask questions about your documents and get intelligent answers backed by actual document content.

## Features

 **Core Features:**
- Upload and process PDF and text files
- AI-powered question answering using GPT models
- Intelligent document retrieval and ranking
- Interactive chat interface with history
- Source attribution - see which parts of documents were used
- Configurable model selection and creativity settings
- Latest LangChain APIs for stability and compatibility

## Project Structure

```
RAG Chat App/
 app.py # Main Streamlit application
 rag_pipeline.py # RAG pipeline implementation
 requirements.txt # Python dependencies
 .env # Environment variables (API keys)
 data/ # Directory for storing documents (optional)
 README.md # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (get from https://platform.openai.com/api-keys)

### Setup Steps

1. **Clone or navigate to the project directory:**
 ```bash
 cd "RAG Chat App"
 ```

2. **Create a virtual environment (optional but recommended):**
 ```bash
 python -m venv .venv
 source .venv/bin/activate # On Windows: .venv\Scripts\activate
 ```

3. **Install dependencies:**
 ```bash
 pip install -r requirements.txt
 ```

4. **Configure environment variables:**
 - Open `.env` file
 - Replace `your_openai_api_key_here` with your actual OpenAI API key
 ```
 OPENAI_API_KEY=sk-your-actual-key-here
 ```

## Usage

### Running the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Using the App

1. **Enter API Key:**
 - Paste your OpenAI API key in the sidebar (or it will use the .env file)

2. **Upload Documents:**
 - Click "Choose files" in the sidebar
 - Select PDF or TXT files
 - Supported formats: `.pdf`, `.txt`

3. **Load Documents:**
 - Click the "Load Documents" button
 - Wait for processing to complete
 - The app will split documents, create embeddings, and index them

4. **Ask Questions:**
 - Type your question in the chat input
 - Press Enter to submit
 - The AI will search your documents and provide an answer

5. **View Sources:**
 - Click "View Source Context" to see which document sections were used

## Configuration Options

In the sidebar, you can configure:

- **Model Selection:** Choose between GPT-3.5-turbo, GPT-4, or GPT-4-turbo
- **Temperature:** Adjust the creativity level (0.0 = precise, 2.0 = creative)
- **Clear History:** Remove chat history and start fresh

## Dependencies

Latest LangChain packages used (March 2026):
- `streamlit` - Web application framework
- `langchain` - Core LLM framework
- `langchain-openai` - OpenAI integration
- `langchain-community` - Additional loaders and vectorstores
- `faiss-cpu` - Vector similarity search
- `pypdf` - PDF document processing
- `python-dotenv` - Environment variable management
- `openai` - OpenAI API client
- `tiktoken` - Token counting for OpenAI models

## How RAG Works

**Retrieval-Augmented Generation** is a technique that combines:

1. **Document Retrieval:** When you ask a question, the system searches your documents for relevant content
2. **Augmentation:** The retrieved documents are combined with your question
3. **Generation:** An LLM generates an answer based on both the question and document context

This approach ensures answers are grounded in your actual documents, reducing hallucination and improving accuracy.

## API Costs

This app uses OpenAI's API, which is a paid service:
- **Embeddings:** $0.02 per 1M tokens
- **GPT-3.5-turbo:** $0.50 per 1M input tokens, $1.50 per 1M output tokens
- **GPT-4:** More expensive but more capable

Monitor your usage at https://platform.openai.com/account/billing/usage

## Troubleshooting

### Issue: "OPENAI_API_KEY not found"
- **Solution:** Make sure your `.env` file has the correct API key, or enter it in the sidebar

### Issue: "Module not found" errors
- **Solution:** Ensure all packages are installed: `pip install -r requirements.txt`

### Issue: "PDF loading fails"
- **Solution:** Ensure the PDF file is not corrupted and is text-based (not image-only)

### Issue: "Slow responses"
- **Solution:** 
 - Reduce the number of documents loaded
 - Use GPT-3.5-turbo instead of GPT-4
 - Lower the chunk size to get faster retrieval

## Performance Tips

1. **Optimize Document Size:**
 - Smaller, focused documents work better than large ones
 - Split large PDFs into chapters

2. **Adjust Chunk Size:**
 - Smaller chunks (500-1000) = faster retrieval but less context
 - Larger chunks (2000+) = more context but slower

3. **Model Selection:**
 - Use GPT-3.5-turbo for faster, cheaper responses
 - Use GPT-4 for complex questions requiring reasoning

4. **Caching:**
 - The app caches embeddings in the vector store
 - Reloading the same documents reuses the cache

## Advanced Usage

### Saving and Loading Vector Stores

You can save your indexed documents for reuse:

```python
# In Python code
from rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
pipeline.load_pdf("path/to/document.pdf")
pipeline.split_documents()
pipeline.create_vector_store()
pipeline.save_vector_store("./saved_vectors")

# Later, load it back
pipeline.load_vector_store("./saved_vectors")
pipeline.setup_chain()
```

### Customizing the Prompt

Edit the `system_prompt` in `rag_pipeline.py` to customize how the AI responds:

```python
system_prompt = """Your custom system prompt here...
Use the context to answer: {context}"""
```

## Security Notes

- Never commit your `.env` file to version control
- Add `.env` to your `.gitignore` file
- Keep your OpenAI API key confidential
- Regularly rotate your API key

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review LangChain documentation: https://python.langchain.com/
3. Check OpenAI API docs: https://platform.openai.com/docs/

## Updates & Compatibility

This code uses the latest LangChain APIs (2026 version) with:
- Updated import paths (`langchain_openai`, `langchain_community`)
- Latest document loaders and splitters
- Modern chat model interfaces
- Current retrieval chain patterns

All code has been tested for compatibility with the latest packages.
