#!/usr/bin/env python3
"""
Utility script to easily switch between different embedding configurations
Usage: python switch_embedding.py [option]
"""

import sys
import os
from pathlib import Path

# Embedding configuration options
EMBEDDING_OPTIONS = {
    "ollama": {
        "name": "Ollama Server (mxbai-embed-large)",
        "description": "Fast, distributed processing on LAN server",
        "config": [
            "EMBEDDING=ollama:mxbai-embed-large",
            "OLLAMA_BASE_URL=http://192.168.8.90:11434"
        ],
        "comment_out": ["EMBEDDING=huggingface:sentence-transformers/all-MiniLM-L6-v2"]
    },
    "local": {
        "name": "Local HuggingFace Sentence Transformers",
        "description": "Runs locally, no network dependency",
        "config": [
            "EMBEDDING=huggingface:sentence-transformers/all-MiniLM-L6-v2"
        ],
        "comment_out": [
            "EMBEDDING=ollama:mxbai-embed-large",
            "OLLAMA_BASE_URL=http://192.168.8.90:11434"
        ]
    },
    "nomic": {
        "name": "Ollama Server (nomic-embed-text)",
        "description": "Alternative Ollama model on LAN server",
        "config": [
            "EMBEDDING=ollama:nomic-embed-text",
            "OLLAMA_BASE_URL=http://192.168.8.90:11434"
        ],
        "comment_out": ["EMBEDDING=huggingface:sentence-transformers/all-MiniLM-L6-v2"]
    }
}

def read_env_file():
    """Read the current .env file"""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found")
        return None
    return env_path.read_text()

def write_env_file(content):
    """Write the updated .env file"""
    env_path = Path(".env")
    env_path.write_text(content)

def update_embedding_config(option_key):
    """Update the .env file with the specified embedding configuration"""
    if option_key not in EMBEDDING_OPTIONS:
        print(f"❌ Invalid option: {option_key}")
        print(f"Valid options: {', '.join(EMBEDDING_OPTIONS.keys())}")
        return False
    
    option = EMBEDDING_OPTIONS[option_key]
    content = read_env_file()
    if content is None:
        return False
    
    lines = content.split('\n')
    new_lines = []
    
    # Process each line
    for line in lines:
        line_stripped = line.strip()
        
        # Comment out lines that should be inactive
        if any(line_stripped.startswith(comment_line) for comment_line in option["comment_out"]):
            if not line.startswith('#'):
                new_lines.append(f"# {line}")
            else:
                new_lines.append(line)
        
        # Uncomment lines that should be active
        elif any(line_stripped.startswith(f"# {config_line}") for config_line in option["config"]):
            new_lines.append(line.lstrip('# '))
        
        # Keep other lines as-is
        else:
            new_lines.append(line)
    
    # Write the updated configuration
    write_env_file('\n'.join(new_lines))
    
    print(f"✅ Switched to: {option['name']}")
    print(f"📝 {option['description']}")
    
    # Show active configuration
    print("\n🔧 Active embedding configuration:")
    for config_line in option["config"]:
        print(f"   {config_line}")
    
    return True

def show_options():
    """Display available embedding options"""
    print("🎯 Available embedding configurations:")
    print()
    
    for key, option in EMBEDDING_OPTIONS.items():
        print(f"📌 {key}: {option['name']}")
        print(f"   {option['description']}")
        for config_line in option['config']:
            print(f"   → {config_line}")
        print()

def show_current_config():
    """Show the currently active embedding configuration"""
    content = read_env_file()
    if content is None:
        return
    
    print("🔍 Current embedding configuration:")
    for line in content.split('\n'):
        if line.strip().startswith('EMBEDDING=') and not line.strip().startswith('#'):
            print(f"   ✅ {line.strip()}")
        elif line.strip().startswith('OLLAMA_BASE_URL=') and not line.strip().startswith('#'):
            print(f"   ✅ {line.strip()}")

def main():
    if len(sys.argv) == 1:
        print("🚀 Embedding Configuration Switcher")
        print("=" * 40)
        show_current_config()
        print()
        show_options()
        print("Usage: python switch_embedding.py [option]")
        print("       python switch_embedding.py current")
        return
    
    command = sys.argv[1].lower()
    
    if command == "current":
        show_current_config()
    elif command in EMBEDDING_OPTIONS:
        update_embedding_config(command)
    else:
        print(f"❌ Unknown option: {command}")
        show_options()

if __name__ == "__main__":
    main()