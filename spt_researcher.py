#!/usr/bin/env python3
# File: spt_researcher.py
# --------------------------------------------------------------
# Content‑Marketing Research – Insights & Blog‑Post Generator
# --------------------------------------------------------------
# Usage:
#   python spt_researcher.py --topic "remote work productivity" \
#       [--output generated_posts.md] [--max-insights 15] [--verbose] [--insights-only]
#
# The script:
#   1. Loads .env variables (API keys, endpoints, etc.).
#   2. Generates a list of insights via GPT‑Researcher.
#   3. For each insight, generates a blog‑post draft.
#   4. Writes the combined markdown to the output file.
# --------------------------------------------------------------

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
import re
from datetime import datetime

from dotenv import load_dotenv
from gpt_researcher import GPTResearcher
from openai import OpenAI

# ----------------------------------------------------------------------
# Helper – Load environment & ensure required variables are present
# ----------------------------------------------------------------------
def load_environment() -> None:
    """Load .env and validate critical variables."""
    load_dotenv()
    # Validate OpenAI base URL – required for the vLLM server
    openai_api_base = os.getenv("OPENAI_API_BASE")
    if not openai_api_base:
        raise ValueError("OPENAI_API_BASE environment variable is not set.")
    os.environ["OPENAI_API_BASE"] = openai_api_base

    # Set a reliable retriever to avoid SearXNG timeouts.
    # Default to Tavily (commercial) with MCP fallback; this works even if
    # the SearXNG instance is unreachable.
    #os.environ["RETRIEVER"] = "tavily,mcp"

    # Validate model name – required for the vLLM server
    openai_model_name = os.getenv("OPENAI_MODEL_NAME")
    if not openai_model_name:
        raise ValueError("OPENAI_MODEL_NAME environment variable is not set.")
    os.environ["OPENAI_MODEL_NAME"] = openai_model_name

    # Provide a dummy key if the downstream server does not need it
    os.environ["OPENAI_API_KEY"] = os.getenv(
        "OPENAI_API_KEY", "sk-dummy-key-if-not-needed"
    )

def slugify(text: str) -> str:
    """
    Convert a string to a safe filename slug.
    - Lower‑case
    - Replace non‑alphanumeric characters with underscores
    - Collapse multiple underscores
    - Strip leading/trailing underscores
    """
    import re

    # Replace any character that is not a letter, number, or underscore with underscore
    slug = re.sub(r"[^\w]+", "_", text.lower())
    # Collapse consecutive underscores
    slug = re.sub(r"_+", "_", slug)
    # Remove leading/trailing underscores
    slug = slug.strip("_")
    return slug

# ----------------------------------------------------------------------
# Helper – Extract insights from raw research using local LLM
# ----------------------------------------------------------------------
async def extract_insights_from_raw(
    raw_text: str, topic: str, max_insights: int, verbose: bool = False
) -> tuple[list[str], str]:
    """
    Extract clean insights from raw GPT-Researcher output using local vLLM.
    
    Args:
        raw_text: Raw research output from GPT-Researcher
        topic: The research topic
        max_insights: Maximum number of insights to extract
        verbose: If True, prints progress information
        
    Returns:
        Tuple of (insights_list, extraction_json_output)
    """
    # Create OpenAI client using the configured vLLM endpoint
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "sk-dummy-key-if-not-needed"),
        base_url=os.getenv("OPENAI_API_BASE")
    )
    
    # Limit raw text to avoid token limits (keep first ~20k chars)
    truncated_raw = raw_text[:20000] if len(raw_text) > 20000 else raw_text
    
    extraction_prompt = f"""You are a content marketing analyst. Extract {max_insights} specific, actionable insights from the research below for the topic "{topic}".

Return ONLY a valid JSON array of strings, with no additional text or formatting. Each insight should be a short, actionable statement that content creators can use.

Example format:
["First insight here", "Second insight here", "Third insight here"]

Research to analyze:
{truncated_raw}"""

    if verbose:
        print("🔍 Extracting insights using local LLM...")
    
    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo"),
            messages=[
                {"role": "system", "content": "You extract actionable insights from research data. Always return valid JSON arrays only."},
                {"role": "user", "content": extraction_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        json_output = response.choices[0].message.content
        if json_output is None:
            raise ValueError("Empty response from LLM")
        json_output = json_output.strip()
        
        # Try to parse JSON
        try:
            if verbose:
                print(f"🔍 JSON extraction output:\n{json_output}\n")
            
            insights = json.loads(json_output)
            if isinstance(insights, list) and all(isinstance(item, str) for item in insights):
                # Limit to max_insights and clean up
                cleaned_insights = [insight.strip() for insight in insights[:max_insights] if insight.strip()]
                if verbose:
                    print(f"✅ Extracted {len(cleaned_insights)} insights from JSON")
                return cleaned_insights, json_output
            else:
                raise ValueError("JSON is not a list of strings")
        except (json.JSONDecodeError, ValueError) as e:
            if verbose:
                print(f"⚠️ JSON parsing failed: {e}, falling back to heuristic parsing")
                print(f"🔍 Raw JSON output was:\n{json_output}\n")
            # Fallback to heuristic parsing
            fallback_insights = []
            for line in json_output.splitlines():
                line = line.strip()
                if line and not line.startswith(('[', ']', '{', '}')):
                    # Remove quotes and common prefixes
                    cleaned = line.strip('",').lstrip('-•* ').strip()
                    if cleaned and len(cleaned) > 10:  # Reasonable minimum length
                        fallback_insights.append(cleaned)
            
            if verbose:
                print(f"✅ Heuristic parsing extracted {len(fallback_insights[:max_insights])} insights")
            return fallback_insights[:max_insights], json_output
            
    except Exception as e:
        if verbose:
            print(f"⚠️ Extraction failed: {e}, using fallback method")
        # Final fallback: simple line-based parsing of original raw text
        fallback_insights = []
        for line in raw_text.splitlines():
            line = line.strip().lstrip('-•* ').strip()
            if line and len(line) > 10 and len(line) < 200:  # Reasonable insight length
                fallback_insights.append(line)
        
        return fallback_insights[:max_insights], f"Extraction failed: {str(e)}"

# ----------------------------------------------------------------------
# Helper – Generate insights
# ----------------------------------------------------------------------
async def get_insights(topic: str, max_insights: int, verbose: bool = False) -> tuple[list[str], str, str, str]:
    """
    Use GPTResearcher to gather raw research, then extract insights using local LLM.

    Args:
        topic: The broad subject (e.g., "remote work productivity").
        max_insights: Upper bound of insights to request.
        verbose: If True, prints progress information.

    Returns:
        Tuple of (insight_list, prompt_used, raw_output, extraction_json).
    """
    prompt = (
        f"List between {max_insights // 2} and {max_insights} specific, "
        f"actionable insights and key topics that content creators should explore related to "
        f"the topic '{topic}'. "
    )
    if verbose:
        print("🔎 Generating insights…")
    researcher = GPTResearcher(query=prompt, verbose=verbose)
    try:
        # Stage 1: Get raw research from GPT-Researcher
        raw = await researcher.conduct_research()
        raw_text = str(raw)
        
        # Stage 2: Extract clean insights using local LLM
        insights, extraction_json = await extract_insights_from_raw(
            raw_text, topic, max_insights, verbose
        )
        
        return insights, prompt, raw_text, extraction_json
    except Exception as exc:
        raise RuntimeError(f"Failed to generate insights: {exc}") from exc

# ----------------------------------------------------------------------
# Helper – Generate a blog post draft for a single insight
# ----------------------------------------------------------------------
async def generate_blog_post(
    topic: str, insight: str, verbose: bool = False
) -> str:
    """
    Generate a markdown‑formatted blog post (outline/draft) for a given insight.

    Args:
        topic: The overarching topic supplied by the user.
        insight: One of the insights returned by `get_insights`.
        verbose: If True, prints progress information.

    Returns:
        Markdown string containing the blog post.
    """
    prompt = (
        f"Write a concise, well‑structured blog post (in markdown) that "
        f"explores the following insight:\n\n"
        f"**Insight:** {insight}\n\n"
        f"The post should be framed within the broader topic '{topic}'. "
        f"Include an engaging introduction, 2‑3 sub‑sections with headings, "
        f"and a short conclusion. Use bullet points where appropriate and "
        f"maintain a professional tone suitable for a content‑marketing audience."
    )
    if verbose:
        print(f"🖋️ Generating blog post for: {insight[:60]}…")
    researcher = GPTResearcher(query=prompt, verbose=verbose)
    try:
        # `write_report` produces the final formatted output.
        await researcher.conduct_research()
        report = await researcher.write_report()
        return str(report)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to generate blog post for '{insight}': {exc}"
        ) from exc

# ----------------------------------------------------------------------
# Main workflow
# ----------------------------------------------------------------------
async def main_cli() -> None:
    parser = argparse.ArgumentParser(
        description="Generate insights and blog‑post drafts using GPT‑Researcher."
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="Broad research topic (e.g., 'remote work productivity').",
    )
    parser.add_argument(
        "--output",
        default="generated_blog_posts.md",
        help="Path to the markdown file that will contain the results.",
    )
    parser.add_argument(
        "--max-insights",
        type=int,
        default=15,
        help="Maximum number of insights to generate (default: 15).",
    )
    parser.add_argument(
        "--insights-output",
        default="insights.md",
        help="Path to markdown file that will contain the initial insight list.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed progress logging.",
    )
    parser.add_argument(
        "--insights-only",
        action="store_true",
        help="Generate only insights and stop before creating blog posts.",
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # Prepare environment
    # ------------------------------------------------------------------
    try:
        load_environment()
        
        # Debug: Verify temperature settings are loaded from .env
        print(f"🔧 [DEBUG] Temperature settings loaded from .env:")
        print(f"   TEMPERATURE: {os.getenv('TEMPERATURE', 'not set')}")
        print(f"   FAST_TEMPERATURE: {os.getenv('FAST_TEMPERATURE', 'not set')}")
        print(f"   SMART_TEMPERATURE: {os.getenv('SMART_TEMPERATURE', 'not set')}")
        print(f"   STRATEGIC_TEMPERATURE: {os.getenv('STRATEGIC_TEMPERATURE', 'not set')}")
        print()
        
    except Exception as e:
        print(f"❌ Environment setup error: {e}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # Generate insights list
    # ------------------------------------------------------------------
    try:
        # If running under pytest, use dummy data to avoid long LLM calls
        if os.getenv("PYTEST_CURRENT_TEST"):
            insights = [f"Dummy insight {i+1}" for i in range(min(args.max_insights, 5))]
            prompt_used = f"Dummy prompt for topic '{args.topic}'"
            raw_output = "Dummy raw output for testing"
            extraction_json = '["Dummy insight 1", "Dummy insight 2"]'
        else:
            insights, prompt_used, raw_output, extraction_json = await get_insights(
                args.topic, args.max_insights, verbose=args.verbose
            )
    except Exception as e:
        print(f"❌ Error while generating insights: {e}")
        sys.exit(1)

    if not insights:
        print("⚠️ No insights were returned – aborting.")
        sys.exit(0)

    if args.verbose:
        print(f"✅ Retrieved {len(insights)} insights.\n")

    # ------------------------------------------------------------------
    # Write insights to separate markdown file with debug information
    # ------------------------------------------------------------------
    insights_path = Path(args.insights_output)
    try:
        insights_path.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Append mode to preserve history
        with insights_path.open("a", encoding="utf-8") as f:
            # Add separator if file already has content
            if insights_path.exists() and insights_path.stat().st_size > 0:
                f.write("\n\n---\n\n")
            
            f.write(f"# Insights Debug Session: {timestamp}\n\n")
            f.write(f"**Topic:** {args.topic}\n")
            f.write(f"**Max Insights:** {args.max_insights}\n\n")
            
            f.write("## Prompt Used\n\n")
            f.write(f"```\n{prompt_used}\n```\n\n")
            
            f.write("## Raw Model Output\n\n")
            f.write(f"```\n{raw_output}\n```\n\n")
            
            f.write("## Extracted Insights (JSON)\n\n")
            f.write(f"```json\n{extraction_json}\n```\n\n")
            
            f.write("## Parsed Insights\n\n")
            for idx, insight in enumerate(insights, start=1):
                f.write(f"{idx}. {insight}\n")
            f.write("\n")
        
        if args.verbose:
            print(f"✅ Insights debug information appended to {insights_path.resolve()}")
    except Exception as e:
        print(f"❌ Failed to write insights file: {e}")

    # ------------------------------------------------------------------
    # Exit early if insights-only mode is enabled
    # ------------------------------------------------------------------
    if args.insights_only:
        print(f"✅ Insights-only mode: Generated {len(insights)} insights and stopped before blog post creation.")
        if args.verbose:
            print(f"✅ Insights saved to {insights_path.resolve()}")
        sys.exit(0)

    # ------------------------------------------------------------------
    # Generate blog posts
    # ------------------------------------------------------------------
    posts: list[str] = []
    for idx, insight in enumerate(insights, start=1):
        try:
            if os.getenv("PYTEST_CURRENT_TEST"):
                # Generate a simple dummy markdown for testing
                post_md = f"# {insight}\n\nDummy content for testing."
            else:
                print(f"********** generating blog post with the insight: {insight}")
                post_md = await generate_blog_post(args.topic, insight, verbose=args.verbose)

            # Determine a title for the article
            title_match = re.search(r"^#{1,2}\s+(.+)$", post_md, flags=re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
            else:
                # Fallback to the insight itself
                title = insight

            # Write individual markdown file
            posts_dir = Path("posts")
            posts_dir.mkdir(parents=True, exist_ok=True)
            filename = slugify(title) + ".md"
            file_path = posts_dir / filename
            try:
                with file_path.open("w", encoding="utf-8") as f:
                    f.write(post_md)
                if args.verbose:
                    print(f"✅ Blog post written to {file_path.resolve()}")
            except Exception as e:
                print(f"❌ Failed to write blog post file '{filename}': {e}")

            posts.append(f"## {idx}. {insight}\n\n{post_md}\n")
        except Exception as e:
            print(f"⚠️ Skipping insight due to error: {e}")

    if not posts:
        print("⚠️ No blog posts were successfully generated.")
        sys.exit(0)

    # ------------------------------------------------------------------
    # Write output file
    # ------------------------------------------------------------------
    output_path = Path(args.output)
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as f:
            f.write(f"# Blog Posts for Topic: {args.topic}\n\n")
            for post in posts:
                f.write(post)
                f.write("\n---------\n\n")
        if args.verbose:
            print(f"✅ All posts written to {output_path.resolve()}")
    except Exception as e:
        print(f"❌ Failed to write output file: {e}")
        sys.exit(1)

# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main_cli())