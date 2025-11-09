"""
LLM Integration Module
Handles interaction with local LLaMA model via Ollama or OpenAI as fallback
"""
import config


class LLMHandler:
    def __init__(self):
        """Initialize LLM handler"""
        self.llm = None
        self._init_llm()
    
    def _init_llm(self):
        """Initialize the LLM (tries Ollama first, then OpenAI as fallback)"""
        try:
            # Try Ollama for local LLaMA
            from langchain_community.llms import Ollama
            self.llm = Ollama(model=config.OLLAMA_MODEL)
            # Test the connection
            self.llm.invoke("Hello")
            print(f"✅ Connected to Ollama with model: {config.OLLAMA_MODEL}")
            self.llm_type = "ollama"
        except Exception as e:
            print(f"⚠️ Ollama not available: {e}")
            
            # Fallback to OpenAI if available
            if config.OPENAI_API_KEY:
                try:
                    from langchain_openai import ChatOpenAI
                    self.llm = ChatOpenAI(
                        temperature=0.7,
                        model_name="gpt-3.5-turbo",
                        openai_api_key=config.OPENAI_API_KEY
                    )
                    print("✅ Using OpenAI as LLM provider")
                    self.llm_type = "openai"
                except Exception as e:
                    print(f"❌ Failed to initialize OpenAI: {e}")
                    self.llm = None
            else:
                print("❌ No LLM available. Please set up Ollama or provide OpenAI API key.")
                self.llm = None
    
    def generate_response(self, prompt: str) -> str:
        """Generate a response from the LLM"""
        if not self.llm:
            return "❌ LLM is not configured. Please set up Ollama or OpenAI."
        
        try:
            if self.llm_type == "openai":
                response = self.llm.invoke(prompt)
                return response.content
            else:
                response = self.llm.invoke(prompt)
                return response
        except Exception as e:
            return f"❌ Error generating response: {e}"
    
    def is_available(self) -> bool:
        """Check if LLM is available"""
        return self.llm is not None
