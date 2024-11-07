from openai import OpenAI, APIError, RateLimitError
from src.config.settings import get_settings
from typing import Optional, Dict, List
from pydantic import BaseModel

class Message(BaseModel):
    """Structure for conversation messages"""
    role: str  # "user" or "assistant"
    content: str
    
class LLMResponse(BaseModel):
    """Structure for LLM responses"""
    content: str
    status: str = "success"
    error: Optional[str] = None
    tokens_used: Optional[int] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    
    
    
class LLMHandler:
    """Basic LLM interaction handler"""
    
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.model_name
        self.conversation_history: List[Message] = []
    
    def add_message(
        self, 
        role:str, 
        content: str):
        """Add a message to conversation history"""
        self.conversation_history.append(Message(role=role, content=content))
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def generate_response(
        self, 
        prompt: str,
        temperature: float=0.7,
        max_tokens: Optional[int] = None,
        use_history: bool = True
        ) -> LLMResponse:
        """
        Generate a simple response from the LLM
        
        Args:
            prompt: The input text
            temperature: Controls randomness (0.0-2.0)
            max_tokens: Maximum tokens in response
            use_history: Whether to include conversation history
            
        Returns:
            LLMResponse object
        """
    
        try:
            self.add_message("user", prompt)
            
            if use_history:
                messages = [
                    {
                        "role": msg.role, 
                        "content": msg.content
                    }
                    for msg in self.conversation_history
                ]
            else:
                messages = [{"role": "user", "content": prompt}]
                
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            assistant_response = response.choices[0].message.content
            self.add_message("assistant", assistant_response)
            
            return LLMResponse(
                content=assistant_response,
                tokens_used=response.usage.total_tokens,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens
            )
        except RateLimitError:
            return LLMResponse(
                content="",
                status="error",
                error="Rate limit exceeded. Please try again later."
            )
        except APIError as e:
            return LLMResponse(
                content="",
                status="error",
                error=f"API error: {str(e)}"
            )
        except Exception as e:
            return LLMResponse(
                content="",
                status="error",
                error=f"Unexpected error: {str(e)}"
            )
    
