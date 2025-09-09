# SPT Researcher – Insights & Blog‑Post Generator

`spt_researcher.py` is a helper utility built on **GPT‑Researcher** that automates the first two stages of a content‑marketing workflow:

1. **Insight discovery** – Given a broad topic, the script asks GPT‑Researcher to list 10‑20 actionable insights and content topics.
2. **Blog‑post drafting** – For each insight, the script generates a concise markdown blog‑post outline.

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
| `--max-insights <int>` | Upper bound for the number of insights to generate (default: `15`). |
| `--insights-output <path>` | Path to markdown file that will contain the initial insight list (default: `insights.md`). |
| `--verbose` | Enable detailed progress logging. |
| `-h, --help` | Show help message. |

### Example

```bash
python spt_researcher.py \
    --topic "remote work productivity" \
    --output remote_posts.md \
    --max-insights 12 \
    --verbose
```

The script will:

1. Print progress messages (if `--verbose` is set).
2. Create `remote_posts.md` containing a top‑level heading, followed by numbered sections—each section starts with the insight title and includes the generated blog‑post markdown.
3. Create `insights.md` with debug information showing the generated insights list.
4. Create individual blog post files in the `posts/` directory.

## Output format

```markdown
# Blog Posts for Topic: remote work productivity

## 1. Insight #1
<markdown blog post>

---

## 2. Insight #2
<markdown blog post>

...
```

## Troubleshooting

- **Missing environment variables** – The script aborts with a clear error if `OPENAI_API_BASE` or `OPENAI_MODEL_NAME` is not set.
- **GPT‑Researcher failures** – Errors from the underlying library are caught and reported; the script will continue with the next insight.
- **No output generated** – Ensure the `.env` file points to a reachable vLLM server and that the required API keys are valid.

## Extending the script

- **Custom prompts** – Modify the `prompt` strings inside `get_insights` or `generate_blog_post` to change the style or depth of the output.
- **Different output formats** – Replace the markdown writer with a Jinja2 template to produce HTML, PDF, etc.

---

*Created by the Content‑Marketing Research System on 2025‑09‑07.*