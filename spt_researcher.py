#!/usr/bin/env python3
# File: spt_researcher.py
# --------------------------------------------------------------
# Content‑Marketing Research – Insights & Blog‑Post Generator
# --------------------------------------------------------------
# Usage:
#   python spt_researcher.py --topic "remote work productivity" \
#       [--max-insights 15] [--verbose] [--gr-verbose] [--insights-only] [--posts-dir custom_folder]
#   python spt_researcher.py --insights-input insights.json \
#       [--topic "dummy"] [--verbose] [--posts-dir custom_folder]
#
# The script:
#   1. Loads .env variables (API keys, endpoints, etc.).
#   2. Generates structured insights via GPT‑Researcher.
#   3. For each insight, generates a blog‑post draft.
#   4. Writes insights to insights.json and each blog post as a markdown file in the posts_dir (default: "posts").
# --------------------------------------------------------------
 
import argparse
import asyncio
import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
import re
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from dotenv import load_dotenv
from gpt_researcher import GPTResearcher
from openai import OpenAI
 
 
@dataclass
class InsightObject:
    """Data class representing a structured insight with context and metadata."""
    insight: str = ""
    context: str = ""
    source_reference: List[str] = field(default_factory=list)
    key_data: str = ""
    priority_level: str = "medium"
    content_type: str = "general"
    target_audience: str = "general"
 
CONTEXT_FILE = Path("llm_guidance/context.md")
TITLES_FILE = Path("llm_guidance/crafting_compelling_titles.md")
COMPANY_OPERATION_FILE = Path("llm_guidance/company_operation.md")
CONTENT_MARKETING_GUIDANCE_FILE = Path("llm_guidance/content_marketing_guidance.md")
 
# Voice definitions (mirroring the associative array in the Bash script)
VOICE_DEFINITIONS: Dict[str, str] = {
    "TheNewYorker": (
        "New Yorker "
        "- Tone: sophisticated, witty, introspective, and conversational, yet authoritative. "
        "- Rhythm: mix short, punchy sentences with longer, meandering ones; allow occasional asides and minor tangents. "
        "- Style: sprinkle in idioms, slang, and light‑hearted rhetorical questions (e.g., “Who hasn’t…?”) to keep it authentic. "
        "- Personality: let the narrator’s sharp curiosity and dry humor shine through; don’t be afraid of a subtle imperfection or a fleeting digression. "
        "- Purpose: inform, entertain, and provoke thought—think of a column that educates while it delights and challenges the reader."
    ),
    "TheAtlantic": (
        "The Atlantic "
        "- Personality: Thought‑provoking, long‑form, measured, policy‑savvy. "
        "- Signature tricks: Structured arguments, data‑driven evidence, historical context, calm but persuasive tone, minimal slang. "
        "- Prompt cheat‑sheet: Write in the voice of an Atlantic columnist: analytical, well‑researched, balanced, with a calm persuasive tone and ample historical context."
    ),
    "Wired": (
        "Wired "
        "- Personality: Futurist, tech‑obsessed, fast‑paced, jargon‑light. "
        "- Signature tricks: Short, punchy sentences; use of bold tech metaphors ('the internet is a nervous system'); occasional emojis or meme references (when appropriate); 'what‑it‑means‑for‑you' framing. "
        "- Prompt cheat‑sheet: Write like a Wired feature: tech‑forward, fast‑paced, with vivid metaphors and a ‘what it means for the reader’ angle."
    ),
}
 
FORMATTING_RULES = (
    "**Formatting rules** "
    "- Do **not** use any tables, ASCII‑art tables, or Markdown tables. "
    "- Keep the output strictly in paragraph form (or simple bullet points if a list is needed). "
    "- Avoid other “grid‑like” structures; use prose instead. "
    "- Deliver a piece that fulfills the voice and purpose while respecting the formatting rules."
)
 
#INSIGHT_PROMPT_FILE = Path("llm_guidance/insight_prompt_guidance.md")
#CREATE_BLOG_PROMPT_FILE = Path("llm_guidance/create_blog-post_guidance.md")
 
def load_prompt_template(template_name: str, **kwargs) -> str:
    """Load a prompt template from the prompts directory and format it with provided variables.
    Uses brace-safe formatting to avoid conflicts with JSON braces in templates."""
    template_path = Path("llm_guidance") / f"{template_name}.md"
    try:
        template_content = template_path.read_text(encoding="utf-8")
        
        # Brace-safe formatting: only replace known placeholders
        for key, value in kwargs.items():
            placeholder = "{" + key + "}"
            template_content = template_content.replace(placeholder, str(value))
        
        return template_content
    except Exception as e:
        sys.stderr.write(f"Error loading prompt template {template_name}: {e}\n")
        sys.exit(1)
 
def read_file(path: Path) -> str:
    """Read a file and return its content as a string."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        sys.stderr.write(f"Error reading {path}: {e}\n")
        sys.exit(1)
 
 
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
 
def count_words(text: str) -> int:
    """
    Count words in text using simple whitespace splitting.
    
    Args:
        text: Input text to count words in
        
    Returns:
        Number of words (approximate)
    """
    if not text or not isinstance(text, str):
        return 0
    return len(text.split())
 
def load_insights_from_file(file_path: Path) -> list[InsightObject]:
    """
    Load structured insights from a JSON file.
    
    Args:
        file_path: Path to JSON file containing insights
        
    Returns:
        List of InsightObject instances
        
    Raises:
        ValueError: If file format is invalid or required fields are missing
    """
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("JSON file must contain a list of insights")
        
        insights = []
        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(f"Insight {idx+1}: must be a dictionary")
            
            # Validate required fields
            required_fields = ["insight", "context", "source_reference", "key_data"]
            for field in required_fields:
                if field not in item:
                    raise ValueError(f"Insight {idx+1}: missing required field '{field}'")
                if field == "source_reference":
                    if not isinstance(item[field], list):
                        raise ValueError(f"Insight {idx+1}: field '{field}' must be a list of strings")
                    if not all(isinstance(src, str) for src in item[field]):
                        raise ValueError(f"Insight {idx+1}: all source_reference entries must be strings")
                else:
                    if not isinstance(item[field], str):
                        raise ValueError(f"Insight {idx+1}: field '{field}' must be a string")
            
            # Create InsightObject with provided data and defaults for optional fields
            insight_obj = InsightObject(
                insight=item["insight"],
                context=item["context"],
                source_reference=item["source_reference"],
                key_data=item["key_data"],
                priority_level=item.get("priority_level", "medium"),
                content_type=item.get("content_type", "general"),
                target_audience=item.get("target_audience", "general")
            )
            insights.append(insight_obj)
        
        return insights
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in {file_path}: {e}")
    except FileNotFoundError:
        raise ValueError(f"Insights file not found: {file_path}")
    except Exception as e:
        raise ValueError(f"Error loading insights from {file_path}: {e}")
 
def validate_insight_object(obj: InsightObject) -> bool:
    """
    Validate that an InsightObject has required fields and proper data types.
    
    Args:
        obj: InsightObject to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = [
        ("insight", str),
        ("context", str),
        ("source_reference", list),
        ("key_data", str)
    ]
    
    for field_name, field_type in required_fields:
        if not hasattr(obj, field_name) or not isinstance(getattr(obj, field_name), field_type):
            return False
    
    return True
 
# ----------------------------------------------------------------------
# Helper – Generate insights
# ----------------------------------------------------------------------
async def get_insights(topic: str, max_insights: int, verbose: bool = False, gr_verbose: bool = False) -> tuple[list[InsightObject], str, str, str, int, int, float]:
    """
    Use GPTResearcher to gather raw research, then extract structured insights using local LLM.

    Args:
        topic: The broad subject (e.g., "remote work productivity").
        max_insights: Upper bound of insights to request.
        verbose: If True, prints general script progress information.
        gr_verbose: If True, enables GPT-Researcher verbose output.

    Returns:
        Tuple of (insight_objects, prompt_used, raw_output, extraction_json, prompt_words, completion_words, research_subtotal_usd).
    """

    company_operation_content = read_file(COMPANY_OPERATION_FILE)
    content_marketing_guidance_content = read_file(CONTENT_MARKETING_GUIDANCE_FILE)
    context_content = read_file(CONTEXT_FILE)

    prompt = load_prompt_template(
        "insight_prompt_guidance",
        company_operation_content=company_operation_content,
        content_marketing_guidance_content=content_marketing_guidance_content,
        context_content=context_content,
        max_insights=max_insights,
        topic=topic
    )

    if verbose:
        print("🔎 Generating insights…")
    researcher = GPTResearcher(
        query=prompt,
    #    report_type="deep",
        verbose=gr_verbose
    )
    try:
        # Capture cost before research
        start_cost = researcher.get_costs()
        
        # Stage 1: Get raw research from GPT-Researcher
        raw = await researcher.conduct_research()
        raw_text = str(raw)
        
        # Capture cost after research to get research subtotal
        research_subtotal_usd = researcher.get_costs() - start_cost
        
        # Calculate word counts for approximation
        prompt_words = count_words(prompt)
        completion_words = count_words(raw_text)
        
        # Stage 2: Extract clean insights using local LLM
        insights, extraction_json = await extract_insights_from_raw(
            raw_text, topic, max_insights, verbose
        )
        
        return insights, prompt, raw_text, extraction_json, prompt_words, completion_words, research_subtotal_usd
    except Exception as exc:
        raise RuntimeError(f"Failed to generate insights: {exc}") from exc

# ----------------------------------------------------------------------
# Helper – Extract insights from raw research using local LLM
# ----------------------------------------------------------------------
async def extract_insights_from_raw(
    raw_text: str, topic: str, max_insights: int, verbose: bool = False
) -> tuple[list[InsightObject], str]:
    """
    Extract structured insights from raw GPT-Researcher output using local vLLM.
    
    Args:
        raw_text: Raw research output from GPT-Researcher
        topic: The research topic
        max_insights: Maximum number of insights to extract
        verbose: If True, prints progress information
        
    Returns:
        Tuple of (insight_objects, extraction_json_output)
    """
    # Create OpenAI client using the configured vLLM endpoint
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "sk-dummy-key-if-not-needed"),
        base_url=os.getenv("OPENAI_API_BASE")
    )
    
    # Limit raw text to avoid token limits (keep first ~80k chars for large context models)
    #truncated_raw = raw_text[:80000] if len(raw_text) > 80000 else raw_text
    truncated_raw = raw_text
    
    extraction_prompt = load_prompt_template(
        "extract_insight_prompt",
        max_insights=max_insights,
        topic=topic,
        truncated_raw=truncated_raw,
    )

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
            temperature=0.1,
            max_tokens=10000
        )
        
        json_output = response.choices[0].message.content
        if json_output is None:
            raise ValueError("Empty response from LLM")
        json_output = json_output.strip()
        
        # Try to parse JSON
        try:
            if verbose:
                print(f"🔍 JSON extraction output:\n{json_output}\n")
            
            insights_data = json.loads(json_output)
            if not isinstance(insights_data, list):
                raise ValueError("JSON is not a list")
            
            # Convert to InsightObject instances
            insight_objects = []
            for item in insights_data:
                if isinstance(item, dict):
                    # Create InsightObject with default values for missing fields
                    insight_obj = InsightObject(
                        insight=item.get("insight", ""),
                        context=item.get("context", ""),
                        source_reference=item.get("source_reference", []),
                        key_data=item.get("key_data", ""),
                        priority_level=item.get("priority_level", "medium"),
                        content_type=item.get("content_type", "general"),
                        target_audience=item.get("target_audience", "general")
                    )
                    insight_objects.append(insight_obj)
                else:
                    # Handle non-dictionary items (shouldn't happen but safe)
                    insight_objects.append(InsightObject(insight=str(item)))
            
            # Limit to max_insights
            insight_objects = insight_objects[:max_insights]
            if verbose:
                print(f"✅ Extracted {len(insight_objects)} structured insights from JSON")
            return insight_objects, json_output
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
                        fallback_insights.append(InsightObject(insight=cleaned))
            
            # If heuristic parsing also fails, use raw text fallback
            if not fallback_insights:
                if verbose:
                    print("⚠️ Heuristic parsing failed, using raw text fallback")
                fallback_insights = []
                for line in raw_text.splitlines():
                    line = line.strip().lstrip('-•* ').strip()
                    if line and len(line) > 10 and len(line) < 200:
                        fallback_insights.append(InsightObject(insight=line))
            
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
                fallback_insights.append(InsightObject(insight=line))
        
        return fallback_insights[:max_insights], f"Extraction failed: {str(e)}"

# ----------------------------------------------------------------------
# Helper – Extract title from blog post using local LLM
# ----------------------------------------------------------------------
async def extract_title_from_blog_post(
    blog_post_md: str, insight: str, verbose: bool = False
) -> str:
    """
    Extract a clean title from blog post markdown using local vLLM.
    
    Args:
        blog_post_md: The generated blog post markdown content
        insight: The original insight (used as fallback)
        verbose: If True, prints progress information
        
    Returns:
        Extracted title string, or insight text if extraction fails
    """
    # Create OpenAI client using the configured vLLM endpoint
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "sk-dummy-key-if-not-needed"),
        base_url=os.getenv("OPENAI_API_BASE")
    )
    
    # Limit blog post to avoid token limits (keep first ~40k chars for large context models)
    #truncated_post = blog_post_md[:40000] if len(blog_post_md) > 40000 else blog_post_md
    truncated_post = blog_post_md
    
    # Read the title guidance content
    titles_content = read_file(TITLES_FILE)
    
    extraction_prompt = load_prompt_template(
        "extract_title_prompt",
        title_guidance=titles_content,        
        truncated_post=truncated_post,
    )

    if verbose:
        print("📝 Extracting title using local LLM...")
    
    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=os.getenv("OPENAI_MODEL_NAME", "none"),
            messages=[
                {"role": "system", "content": "You extract clean titles from blog post content. Return only the title text without markdown formatting."},
                {"role": "user", "content": extraction_prompt}
            ],
            temperature=0.1,
            max_tokens=5000
        )
        
        title_output = response.choices[0].message.content
        if title_output is None:
            raise ValueError("Empty response from LLM")
        
        # Clean up the extracted title
        title = title_output.strip().strip('"').strip("'").strip("#").strip()
        
        if verbose:
            print(f"📝 Extracted title: {title}")
        
        # Validate the title - should be reasonable length and not empty
        if title and len(title) > 3 and len(title) < 200:
            return title
        else:
            if verbose:
                print(f"⚠️ Title extraction gave unreasonable result: '{title}', using fallback")
            return insight
          
    except Exception as e:
        if verbose:
            print(f"⚠️ Title extraction failed: {e}, using insight as fallback")
        return insight

# ----------------------------------------------------------------------
# Helper – Generate a blog post draft for a single insight
# ----------------------------------------------------------------------
async def generate_blog_post(
    topic: str, insight_obj: InsightObject, verbose: bool = False, gr_verbose: bool = False
) -> tuple[str, int, int, float]:
    """
    Generate a markdown‑formatted blog post (outline/draft) for a given structured insight.

    Args:
        topic: The overarching topic supplied by the user.
        insight_obj: Structured insight object containing context, data, and metadata.
        verbose: If True, prints general script progress information.
        gr_verbose: If True, enables GPT-Researcher verbose output.

    Returns:
        Markdown string containing the blog post.
    """

    company_operation_content = read_file(COMPANY_OPERATION_FILE)
    content_marketing_guidance_content = read_file(CONTENT_MARKETING_GUIDANCE_FILE)
    context_content = read_file(CONTEXT_FILE)
    titles_content = read_file(TITLES_FILE)

    prompt = load_prompt_template(
        "create_blog-post_prompt_guidance",
        company_operation_content=company_operation_content,
        content_marketing_guidance_content=content_marketing_guidance_content,
        context_content=context_content,
        voice_new_yorker=VOICE_DEFINITIONS["TheNewYorker"],
        voice_atlantic=VOICE_DEFINITIONS["TheAtlantic"],
        voice_wired=VOICE_DEFINITIONS["Wired"],
        titles_content=titles_content,
        insight=insight_obj.insight,
        context=insight_obj.context,
        key_data=insight_obj.key_data,
        source_reference="; ".join(insight_obj.source_reference) if insight_obj.source_reference else "",
        priority_level=insight_obj.priority_level,
        content_type=insight_obj.content_type,
        target_audience=insight_obj.target_audience,
        topic=topic,
        formatting_rules=FORMATTING_RULES,
    )

    if verbose:
        print(f"🖋️ Generating blog post for: {insight_obj.insight[:60]}…")
    researcher = GPTResearcher(
        query=prompt,
        report_type="deep",
        verbose=gr_verbose
    )
    try:
        # Capture cost before research
        start_cost = researcher.get_costs()
        
        # Conduct research and write report
        await researcher.conduct_research()
        report = await researcher.write_report()
        
        # Capture cost after generation to get subtotal
        subtotal_usd = researcher.get_costs() - start_cost
        
        # Calculate word counts for approximation
        prompt_words = count_words(prompt)
        completion_words = count_words(str(report))
        
        return str(report), prompt_words, completion_words, subtotal_usd
    except Exception as exc:
        raise RuntimeError(
            f"Failed to generate blog post for '{insight_obj.insight}': {exc}"
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
        required=False,
        help="Broad research topic (e.g., 'remote work productivity').",
    )
    parser.add_argument(
        "--max-insights",
        type=int,
        default=15,
        help="Maximum number of insights to generate (default: 15).",
    )
    parser.add_argument(
        "--insights-output",
        default="insights.json",
        help="Path to JSON file that will contain the initial insight list.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed progress logging for the script.",
    )
    parser.add_argument(
        "--gr-verbose",
        action="store_true",
        help="Enable verbose output for GPT-Researcher operations.",
    )
    parser.add_argument(
        "--insights-only",
        action="store_true",
        help="Generate only insights and stop before creating blog posts.",
    )
    parser.add_argument(
        "--insights-input",
        type=str,
        help="Path to JSON file containing structured insights for blog generation. When provided, skips insight generation and creates blog posts from the file.",
    )
    parser.add_argument(
        "--posts-dir",
        type=str,
        default="posts",
        help="Directory to save blog post files (default: 'posts'). Will be created if it doesn't exist.",
    )
    args = parser.parse_args()

    # Validate that topic is provided unless insights-input is used
    if not args.insights_input and not args.topic:
        parser.error("--topic is required unless --insights-input is provided")

    # ------------------------------------------------------------------
    # Prepare environment
    # ------------------------------------------------------------------
    try:
        load_environment()
        
        # Debug: Verify temperature settings are loaded from .env
    #    print(f"🔧 [DEBUG] Temperature settings loaded from .env:")
    #    print(f"   TEMPERATURE: {os.getenv('TEMPERATURE', 'not set')}")
    #    print(f"   FAST_TEMPERATURE: {os.getenv('FAST_TEMPERATURE', 'not set')}")
    #    print(f"   SMART_TEMPERATURE: {os.getenv('SMART_TEMPERATURE', 'not set')}")
    #    print(f"   STRATEGIC_TEMPERATURE: {os.getenv('STRATEGIC_TEMPERATURE', 'not set')}")
        print()
        
    except Exception as e:
        print(f"❌ Environment setup error: {e}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # Generate insights list
    # ------------------------------------------------------------------
    try:
        if args.insights_input:
            # Load insights from file and skip generation
            insights_path = Path(args.insights_input)
            if not insights_path.exists():
                print(f"❌ Error: Insights file not found: {insights_path}")
                sys.exit(1)
            
            if args.verbose:
                print(f"📂 Loading insights from: {insights_path.resolve()}")
            
            insights = load_insights_from_file(insights_path)
            prompt_used = f"Blog generation from provided insights file: {args.insights_input}"
            raw_output = "Insights loaded from file"
            extraction_json = json.dumps([{
                "insight": obj.insight,
                "context": obj.context,
                "source_reference": obj.source_reference,
                "key_data": obj.key_data,
                "priority_level": obj.priority_level,
                "content_type": obj.content_type,
                "target_audience": obj.target_audience
            } for obj in insights])
            research_prompt_words = count_words(prompt_used)
            research_completion_words = count_words(raw_output)
            research_subtotal_usd = 0.0
        else:
            # Normal mode - generate insights using GPT-Researcher
            # If running under pytest, use dummy data to avoid long LLM calls
            if os.getenv("PYTEST_CURRENT_TEST"):
                # Create structured dummy insights
                insights = [
                    InsightObject(
                        insight=f"Dummy insight {i+1}",
                        context="This is a dummy context for testing purposes",
                        source_reference=["https://example.com/dummy"],
                        key_data="Dummy data: 100%",
                        priority_level="medium",
                        content_type="general",
                        target_audience="general"
                    ) for i in range(min(args.max_insights, 5))
                ]
                prompt_used = f"Dummy prompt for topic '{args.topic}'"
                raw_output = "Dummy raw output for testing"
                extraction_json = '[{"insight": "Dummy insight 1", "context": "Dummy context", "source_reference": ["https://example.com/dummy"], "key_data": "Dummy data", "priority_level": "medium", "content_type": "general", "target_audience": "general"}]'
                research_prompt_words = count_words(prompt_used)
                research_completion_words = count_words(raw_output)
                research_subtotal_usd = 0.0
            else:
                insights, prompt_used, raw_output, extraction_json, research_prompt_words, research_completion_words, research_subtotal_usd = await get_insights(
                    args.topic, args.max_insights, verbose=args.verbose, gr_verbose=args.gr_verbose
                )
    except Exception as e:
        print(f"❌ Error while loading/generating insights: {e}")
        sys.exit(1)

    if not insights:
        print("⚠️ No insights were returned – aborting.")
        sys.exit(0)

    if args.verbose:
        print(f"✅ Retrieved {len(insights)} structured insights.\n")

    # ------------------------------------------------------------------
    # Write insights to JSON file with debug information
    # ------------------------------------------------------------------
    insights_path = Path(args.insights_output)
    try:
        insights_path.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create JSON-compatible data structure that matches load_insights_from_file() expectations
        # The function expects a list of insight dictionaries, so we write the insights array directly
        insights_for_json = []
        for insight_obj in insights:
            insight_dict = {
                "insight": insight_obj.insight,
                "context": insight_obj.context,
                "source_reference": insight_obj.source_reference,
                "key_data": insight_obj.key_data,
                "priority_level": insight_obj.priority_level,
                "content_type": insight_obj.content_type,
                "target_audience": insight_obj.target_audience
            }
            insights_for_json.append(insight_dict)
        
        # Write JSON data to file (overwrite mode for canonical format)
        with insights_path.open("w", encoding="utf-8") as f:
            json.dump(insights_for_json, f, indent=2, ensure_ascii=False)
        
        if args.verbose:
            print(f"✅ Insights debug information written to {insights_path.resolve()}")
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
    for idx, insight_obj in enumerate(insights, start=1):
        try:
            if os.getenv("PYTEST_CURRENT_TEST"):
                # Generate a simple dummy markdown for testing
                post_md = f"# {insight_obj.insight}\n\nDummy content for testing."
                post_prompt_words = count_words(f"Generate blog post for: {insight_obj.insight}")
                post_completion_words = count_words(post_md)
                post_subtotal_usd = 0.0
            else:
                #print(f"********** generating blog post with the insight: {insight_obj.insight}")
                post_md, post_prompt_words, post_completion_words, post_subtotal_usd = await generate_blog_post(args.topic, insight_obj, verbose=args.verbose, gr_verbose=args.gr_verbose)

            # Extract title using LLM instead of regex matching
            if os.getenv("PYTEST_CURRENT_TEST"):
                # Use simple title for testing
                title = insight_obj.insight
            else:
                title = await extract_title_from_blog_post(post_md, insight_obj.insight, verbose=args.verbose)

            # Write individual markdown file with cost summary
            posts_dir = Path(args.posts_dir)
            posts_dir.mkdir(parents=True, exist_ok=True)
            filename = slugify(title) + ".md"
            file_path = posts_dir / filename
            try:
                with file_path.open("w", encoding="utf-8") as f:
                    f.write(post_md)
                    f.write("\n\n---\n\n")
                    f.write("## Cost Summary\n\n")
                    f.write(f"- prompt_words: {post_prompt_words}\n")
                    f.write(f"- completion_words: {post_completion_words}\n")
                    f.write(f"- subtotal_usd: ${post_subtotal_usd:.4f}\n")
                if args.verbose:
                    print(f"✅ Blog post written to {file_path.resolve()}")
            except Exception as e:
                print(f"❌ Failed to write blog post file '{filename}': {e}")

        except Exception as e:
            print(f"⚠️ Skipping insight due to error: {e}")

    if args.verbose:
        print(f"✅ Blog post generation completed for {len(insights)} insights.")

# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main_cli())
