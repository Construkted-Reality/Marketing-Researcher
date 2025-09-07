import asyncio
import os
from gpt_researcher import GPTResearcher
from dotenv import load_dotenv

async def main():
    """
    Note: The example from the GPT-Researcher README uses top-level await,
    which works in Jupyter notebooks but not in regular Python scripts.
    This version wraps the code in an async main function for script compatibility.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Set up environment variables for vLLM server
    openai_api_base = os.getenv("OPENAI_API_BASE")
    if openai_api_base is None:
        raise ValueError("OPENAI_API_BASE environment variable is not set.")
    os.environ["OPENAI_API_BASE"] = openai_api_base

    openai_model_name = os.getenv("OPENAI_MODEL_NAME")
    if openai_model_name is None:
        raise ValueError("OPENAI_MODEL_NAME environment variable is not set.")
    os.environ["OPENAI_MODEL_NAME"] = openai_model_name

    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "sk-your-key-if-needed")

    print(f"Using vLLM server at: {openai_api_base}")
    print(f"Using model: {openai_model_name}")

    query = "pain points currently experienced by users doing photogrammetry"
    researcher = GPTResearcher(query=query, verbose=True)
    
    print("Starting research...")
    try:
        # Conduct research on the given query
        research_result = await researcher.conduct_research()
        print("Research complete! Writing report...")
        
        # Write the report
        report = await researcher.write_report()
        print(f"Report generated:\n{report}")
        # Write the report to a file (default: research_report.txt)
        output_path = os.getenv("RESEARCH_OUTPUT", "research_report.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n✅ Report saved to {output_path}")
    except Exception as e:
        print(f"An error occurred during research: {e}")

if __name__ == "__main__":
    asyncio.run(main())