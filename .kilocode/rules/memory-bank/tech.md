# Technology Stack: Content Marketing Research & Automation System

## Core Technologies

### Programming Language
- **Python 3.12**: Primary development language
- **Async/Await**: Required for GPT Researcher framework compatibility
- **Type Hints**: Used throughout for better code maintainability
- **JSON Processing**: Extensive JSON handling for canonical workflows

### AI/ML Frameworks
- **GPT Researcher**: Orchestrates research workflow and insight extraction
- **vLLM**: High-performance LLM serving for chat completions and content generation
- **Ollama**: Local LLM serving with embedding support
- **Sentence Transformers**: Local embedding models (HuggingFace)
- **LangChain**: Integration layer for different AI providers
- **LLM Guidance System**: Sophisticated prompt engineering with voice selection

### Content Generation Technologies
- **Markdown Processing**: Dynamic content generation and file management
- **Template Engineering**: Sophisticated prompt templates with variable substitution
- **Voice Selection System**: Context-aware writing style adaptation (New Yorker, Atlantic, Wired)
- **Quality Scoring**: Source analysis and content quality assessment
- **Image Prompt Generation**: Structured prompts for visual content creation

### Networking & APIs
- **OpenAI Client Library**: Unified API interface for different LLM providers
- **SearXNG API**: Self-hosted privacy-first search engine with JSON API
- **Tavily API**: Commercial web search and content scraping (backup)
- **Requests**: HTTP client for direct API testing
- **RESTful APIs**: Standard communication protocol

## Development Setup

### Environment Management
```bash
# Virtual environment and dependency management
pipenv install
pipenv shell
pipenv run python script.py
```

### Configuration Management
```bash
# Environment variables in .env file
load_dotenv()  # Python pattern used throughout

# Dynamic configuration switching
python switch_embedding.py [option]
python switch_search.py [option]
```

### Testing Strategy
```bash
# Component-specific testing
pipenv run python test_vllm_direct.py      # vLLM server
pipenv run python test_ollama_embedding.py # Ollama server
pipenv run python test_tavily_direct.py    # Tavily API
pipenv run python test_searxng_direct.py   # SearXNG connectivity
pipenv run python test.py                  # End-to-end research
```

## Technical Constraints

### Performance Requirements
- **Research Generation**: Target < 3 minutes end-to-end
- **Network Latency**: LAN-based servers minimize latency < 100ms
- **Memory Usage**: Local embeddings require ~2GB RAM
- **Concurrent Processing**: Async operations for parallel web scraping

### Infrastructure Dependencies
- **LAN Connectivity**: Required for distributed server architecture
- **Server Resources**: vLLM server needs GPU acceleration
- **Network Bandwidth**: Web scraping requires stable internet connection
- **Storage**: Model files require 5-10GB disk space per server

### API Compatibility
- **OpenAI Format**: All LLM servers must expose OpenAI-compatible APIs
- **Ollama Native**: Embedding server uses Ollama's native API format
- **Environment Variables**: Configuration through dotenv standard

## Dependencies

### Core Dependencies (Pipfile)
```toml
[packages]
langchain-mcp-adapters = "*"      # MCP integration (future use)
gpt-researcher = "*"              # Main research framework
python-dotenv = "*"               # Environment variable management
openai = "*"                      # Unified LLM client library
tavily-python = "*"               # Web search integration
sentence-transformers = "*"       # Local embedding models
langchain-huggingface = "*"       # HuggingFace model integration

[dev-packages]
pytest = "*"                      # Testing framework for development
```

### System Dependencies
- **Python 3.12+**: Required for modern async features
- **pipenv**: Package and virtual environment management
- **vLLM Server**: External service (192.168.8.90:42069)
- **Ollama Server**: External service (192.168.8.90:11434)

### Content Generation Dependencies
- **LLM Guidance Templates**: Markdown-based prompt engineering system
- **Company Context Files**: Domain-specific constraints and product information
- **Voice Style Definitions**: Writing style templates for different publication types
- **JSON Schema Validation**: Structured data handling for insights and content

## Tool Usage Patterns

### Configuration Management
```python
# Standard pattern for environment loading
from dotenv import load_dotenv
import os

load_dotenv()
api_base = os.getenv("OPENAI_API_BASE")
os.environ["OPENAI_API_BASE"] = api_base
```

### Async Script Pattern
```python
# Required pattern for GPT Researcher compatibility
import asyncio

async def main():
    # Async operations here
    researcher = GPTResearcher(query=query)
    result = await researcher.conduct_research()

if __name__ == "__main__":
    asyncio.run(main())
```

### Error Handling Pattern
```python
# Consistent error handling across scripts
try:
    # Operation
    result = await operation()
    print(f"✅ Success: {result}")
except Exception as e:
    print(f"❌ Error: {e}")
    return False
```

### Testing Pattern
```python
# Standard testing function structure
def test_component():
    """Test component connectivity"""
    # 1. Load configuration
    # 2. Test connectivity
    # 3. Report results with emoji indicators
    # 4. Return boolean success/failure
```

## Development Workflows

### Adding New Embedding Servers
1. Update `switch_embedding.py` with new configuration
2. Add server details to `.env` file
3. Create dedicated test script
4. Update `EMBEDDING_SWITCHING_GUIDE.md`

### Adding New Search Engines
1. Update `switch_search.py` with new configuration
2. Add server/API details to `.env` file
3. Create dedicated test script
4. Update `SEARCH_ENGINE_SWITCHING_GUIDE.md`

### Content Generation Workflow Development
1. Update LLM guidance templates in `llm_guidance/` directory
2. Test voice selection and content quality with sample insights
3. Validate company context constraints prevent hallucination
4. Update content marketing guidance for new domains or products

### Debugging Connection Issues
1. Run component-specific test scripts
2. Check server status and connectivity
3. Validate API key configurations
4. Review network connectivity between servers

### Performance Optimization
1. Monitor server resource usage
2. Adjust batch sizes for embedding processing
3. Optimize network round-trips
4. Cache frequently used embeddings
5. Optimize content generation templates for faster processing

## Security Considerations

### API Key Management
- **Local Storage**: API keys stored in `.env` file
- **Access Control**: File permissions restrict access
- **External APIs**: Tavily API key for commercial search (optional)
- **Network Security**: All AI processing within LAN boundary

### Data Privacy
- **Local Processing**: LLM and embedding operations stay on LAN
- **Privacy-First Search**: SearXNG provides complete search privacy
- **No Cloud AI**: Eliminates data leakage to commercial AI services
- **Flexible Privacy**: Easy switching between private (SearXNG) and commercial (Tavily) search
- **Audit Trail**: All operations logged for debugging

## Scalability Architecture

### Horizontal Scaling
- **Multiple Embedding Servers**: Easy addition of new Ollama instances
- **Load Balancing**: Round-robin between multiple servers
- **Fault Tolerance**: Automatic fallback to local embeddings

### Resource Management
- **Server Separation**: Different models on different hardware
- **Memory Optimization**: Distributed processing reduces per-node requirements
- **GPU Utilization**: vLLM server leverages GPU acceleration