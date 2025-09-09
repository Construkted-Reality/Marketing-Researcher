# SPT Researcher – Insights & Blog‑Post Generator

`spt_researcher.py` is a helper utility built on **GPT‑Researcher** that automates the first two stages of a content‑marketing workflow:

<<<<<<< HEAD
1. **Insight discovery** – Given a broad topic, the script asks GPT‑Researcher to list 10‑20 actionable insights and content topics.
2. **Blog‑post drafting** – For each insight, the script generates a concise markdown blog‑post outline.
=======
1. **Pain‑point discovery** – Given a broad topic, the script uses a JSON-only schema to generate structured, clean pain points.
2. **Blog‑post drafting** – For each pain‑point, the script generates a concise markdown blog‑post outline.
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba

## Key Features

- **JSON-First Architecture**: Step-1 outputs canonical JSON that feeds directly into step-2
- **Noise-Filtered Parsing**: Automatically filters out web scraping artifacts like "Source:", "Try again", etc.
- **Reproducible Workflows**: Save step-1 output and replay step-2 without re-generation
- **Troubleshooting Support**: Inspect exact payload between steps for debugging

## Prerequisites

- Python 3.12 (or later)
- Project dependencies installed (`pipenv install` or `pip install -r requirements.txt`)
- `.env` file with required variables:
  - `OPENAI_API_BASE` – URL of the vLLM server (e.g., `http://192.168.8.90:42069/v1`)
  - `OPENAI_MODEL_NAME` – model identifier used by the vLLM server
  - `OPENAI_API_KEY` – dummy key is acceptable if the server does not require it
  - Optional: `TAVILY_API_KEY` if you prefer the Tavily search backend

## Installation

The script lives in the project root. No additional installation steps are required beyond the standard project setup.

```bash
# Ensure you are in the project directory
cd "/home/outsider/Coding Projects/Content-Marketing-Research-02"

# Activate the Pipenv environment (if used)
pipenv shell

# Verify the script is executable
chmod +x spt_researcher.py
```

## Usage

```bash
python spt_researcher.py --topic "<broad topic>" [options]
```

### Required argument

- `--topic` – The high‑level subject you want to research (e.g., `"remote work productivity"`).

### Optional arguments

| Flag | Description |
|------|-------------|
| `--output <path>` | Destination markdown file (default: `generated_blog_posts.md`). |
<<<<<<< HEAD
| `--max-insights <int>` | Upper bound for the number of insights to generate (default: `15`). |
| `--insights-output <path>` | Path to markdown file that will contain the initial insight list (default: `insights.md`). |
=======
| `--max-points <int>` | Upper bound for the number of pain‑points to generate (default: `15`). |
| `--pain-points-output <path>` | **Canonical JSON dump** of step-1 output (default: `pain_points.json`). |
| `--pain-points-input <path>` | Load existing JSON dump and skip step-1 generation. |
| `--pain-points-markdown <path>` | Optional human-readable markdown list (non-canonical). |
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba
| `--verbose` | Enable detailed progress logging. |
| `-h, --help` | Show help message. |

### Basic Example

```bash
python spt_researcher.py \
    --topic "remote work productivity" \
    --output remote_posts.md \
    --max-insights 12 \
    --verbose
```

This will:
1. Generate pain points using JSON-only schema (step-1)
2. Write canonical JSON to `pain_points.json`
3. Generate blog posts for each pain point (step-2)
4. Create individual post files in `posts/` directory
5. Create combined markdown in `remote_posts.md`

<<<<<<< HEAD
1. Print progress messages (if `--verbose` is set).
2. Create `remote_posts.md` containing a top‑level heading, followed by numbered sections—each section starts with the insight title and includes the generated blog‑post markdown.
3. Create `insights.md` with debug information showing the generated insights list.
4. Create individual blog post files in the `posts/` directory.
=======
### Advanced Examples
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba

**Troubleshooting workflow** (inspect step-1 output):
```bash
# Generate and inspect step-1 output
python spt_researcher.py --topic "photogrammetry" --pain-points-output debug_painpoints.json --verbose

# Examine the JSON file to troubleshoot parsing issues
cat debug_painpoints.json | jq .

# Re-run step-2 only using the saved data
python spt_researcher.py --topic "ignored" --pain-points-input debug_painpoints.json --output final_posts.md
```

**Human-readable output** (for review):
```bash
python spt_researcher.py \
    --topic "cloud migration" \
    --pain-points-markdown review_list.md \
    --verbose
```

## Output Files

### Canonical JSON Dump (`pain_points.json`)
The primary output of step-1 - exact payload fed to step-2:
```json
{
  "topic": "photogrammetry",
  "pain_points": [
    "Reflective surfaces break feature matching in reconstruction",
    "Insufficient overlap causes incomplete scene coverage"
  ],
  "meta": {
    "count": 2,
    "generated_at": "2025-09-08T13:30:00Z",
    "source": "gpt_researcher",
    "max_points": 15,
    "parser": "json"
  }
}
```

### Individual Blog Posts (`posts/`)
Each pain point generates a separate markdown file:
- `posts/reflective_surfaces_break_feature_matching.md`
- `posts/insufficient_overlap_causes_incomplete_coverage.md`

### Combined Output (`generated_blog_posts.md`)
```markdown
# Blog Posts for Topic: photogrammetry

<<<<<<< HEAD
## 1. Insight #1
<markdown blog post>
=======
## 1. Reflective surfaces break feature matching in reconstruction
<markdown blog post content>
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba

---------

<<<<<<< HEAD
## 2. Insight #2
<markdown blog post>
=======
## 2. Insufficient overlap causes incomplete scene coverage
<markdown blog post content>
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba

...
```

### Optional Human-Readable List
If `--pain-points-markdown` is specified:
```markdown
# Pain Points for Topic: photogrammetry

*This is a human-readable version. The canonical data is in the JSON file.*

1. Reflective surfaces break feature matching in reconstruction
2. Insufficient overlap causes incomplete scene coverage

---
*Generated: 2025-09-08T13:30:00Z*
*Parser: json*
```

## JSON Schema & Parsing

### Step-1 Prompt Strategy
The script uses a strict JSON-only prompt that enforces:
- No markdown, prose, or commentary
- Exact schema compliance
- Filtering of web scraping artifacts
- Domain-specific, actionable pain points

### Parser Modes
1. **JSON Parser** (preferred): Parses valid JSON with `pain_points[].idea` extraction
2. **Fallback Parser**: Noise-filtered line parsing with regex patterns to remove:
   - `Source: https://...`
   - `Title: ...`
   - `Content: ...`
   - `Try again`
   - `Please enable Javascript`

## Troubleshooting

### Common Issues

**Step-1 Generation Problems**:
```bash
# Inspect the canonical JSON dump
cat pain_points.json | jq .

# Check which parser was used
jq '.meta.parser' pain_points.json

# If fallback parser was used, check for noise
jq '.pain_points[]' pain_points.json | grep -E "(Source|Title|Try again)"
```

**Environment Issues**:
- **Missing environment variables** – The script aborts with a clear error if `OPENAI_API_BASE` or `OPENAI_MODEL_NAME` is not set.
<<<<<<< HEAD
- **GPT‑Researcher failures** – Errors from the underlying library are caught and reported; the script will continue with the next insight.
=======
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba
- **No output generated** – Ensure the `.env` file points to a reachable vLLM server and that the required API keys are valid.

**Step-2 Generation Problems**:
```bash
# Use existing JSON to skip step-1 and isolate step-2 issues
python spt_researcher.py --pain-points-input pain_points.json --topic "ignored" --verbose
```

**Performance Issues**:
- **Long generation times** – Use `--pain-points-input` to iterate on step-2 without re-running step-1
- **GPT‑Researcher failures** – Errors from the underlying library are caught and reported; the script will continue with the next pain‑point.

## Workflow Patterns

### Development Iteration
```bash
# 1. Generate step-1 with debugging
python spt_researcher.py --topic "AI tools" --pain-points-output ai_painpoints.json --verbose

# 2. Review and refine (manual inspection)
cat ai_painpoints.json | jq '.pain_points[]'

# 3. Iterate on step-2 only
python spt_researcher.py --pain-points-input ai_painpoints.json --topic "ignored" --output final_ai_posts.md
```

### Quality Control
```bash
# Generate with human-readable review file
python spt_researcher.py \
    --topic "blockchain adoption" \
    --pain-points-markdown review.md \
    --verbose

# Review the markdown list, then proceed with JSON if satisfied
# (The canonical JSON is always written regardless)
```

## Extending the script

<<<<<<< HEAD
- **Custom prompts** – Modify the `prompt` strings inside `get_insights` or `generate_blog_post` to change the style or depth of the output.
- **Different output formats** – Replace the markdown writer with a Jinja2 template to produce HTML, PDF, etc.
=======
- **Custom prompts** – Modify the JSON schema and rules in `get_pain_points` to change output style
- **Parser improvements** – Enhance `parse_pain_points` noise patterns for better filtering
- **Different output formats** – Replace the markdown writer with templates for HTML, PDF, etc.
- **Integration** – Use `--pain-points-input` to integrate with external pain-point databases

## Testing

Run the test suite to validate functionality:
```bash
# Test JSON dump creation and parsing
PYTEST_CURRENT_TEST=1 pipenv run pytest test_spt_researcher.py::test_json_dump_creation -v

# Test input override functionality
pipenv run pytest test_spt_researcher.py::test_pain_points_input_override -v

# Test parsing functions
pipenv run pytest test_spt_researcher.py::test_json_parsing_functions -v
```
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba

---

*Updated for JSON-first architecture on 2025‑09‑08.*