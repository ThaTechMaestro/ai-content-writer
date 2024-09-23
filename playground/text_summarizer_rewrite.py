'''
Rewriting this following best practices
using openAI version1.0.0+(The latest version of OpenAi SDK) &
there is a better way than defining a global client &
interacting with openai apis
'''

import asyncio
import os 
from dotenv import load_dotenv
from openai import AsyncOpenAI

class SummaryGenerator:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        load_dotenv(dotenv_path=dotenv_path)
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def get_summary(self, text: str) -> str:
        prompt = self._create_prompt(text)
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error occurred while getting summary: {e}")
            return ""
    
    @staticmethod
    def _create_prompt(text: str) -> str:
        return f"""
        Direction: Summarize the following blog post to highlight its key points, main ideas, and overall message. 
                   Aim for a clear and concise summary that captures the essence of the content.
        
        Format: Provide a summary in 3 sentences, making sure to include the main topic, 
                significant insights, and any notable conclusions or recommendations.
                
        Examples: For instance, if the blog post is about effective time management techniques, 
                  your summary should mention the primary techniques discussed, any unique approaches presented, 
                  and the main takeaway or recommendation.
        
        Evaluation: Verify that the summary accurately reflects the blog post's content without omitting critical information. 
                    The summary should be clear, informative, and avoid unnecessary details or personal interpretations.
        
        Division: If the blog post is lengthy, break it into logical sections (e.g., introduction, main points, conclusion), 
                  summarize each section separately, and then combine the summaries into a cohesive overview.

        Text: {text}
        """

async def main():
    input_text = """
    Lionel Messi, widely regarded as one of the greatest football players of all time, 
    has had a remarkable career filled with numerous achievements and accolades. 
    Born on June 24, 1987, in Rosario, Argentina, Messi began his professional career with FC Barcelona, 
    where he spent over two decades. During his time at Barcelona, Messi won 10 La Liga titles, 
    7 Copa del Rey titles, and 4 UEFA Champions League trophies.
    He is also known for his impressive individual awards, 
    including winning the Ballon d'Or award 7 times, which is a record. 
    Messi's goal-scoring prowess is evident as he holds the record for the most goals scored in a calendar year
    with 91 goals in 2012. In addition to his club success, Messi has also made significant contributions on the international stage, 
    leading Argentina to victory in the 2021 Copa América and the 2022 FIFA World Cup.
    Messi's playing style, characterized by his dribbling ability, vision, and precision, 
    has earned him admiration from fans and experts worldwide. His influence extends beyond the pitch, 
    as he has been involved in various charitable activities and is a global ambassador for numerous causes.
    """
    
    summary_generator = SummaryGenerator()
    summary = await summary_generator.get_summary(input_text)
    print("------------Summary------------------")
    print(summary)