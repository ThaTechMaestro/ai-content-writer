from openai import OpenAI
from src.config.settings import get_settings
from typing import Optional

class LLMHandler:
    """Basic LLM interaction handler"""
    
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.model_name
    
    def generate_response(self, prompt: str) -> Optional[str]:
        """
        Generate a simple response from the LLM
        
        Args:
            prompt: The input text
            
        Returns:
            Response string or None if there's an error
        """
    
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.choices[0].message.content
        except Exception as e:
            pass
