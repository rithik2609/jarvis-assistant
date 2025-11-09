# 🤖 JARVIS - Personal AI Assistant

A personal AI assistant powered by RAG (Retrieval Augmented Generation) that can learn from your documents and answer questions based on your notes.

![Architecture](https://i.imgur.com/placeholder.png)

## 🌟 Features

- 📚 **Document Ingestion**: Upload and process PDF, DOCX, and TXT files
- 🔍 **Vector Search**: Fast and accurate retrieval using Pinecone
- 🧠 **AI-Powered Responses**: Uses LLaMA (via Ollama) or OpenAI for intelligent answers
- 💬 **Conversational Interface**: Clean and intuitive Streamlit chat UI
- 🎯 **Context-Aware**: Retrieves relevant information from your notes
- 📊 **Source Attribution**: Shows which documents were used to answer questions

## 🏗️ Architecture

The system follows a RAG (Retrieval Augmented Generation) pattern:

1. **Ingestion**: Documents are read, chunked, and embedded
2. **Storage**: Embeddings are stored in Pinecone vector database
3. **Retrieval**: User queries are embedded and similar chunks are retrieved
4. **Generation**: LLM uses retrieved context to generate accurate answers

## 📋 Prerequisites

- Python 3.8 or higher
- Pinecone account (free tier available)
- Ollama installed (for local LLaMA) OR OpenAI API key

## 🚀 Quick Start

### 1. Clone or Download the Project

```bash
cd d:\Projects\jarvis-assistant
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows CMD:
.\venv\Scripts\activate.bat

# Install required packages
pip install -r requirements.txt
```

### 3. Set Up Pinecone

1. Go to [Pinecone](https://www.pinecone.io/) and create a free account
2. Create a new API key
3. Note your environment (e.g., `us-east-1`)

### 4. Set Up LLM (Choose One)

#### Option A: Ollama (Recommended - Free & Local)

1. Download and install [Ollama](https://ollama.ai/)
2. Pull the LLaMA model:
   ```bash
   ollama pull llama2
   ```
3. Verify it's running:
   ```bash
   ollama list
   ```

#### Option B: OpenAI (Cloud-based)

1. Get an API key from [OpenAI](https://platform.openai.com/)
2. You'll use this in the next step

### 5. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```env
   # Required: Pinecone Configuration
   PINECONE_API_KEY=your_actual_api_key_here
   PINECONE_ENVIRONMENT=us-east-1
   PINECONE_INDEX_NAME=jarvis-assistant

   # For Ollama (local LLaMA)
   OLLAMA_MODEL=llama2

   # OR for OpenAI (if not using Ollama)
   # OPENAI_API_KEY=your_openai_api_key_here
   ```

### 6. Run JARVIS

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Upload Documents

1. Click on the sidebar
2. Use the "Upload Documents" section
3. Select your PDF, DOCX, or TXT files
4. Click "Process Files"
5. Wait for confirmation

### Chat with JARVIS

1. Type your question in the chat input at the bottom
2. Press Enter or click Send
3. JARVIS will:
   - Search your uploaded documents
   - Retrieve relevant information
   - Generate a contextual answer
4. Click "Sources" to see which documents were used

### Tips for Best Results

- **Be specific**: Ask clear, focused questions
- **Upload organized notes**: Better organization = better answers
- **Check sources**: Review which documents were referenced
- **Iterative questioning**: Ask follow-up questions for more details

## 📁 Project Structure

```
jarvis-assistant/
├── app.py                  # Streamlit UI application
├── config.py              # Configuration settings
├── ingestion.py           # Document ingestion module
├── llm_handler.py         # LLM integration
├── rag_assistant.py       # RAG logic and chat handler
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 Configuration Options

Edit `config.py` to customize:

- **CHUNK_SIZE**: Size of text chunks (default: 1000)
- **CHUNK_OVERLAP**: Overlap between chunks (default: 200)
- **TOP_K_RESULTS**: Number of results to retrieve (default: 3)
- **EMBEDDING_MODEL**: Embedding model to use

## 🐛 Troubleshooting

### Pinecone Connection Issues

- Verify your API key is correct
- Check your environment/region setting
- Ensure you have internet connection

### Ollama Not Working

- Make sure Ollama is installed and running
- Check that llama2 model is downloaded: `ollama list`
- Try running: `ollama serve` in a separate terminal

### Import Errors

- Ensure you're in the virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

### No Context Retrieved

- Make sure you've uploaded and processed documents
- Check that Pinecone index has data
- Try asking questions differently

## 🔐 Security Notes

- **Never commit `.env`** to version control
- Keep your API keys secret
- Use environment variables for all credentials
- The `.gitignore` file is configured to exclude sensitive files

## 🚀 Advanced Features

### Using Different LLM Models

Edit your `.env`:
```env
# For different Ollama models
OLLAMA_MODEL=mistral
OLLAMA_MODEL=codellama
OLLAMA_MODEL=llama2:13b
```

### Batch Document Upload

Place multiple files in a folder and process them programmatically:

```python
from ingestion import DocumentIngestion
import os

ingestion = DocumentIngestion()
folder_path = "path/to/your/documents"

for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    ingestion.ingest_file(file_path)
```

## 📚 Dependencies

- **Streamlit**: Web UI framework
- **LangChain**: LLM application framework
- **Pinecone**: Vector database
- **Ollama**: Local LLM runtime
- **Sentence Transformers**: Embedding generation
- **PyPDF/python-docx**: Document parsing

## 🤝 Contributing

Feel free to fork, modify, and enhance this project! Some ideas:

- Add support for more file types
- Implement conversation memory
- Add voice interface
- Create API endpoints
- Enhance UI/UX

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Meta AI for LLaMA
- Pinecone for vector database
- LangChain community
- Streamlit team

---

**Happy chatting with JARVIS! 🤖**

For issues or questions, please create an issue in the repository.
