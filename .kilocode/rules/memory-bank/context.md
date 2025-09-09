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
**SPT Researcher Insights-Only Mode (September 9, 2025)**: Added `--insights-only` command line switch to `spt_researcher.py` that stops execution after generating insights but before creating blog posts. This provides users with a faster way to get research insights without the time-consuming blog post generation phase.

**New Feature**:
- **Early Exit Logic**: Added conditional check for `args.insights_only` flag
- **Clean Termination**: Script exits gracefully with success message after insights generation
- **Preserved Functionality**: All existing insights generation and file output remains intact
- **Usage Documentation**: Updated file header and argument parser with new flag

**Previous Achievement - SPT Researcher Two-Stage Insight Extraction**: Implemented robust two-stage insight extraction to fix parsing issues. The previous single-stage approach failed because GPT-Researcher returns research corpus data instead of clean bullet lists.

**Two-Stage Architecture**:
- **Stage 1**: GPT-Researcher gathers raw research data from web sources
- **Stage 2**: Local vLLM server extracts clean JSON array of actionable insights from raw data
- **Fallback Logic**: Heuristic parsing if JSON extraction fails, with comprehensive error handling

**Key Improvements from Recent Work**:
- `--insights-only` flag for faster research workflow (new)
- Reliable insight extraction regardless of GPT-Researcher output format changes
- Local processing maintains privacy (no external AI API calls)
- JSON-first approach eliminates brittle regex/line-based parsing
- Multiple fallback strategies ensure robustness
- Enhanced debugging for troubleshooting extraction issues

## Active Configuration
- **vLLM Server**: 192.168.8.90:42069 (gpt-oss-120b model)
- **Ollama Server**: 192.168.8.90:11434 (mxbai-embed-large model)
- **Embedding Mode**: Distributed (Ollama server)
- **Web Search**: SearXNG + MCP hybrid mode (default) with Tavily backup
- **GPT Researcher**: Full web + LLM hybrid mode with privacy-first search

## Next Steps
1. Monitor SearXNG performance and reliability over time
2. Consider setting up backup SearXNG instances for redundancy
3. Explore additional privacy-first research tools and integrations
4. Document maintenance procedures for SearXNG instance management

## Key Files Modified Recently
**SPT Researcher Insights-Only Mode (September 9, 2025):**
- Added `--insights-only` command line argument to argument parser
- Implemented early exit logic after insights file writing but before blog post generation
- Updated usage documentation in file header comments
- Added success message showing number of insights generated in insights-only mode

**SPT Researcher Two-Stage Extraction (September 9, 2025):**
- Implemented `extract_insights_from_raw()` function with local vLLM integration
- Modified `get_insights()` to use two-stage approach (GPT-Researcher + local extractor)
- Added JSON import and OpenAI client setup for extractor functionality
- Enhanced debugging output to include JSON extraction stage with console debugging
- Added robust fallback parsing when JSON extraction fails
- Updated function signatures to handle new tuple return format

**Previous Enhancements:**
- **SearXNG Integration (September 7, 2025)**: Complete privacy-first search integration
- **SPT Researcher Debug Enhancement (September 8, 2025)**: Timestamped debug sessions and comprehensive output logging

## Performance Metrics
- Research report generation: ~2 minutes end-to-end (both SearXNG and Tavily)
- Web source scraping: 15+ relevant sources per query (36 results found with SearXNG)
- Embedding processing: Fast (distributed server)
- System reliability: 100% success rate in recent tests
- SearXNG cost: $0.0224863 per research report (very economical vs. Tavily)
- Privacy: Complete search privacy achieved with SearXNG integration