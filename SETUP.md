# JARVIS Assistant - Quick Setup Guide

## 🎯 Step-by-Step Setup

Follow these steps to get JARVIS running on your Windows machine:

### Step 1: Install Python Dependencies

Open PowerShell in this directory and run:

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt
```

### Step 2: Set Up Pinecone

1. Visit: https://www.pinecone.io/
2. Sign up for a free account
3. Create a new API key
4. Note your environment (region)

### Step 3: Set Up Ollama (Local LLaMA)

1. Download Ollama from: https://ollama.ai/
2. Install it
3. Open a new PowerShell window and run:
   ```powershell
   ollama pull llama2
   ```
4. Wait for the model to download (~4GB)

### Step 4: Configure Environment

1. Copy the environment template:
   ```powershell
   copy .env.example .env
   ```

2. Open `.env` in a text editor

3. Fill in your Pinecone credentials:
   ```
   PINECONE_API_KEY=your_api_key_here
   PINECONE_ENVIRONMENT=us-east-1
   PINECONE_INDEX_NAME=jarvis-assistant
   ```

### Step 5: Run JARVIS

```powershell
streamlit run app.py
```

Your browser will open to http://localhost:8501

### Step 6: Upload Your First Document

1. Click on the sidebar
2. Upload a PDF, DOCX, or TXT file
3. Click "Process Files"
4. Start asking questions!

## 🆘 Quick Troubleshooting

### "Module not found" errors
```powershell
pip install -r requirements.txt --upgrade
```

### Ollama not working
```powershell
# Check if Ollama is running
ollama list

# If not, start it
ollama serve
```

### Pinecone connection issues
- Double-check your API key in `.env`
- Make sure you have internet connection
- Verify your environment region is correct

## 🎓 First Time Using?

Try uploading a simple text file with some notes about yourself, your projects, or any topic. Then ask JARVIS questions about that content!

Example:
- Upload: `my_notes.txt` containing information about your projects
- Ask: "What projects am I working on?"
- JARVIS will search your notes and answer!

## 📞 Need Help?

Check the full README.md for detailed information and advanced usage.
