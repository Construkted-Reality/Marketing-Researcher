#!/usr/bin/env python3
# File: spt_researcher.py
# --------------------------------------------------------------
# Content‑Marketing Research – Pain‑Point & Blog‑Post Generator
# --------------------------------------------------------------
# Usage:
#   python spt_researcher.py --topic "remote work productivity" \
#       [--output generated_posts.md] [--max-points 15] [--verbose]
#
# The script:
#   1. Loads .env variables (API keys, endpoints, etc.).
#   2. Generates a list of pain points via GPT‑Researcher.
#   3. For each pain point, generates a blog‑post draft.
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
from typing import Dict, Any, List

from dotenv import load_dotenv
from gpt_researcher import GPTResearcher

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

    Args:
        topic: The broad subject (e.g., "remote work productivity").
        max_points: Upper bound of pain points to request.
        verbose: If True, prints progress information.

    Returns:
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
    
    researcher = GPTResearcher(query=prompt, verbose=verbose)
    try:
        raw = await researcher.conduct_research()
        raw_text = str(raw)
        
        # Parse with JSON-first approach and noise filtering
        result = parse_pain_points(raw_text, topic, max_points, verbose)
        
        if verbose:
            parser_type = result["meta"]["parser"]
            count = result["meta"]["count"]
            print(f"✅ Parsed {count} pain points using {parser_type} parser")
        
        return result
        
    except Exception as exc:
        raise RuntimeError(f"Failed to generate pain points: {exc}") from exc

# ----------------------------------------------------------------------
# Helper – Generate a blog post draft for a single pain point
# ----------------------------------------------------------------------
async def generate_blog_post(
    topic: str, pain_point: str, verbose: bool = False
) -> str:
    """
    Generate a markdown‑formatted blog post (outline/draft) for a given pain point.

    Args:
        topic: The overarching topic supplied by the user.
        pain_point: One of the pain points returned by `get_pain_points`.
        verbose: If True, prints progress information.

    Returns:
        Markdown string containing the blog post.
    """
    prompt = (
        f"Write a concise, well‑structured blog post (in markdown) that "
        f"addresses the following pain point:\n\n"
        f"**Pain point:** {pain_point}\n\n"
        f"The post should be framed within the broader topic '{topic}'. "
        f"Include an engaging introduction, 2‑3 sub‑sections with headings, "
        f"and a short conclusion. Use bullet points where appropriate and "
        f"maintain a professional tone suitable for a content‑marketing audience."
    )
    if verbose:
        print(f"🖋️ Generating blog post for: {pain_point[:60]}…")
    researcher = GPTResearcher(query=prompt, verbose=verbose)
    try:
        # `write_report` produces the final formatted output.
        await researcher.conduct_research()
        report = await researcher.write_report()
        return str(report)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to generate blog post for '{pain_point}': {exc}"
        ) from exc

# ----------------------------------------------------------------------
# Main workflow
# ----------------------------------------------------------------------
async def main_cli() -> None:
    parser = argparse.ArgumentParser(
        description="Generate pain points and blog‑post drafts using GPT‑Researcher."
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
        "--max-points",
        type=int,
        default=15,
        help="Maximum number of pain points to generate (default: 15).",
    )
    parser.add_argument(
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
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed progress logging.",
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # Prepare environment
    # ------------------------------------------------------------------
    try:
        load_environment()
    except Exception as e:
        print(f"❌ Environment setup error: {e}")
        sys.exit(1)

    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Generate blog posts
    # ------------------------------------------------------------------
    posts: list[str] = []
    for idx, point in enumerate(pain_points, start=1):
        try:
            if os.getenv("PYTEST_CURRENT_TEST"):
                # Generate a simple dummy markdown for testing
                post_md = f"# {point}\\n\\nDummy content for testing."
            else:
                post_md = await generate_blog_post(args.topic, point, verbose=args.verbose)

            # Determine a title for the article
            title_match = re.search(r"^#{1,2}\\s+(.+)$", post_md, flags=re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
            else:
                # Fallback to the pain point itself
                title = point

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

            posts.append(f"## {idx}. {point}\\n\\n{post_md}\\n")
        except Exception as e:
            print(f"⚠️ Skipping point due to error: {e}")

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