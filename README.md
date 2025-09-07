# Content Marketing Research System

This repository implements a distributed AI research platform for generating professional content‑marketing reports.

## New Feature

**`spt_researcher.py`** – a CLI utility that:
- Accepts a broad topic (`--topic`) and optional output path.
- Generates 10‑20 user pain points using **GPT‑Researcher**.
- Iteratively creates markdown‑formatted blog‑post drafts for each pain point.
- Writes all results to a single markdown file.

### Usage
```bash
pipenv run python spt_researcher.py --topic "remote work productivity" \
    --output generated_posts.md --max-points 15 --verbose
```

For detailed documentation see **[SPT_RESEARCHER_GUIDE.md](SPT_RESEARCHER_GUIDE.md)**.

## Existing Components

- `test.py` / `test_researcher.py` – core research scripts.
- `switch_embedding.py` / `switch_search.py` – utilities for switching configurations.
- Test suite (`test_*.py`) validates vLLM, Ollama, Tavily, and SearXNG integrations.

## Architecture & Context

- Updated architecture diagram now includes `spt_researcher.py` as a core script.
- Memory bank (`.kilocode/rules/memory-bank/`) reflects the new feature in both **architecture.md** and **context.md**.

---

*Generated on 2025‑09‑07 by the Content‑Marketing Research System.*