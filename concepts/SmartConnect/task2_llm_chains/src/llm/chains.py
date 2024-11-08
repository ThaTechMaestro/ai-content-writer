from typing import Optional, Dict
from pydantic import BaseModel
from .base import LLMHandler

class QuestionResponse(BaseModel):
    """Structured response for Q&A chain"""
    question: str
    answer: str
    confidence: float
    context: Optional[str] = None
    
class QuestionAnswerChain:
    """Chain for handling question-answer interactions"""
    
    def __init__(self):
        self.llm = LLMHandler()
        
    async def format_question(self, raw_question: str) -> str:
        """Format the raw question for better response"""
        format_prompt = f"""
        Format this question to be clear and specific: '{raw_question}'
        Return only the formatted question without any explanation.
        """
        
        response = self.llm.generate_response(
            format_prompt,
            temperature=0.3
        )
        return response.content.strip()
