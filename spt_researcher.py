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
from datetime import datetime
from pathlib import Path
import re
<<<<<<< HEAD
from datetime import datetime
=======
from typing import Dict, Any, List
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba

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
<<<<<<< HEAD
# Helper – Generate insights
# ----------------------------------------------------------------------
async def get_insights(topic: str, max_insights: int, verbose: bool = False) -> tuple[list[str], str, str, str]:
    """
    Use GPTResearcher to gather raw research, then extract insights using local LLM.
=======
# Helper – Parse pain points from raw LLM output
# ----------------------------------------------------------------------
def parse_pain_points(raw_text: str, topic: str, max_points: int, verbose: bool = False) -> Dict[str, Any]:
    """
    Parse pain points from raw LLM output with JSON-first parsing and noise-filtered fallback.
    
    Args:
        raw_text: Raw output from LLM
        topic: The research topic
        max_points: Maximum number of pain points
        verbose: Whether to print debug info
        
    Returns:
        Dict with canonical structure: {"topic": str, "pain_points": [str, ...], "meta": {...}}
    """
    # Try JSON parsing first
    try:
        json_data = json.loads(raw_text.strip())
        if isinstance(json_data, dict) and "pain_points" in json_data:
            # Validate JSON structure
            pain_points = []
            if isinstance(json_data["pain_points"], list):
                for item in json_data["pain_points"]:
                    if isinstance(item, dict) and "idea" in item:
                        pain_points.append(item["idea"])
                    elif isinstance(item, str):
                        pain_points.append(item)
            
            # Limit to max_points and ensure unique
            pain_points = list(dict.fromkeys(pain_points))[:max_points]
            
            return {
                "topic": json_data.get("topic", topic),
                "pain_points": pain_points,
                "meta": {
                    "count": len(pain_points),
                    "generated_at": datetime.utcnow().isoformat() + "Z",
                    "source": "gpt_researcher",
                    "max_points": max_points,
                    "parser": "json"
                }
            }
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        if verbose:
            print(f"⚠️ JSON parsing failed, using fallback: {e}")
    
    # Fallback: noise-filtered line parsing
    noise_patterns = [
        r"^source:\s*https?://",
        r"^title:\s*",
        r"^content:\s*",
        r"^conclusion:\s*",
        r"^try again\s*$",
        r"please enable javascript",
        r"something went wrong",
        r"wait a moment",
        r"^\s*$"  # empty lines
    ]
    
    lines = raw_text.splitlines()
    clean_points = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip noise patterns
        is_noise = any(re.search(pattern, line, re.IGNORECASE) for pattern in noise_patterns)
        if is_noise:
            continue
            
        # Clean bullet points and extract content
        cleaned = line.lstrip("-•* ").strip()
        if cleaned and len(cleaned) > 5:  # Basic quality filter
            clean_points.append(cleaned)
    
    # Deduplicate and limit
    unique_points = list(dict.fromkeys(clean_points))[:max_points]
    
    return {
        "topic": topic,
        "pain_points": unique_points,
        "meta": {
            "count": len(unique_points),
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "source": "gpt_researcher",
            "max_points": max_points,
            "parser": "fallback"
        }
    }

# ----------------------------------------------------------------------
# Helper – Generate pain points with JSON schema
# ----------------------------------------------------------------------
async def get_pain_points(topic: str, max_points: int, verbose: bool = False) -> Dict[str, Any]:
    """
    Use GPTResearcher with JSON-only schema to produce structured pain points.
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba

    Args:
        topic: The broad subject (e.g., "remote work productivity").
        max_insights: Upper bound of insights to request.
        verbose: If True, prints progress information.

    Returns:
<<<<<<< HEAD
        Tuple of (insight_list, prompt_used, raw_output, extraction_json).
    """
    prompt = (
        f"List between {max_insights // 2} and {max_insights} specific, "
        f"actionable insights and key topics that content creators should explore related to "
        f"the topic '{topic}'. "
    )
    if verbose:
        print("🔎 Generating insights…")
=======
        Dict with canonical structure for step-2 input.
    """
    min_points = max_points // 2
    prompt = f"""You are generating a structured list of real customer/user pain points for the topic: {topic}.
Return ONLY a single valid JSON object. No markdown, no prose, no comments, no trailing commas, no extra keys, no preface.

JSON schema (exact keys, in this order):
{{
  "topic": "string",
  "pain_points": [
    {{
      "id": "PP01-style string",
      "idea": "concise, specific pain point statement, 9–14 words, no punctuation at end",
      "description": "one or two sentences elaborating the idea in plain language"
    }}
  ],
  "meta": {{
    "generator": "gpt_researcher",
    "min_points": {min_points},
    "max_points": {max_points}
  }}
}}

Rules:
- Emit between {min_points} and {max_points} items in pain_points.
- The idea field must be unique, domain‑specific, and actionable.
- Do NOT include any of the following anywhere: URLs, "Source:", "Title:", "Content:", "Conclusion:", "Try again", "Please enable Javascript".
- Do not include citations or links.
- If you cannot comply, return: {{"topic":"{topic}","pain_points":[],"meta":{{"generator":"gpt_researcher","min_points":{min_points},"max_points":{max_points},"error":"FORMAT_VIOLATION"}}}}

Example shape (illustrative only):
{{"topic":"photogrammetry","pain_points":[{{"id":"PP01","idea":"Reflective surfaces break feature matching in reconstruction","description":"Metallic and glossy materials cause specular highlights, reducing feature consistency and producing holes or noise."}},{{"id":"PP02","idea":"Insufficient overlap causes incomplete scene coverage","description":"Low forward and side overlap creates gaps and misalignment; enforce 70 to 80 percent overlap for reliable alignment."}}],"meta":{{"generator":"gpt_researcher","min_points":{min_points},"max_points":{max_points}}}}}"""

    if verbose:
        print("🔎 Generating pain points with JSON schema…")
    
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba
    researcher = GPTResearcher(query=prompt, verbose=verbose)
    try:
        # Stage 1: Get raw research from GPT-Researcher
        raw = await researcher.conduct_research()
        raw_text = str(raw)
        
<<<<<<< HEAD
        # Stage 2: Extract clean insights using local LLM
        insights, extraction_json = await extract_insights_from_raw(
            raw_text, topic, max_insights, verbose
        )
        
        return insights, prompt, raw_text, extraction_json
=======
        # Parse with JSON-first approach and noise filtering
        result = parse_pain_points(raw_text, topic, max_points, verbose)
        
        if verbose:
            parser_type = result["meta"]["parser"]
            count = result["meta"]["count"]
            print(f"✅ Parsed {count} pain points using {parser_type} parser")
        
        return result
        
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba
    except Exception as exc:
        raise RuntimeError(f"Failed to generate insights: {exc}") from exc

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
            model=os.getenv("OPENAI_MODEL_NAME", "none"),
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
<<<<<<< HEAD
        "--insights-output",
        default="insights.md",
        help="Path to markdown file that will contain the initial insight list.",
=======
        "--pain-points-output",
        default="pain_points.json",
        help="Path to JSON file that will contain the canonical pain‑point data (default: pain_points.json).",
    )
    parser.add_argument(
        "--pain-points-input",
        type=str,
        help="Path to existing JSON file to load pain points from (skips step-1 generation).",
    )
    parser.add_argument(
        "--pain-points-markdown",
        type=str,
        help="Optional: also write a human-readable markdown list (non-canonical).",
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba
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
<<<<<<< HEAD
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
=======
    # Load or generate pain points
    # ------------------------------------------------------------------
    pain_points_data: Dict[str, Any]
    
    if args.pain_points_input:
        # Load existing JSON dump and skip step-1
        try:
            input_path = Path(args.pain_points_input)
            if not input_path.exists():
                print(f"❌ Pain points input file not found: {input_path}")
                sys.exit(1)
                
            with input_path.open("r", encoding="utf-8") as f:
                pain_points_data = json.load(f)
                
            if args.verbose:
                count = len(pain_points_data.get("pain_points", []))
                print(f"✅ Loaded {count} pain points from {input_path.resolve()}")
                print("🚀 Skipping step-1 generation, proceeding to step-2...")
                
        except Exception as e:
            print(f"❌ Failed to load pain points input: {e}")
            sys.exit(1)
    else:
        # Generate new pain points (step-1)
        try:
            if os.getenv("PYTEST_CURRENT_TEST"):
                # Create dummy data structure for testing
                pain_points_data = {
                    "topic": args.topic,
                    "pain_points": [f"Dummy pain point {i+1}" for i in range(min(args.max_points, 5))],
                    "meta": {
                        "count": min(args.max_points, 5),
                        "generated_at": datetime.utcnow().isoformat() + "Z",
                        "source": "pytest_dummy",
                        "max_points": args.max_points,
                        "parser": "dummy"
                    }
                }
            else:
                pain_points_data = await get_pain_points(
                    args.topic, args.max_points, verbose=args.verbose
                )
        except Exception as e:
            print(f"❌ Error while generating pain points: {e}")
            sys.exit(1)

    # Extract pain points list for step-2
    pain_points = pain_points_data.get("pain_points", [])
    if not pain_points:
        print("⚠️ No pain points were returned – aborting.")
        sys.exit(0)

    if args.verbose:
        print(f"✅ Using {len(pain_points)} pain points for blog post generation.\n")

    # ------------------------------------------------------------------
    # Write canonical JSON dump (exact step-2 input)
    # ------------------------------------------------------------------
    json_output_path = Path(args.pain_points_output)
    try:
        json_output_path.parent.mkdir(parents=True, exist_ok=True)
        with json_output_path.open("w", encoding="utf-8") as f:
            json.dump(pain_points_data, f, indent=2, ensure_ascii=False)
        if args.verbose:
            print(f"✅ Canonical pain points data written to {json_output_path.resolve()}")
    except Exception as e:
        print(f"❌ Failed to write canonical JSON dump: {e}")

    # ------------------------------------------------------------------
    # Optional: Write human-readable markdown
    # ------------------------------------------------------------------
    if args.pain_points_markdown:
        try:
            md_path = Path(args.pain_points_markdown)
            md_path.parent.mkdir(parents=True, exist_ok=True)
            with md_path.open("w", encoding="utf-8") as f:
                f.write(f"# Pain Points for Topic: {args.topic}\n\n")
                f.write("*This is a human-readable version. The canonical data is in the JSON file.*\n\n")
                for idx, point in enumerate(pain_points, start=1):
                    f.write(f"{idx}. {point}\n")
                f.write(f"\n---\n*Generated: {pain_points_data['meta']['generated_at']}*\n")
                f.write(f"*Parser: {pain_points_data['meta']['parser']}*\n")
            if args.verbose:
                print(f"✅ Human-readable markdown written to {md_path.resolve()}")
        except Exception as e:
            print(f"❌ Failed to write markdown file: {e}")
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba

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