from openai import OpenAI, APIError, RateLimitError
from src.config.settings import get_settings
from typing import Optional
from pydantic import BaseModel

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
    
    def generate_response(
        self, 
        prompt: str,
        temperature: float=0.7,
        max_tokens: Optional[int] = None
        ) -> LLMResponse:
        """
        Generate a simple response from the LLM
        
        Args:
            prompt: The input text
            temperature: Controls randomness (0.0-2.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            LLMResponse object
        """
    
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
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
    
