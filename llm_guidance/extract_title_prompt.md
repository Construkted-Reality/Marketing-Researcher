Extract the main title from this blog post markdown content. Return ONLY the title text from the first H1 heading (a line starting with a single '# ').
If no H1 heading exists, return an empty string.

Use these instructions to guide your title generation:
{title_guidance}

Constraints:
- Do not generate or rewrite a title; only extract.
- Do not include markdown, quotes, code fences, labels (e.g., "Title:"), or extra text.
- Trim surrounding whitespace.

Blog post content:
{truncated_post}
