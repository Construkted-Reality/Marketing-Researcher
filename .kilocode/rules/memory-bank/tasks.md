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

## Task: Implement SPT Researcher JSON-First Architecture
**Last performed:** September 8, 2025
**Files modified:**
<<<<<<< HEAD
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
=======
- `spt_researcher.py` - Complete rewrite with JSON-first schema and canonical dumps
- `test_spt_researcher.py` - Comprehensive test suite with 5 new test functions
- `SPT_RESEARCHER_GUIDE.md` - Complete documentation rewrite with troubleshooting workflows

**Problem solved:**
- Original step-1 output contained web scraping noise: "Source:", "Try again", "Please enable Javascript"
- No canonical way to inspect exact payload fed to step-2
- Difficult to troubleshoot and iterate on step-2 without re-running step-1

**Implementation:**
1. **JSON-First Parser**: Added `parse_pain_points()` helper with JSON-first parsing and noise-filtered fallback
2. **Strict JSON Schema**: Updated step-1 prompt to enforce exact JSON structure with validation rules
3. **Canonical Dumps**: Changed `--pain-points-output` default from `.md` to `.json` with exact step-2 payload
4. **Input Override**: Added `--pain-points-input` flag to load existing JSON and skip step-1 generation
5. **Human-Readable Option**: Added `--pain-points-markdown` for optional review files (clearly non-canonical)
6. **Enhanced Testing**: 5 comprehensive test functions covering JSON parsing, input override, and dummy modes
7. **Noise Filtering**: Robust regex patterns to eliminate 8+ common web scraping artifacts
8. **Verbose Logging**: Enhanced progress tracking with parser types and file paths
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba

**New CLI flags:**
- `--pain-points-output <path>` - Canonical JSON dump (default: pain_points.json)
- `--pain-points-input <path>` - Load existing JSON and skip step-1
- `--pain-points-markdown <path>` - Optional human-readable list (non-canonical)

**Workflow patterns:**
```bash
# Generate and troubleshoot
python spt_researcher.py --topic "photogrammetry" --verbose
cat pain_points.json | jq .

<<<<<<< HEAD
# Custom insights filename
python spt_researcher.py --topic "remote work" --insights-output "my_insights.md"
=======
# Iterate on step-2 only
python spt_researcher.py --pain-points-input pain_points.json --topic "ignored"
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba

# Generate with review file
python spt_researcher.py --topic "AI tools" --pain-points-markdown review.md
```

**Testing coverage:**
- `test_json_dump_creation()` - Validates canonical JSON structure and content
- `test_pain_points_input_override()` - Tests input flag skips step-1 correctly
- `test_human_readable_markdown()` - Validates optional markdown output
- `test_json_parsing_functions()` - Unit tests for parser with different input formats
- Enhanced existing tests for backward compatibility

**Quality improvements:**
- JSON parser extracts clean `pain_points[].idea` fields
- Fallback parser filters noise with regex patterns for Source:, Title:, Try again, etc.
- Deduplication and max-points enforcement
- Parser type logging (json/fallback/dummy) for debugging
- Reproducible workflows with exact step-2 input preservation

**Important notes:**
<<<<<<< HEAD
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

## Task: Add SPT Researcher Insights-Only Mode
**Last performed:** September 9, 2025
**Files modified:**
- `spt_researcher.py` - Added `--insights-only` command line switch

**Steps:**
1. Add new CLI argument `--insights-only` to argument parser with description
2. Update usage documentation in file header comments to include new flag
3. Implement early exit logic after insights file writing but before blog post generation
4. Add conditional check for `args.insights_only` flag after insights are written
5. Display success message showing number of insights generated
6. Exit cleanly with `sys.exit(0)` before blog post generation begins

**New functionality:**
- Insights-only mode stops execution after generating and writing insights
- Preserves all existing functionality when flag is not used
- Provides faster workflow for users who only need research insights
- Clean exit with informative success message

**Usage examples:**
```bash
# Generate only insights for a topic
python spt_researcher.py --topic "remote work productivity" --insights-only

# Generate insights with custom output file and verbose logging
python spt_researcher.py --topic "AI automation" --insights-only --insights-output "ai_insights.md" --verbose

# Generate insights with custom max count
python spt_researcher.py --topic "digital marketing trends" --insights-only --max-insights 10
```

**Benefits:**
- **Faster Workflow**: Skip time-consuming blog post generation when only insights are needed
- **Iterative Research**: Quickly generate insights to evaluate topic viability before committing to full blog post creation
- **Resource Efficiency**: Reduces processing time and server usage for insight-only research
- **Flexible Usage**: Maintains backward compatibility while adding new capability

**Important notes:**
- Exit occurs after all insights debug information is written to file
- Success message includes count of insights generated
- All existing command line arguments remain functional with insights-only mode
- Maintains complete debug information output for insights extraction process
## Task: Migrate GPT Researcher LLM Env Vars to New Format
Last performed: 2025-09-09
Files to modify:
- `.env`

Purpose:
- Remove deprecated env vars that trigger FutureWarning and configure GPT Researcher with the new provider-specific variables while preserving local extractor settings used by the insights extractor in [extract_insights_from_raw()](spt_researcher.py:79).

Deprecated variables to remove/comment:
- LLM_PROVIDER
- FAST_LLM_MODEL
- SMART_LLM_MODEL

New variables to use:
- FAST_LLM
- SMART_LLM
- STRATEGIC_LLM (optional)
- Provider-specific keys for vLLM OpenAI:
  - VLLM_OPENAI_API_BASE
  - VLLM_OPENAI_API_KEY

Keep these for local extractor used by the script:
- OPENAI_API_KEY
- OPENAI_API_BASE
- OPENAI_MODEL_NAME

Steps:
1) Open `.env` and comment/remove deprecated keys:
   - Example: change to `# LLM_PROVIDER=openai`
   - Ensure there is no FAST_LLM_MODEL or SMART_LLM_MODEL anywhere (shell or file).
2) Add or update new LLM config for GPT Researcher (vLLM OpenAI provider):
   - FAST_LLM=vllm_openai:gpt-oss-120b (see [.env](.env:50))
   - SMART_LLM=vllm_openai:gpt-oss-120b (see [.env](.env:51))
   - STRATEGIC_LLM=vllm_openai:gpt-oss-120b (see [.env](.env:52))
   - VLLM_OPENAI_API_BASE=http://192.168.8.90:42069/v1 (see [.env](.env:9))
   - VLLM_OPENAI_API_KEY=outsider (see [.env](.env:5))
3) Preserve local extractor settings for the OpenAI client used by the script:
   - OPENAI_API_KEY=outsider (see [.env](.env:5) or [.env](.env:4) if present)
   - OPENAI_API_BASE=http://192.168.8.90:42069/v1 (see [.env](.env:8))
   - OPENAI_MODEL_NAME=gpt-oss-120b (see [.env](.env:12))
4) Configure search engines with RETRIEVER (not SEARCH_PROVIDER):
   - Example: `RETRIEVER=searx,mcp` (privacy-first hybrid) or `RETRIEVER=tavily,mcp` (see [.env](.env:27))
   - Provide matching API envs (e.g., `SEARX_URL` or `TAVILY_API_KEY`).
5) Set scraper method to match environment:
   - Example: `SCRAPER=bs` or `SCRAPER=tavily_extract` (see [.env](.env:44)).
6) Reload environment (new shell or re-source env) to clear deprecated variables from the process environment.
7) Validate:
   - vLLM connectivity: `pipenv run python test_vllm_direct.py` ([test_vllm_direct.py](test_vllm_direct.py:1))
   - Retriever connectivity (if SearXNG): `pipenv run python test_searxng_direct.py` ([test_searxng_direct.py](test_searxng_direct.py:1))
   - Run insights-only to verify pipeline: `pipenv run python spt_researcher.py --topic "test" --insights-only --verbose` ([main_cli()](spt_researcher.py:256))

Example .env (post-migration):
```env
# vLLM OpenAI provider for GPT Researcher
FAST_LLM=vllm_openai:gpt-oss-120b
SMART_LLM=vllm_openai:gpt-oss-120b
STRATEGIC_LLM=vllm_openai:gpt-oss-120b
VLLM_OPENAI_API_BASE=http://192.168.8.90:42069/v1
VLLM_OPENAI_API_KEY=outsider

# Local extractor used by spt_researcher.py
OPENAI_API_KEY=outsider
OPENAI_API_BASE=http://192.168.8.90:42069/v1
OPENAI_MODEL_NAME=gpt-oss-120b

# Search engines and scraper
RETRIEVER=searx,mcp
SEARX_URL=https://search.roci.me/
# TAVILY_API_KEY=your_tavily_key_if_used
SCRAPER=bs
```

Failure modes and resolutions:
- Warning persists: A deprecated variable is still set in the shell. Open a new terminal and verify with `env | grep -E "LLM_PROVIDER|FAST_LLM_MODEL|SMART_LLM_MODEL"`.
- GPT Researcher returns None for LLM calls after migration: Add `VLLM_OPENAI_API_BASE` and `VLLM_OPENAI_API_KEY` to `.env` (provider-specific).
- Script errors with `OPENAI_API_BASE not set`: Restore `OPENAI_*` variables; they are required by [load_environment()](spt_researcher.py:33).
- Misleading variable: `SEARCH_PROVIDER` is unused by current GPT Researcher in this repo; use `RETRIEVER` instead.

Notes:
- This migration satisfies the FutureWarning emitted by GPT Researcher and preserves end-to-end functionality by distinguishing between GPT Researcher provider config (using `VLLM_OPENAI_*`) and the script’s local extractor config (`OPENAI_*`).
- Confirmed via GPT Researcher docs (Context7) for vLLM OpenAI provider and `FAST_LLM`/`SMART_LLM` usage.
=======
- Maintains full backward compatibility with existing workflows
- Default output changed from pain_points.md to pain_points.json
- Human-readable markdown is optional and clearly marked as non-canonical
- Test mode uses dummy data to avoid LLM calls during development
- Complete documentation rewrite with troubleshooting patterns

## Task: Add SPT Researcher Blog-Generation-Only Mode
**Last performed:** September 17, 2025
**Files modified:**
- `spt_researcher.py` - Enhanced with blog-generation-only mode using `--blog-generation-only` and `--insights-input` flags
- `sample_insights.json` - Created sample insights file for testing blog-generation-only functionality
- `test_spt_researcher.py` - Expanded with comprehensive test coverage for new blog-generation-only mode
- `SPT_RESEARCHER_GUIDE.md` - Updated with documentation for blog-generation-only mode usage

**Steps:**
1. Add new CLI arguments `--blog-generation-only` and `--insights-input` to argument parser
2. Create `load_insights_from_file(file_path: Path) -> List[InsightObject]` function for loading structured insights from JSON files
3. Implement JSON validation with comprehensive error handling for malformed data
4. Add conditional check for `args.blog_generation_only` flag to skip insight generation
5. Use provided insight data directly for blog post generation phase
6. Enhanced data validation with required fields (insight, context, source_reference, key_data) and optional defaults
7. Preserved backward compatibility: all existing functionality remains unchanged
8. Created sample insights file for testing and demonstration purposes

**New functionality:**
- **Flexible Input**: Load insights from JSON files with structured data format
- **Error Handling**: Comprehensive validation of required and optional fields
- **Data Format**: JSON array with required fields (insight, context, source_reference, key_data) and optional defaults (priority_level, content_type, target_audience)
- **CLI Interface**: `--blog-generation-only --insights-input insights.json` for targeted blog generation
- **Sample Data**: `sample_insights.json` provided for testing and demonstration
- **Backward Compatibility**: All existing functionality preserved and unchanged

**Performance metrics:**
- Blog generation only: Fast (skips expensive insight generation phase)
- Input validation: Minimal overhead with comprehensive error checking
- Memory usage: Reduced (no GPT-Researcher calls for insight generation)
- System reliability: Maintained with robust error handling

**Usage examples:**
```bash
# Generate blog posts from existing insights
python spt_researcher.py --blog-generation-only --insights-input insights.json --topic "dummy"

# Generate with custom output and verbose logging
python spt_researcher.py --blog-generation-only --insights-input my_insights.json --output blog_posts.md --verbose

# Generate with custom insights file
python spt_researcher.py --blog-generation-only --insights-input sample_insights.json --topic "test"
```

**Data format specification:**
```json
[
  {
    "insight": "Companies lose 30% productivity due to inefficient workflows",
    "context": "Recent industry studies show workflow inefficiencies",
    "source_reference": "https://forrester.com/study-2024",
    "key_data": "30% productivity loss, $2.5B annual cost",
    "priority_level": "high",
    "content_type": "business",
    "target_audience": "managers"
  }
]
```

**Important notes:**
- Required fields: insight, context, source_reference, key_data (all strings)
- Optional fields: priority_level ("low", "medium", "high"), content_type ("general"), target_audience ("general")
- File validation occurs before blog post generation begins
- Error messages provide specific guidance for missing or invalid fields
- Maintains complete feature parity with existing workflows
>>>>>>> 2a84ef1cc31bfde94e0bd90ba772ee6d0d3f97ba
