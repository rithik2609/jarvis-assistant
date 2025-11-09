# 🚀 JARVIS Installation & Testing Guide

## Complete Installation Steps

### 1. Verify Python Installation

```powershell
python --version
# Should show Python 3.8 or higher
```

If Python is not installed, download from: https://www.python.org/downloads/

### 2. Create Virtual Environment

```powershell
# Navigate to project directory
cd d:\Projects\jarvis-assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies

```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# This will install:
# - streamlit (UI framework)
# - langchain (LLM framework)
# - pinecone-client (vector database)
# - sentence-transformers (embeddings)
# - pypdf, python-docx (document parsing)
# - ollama (local LLM)
```

### 4. Set Up Pinecone

#### Create Account
1. Go to https://www.pinecone.io/
2. Click "Sign Up" (free tier available)
3. Verify your email
4. Log in to the console

#### Create API Key
1. Go to "API Keys" section
2. Click "Create API Key"
3. Copy the key (you'll need this for .env)
4. Note your environment (e.g., "us-east-1")

### 5. Set Up Ollama (Local LLaMA)

#### Install Ollama
1. Go to https://ollama.ai/
2. Download the Windows installer
3. Run the installer
4. Verify installation:
   ```powershell
   ollama --version
   ```

#### Download LLaMA Model
```powershell
# Pull llama2 model (this will take a few minutes, ~4GB download)
ollama pull llama2

# Verify it's downloaded
ollama list

# Test it
ollama run llama2 "Hello, how are you?"
```

#### Alternative Models
```powershell
# Faster, smaller model
ollama pull phi

# More capable model (larger)
ollama pull mistral

# Code-focused model
ollama pull codellama
```

### 6. Configure Environment

```powershell
# Copy the example environment file
copy .env.example .env

# Edit .env with your favorite text editor
notepad .env
```

Add your credentials:
```env
PINECONE_API_KEY=pcsk_xxxxx_your_actual_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=jarvis-assistant
OLLAMA_MODEL=llama2
```

### 7. Run Environment Check

```powershell
python utils.py
```

This will verify:
- ✅ All Python packages are installed
- ✅ .env file is configured
- ✅ Pinecone credentials are valid
- ✅ Ollama is running
- ✅ LLaMA model is available

### 8. Launch JARVIS

```powershell
streamlit run app.py
```

Your browser should automatically open to: http://localhost:8501

## 🧪 Testing JARVIS

### Test 1: Basic Functionality

1. **Start the app**: `streamlit run app.py`
2. **Check status**: Look at the sidebar
   - Should show "✅ Pinecone Connected"
   - Should show "✅ LLM Ready (ollama)"

### Test 2: Upload Sample Document

1. The project includes a sample file: `data/sample_notes.txt`
2. In the sidebar, click "Browse files"
3. Select `data/sample_notes.txt`
4. Click "Process Files"
5. Wait for confirmation: "✅ Successfully processed 1 file(s)"

### Test 3: Ask Questions

Try these queries:

**Query 1**: "What is my name?"
- Expected: Should return "Alex Johnson" from the sample notes

**Query 2**: "What projects am I working on?"
- Expected: Should list JARVIS Assistant, Weather Dashboard, and Task Manager

**Query 3**: "What are my skills?"
- Expected: Should mention Python, JavaScript, AI/ML, etc.

**Query 4**: "What are my goals for 2025?"
- Expected: Should list the goals from the sample notes

### Test 4: Upload Your Own Document

1. Create a simple text file with your own notes
2. Upload it through the UI
3. Process it
4. Ask questions about your content

## 🐛 Common Issues & Solutions

### Issue: "Execution policy error"
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Pinecone not connected"
**Symptoms**: Red warning in sidebar
**Solutions**:
1. Check your API key in `.env`
2. Verify internet connection
3. Check Pinecone console is accessible
4. Try creating a new API key

### Issue: "Ollama not found"
**Symptoms**: Warning about Ollama
**Solutions**:
```powershell
# Check if Ollama is installed
ollama --version

# If not, download from https://ollama.ai/

# If installed, start the service
ollama serve

# In another terminal, pull the model
ollama pull llama2
```

### Issue: "LLM Not Available"
**Symptoms**: Warning in sidebar
**Solutions**:
1. Make sure Ollama is running: `ollama serve`
2. Check model is downloaded: `ollama list`
3. Verify OLLAMA_MODEL in .env matches downloaded model
4. Alternative: Use OpenAI by adding OPENAI_API_KEY to .env

### Issue: "Module not found" errors
**Solution**:
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall requirements
pip install -r requirements.txt --upgrade
```

### Issue: No responses from chatbot
**Symptoms**: Questions don't get answered
**Solutions**:
1. Upload and process documents first
2. Check Pinecone has data: `python utils.py`
3. Verify LLM is working
4. Check terminal for error messages

### Issue: "Too slow" responses
**Solutions**:
1. Use a smaller/faster Ollama model:
   ```powershell
   ollama pull phi
   # Update .env: OLLAMA_MODEL=phi
   ```
2. Reduce TOP_K_RESULTS in config.py
3. Use smaller documents
4. Consider using OpenAI API instead

## 📊 Monitoring & Logs

### View Streamlit Logs
The terminal where you ran `streamlit run app.py` shows all logs

### Check Pinecone Index
```powershell
python utils.py
```
Shows number of vectors stored

### Test Ollama Directly
```powershell
ollama run llama2 "What is AI?"
```

## 🔄 Updates & Maintenance

### Update Dependencies
```powershell
pip install -r requirements.txt --upgrade
```

### Clear Pinecone Index
If you want to start fresh:
1. Go to Pinecone console
2. Delete the index "jarvis-assistant"
3. Restart the app (it will recreate it)

### Change LLM Model
Edit `.env`:
```env
OLLAMA_MODEL=mistral  # or phi, codellama, etc.
```

## 🎓 Next Steps

After successful testing:

1. **Add Your Own Documents**
   - Upload PDFs, DOCX, or TXT files
   - Process them through the UI
   - Start asking questions!

2. **Customize Configuration**
   - Edit `config.py` to adjust chunk sizes
   - Change number of results retrieved
   - Modify embedding models

3. **Explore Advanced Features**
   - Try `example_usage.py` for programmatic access
   - Batch upload multiple documents
   - Experiment with different LLM models

4. **Share Your Assistant**
   - Export your configuration
   - Document your use cases
   - Share with others!

## 📞 Getting Help

If you encounter issues:

1. Check the terminal logs for error messages
2. Run `python utils.py` to diagnose issues
3. Review the README.md for detailed info
4. Check Ollama logs: `ollama logs`
5. Verify Pinecone console for index status

---

**Congratulations!** 🎉

You now have a fully functional personal AI assistant powered by RAG, LLaMA, and Pinecone!
