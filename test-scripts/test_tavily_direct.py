#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_tavily_api():
    """Test Tavily API key directly"""
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    if not tavily_api_key:
        print("❌ TAVILY_API_KEY not found in environment variables")
        return False
    
    print(f"🔑 TAVILY_API_KEY found: {tavily_api_key[:8]}...")
    
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=tavily_api_key)
        
        # Test with a simple search
        print("🔍 Testing Tavily search...")
        result = client.get_search_context("test query", search_depth="basic", max_tokens=100)
        print("✅ Tavily API key is working!")
        print(f"📄 Search result preview: {str(result)[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Tavily API error: {e}")
        if "401" in str(e) or "Unauthorized" in str(e):
            print("💡 This suggests your API key is invalid or expired")
            print("💡 Get a free key at: https://app.tavily.com")
        return False

if __name__ == "__main__":
    test_tavily_api()