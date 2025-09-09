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
**SPT Researcher Two-Stage Insight Extraction**: Implemented robust two-stage insight extraction to fix parsing issues in `spt_researcher.py`. The previous single-stage approach failed because GPT-Researcher returns research corpus data instead of clean bullet lists, causing line-by-line parsing to produce garbage insights.

**New Architecture**:
- **Stage 1**: GPT-Researcher gathers raw research data from web sources
- **Stage 2**: Local vLLM server extracts clean JSON array of actionable insights from raw data
- **Fallback Logic**: Heuristic parsing if JSON extraction fails, with comprehensive error handling

**Enhanced Debugging**: Extended debug output to include JSON extraction stage, showing the exact JSON output from the local LLM extractor before parsing into the final insights array. Console debugging added for real-time visibility during extraction process.

**Key Improvements**:
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