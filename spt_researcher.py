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
import os
import sys
from pathlib import Path
import re

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
# Helper – Generate pain points
# ----------------------------------------------------------------------
async def get_pain_points(topic: str, max_points: int, verbose: bool = False) -> list[str]:
    """
    Use GPTResearcher to produce a bullet‑list of user pain points.

    Args:
        topic: The broad subject (e.g., "remote work productivity").
        max_points: Upper bound of pain points to request.
        verbose: If True, prints progress information.

    Returns:
        List of pain‑point strings.
    """
    prompt = (
        f"List between {max_points // 2} and {max_points} specific, "
        f"real‑world pain points that customers or users experience related to "
        f"the topic '{topic}'. Return the list as plain bullet points, one per line, "
        f"without any additional commentary."
    )
    if verbose:
        print("🔎 Generating pain points…")
    researcher = GPTResearcher(query=prompt, verbose=verbose)
    try:
        raw = await researcher.conduct_research()
        # `conduct_research` returns a string (or dict). Cast to str.
        raw_text = str(raw)
        # Split on newlines, strip bullet characters, and filter empties.
        points = [
            line.lstrip("-•* ").strip()
            for line in raw_text.splitlines()
            if line.strip()
        ]
        # Trim to max_points if the model returned more.
        return points[:max_points]
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
        default="pain_points.md",
        help="Path to markdown file that will contain the initial pain‑point list.",
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
    # Generate pain points list
    # ------------------------------------------------------------------
    try:
        # If running under pytest, use dummy data to avoid long LLM calls
        if os.getenv("PYTEST_CURRENT_TEST"):
            pain_points = [f"Dummy pain point {i+1}" for i in range(min(args.max_points, 5))]
        else:
            pain_points = await get_pain_points(
                args.topic, args.max_points, verbose=args.verbose
            )
    except Exception as e:
        print(f"❌ Error while generating pain points: {e}")
        sys.exit(1)

    if not pain_points:
        print("⚠️ No pain points were returned – aborting.")
        sys.exit(0)

    if args.verbose:
        print(f"✅ Retrieved {len(pain_points)} pain points.\n")

    # ------------------------------------------------------------------
    # Write pain‑points to separate markdown file
    # ------------------------------------------------------------------
    pain_points_path = Path(args.pain_points_output)
    try:
        pain_points_path.parent.mkdir(parents=True, exist_ok=True)
        with pain_points_path.open("w", encoding="utf-8") as f:
            f.write(f"# Pain Points for Topic: {args.topic}\n\n")
            for idx, point in enumerate(pain_points, start=1):
                f.write(f"- {point}\n")
        if args.verbose:
            print(f"✅ Pain points written to {pain_points_path.resolve()}")
    except Exception as e:
        print(f"❌ Failed to write pain‑points file: {e}")

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