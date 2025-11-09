"""
RAG (Retrieval Augmented Generation) Module
Handles retrieving relevant context and generating responses
"""
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone
import config
from llm_handler import LLMHandler


class RAGAssistant:
    def __init__(self):
        """Initialize RAG assistant"""
        self.embeddings = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        
        self.llm_handler = LLMHandler()
        
        # Initialize Pinecone
        self.pc = None
        self.index = None
        if config.PINECONE_API_KEY:
            self._init_pinecone()
    
    def _init_pinecone(self):
        """Initialize Pinecone connection"""
        try:
            self.pc = Pinecone(api_key=config.PINECONE_API_KEY)
            self.index = self.pc.Index(config.PINECONE_INDEX_NAME)
            print(f"✅ RAG connected to Pinecone index: {config.PINECONE_INDEX_NAME}")
        except Exception as e:
            print(f"⚠️ Pinecone initialization error: {e}")
    
    def retrieve_context(self, query: str, top_k: int = None) -> List[dict]:
        """Retrieve relevant context from Pinecone"""
        if not self.index:
            print("⚠️ Pinecone index not available")
            return []
        
        if top_k is None:
            top_k = config.TOP_K_RESULTS
        
        try:
            # Create query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Search Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Extract relevant information
            contexts = []
            for match in results['matches']:
                contexts.append({
                    'text': match['metadata'].get('text', ''),
                    'source': match['metadata'].get('source', 'Unknown'),
                    'score': match['score']
                })
            
            return contexts
        except Exception as e:
            print(f"❌ Error retrieving context: {e}")
            return []
    
    def format_context(self, contexts: List[dict]) -> str:
        """Format retrieved contexts into a string"""
        if not contexts:
            return "No relevant information found in your notes."
        
        formatted = "Here's what I found in your notes:\n\n"
        for i, ctx in enumerate(contexts, 1):
            formatted += f"[Source: {ctx['source']}]\n{ctx['text']}\n\n"
        
        return formatted
    
    def generate_answer(self, query: str, contexts: List[dict]) -> str:
        """Generate answer using LLM with retrieved context"""
        if not self.llm_handler.is_available():
            # If no LLM, just return the context
            return self.format_context(contexts)
        
        # Create prompt with context
        context_text = "\n\n".join([ctx['text'] for ctx in contexts])
        
        prompt = f"""You are JARVIS, a helpful personal assistant. Answer the user's question based on the provided context from their notes.

Context from notes:
{context_text}

User Question: {query}

Instructions:
- Answer based primarily on the provided context
- If the context doesn't contain enough information, say so
- Be concise and helpful
- Cite sources when relevant

Answer:"""
        
        # Generate response
        response = self.llm_handler.generate_response(prompt)
        return response
    
    def chat(self, query: str) -> dict:
        """Main chat function that retrieves context and generates response"""
        print(f"💬 Processing query: {query}")
        
        # Retrieve relevant context
        contexts = self.retrieve_context(query)
        
        # Generate answer
        answer = self.generate_answer(query, contexts)
        
        return {
            'query': query,
            'answer': answer,
            'sources': [ctx['source'] for ctx in contexts],
            'num_sources': len(contexts)
        }
