from src.config.settings import get_settings
from src.llm.base import LLMHandler

def test_llm():
    handler = LLMHandler()
    prompt = "What is your name and model name and model version"
    print(f"\nPrompt: {prompt}")
    response = handler.generate_response(prompt)
    print(f"Response: {response}")

def test_get_settings():
    settings = get_settings()
    print("Settings loaded successfully")
    print(f"Using model: {settings.model_name}")
    print(f"Api_Key: {settings.openai_api_key}")
    print("\nSettings loaded:")
    print(f"Test value: {settings.test_value}")
    print(f"API key exists: {bool(settings.openai_api_key)}")
    print(f"API key length: {len(settings.openai_api_key)}")
    print(f"Model name: {settings.model_name}")
    
    

if __name__ == '__main__':
    test_get_settings()
    # test_llm()
    