## Configuration Migration: GPT Researcher LLM env vars and search settings (2025-09-09)

- Deprecated variables removed to satisfy FutureWarning:
  - LLM_PROVIDER, FAST_LLM_MODEL, SMART_LLM_MODEL
- Adopted new GPT Researcher LLM variables and provider-specific settings:
  - FAST_LLM=vllm_openai:gpt-oss-120b
  - SMART_LLM=vllm_openai:gpt-oss-120b
  - STRATEGIC_LLM=vllm_openai:gpt-oss-120b
  - VLLM_OPENAI_API_BASE=http://192.168.8.90:42069/v1
  - VLLM_OPENAI_API_KEY=outsider
- Retained local extractor variables required by spt_researcher.py for OpenAI-compatible client:
  - OPENAI_API_KEY=outsider
  - OPENAI_API_BASE=http://192.168.8.90:42069/v1
  - OPENAI_MODEL_NAME=gpt-oss-120b
- Important: Removing legacy LLM_PROVIDER without adding VLLM_OPENAI_* caused GPT Researcher LLM calls to return None, producing JSON parsing errors in insight extraction. Resolved by adding VLLM_OPENAI_* while keeping OPENAI_* for the local extractor.

Search configuration clarification:
- RETRIEVER controls which web search engines GPT Researcher uses and can chain engines, e.g.:
  - RETRIEVER=searx,mcp
  - RETRIEVER=tavily,mcp
  - RETRIEVER=tavily,bing,arxiv
- SEARCH_PROVIDER is not used by current GPT Researcher in this repo and can be removed or ignored to avoid confusion.
# Current Context: Content Marketing Research System

## Current Status
**System is fully operational** as of September 7, 2025. All major components working together seamlessly.

## Recent Achievements
- ✅ Resolved GPT Researcher syntax errors (top-level await issue)
- ✅ Implemented distributed LAN architecture with multiple servers
- ✅ Configured Ollama embeddings on separate server (192.168.8.90:11434)
- ✅ Integrated SearXNG self-hosted search engine with privacy-first architecture
- ✅ Created search engine configuration switching system (SearXNG/Tavily)
- ✅ Built comprehensive testing suite for all components including SearXNG connectivity
- ✅ Generated high-quality research reports with real web citations
- ✅ Validated end-to-end SearXNG research workflow with professional report output

## Current Work Focus
## Key Files Modified Today (SPT Researcher: Two-Stage Insight Extraction & Insights-Only Mode)
- **`spt_researcher.py`**: Enhanced with two-stage insight extraction using local vLLM server and `--insights-only` mode
- **`test_spt_researcher.py`**: Expanded with 5 new test functions covering JSON parsing, input override, and debug logging
- **`SPT_RESEARCHER_GUIDE.md`**: Updated with troubleshooting workflows for JSON extraction and insights-only flow
- Added `extract_insights_from_raw()` with vLLM-powered JSON-first parser and noise-filtered fallback
- Implemented `--insights-only` CLI flag to skip blog post generation and exit after insights write
- Enhanced debug output with timestamped sessions: prompt, raw output, and parsed insights
- Preserved backward compatibility: canonical JSON (`pain_points.json`) + optional markdown (`--pain-points-markdown`)

## Performance Metrics
- Research report generation: ~2 minutes end-to-end (both SearXNG and Tavily)
- Web source scraping: 15+ relevant sources per query (36 results found with SearXNG)
- Embedding processing: Fast (distributed server)
- System reliability: 100% success rate in recent tests
- SearXNG cost: $0.0224863 per research report (very economical vs. Tavily)
- Privacy: Complete search privacy achieved with SearXNG integration