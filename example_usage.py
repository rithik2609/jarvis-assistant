"""
Example usage script for JARVIS Assistant
This script demonstrates how to use the ingestion and RAG components programmatically
"""
import os
from ingestion import DocumentIngestion
from rag_assistant import RAGAssistant


def example_ingestion():
    """Example: Ingest documents programmatically"""
    print("=" * 50)
    print("EXAMPLE: Document Ingestion")
    print("=" * 50)
    
    ingestion = DocumentIngestion()
    
    # Example: Ingest a single file
    # ingestion.ingest_file("path/to/your/file.pdf", "my_notes.pdf")
    
    # Example: Batch ingest all files from a folder
    folder_path = "data"  # Change this to your folder path
    
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                ingestion.ingest_file(file_path, filename)
    else:
        print(f"Folder {folder_path} does not exist. Create it and add files.")


def example_chat():
    """Example: Chat with JARVIS programmatically"""
    print("\n" + "=" * 50)
    print("EXAMPLE: Chat with JARVIS")
    print("=" * 50)
    
    assistant = RAGAssistant()
    
    # Example queries
    queries = [
        "What are the main topics in my notes?",
        "Can you summarize the key points?",
        "What did I write about AI?"
    ]
    
    for query in queries:
        print(f"\n📝 Query: {query}")
        response = assistant.chat(query)
        print(f"🤖 Answer: {response['answer']}")
        if response['sources']:
            print(f"📚 Sources: {', '.join(set(response['sources']))}")
        print("-" * 50)


def interactive_chat():
    """Interactive chat session"""
    print("\n" + "=" * 50)
    print("INTERACTIVE CHAT MODE")
    print("=" * 50)
    print("Type 'quit' or 'exit' to end the session\n")
    
    assistant = RAGAssistant()
    
    while True:
        query = input("You: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! 👋")
            break
        
        if not query:
            continue
        
        response = assistant.chat(query)
        print(f"\nJARVIS: {response['answer']}")
        
        if response['sources']:
            print(f"[Sources: {', '.join(set(response['sources']))}]")
        print()


if __name__ == "__main__":
    # Uncomment the function you want to run
    
    # example_ingestion()
    # example_chat()
    interactive_chat()
