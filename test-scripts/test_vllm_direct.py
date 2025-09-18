import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
api_key = os.getenv("OPENAI_API_KEY", "sk-dummy-key")
api_base = os.getenv("OPENAI_API_BASE")
model_name = os.getenv("OPENAI_MODEL_NAME")

if not api_base:
    raise ValueError("OPENAI_API_BASE environment variable is not set.")
if not model_name:
    raise ValueError("OPENAI_MODEL_NAME environment variable is not set.")

print(f"Testing vLLM server at: {api_base}")
print(f"Using model: {model_name}")

try:
    client = OpenAI(
        api_key=api_key,
        base_url=api_base,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Hello, how are you?",
            }
        ],
        model=model_name,
        max_tokens=50,
        temperature=0.7,
    )

    print("\n--- Raw API Response ---")
    print(chat_completion.model_dump_json(indent=2))

    if chat_completion.choices and chat_completion.choices[0].message:
        print("\n--- Parsed Content ---")
        print(chat_completion.choices[0].message.content)
    else:
        print("\n--- No content received from LLM ---")
        print(f"Choices: {chat_completion.choices}")

except Exception as e:
    print(f"\nAn error occurred: {e}")