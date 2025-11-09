"""
Utility functions for JARVIS Assistant
"""
import os
from typing import List
from pathlib import Path


def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['data', 'uploaded_files']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")


def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment configuration...\n")
    
    issues = []
    warnings = []
    
    # Check .env file
    if not os.path.exists('.env'):
        issues.append("❌ .env file not found. Copy .env.example to .env")
    else:
        print("✅ .env file exists")
        
        # Check environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check Pinecone
        if not os.getenv('PINECONE_API_KEY'):
            issues.append("❌ PINECONE_API_KEY not set in .env")
        else:
            print("✅ PINECONE_API_KEY is set")
        
        if not os.getenv('PINECONE_ENVIRONMENT'):
            warnings.append("⚠️ PINECONE_ENVIRONMENT not set (will use default)")
        else:
            print("✅ PINECONE_ENVIRONMENT is set")
    
    # Check Ollama
    import subprocess
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Ollama is installed and running")
            if 'llama2' in result.stdout:
                print("✅ llama2 model is available")
            else:
                warnings.append("⚠️ llama2 model not found. Run: ollama pull llama2")
        else:
            warnings.append("⚠️ Ollama installed but not running properly")
    except FileNotFoundError:
        warnings.append("⚠️ Ollama not found. Install from https://ollama.ai/")
    except Exception as e:
        warnings.append(f"⚠️ Could not check Ollama: {e}")
    
    # Check Python packages
    try:
        import streamlit
        print("✅ Streamlit installed")
    except ImportError:
        issues.append("❌ Streamlit not installed. Run: pip install -r requirements.txt")
    
    try:
        import pinecone
        print("✅ Pinecone client installed")
    except ImportError:
        issues.append("❌ Pinecone not installed. Run: pip install -r requirements.txt")
    
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        print("✅ LangChain installed")
    except ImportError:
        issues.append("❌ LangChain not installed. Run: pip install -r requirements.txt")
    
    # Summary
    print("\n" + "=" * 50)
    if issues:
        print("🚨 CRITICAL ISSUES:")
        for issue in issues:
            print(f"  {issue}")
    
    if warnings:
        print("\n⚠️ WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not issues and not warnings:
        print("✅ ALL CHECKS PASSED! You're ready to run JARVIS!")
    elif not issues:
        print("\n✅ No critical issues. JARVIS can run but with limited features.")
    else:
        print("\n❌ Please fix the critical issues before running JARVIS.")
    
    print("=" * 50)


def list_uploaded_files() -> List[str]:
    """List all uploaded files"""
    upload_dir = Path('uploaded_files')
    if not upload_dir.exists():
        return []
    
    files = []
    for file_path in upload_dir.iterdir():
        if file_path.is_file():
            files.append(str(file_path))
    
    return files


def get_index_stats():
    """Get statistics about the Pinecone index"""
    try:
        from pinecone import Pinecone
        import config
        
        if not config.PINECONE_API_KEY:
            print("❌ Pinecone API key not configured")
            return
        
        pc = Pinecone(api_key=config.PINECONE_API_KEY)
        index = pc.Index(config.PINECONE_INDEX_NAME)
        stats = index.describe_index_stats()
        
        print("📊 Pinecone Index Statistics:")
        print(f"  Total vectors: {stats.get('total_vector_count', 0)}")
        print(f"  Dimension: {stats.get('dimension', 'N/A')}")
        print(f"  Index fullness: {stats.get('index_fullness', 0)}")
        
    except Exception as e:
        print(f"❌ Error getting index stats: {e}")


if __name__ == "__main__":
    print("🤖 JARVIS Assistant - Utility Script\n")
    
    # Create directories
    create_directories()
    print()
    
    # Check environment
    check_environment()
    print()
    
    # Show uploaded files
    files = list_uploaded_files()
    if files:
        print(f"📁 Uploaded files ({len(files)}):")
        for f in files:
            print(f"  - {f}")
    else:
        print("📁 No uploaded files yet")
    print()
    
    # Get index stats
    get_index_stats()
