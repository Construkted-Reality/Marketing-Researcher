# Task Documentation: Content Marketing Research System

## Task: Switch Embedding Configuration
**Last performed:** September 7, 2025
**Files to modify:**
- `.env` - Embedding configuration
- No restart required

**Steps:**
1. Use automated switching utility: `python switch_embedding.py [option]`
2. Or manually edit `.env` file to comment/uncomment desired embedding lines
3. Verify with `python switch_embedding.py current`
4. Test with appropriate validation script

**Options:**
- `ollama`: Distributed Ollama server processing
- `local`: Local HuggingFace sentence transformers
- `nomic`: Alternative Ollama model (nomic-embed-text)

**Important notes:**
- Changes take effect immediately (no restart needed)
- Test connectivity after switching servers
- Local mode requires more memory but no network dependency

## Task: Switch Search Engine Configuration
**Last performed:** September 7, 2025
**Files to modify:**
- `.env` - Search engine configuration
- No restart required

**Steps:**
1. Use automated switching utility: `python switch_search.py [option]`
2. Or manually edit `.env` file to comment/uncomment desired search engine lines
3. Verify with `python switch_search.py current`
4. Test with appropriate validation script

**Options:**
- `searx,mcp`: SearXNG + MCP Hybrid (privacy-first with AI reasoning)
- `tavily,mcp`: Tavily + MCP Hybrid (commercial with AI reasoning)
- `searx`: SearXNG Only (pure self-hosted search)
- `tavily`: Tavily Only (pure commercial search)

**Important notes:**
- Changes take effect immediately (no restart needed)
- Test connectivity after switching search engines
- SearXNG requires working self-hosted instance
- Tavily requires valid API key

## Task: Add New Search Engine
**Last performed:** September 7, 2025
**Files to modify:**
- `switch_search.py` - Add new configuration option
- `.env` - Add new search engine configuration section
- `SEARCH_ENGINE_SWITCHING_GUIDE.md` - Update documentation

**Steps:**
1. Add new search engine configuration to `switch_search.py` SEARCH_OPTIONS dict
2. Add commented configuration lines to `.env` file
3. Create test script if needed (follow `test_searxng_direct.py` pattern)
4. Update switching guide documentation
5. Test new configuration works

**Example addition:**
```python
"custom": {
    "name": "Custom Search Engine",
    "description": "Alternative search service",
    "config": [
        "RETRIEVER=custom",
        "RETRIEVER_ENDPOINT=https://api.mysearch.com",
        "RETRIEVER_ARG_API_KEY=YOUR_API_KEY"
    ],
    "comment_out": ["RETRIEVER=searx,mcp", "RETRIEVER=tavily,mcp"]
}
```

## Task: Add New Embedding Server
**Last performed:** September 7, 2025
**Files to modify:**
- `switch_embedding.py` - Add new configuration option
- `.env` - Add new server configuration section
- `EMBEDDING_SWITCHING_GUIDE.md` - Update documentation

**Steps:**
1. Add new server configuration to `switch_embedding.py` EMBEDDING_OPTIONS dict
2. Add commented configuration lines to `.env` file
3. Create test script if needed (follow `test_ollama_embedding.py` pattern)
4. Update switching guide documentation
5. Test new configuration works

**Example addition:**
```python
"server2": {
    "name": "Ollama Server 2 (different-model)",
    "description": "Alternative server setup",
    "config": [
        "EMBEDDING=ollama:different-model",
        "OLLAMA_BASE_URL=http://192.168.8.91:11434"
    ],
    "comment_out": ["EMBEDDING=huggingface:sentence-transformers/all-MiniLM-L6-v2"]
}
```

## Task: Troubleshoot GPT Researcher Issues
**Last performed:** September 7, 2025
**Common issues and solutions:**

**1. Top-level await errors:**
- Symptom: `SyntaxError: 'await' outside function`
- Solution: Wrap code in `async def main()` and call with `asyncio.run(main())`

**2. Missing dependencies:**
- Symptom: `ModuleNotFoundError: No module named 'X'`
- Solution: Add to `Pipfile` and run `pipenv install`

**3. LLM connection errors:**
- Symptom: `None` responses or 404 errors
- Solution: Verify server connectivity with `test_vllm_direct.py`

**4. Embedding errors:**
- Symptom: `No embedding data received`
- Solution: Test with `test_ollama_embedding.py`, switch to local if needed

**5. Tavily authentication:**
- Symptom: `401 Unauthorized`
- Solution: Test with `test_tavily_direct.py`, update API key if expired

**6. SearXNG connectivity:**
- Symptom: `Failed to connect to SearXNG`
- Solution: Test with `test_searxng_direct.py`, verify SearXNG URL and instance status

**7. SearXNG search failures:**
- Symptom: `Search API returned status code 429` or empty results
- Solution: Check SearXNG rate limits, switch to `SCRAPER=browser` for slower scraping

**Debugging workflow:**
1. Run component test scripts to isolate issue
2. Check `.env` configuration matches server setup
3. Verify network connectivity between servers
4. Review error logs for specific failure points

## Task: Generate Research Report
**Last performed:** September 7, 2025
**Files used:**
- `test.py` - Main research script
- `test_researcher.py` - Alternative with different query
- `.env` - Configuration

**Steps:**
1. Ensure all servers are running and configured
2. Run validation: `pipenv run python test_vllm_direct.py`
3. Run research: `pipenv run python test.py`
4. Monitor output for errors and performance
5. Review generated report quality

**Performance expectations:**
- Total time: ~2 minutes end-to-end
- Web sources: 15+ relevant URLs found and scraped
- Report length: 2000+ words with proper citations
- Cost: ~$0.02 for complete research cycle

**Quality indicators:**
- Real financial data and current market information
- Proper citation format with working URLs
- Professional formatting with tables and sections
- No hallucinated data (all claims sourced)

## Task: System Health Check
**Frequency:** Weekly or before important research
**Files to run:**
- `test_vllm_direct.py` - vLLM server health
- `test_ollama_embedding.py` - Ollama server health
- `test_tavily_direct.py` - Tavily API key validation
- `test_searxng_direct.py` - SearXNG connectivity validation

**Steps:**
1. Test vLLM connectivity: `pipenv run python test_vllm_direct.py`
2. Test Ollama embeddings: `pipenv run python test_ollama_embedding.py`
3. Test Tavily API: `pipenv run python test_tavily_direct.py`
4. Test SearXNG connectivity: `pipenv run python test_searxng_direct.py`
5. Run end-to-end test: `pipenv run python test.py`
6. Document any issues or performance changes

**Success criteria:**
- All tests pass with ✅ indicators
- Response times within expected ranges
- No 404, 401, or connection errors
- Generated reports maintain quality standards

## Task: Update Dependencies
**When needed:** New GPT Researcher version, security updates
**Files to modify:**
- `Pipfile` - Package versions
- May require code updates for breaking changes

**Steps:**
1. Backup current working configuration
2. Update `Pipfile` with new versions
3. Run `pipenv install`
4. Test all components for compatibility
5. Update code if API changes occurred
6. Validate system still works end-to-end

**Rollback plan:**
- Restore `Pipfile.lock` from backup
- Run `pipenv install` to restore previous versions
- Test system functionality

## Task: Test SearXNG Research Quality
**Last performed:** September 7, 2025
**Files used:**
- `test_searxng_direct.py` - SearXNG connectivity test
- `test.py` - Research with SearXNG
- `switch_search.py` - Configuration switching

**Steps:**
1. Switch to SearXNG: `python switch_search.py searx,mcp`
2. Test connectivity: `pipenv run python test_searxng_direct.py`
3. Run research: `pipenv run python test.py`
4. Compare with Tavily: `python switch_search.py tavily,mcp` and rerun
5. Document quality and performance differences

**SearXNG Performance expectations:**
- Total time: ~2 minutes end-to-end
- Web sources: 30+ search results found (vs 15+ with Tavily)
- Cost: ~$0.02 per research report (very economical)
- Privacy: Complete search privacy, no external API calls

**Quality indicators:**
- Similar citation quality to Tavily
- Real-time web data integration
- Professional report formatting
- No degradation in research depth

## Task: Enhance SPT Researcher with File Output
**Last performed:** September 8, 2025
**Files modified:**
- `spt_researcher.py` - Enhanced with insights file output and individual blog post files
- `Pipfile` - Added pytest as dev dependency
- `test_spt_researcher.py` - Updated to handle new functionality

**Steps:**
1. Add new CLI argument `--insights-output` for specifying insights output file
2. Create `slugify(text: str) -> str` helper for safe filename generation
3. Write insights list to separate markdown file after generation
4. Extract article titles from generated blog posts (first `#` or `##` heading)
5. Save each blog post as individual markdown file in `posts/` directory
6. Use slugified title as filename for each blog post
7. Add verbose logging for all file operations
8. Preserve original combined output behavior for backward compatibility
9. Add pytest test optimization with dummy data when `PYTEST_CURRENT_TEST` is set
10. Update memory bank to reflect changes

**New functionality:**
- Insights saved to `insights.md` (or custom filename via `--insights-output`)
- Individual blog posts saved to `posts/<slugified-title>.md`
- Maintains original combined output in addition to new separate files
- Test suite optimized for fast execution during development

**Usage examples:**
```bash
# Basic usage with new file outputs
python spt_researcher.py --topic "remote work" --verbose

# Custom insights filename
python spt_researcher.py --topic "remote work" --insights-output "my_insights.md"

# Run tests quickly
PYTEST_CURRENT_TEST=1 pipenv run pytest -q test_spt_researcher.py
```

**Important notes:**
- Individual blog post files use article title as filename when available
- Falls back to insight text if no title found in markdown
- All directory creation is automatic (`posts/` directory created as needed)
- Test mode uses dummy data to avoid long LLM calls during testing

## Task: Add SPT Researcher Debug Enhancement
**Last performed:** September 8, 2025
**Files modified:**
- `spt_researcher.py` - Enhanced with comprehensive debugging functionality for insight generation

**Steps:**
1. Add `datetime` import for timestamping debug sessions
2. Modify `get_insights()` function to return tuple: `(insights, prompt_used, raw_output)`
3. Update function call in main workflow to handle new tuple return
4. Replace simple insights file writing with debug-enhanced version
5. Implement append-mode writing with timestamped sessions
6. Include prompt, raw output, and parsed results in debug file
7. Test functionality and update memory bank documentation

**New debug functionality:**
- **Timestamped Sessions**: Each run appends a new debug section with timestamp
- **Complete Prompt Visibility**: Shows exact prompt sent to GPT Researcher
- **Raw Model Output**: Preserves unprocessed response from the AI model
- **Parsed Results**: Shows final insight list after processing
- **History Preservation**: Maintains all previous debug sessions in append mode

**Debug output format:**
```markdown
# Insights Debug Session: 2025-09-08 23:04:41

**Topic:** [user topic]
**Max Insights:** [max_insights value]

## Prompt Used

```
[exact prompt sent to GPT Researcher]
```

## Raw Model Output

```
[unprocessed response from AI model]
```

## Parsed Insights

1. [first parsed insight]
2. [second parsed insight]
...
```

**Usage:**
- Same CLI usage as before: `pipenv run python spt_researcher.py --topic "your topic" --verbose`
- Debug information automatically written to insights output file (default: `insights.md`)
- Custom debug file: `--insights-output "custom_debug.md"`

**Benefits:**
- **Complete AI Agent Visibility**: See exactly what prompt was used and how the model responded
- **Debugging Support**: Easily identify why certain insights were generated or missed
- **Prompt Engineering**: Understand how different prompts affect output quality
- **Historical Analysis**: Track how insight generation changes over time
- **Troubleshooting**: Quickly identify parsing issues or unexpected model behavior

## Task: Fix SPT Researcher Two-Stage Insight Extraction
**Last performed:** September 9, 2025
**Files modified:**
- `spt_researcher.py` - Implemented two-stage insight extraction with local vLLM

**Problem:**
- GPT-Researcher returns research corpus data instead of clean bullet lists
- Line-by-line parsing produced garbage insights from complex web content
- Previous approach was brittle and unreliable

**Solution implemented:**
- **Stage 1**: GPT-Researcher gathers raw research data from web sources
- **Stage 2**: Local vLLM server extracts clean JSON array of actionable insights
- **Robust fallback**: Heuristic parsing if JSON extraction fails

**Steps taken:**
1. Added JSON import and OpenAI client setup for local vLLM integration
2. Implemented `extract_insights_from_raw()` function with JSON-first approach
3. Modified `get_insights()` to use two-stage approach (GPT-Researcher + extractor)
4. Enhanced debugging output to include JSON extraction stage
5. Added console debugging for real-time visibility during extraction
6. Updated function signatures to handle new tuple return format
7. Added comprehensive fallback strategies for robustness

**Technical details:**
- Uses local vLLM server (maintains privacy)
- JSON-first parsing eliminates brittle regex/line-based parsing
- Multiple fallback strategies ensure reliability
- Enhanced debugging shows exact JSON output from extractor
- Temperature 0.3 for consistent extraction results
- 20k character limit on raw input to avoid token limits

**Usage:**
```bash
pipenv run python spt_researcher.py --topic "your topic" --max-insights 5 --verbose
```

**Benefits:**
- Reliable insight extraction regardless of GPT-Researcher output format
- Local processing maintains complete privacy
- Robust error handling with multiple fallback strategies
- Enhanced debugging for troubleshooting extraction issues
- JSON-structured output enables future extensibility

**Important notes:**
- Function signature changed: `get_insights()` now returns 4-tuple instead of 3-tuple
- Enhanced debug output includes new "Extracted Insights (JSON)" section
- Console debugging shows real-time JSON extraction process
- Maintains backward compatibility for all other script functionality