import openai
import asyncio
import os 
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

key = os.getenv("OPENAI_API_KEY")

async def get_summary(
    text: str) -> str:
    
    prompt = (
        """
        Direction: Summarize the following blog post to highlight its key points, main ideas, and overall message. 
                   Aim for a clear and concise summary that captures the essence of the content.
        
        Format: Provide a summary in 3 sentences, making sure to include the main topic, 
                significant insights, and any notable conclusions or recommendations.
                
        Examples: For instance, if the blog post is about effective time management techniques, 
                  your summary should mention the primary techniques discussed, any unique approaches presented, 
                  and the main takeaway or recommendation.
        
        Evaluation: Verify that the summary accurately reflects the blog post’s content without omitting critical information. 
                    The summary should be clear, informative, and avoid unnecessary details or personal interpretations.
        
        Division: If the blog post is lengthy, break it into logical sections (e.g., introduction, main points, conclusion), 
                  summarize each section separately, and then combine the summaries into a cohesive overview.

        Text: {text}
        """.format(text=text)
    )
    
    response = await asyncio.to_thread(
        openai.completions.create,
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150
    )
    
    summary = response.choices[0].text.strip()
    return summary

async def main():
    
    long_text = (
        """
        Lionel Messi, widely regarded as one of the greatest football players of all time, 
        has had a remarkable career filled with numerous achievements and accolades. 
        Born on June 24, 1987, in Rosario, Argentina, Messi began his professional career with FC Barcelona, 
        where he spent over two decades. During his time at Barcelona, Messi won 10 La Liga titles, 
        7 Copa del Rey titles, and 4 UEFA Champions League trophies.
        He is also known for his impressive individual awards, 
        including winning the Ballon d'Or award 7 times, which is a record. 
        Messi's goal-scoring prowess is evident as he holds the record for the most goals scored in a calendar year
        with 91 goals in 2012. In addition to his club success, Messi has also made significant contributions on the international stage, leading Argentina to victory in the 2021 Copa América and the 2022 FIFA World Cup.
        Messi’s playing style, characterized by his dribbling ability, vision, and precision, has earned him admiration from fans and experts worldwide. His influence extends beyond the pitch, as he has been involved in various charitable activities and is a global ambassador for numerous causes.
        """
    )
    
    summary = await get_summary(long_text)
    print("------------Summary------------------")
    print(summary)
    
    
if __name__ == "__main__":
    asyncio.run(main())
    
'''
The goal of the script is to test the changes associated with using 
the grit tool for migrating code relating to the use of openai sdk
ChatGpt currently pours out code with openai integration
    which are the old way of doing things that is
    writing code as if you are using versions below 1.0.0
    But from v1.0.0, changes have been made and there are better way
    of implementing stuff which is what I hope to see from using the grit tool

The code in this script is a clone of what is in text_summarizer.py
& the final version will be after i have executed the openai migration command
    
More Details can be found here: https://github.com/openai/openai-python/discussions/742
'''
