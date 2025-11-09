# 🎯 JARVIS Quick Reference

## Quick Start Commands

```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Run JARVIS
streamlit run app.py

# 3. Check system health
python utils.py

# 4. Interactive chat (no UI)
python example_usage.py
```

## Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                    (Conversations)                           │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    JARVIS (app.py)                           │
│                  Streamlit Chat UI                           │
└───────────┬─────────────────────────────────┬───────────────┘
            │                                 │
            │ Upload Files                    │ Ask Questions
            ▼                                 ▼
┌─────────────────────┐            ┌──────────────────────────┐
│  Document Ingestion │            │    RAG Assistant         │
│   (ingestion.py)    │            │  (rag_assistant.py)      │
│                     │            │                          │
│ • Read files        │            │ • Retrieve context       │
│ • Chunk text        │            │ • Generate answers       │
│ • Create embeddings │            │ • Format responses       │
└──────────┬──────────┘            └───────┬──────────────────┘
           │                               │
           │ Store                         │ Query
           ▼                               ▼
┌─────────────────────────────────────────────────────────────┐
│               Vector Database (Pinecone)                     │
│          • Stores document embeddings                        │
│          • Fast semantic search                              │
└─────────────────────────────────────────────────────────────┘
                                           │
                                           │ Retrieved Context
                                           ▼
                                ┌──────────────────────┐
                                │   LLM (llm_handler)  │
                                │   • Ollama (LLaMA2)  │
                                │   • OpenAI (backup)  │
                                └──────────────────────┘
```

## File Overview

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit UI application |
| `config.py` | Configuration settings |
| `ingestion.py` | Document upload & processing |
| `llm_handler.py` | LLM integration (Ollama/OpenAI) |
| `rag_assistant.py` | RAG logic & chat handling |
| `utils.py` | Utility functions & health checks |
| `example_usage.py` | Command-line usage examples |
| `requirements.txt` | Python dependencies |
| `.env` | Environment variables (YOU CREATE THIS) |

## Environment Variables

```env
# Required
PINECONE_API_KEY=your_api_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=jarvis-assistant

# LLM (choose one)
OLLAMA_MODEL=llama2                    # For local LLaMA
# OR
OPENAI_API_KEY=your_openai_key_here   # For cloud OpenAI
```

## Key Configuration (config.py)

```python
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000          # Size of text chunks
CHUNK_OVERLAP = 200        # Overlap between chunks
TOP_K_RESULTS = 3          # Number of results to retrieve
```

## Supported File Types

- ✅ `.txt` - Plain text files
- ✅ `.pdf` - PDF documents
- ✅ `.docx` - Word documents

## Common Tasks

### Add Documents
```python
from ingestion import DocumentIngestion

ingest = DocumentIngestion()
ingest.ingest_file("path/to/file.pdf", "my_document.pdf")
```

### Query Programmatically
```python
from rag_assistant import RAGAssistant

assistant = RAGAssistant()
response = assistant.chat("What are my projects?")
print(response['answer'])
```

### Check System Status
```powershell
python utils.py
```

## Streamlit UI Features

### Sidebar
- 📁 File upload
- ⚙️ System status
- 🗑️ Clear chat
- ℹ️ About section

### Main Chat
- 💬 Conversational interface
- 📚 Source attribution
- 🔄 Real-time responses

## LLM Models

### Ollama Models (Local)
```powershell
ollama pull llama2      # Recommended, balanced
ollama pull phi         # Fastest, lighter
ollama pull mistral     # More capable
ollama pull codellama   # Best for code
```

### Model Comparison
| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| phi | 2.7GB | ⚡⚡⚡ | ⭐⭐ |
| llama2 | 3.8GB | ⚡⚡ | ⭐⭐⭐ |
| mistral | 4.1GB | ⚡⚡ | ⭐⭐⭐⭐ |
| llama2:13b | 7.3GB | ⚡ | ⭐⭐⭐⭐⭐ |

## Performance Tips

### Faster Responses
1. Use smaller model: `phi` or `llama2`
2. Reduce `TOP_K_RESULTS` in config
3. Use shorter documents
4. Consider OpenAI API

### Better Quality
1. Use larger model: `mistral` or `llama2:13b`
2. Increase `CHUNK_OVERLAP` for better context
3. Upload well-structured documents
4. Ask more specific questions

## Troubleshooting Checklist

- [ ] Virtual environment activated?
- [ ] All packages installed? (`pip list`)
- [ ] `.env` file created and configured?
- [ ] Pinecone API key valid?
- [ ] Ollama installed and running?
- [ ] LLaMA model downloaded?
- [ ] Documents uploaded and processed?
- [ ] Internet connection active?

## Useful Commands

```powershell
# Check what's running
Get-Process | Where-Object {$_.ProcessName -like "*ollama*"}

# Stop Streamlit
Ctrl + C (in the terminal)

# Restart with fresh cache
streamlit run app.py --server.headless true

# Check Ollama models
ollama list

# Test Ollama
ollama run llama2 "Hello"

# View uploaded files
ls uploaded_files

# View Pinecone stats
python -c "from utils import get_index_stats; get_index_stats()"
```

## Example Queries

### Personal Information
- "What is my name?"
- "What are my skills?"
- "What projects am I working on?"

### Specific Topics
- "Tell me about my AI projects"
- "What books do I like?"
- "What are my goals for 2025?"

### Summaries
- "Summarize my notes about machine learning"
- "What are the key points in my documents?"
- "Give me an overview of my interests"

## API Usage (Advanced)

```python
# Custom chunk size
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Custom retrieval
assistant = RAGAssistant()
contexts = assistant.retrieve_context("query", top_k=5)

# Direct LLM access
from llm_handler import LLMHandler

llm = LLMHandler()
response = llm.generate_response("Your prompt here")
```

## Resources

### Official Documentation
- Streamlit: https://docs.streamlit.io/
- LangChain: https://python.langchain.com/
- Pinecone: https://docs.pinecone.io/
- Ollama: https://ollama.ai/

### Learning Materials
- RAG Tutorial: Search "Retrieval Augmented Generation tutorial"
- Vector Databases: Pinecone learning center
- LLaMA Guide: Ollama documentation

### Community
- Streamlit Forum: https://discuss.streamlit.io/
- LangChain Discord: Via langchain.com
- GitHub Issues: Create in your repo

## Development Workflow

1. **Setup** (one time)
   - Install dependencies
   - Configure environment
   - Set up Pinecone & Ollama

2. **Daily Use**
   - Activate venv
   - Run `streamlit run app.py`
   - Upload documents
   - Chat with JARVIS

3. **Maintenance**
   - Update dependencies occasionally
   - Clear old uploaded files
   - Monitor Pinecone usage

---

## 🎉 You're Ready!

Start JARVIS with:
```powershell
streamlit run app.py
```

Happy chatting! 🤖
