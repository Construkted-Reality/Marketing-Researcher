#!/usr/bin/env python3
"""
Utility script to easily switch between different search engine configurations
Usage: python switch_search.py [option]
"""

import sys
import os
from pathlib import Path

# Search engine configuration options
SEARCH_OPTIONS = {
    "searx,mcp": {
        "name": "SearXNG + MCP Hybrid (Default)",
        "description": "Privacy-first self-hosted search with AI reasoning",
        "config": [
            "RETRIEVER=searx,mcp"
        ],
        "comment_out": [
            "RETRIEVER=tavily,mcp",
            "RETRIEVER=searx", 
            "RETRIEVER=tavily"
        ]
    },
    "tavily,mcp": {
        "name": "Tavily + MCP Hybrid",
        "description": "Commercial search API with AI reasoning",
        "config": [
            "RETRIEVER=tavily,mcp"
        ],
        "comment_out": [
            "RETRIEVER=searx,mcp",
            "RETRIEVER=searx",
            "RETRIEVER=tavily"
        ]
    },
    "searx": {
        "name": "SearXNG Only",
        "description": "Pure self-hosted search, no AI reasoning",
        "config": [
            "RETRIEVER=searx"
        ],
        "comment_out": [
            "RETRIEVER=searx,mcp",
            "RETRIEVER=tavily,mcp",
            "RETRIEVER=tavily"
        ]
    },
    "tavily": {
        "name": "Tavily Only", 
        "description": "Pure commercial search API, no AI reasoning",
        "config": [
            "RETRIEVER=tavily"
        ],
        "comment_out": [
            "RETRIEVER=searx,mcp",
            "RETRIEVER=tavily,mcp", 
            "RETRIEVER=searx"
        ]
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

def update_search_config(option_key):
    """Update the .env file with the specified search configuration"""
    if option_key not in SEARCH_OPTIONS:
        print(f"❌ Invalid option: {option_key}")
        print(f"Valid options: {', '.join(SEARCH_OPTIONS.keys())}")
        return False
    
    option = SEARCH_OPTIONS[option_key]
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
    print("\n🔧 Active search configuration:")
    for config_line in option["config"]:
        print(f"   {config_line}")
    
    return True

def show_options():
    """Display available search engine options"""
    print("🎯 Available search engine configurations:")
    print()
    
    for key, option in SEARCH_OPTIONS.items():
        print(f"📌 {key}: {option['name']}")
        print(f"   {option['description']}")
        for config_line in option['config']:
            print(f"   → {config_line}")
        print()

def show_current_config():
    """Show the currently active search configuration"""
    content = read_env_file()
    if content is None:
        return
    
    print("🔍 Current search engine configuration:")
    for line in content.split('\n'):
        if line.strip().startswith('RETRIEVER=') and not line.strip().startswith('#'):
            print(f"   ✅ {line.strip()}")
        elif line.strip().startswith('SEARX_URL=') and not line.strip().startswith('#'):
            print(f"   ✅ {line.strip()}")
        elif line.strip().startswith('TAVILY_API_KEY=') and not line.strip().startswith('#'):
            print(f"   ✅ {line.strip()}")

def main():
    if len(sys.argv) == 1:
        print("🚀 Search Engine Configuration Switcher")
        print("=" * 45)
        show_current_config()
        print()
        show_options()
        print("Usage: python switch_search.py [option]")
        print("       python switch_search.py current")
        return
    
    command = sys.argv[1].lower()
    
    if command == "current":
        show_current_config()
    elif command in SEARCH_OPTIONS:
        update_search_config(command)
    else:
        print(f"❌ Unknown option: {command}")
        show_options()

if __name__ == "__main__":
    main()