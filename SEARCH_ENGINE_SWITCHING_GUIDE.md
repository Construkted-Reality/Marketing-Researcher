# Search Engine Switching Guide

This guide explains how to easily switch between Tavily and SearXNG search engines in your GPT Researcher setup.

## Overview

Your system supports multiple search engine configurations:

1. **SearXNG + MCP Hybrid** (Default) - Privacy-first self-hosted search with AI reasoning
2. **Tavily + MCP Hybrid** - Commercial search API with AI reasoning  
3. **SearXNG Only** - Pure self-hosted search, no AI reasoning
4. **Tavily Only** - Pure commercial search API, no AI reasoning

## Quick Start

### 1. Check Current Configuration
```bash
python switch_search.py current
```

### 2. Switch to SearXNG (Default)
```bash
python switch_search.py searx,mcp
```

### 3. Switch to Tavily (Backup)
```bash
python switch_search.py tavily,mcp
```

### 4. Test SearXNG Connectivity
```bash
python test_searxng_direct.py
```

### 5. Run Research
```bash
pipenv run python test.py
```

## Configuration Details

### SearXNG Configuration

**Environment Variables:**
- `RETRIEVER=searx` or `RETRIEVER=searx,mcp`
- `SEARX_URL=https://search.example.com`
- `SCRAPER=bs` (recommended for SearXNG)

**Benefits:**
- ✅ Complete privacy - no external API calls for search
- ✅ No API rate limits or costs
- ✅ Full control over search engines and filters
- ✅ Works with your existing distributed LAN setup

**Requirements:**
- Self-hosted SearXNG instance accessible via HTTPS
- JSON API enabled (`search?format=json`)
- Network connectivity to your SearXNG server

### Tavily Configuration

**Environment Variables:**
- `RETRIEVER=tavily` or `RETRIEVER=tavily,mcp`
- `TAVILY_API_KEY=your_api_key`
- `SCRAPER=tavily_extract` (recommended for Tavily)

**Benefits:**
- ✅ No setup required - works immediately
- ✅ High-quality search results and content extraction
- ✅ Built-in content scraping and filtering
- ✅ Optimized for research workflows

**Requirements:**
- Tavily API key with sufficient credits
- Internet connectivity for API calls

## Available Commands

### Search Engine Switcher
```bash
# Show all options and current config
python switch_search.py

# Show current configuration only
python switch_search.py current

# Switch to specific configuration
python switch_search.py searx,mcp     # SearXNG + AI reasoning
python switch_search.py tavily,mcp    # Tavily + AI reasoning  
python switch_search.py searx         # SearXNG only
python switch_search.py tavily        # Tavily only
```

### Testing Scripts
```bash
# Test SearXNG connectivity and API
python test_searxng_direct.py

# Test Tavily connectivity and API
python test_tavily_direct.py

# Test end-to-end research workflow
pipenv run python test.py
```

## Hybrid vs Pure Modes

### Hybrid Modes (`retriever,mcp`)
- **Search Phase**: Use web search engine (SearXNG or Tavily) to find sources
- **Analysis Phase**: Use MCP + local LLM to analyze and synthesize
- **Best For**: Comprehensive research combining web data with AI reasoning

### Pure Modes (`retriever` only)
- **Search Phase**: Use web search engine only
- **Analysis Phase**: Use local LLM only (no MCP)
- **Best For**: Simple web search with basic LLM processing

## Performance Comparison

| Configuration | Privacy | Cost | Speed | Quality | Setup |
|---------------|---------|------|-------|---------|-------|
| SearXNG + MCP | 🟢 High | 🟢 Free | 🟡 Medium | 🟢 High | 🟡 Medium |
| Tavily + MCP  | 🟡 Medium | 🔴 Paid | 🟢 Fast | 🟢 High | 🟢 Easy |
| SearXNG Only  | 🟢 High | 🟢 Free | 🟢 Fast | 🟡 Medium | 🟡 Medium |
| Tavily Only   | 🟡 Medium | 🔴 Paid | 🟢 Fast | 🟡 Medium | 🟢 Easy |

## Troubleshooting

### SearXNG Issues

**Problem: "SEARX_URL not found"**
```bash
# Check if SEARX_URL is set
echo $SEARX_URL

# Set manually if needed
export SEARX_URL=https://search.example.com
```

**Problem: "Failed to connect to SearXNG"**
- Verify SearXNG URL is accessible
- Check if HTTPS is properly configured
- Ensure JSON API is enabled
- Test manually: `curl "https://search.example.com/search?q=test&format=json"`

**Problem: "Search API returned status code 429"**
- SearXNG instance is rate-limited
- Try switching to `SCRAPER=browser` for slower but more reliable scraping
- Consider using hybrid mode with MCP to reduce search frequency

### Tavily Issues

**Problem: "401 Unauthorized"**
```bash
# Test Tavily API key
python test_tavily_direct.py

# Check API key in environment
echo $TAVILY_API_KEY
```

**Problem: "Rate limit exceeded"**
- Tavily API quota exhausted
- Switch to SearXNG: `python switch_search.py searx,mcp`
- Or upgrade Tavily plan

### General Issues

**Problem: "No search results found"**
- Test search engine directly with test scripts
- Try different scraper methods: `SCRAPER=browser` or `SCRAPER=bs`
- Check network connectivity and firewall settings

**Problem: "Report quality is poor"**
- Switch to hybrid mode: `RETRIEVER=searx,mcp` or `RETRIEVER=tavily,mcp`
- Verify LLM and embedding servers are running
- Check that MCP configuration is properly set

## Integration with Existing System

### Current Architecture Compatibility
Your existing distributed LAN setup works perfectly with both search engines:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client App    │    │   vLLM Server   │    │  Ollama Server  │
│  (test.py)      │───▶│ 192.168.8.90    │    │ 192.168.8.90    │
│                 │    │ :42069          │    │ :11434          │
│ GPT Researcher  │    │                 │    │                 │
│ Framework       │    │ gpt-oss-120b    │    │ mxbai-embed-    │
│                 │    │ Model           │    │ large Model     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                                             
         ▼                       
┌─────────────────┐              ┌─────────────────┐
│  Search Engine  │              │    SearXNG      │
│   (Flexible)    │              │   (Privacy)     │
│                 │              │                 │
│ Tavily API      │              │ Self-hosted     │
│ (External)      │              │ (Local/LAN)     │
└─────────────────┘              └─────────────────┘
```

### Performance Optimization
- **SearXNG**: Use `SCRAPER=bs` for fast static scraping
- **Tavily**: Use `SCRAPER=tavily_extract` for optimized content extraction
- **Hybrid modes**: Balance search quality with AI reasoning

## Advanced Configuration

### Custom SearXNG Settings
You can fine-tune SearXNG behavior by modifying search parameters in your instance:

```yaml
# searxng/settings.yml
search:
  safe_search: 0
  autocomplete: duckduckgo
  default_lang: en
  formats:
    - html
    - json
```

### Multiple SearXNG Instances
For redundancy, you can set up multiple SearXNG instances and switch between them:

```bash
# Switch SearXNG instance
export SEARX_URL=https://searx-backup.example.com
python test_searxng_direct.py
```

### Custom Scraper Configuration
```bash
# Fast static scraping (default)
export SCRAPER=bs

# Dynamic scraping for JavaScript-heavy sites
export SCRAPER=browser

# High-scale production scraping
export SCRAPER=firecrawl
```

## Next Steps

1. **Test Your SearXNG Instance**: Run `python test_searxng_direct.py`
2. **Switch to SearXNG**: Run `python switch_search.py searx,mcp`
3. **Generate a Research Report**: Run `pipenv run python test.py`
4. **Compare Quality**: Switch between engines and compare output quality
5. **Monitor Performance**: Track research speed and result relevance

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Test individual components with provided test scripts
3. Verify network connectivity and API keys
4. Review GPT Researcher logs for detailed error information