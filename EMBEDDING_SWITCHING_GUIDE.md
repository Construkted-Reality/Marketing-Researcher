# Embedding Configuration Switching Guide

## Quick Switching Methods

### Method 1: Using the Switch Script (Recommended)
```bash
# View current configuration and options
pipenv run python switch_embedding.py

# Switch to local embeddings (no network dependency)
pipenv run python switch_embedding.py local

# Switch to Ollama server on LAN
pipenv run python switch_embedding.py ollama

# Switch to alternative Ollama model
pipenv run python switch_embedding.py nomic

# Check current active configuration
pipenv run python switch_embedding.py current
```

### Method 2: Manual .env File Editing

Edit your `.env` file and comment/uncomment the desired configuration:

#### Option A: Ollama Server (Fast, Distributed)
```env
# Active configuration
EMBEDDING=ollama:mxbai-embed-large
OLLAMA_BASE_URL=http://192.168.8.90:11434

# Inactive (commented out)
# EMBEDDING=huggingface:sentence-transformers/all-MiniLM-L6-v2
```

#### Option B: Local Processing (No Network Dependency)
```env
# Active configuration  
EMBEDDING=huggingface:sentence-transformers/all-MiniLM-L6-v2

# Inactive (commented out)
# EMBEDDING=ollama:mxbai-embed-large
# OLLAMA_BASE_URL=http://192.168.8.90:11434
```

## Available Configurations

| Configuration | Speed | Network | Memory | Use Case |
|---------------|-------|---------|--------|----------|
| **Ollama Server** | Fast | Required | Low local | Distributed processing |
| **Local HuggingFace** | Slower | None | High local | Offline/single machine |
| **Nomic Model** | Fast | Required | Low local | Alternative Ollama model |

## Adding New Server IPs

To add a different Ollama server, update your `.env`:

```env
# Different server example
EMBEDDING=ollama:mxbai-embed-large
OLLAMA_BASE_URL=http://192.168.8.91:11434
```

## Testing Your Configuration

After switching, verify it works:

```bash
# Test Ollama server connectivity
pipenv run python test_ollama_embedding.py

# Test local embeddings with research
pipenv run python test.py
```

## Performance Comparison

- **Ollama Server**: ~30 seconds for embedding processing
- **Local HuggingFace**: ~60 seconds for embedding processing  
- **Network Latency**: Minimal impact on LAN (< 1 second difference)

## Troubleshooting

1. **Ollama not responding**: Check if server is running with `ollama serve`
2. **Model not found**: Ensure model is pulled with `ollama pull mxbai-embed-large`
3. **Local embedding slow**: First run downloads model (~100MB), subsequent runs are faster
4. **Network issues**: Switch to local mode for offline research

## Best Practices

- Use **Ollama server** for production/frequent research
- Use **local embeddings** for offline work or testing
- Keep both options configured for easy switching
- Monitor server resources when using distributed setup