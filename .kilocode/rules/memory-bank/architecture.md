# System Architecture: Content Marketing Research System

## High-Level Architecture

### Distributed LAN Infrastructure
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

## Source Code Structure

### Core Files
- **`test.py`**: Main research script with async wrapper for GPT Researcher
- **`test_researcher.py`**: Alternative research script with different query
- **`spt_researcher.py`** – Script for generating user pain‑points and automated blog‑post drafts with individual file output
- **`.env`**: Configuration file containing all server endpoints and API keys

### Testing Suite
- **`test_vllm_direct.py`**: Direct vLLM server connectivity validation
- **`test_ollama_embedding.py`**: Ollama embedding server testing
- **`test_embedding_server.py`**: Generic embedding server testing (OpenAI-compatible)
- **`test_tavily_direct.py`**: Tavily API key validation
- **`test_searxng_direct.py`**: SearXNG connectivity and search API testing

### Configuration Management
- **`switch_embedding.py`**: Automated utility for switching between embedding configurations
- **`switch_search.py`**: Automated utility for switching between search engines
- **`EMBEDDING_SWITCHING_GUIDE.md`**: User documentation for embedding options
- **`SEARCH_ENGINE_SWITCHING_GUIDE.md`**: User documentation for search engine options
- **`Pipfile`**: Python dependency management

## Key Technical Decisions

### 1. Distributed Processing Architecture
- **Decision**: Separate vLLM and Ollama servers on different ports
- **Rationale**: Optimal resource allocation, fault isolation, scalability
- **Implementation**: Different server endpoints in `.env` configuration

### 2. Async/Await Pattern with Script Compatibility
- **Decision**: Wrap top-level awaits in `async def main()` with `asyncio.run()`
- **Rationale**: GPT Researcher requires async but scripts need sync entry points
- **Implementation**: All main scripts use this pattern for compatibility

### 3. Privacy-First Local Processing
- **Decision**: Keep all AI processing within local network
- **Rationale**: Data privacy, cost control, performance optimization
- **Implementation**: Local vLLM and Ollama servers, only web search external

### 4. Flexible Configuration Switching
- **Decision**: Multiple embedding and search engine configuration options with easy switching
- **Rationale**: Support both local and distributed deployments, privacy vs. commercial trade-offs
- **Implementation**: `.env` sections + automated switching utilities (`switch_embedding.py`, `switch_search.py`)

### 5. Privacy-First Search Integration
- **Decision**: Integrate self-hosted SearXNG alongside commercial Tavily API
- **Rationale**: Complete privacy for sensitive research, no external search API dependencies
- **Implementation**: GPT Researcher built-in SearX/SearXNG retriever with easy switching

## Design Patterns

### 1. Environment-Driven Configuration
```python
# Pattern used throughout codebase
load_dotenv()
api_base = os.getenv("OPENAI_API_BASE")
os.environ["OPENAI_API_BASE"] = api_base
```

### 2. Async Wrapper Pattern
```python
# Standard pattern for all main scripts
async def main():
    # async operations here
    researcher = GPTResearcher(query=query)
    result = await researcher.conduct_research()

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Modular Testing Strategy
- Each component has dedicated test script
- All follow similar structure: load config → test connectivity → report results
- Enables independent validation of system components

## Component Relationships

### Research Workflow
1. **User Input** → `test.py` or `test_researcher.py`
2. **GPT Researcher** orchestrates the entire workflow
3. **Web Search** → SearXNG or Tavily API finds relevant sources
4. **Content Scraping** → SearXNG or Tavily extracts article content
5. **Embedding Processing** → Ollama server ranks and filters content
6. **Report Generation** → vLLM server synthesizes final report
7. **Output** → Professional research report with citations

### Configuration Flow
1. **Environment Variables** → `.env` file defines all endpoints
2. **Runtime Loading** → `load_dotenv()` in each script
3. **Dynamic Switching** → `switch_embedding.py` modifies `.env`
4. **Immediate Effect** → No restart required for configuration changes

## Critical Implementation Paths

### Primary Research Path
```
test.py → load_dotenv() → GPTResearcher() →
├─ SearXNG.search() OR Tavily.search() → web sources
├─ Ollama.embed() → content ranking
├─ vLLM.generate() → report synthesis
└─ output: professional report
```

### Configuration Management Path
```
switch_embedding.py → read .env →
├─ comment/uncomment embedding lines
├─ write updated .env
└─ immediate effect on next run

switch_search.py → read .env →
├─ comment/uncomment search engine lines
├─ write updated .env
└─ immediate effect on next run
```

### Testing Validation Path
```
test_*.py scripts →
├─ test_vllm_direct.py → vLLM connectivity
├─ test_ollama_embedding.py → Ollama embedding
├─ test_tavily_direct.py → Tavily API
├─ test_searxng_direct.py → SearXNG connectivity
└─ comprehensive system validation
```

## Server Specifications

### vLLM Server (192.168.8.90:42069)
- **Model**: gpt-oss-120b
- **Purpose**: Chat completions for report generation
- **API**: OpenAI-compatible
- **Performance**: ~60 seconds per report generation

### Ollama Server (192.168.8.90:11434)
- **Model**: mxbai-embed-large (768-dimensional embeddings)
- **Purpose**: Content embedding for ranking and filtering
- **API**: Ollama native API
- **Performance**: ~30 seconds for web content processing

### Search Engine Options

#### SearXNG Instance (https://search.roci.me/)
- **Type**: Self-hosted privacy-first search engine
- **API**: JSON format search results (`/search?format=json`)
- **Privacy**: Complete search privacy, no external API calls
- **Performance**: 36 results found, ~$0.02 per research report
- **Features**: Aggregates multiple search engines (Google, Bing, DuckDuckGo)

#### Tavily API (Backup/Commercial)
- **Type**: Commercial search API with content extraction
- **API**: Tavily Python SDK with advanced scraping
- **Privacy**: External API calls required
- **Performance**: High-quality results with optimized scraping
- **Features**: Built-in content extraction and filtering

### External Dependencies
- **SearXNG Instance**: Self-hosted search engine (primary)
- **Tavily API**: Commercial web search and content scraping (backup)
- **Python Environment**: Pipenv with specific dependencies
- **Network**: LAN connectivity between servers required