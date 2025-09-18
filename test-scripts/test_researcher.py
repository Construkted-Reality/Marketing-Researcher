import asyncio
import os
from gpt_researcher import GPTResearcher
from dotenv import load_dotenv

async def main():
    load_dotenv() # Load environment variables from .env file

    openai_api_base = os.getenv("OPENAI_API_BASE")
    if openai_api_base is None:
        raise ValueError("OPENAI_API_BASE environment variable is not set.")
    os.environ["OPENAI_API_BASE"] = openai_api_base

    openai_model_name = os.getenv("OPENAI_MODEL_NAME")
    if openai_model_name is None:
        raise ValueError("OPENAI_MODEL_NAME environment variable is not set.")
    os.environ["OPENAI_MODEL_NAME"] = openai_model_name

    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "sk-your-key-if-needed") # Provide a dummy key if vLLM doesn't need it

    # Set retriever (e.g., "tavily" or "tavily,mcp")
    # We will use 'tavily' here to ensure the LLM is called. 
    # If Tavily API key is not set, it might still interact with the LLM.
    # os.environ["RETRIEVER"] = "tavily"  # Disable retriever for this test

    researcher = GPTResearcher(
        query="What is the latest advancement in AI?",
        verbose=True
    )
    
    print("Starting research with vLLM server...")
    try:
        context = await researcher.conduct_research()
        print(f"Context from researcher.conduct_research():\n{context}") # Add this line
        print("Generating report...")
        report = await researcher.write_report()
        print("Research complete!")
        print(f"Report:\n{report}")
    except Exception as e:
        print(f"An error occurred during research: {e}")

if __name__ == "__main__":
    asyncio.run(main())
