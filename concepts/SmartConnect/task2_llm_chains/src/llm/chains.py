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
    
    async def get_answer(self, formatted_question: str) -> str:
        """Get answer from LLM"""
        answer_prompt = f"""
        Answer this question as precisely as possible: '{formatted_question}'
        If you're not certain, indicate your level of confidence.
        """
        
        response = self.llm.generate_response(
            answer_prompt,
            temperature=0.7
        )
        return response.content.strip()
    
    async def validate_answer(self, question: str, answer: str) -> Dict:
        """Validate and rate the answer's confidence"""
        validation_prompt = f"""
        Rate the following answer to the question on a scale of 0 to 1:
        Question: {question}
        Answer: {answer}
        
        Return only a number between 0 and 1 representing confidence.
        """
        
        response = self.llm.generate_response(
            validation_prompt,
            temperature=0.1
        )
        
        try:
            confidence = float(response.content.strip())
        except ValueError:
            confidence = 0.5
            
        return {
            "confidence": confidence,
            "needs_improvement": confidence < 0.7
        }
    
    async def process_question(self, raw_question: str) -> QuestionResponse:
        """Process question through the entire chain"""
        try:
            formatted_question = await self.format_question(raw_question)
            
            answer = await self.get_answer(formatted_question)
            
            validation = await self.validate_answer(formatted_question, answer)
            
            if validation["needs_improvement"]:
                improved_prompt = f"""
                The previous answer might need improvement:
                Question: {formatted_question}
                Previous Answer: {answer}
                Please provide a more accurate and detailed answer.
                """
                
                improved_response = self.llm.generate_response(improved_prompt)
                answer = improved_response.content.strip()
                validation = await self.validate_answer(formatted_question, answer)
            
            return QuestionResponse(
                question=formatted_question,
                answer=answer,
                confidence=validation["confidence"]
            )
        except Exception as e:
            return QuestionResponse(
                question=raw_question,
                answer=f"Error processing question: {str(e)}",
                confidence=0.0
            )
