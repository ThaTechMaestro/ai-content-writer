'''
Rewriting the text_summarizer proj using ell ->
Link: https://docs.ell.so/installation
'''

import ell
import os 
from dotenv import load_dotenv
from openai import OpenAI

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)
print(dotenv_path)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@ell.simple(model="gpt-4o", client=client)
def hello(name: str):
    """You are a helpful assistant."""
    return f"Say hello to {name}!"

print(hello("world"))