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