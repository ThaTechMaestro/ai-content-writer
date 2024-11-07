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

def test_llm_features():
    handler = LLMHandler()
    
    # Test different temperatures
    prompts = [
        {
            "text": "Write a creative story about a robot",
            "temperature": 1.0,  # More creative
            "max_tokens": 100
        },
        {
            "text": "What is 2+2?",
            "temperature": 0.1,  # More focused/deterministic
            "max_tokens": 50
        }
    ]
    
    for prompt in prompts:
        print(f"\nPrompt: {prompt['text']}")
        print(f"Temperature: {prompt['temperature']}")
        
        response = handler.generate_response(
            prompt=prompt['text'],
            temperature=prompt['temperature'],
            max_tokens=prompt['max_tokens']
        )
        
        print(f"Status: {response.status}")
        print(f"Response: {response.content}")
        print(f"Total tokens: {response.tokens_used}")
        print(f"Prompt tokens: {response.prompt_tokens}")
        print(f"Completion tokens: {response.completion_tokens}")
        
        if response.error:
            print(f"Error: {response.error}")
    
def test_conversation():
    handler = LLMHandler()
    
    # Test conversation with context
    conversation = [
        "What is Python?",
        "Can you give me an example of a Python function?",
        "Can you explain the function you just showed?",
    ]
    
    print("Testing conversation with memory:")
    print("=" * 50)
    
    for prompt in conversation:
        print(f"\nUser: {prompt}")
        response = handler.generate_response(prompt)
        print(f"Assistant: {response.content}")
        print(f"Tokens used: {response.tokens_used}")
        
    # Test without history
    print("\nTesting single response without history:")
    print("=" * 50)
    
    handler.clear_history()
    response = handler.generate_response(
        "Can you explain the function you just showed?",
        use_history=False
    )
    print(f"\nUser: Can you explain the function you just showed?")
    print(f"Assistant: {response.content}")

def test_memory_behavior():
    handler = LLMHandler()
    
    print("Test 1: With History")
    print("=" * 50)
    # First conversation
    prompts_1 = [
        "My favorite color is blue.",
        "What's my favorite color?"
    ]
    
    for prompt in prompts_1:
        print(f"\nUser: {prompt}")
        response = handler.generate_response(prompt, use_history=True)
        print(f"Assistant: {response.content}")

    print("\nTest 2: Without History")
    print("=" * 50)
    # New handler (no history)
    handler2 = LLMHandler()
    print("\nUser: What's my favorite color?")
    response = handler2.generate_response(
        "What's my favorite color?",
        use_history=False
    )
    print(f"Assistant: {response.content}")

if __name__ == '__main__':
    # test_get_settings()
    # test_llm()
    # test_llm_features()
    # test_conversation()
    test_memory_behavior()
    