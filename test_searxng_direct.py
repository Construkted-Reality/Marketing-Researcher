#!/usr/bin/env python3
"""
Test script to validate SearXNG connectivity and response format
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_searxng_connectivity():
    """Test basic connectivity to SearXNG instance"""
    searx_url = os.getenv("SEARX_URL")
    
    if not searx_url:
        print("❌ SEARX_URL not found in environment variables")
        print("   Please set SEARX_URL=https://your-searxng-instance.com")
        return False
    
    print(f"🔍 Testing SearXNG connectivity...")
    print(f"📡 SearXNG URL: {searx_url}")
    
    # Test basic endpoint availability
    try:
        response = requests.get(searx_url, timeout=10)
        if response.status_code == 200:
            print("✅ SearXNG instance is reachable")
        else:
            print(f"⚠️ SearXNG returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to SearXNG: {e}")
        return False
    
    return True

def test_searxng_search_api():
    """Test SearXNG search API with JSON format"""
    searx_url = os.getenv("SEARX_URL")
    
    if not searx_url:
        return False
    
    # Construct search endpoint
    search_endpoint = f"{searx_url.rstrip('/')}/search"
    
    print(f"\n🔎 Testing SearXNG search API...")
    print(f"📡 Search endpoint: {search_endpoint}")
    
    # Test search query
    test_query = "artificial intelligence latest news"
    params = {
        'q': test_query,
        'format': 'json',
        'categories': 'general',
        'engines': 'duckduckgo,bing,google',  # Common engines
        'lang': 'en'
    }
    
    try:
        print(f"🔍 Searching for: '{test_query}'")
        response = requests.get(search_endpoint, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Search API returned status code: {response.status_code}")
            print(f"Response text: {response.text[:200]}...")
            return False
        
        # Parse JSON response
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON response: {e}")
            print(f"Response text: {response.text[:200]}...")
            return False
        
        # Validate response structure
        if 'results' not in data:
            print("❌ Response missing 'results' field")
            print(f"Available fields: {list(data.keys())}")
            return False
        
        results = data['results']
        print(f"✅ Search successful! Found {len(results)} results")
        
        # Show sample results
        if results:
            print("\n📋 Sample search results:")
            for i, result in enumerate(results[:3]):  # Show first 3 results
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                content = result.get('content', 'No content')
                
                print(f"   {i+1}. {title}")
                print(f"      URL: {url}")
                print(f"      Content: {content[:100]}...")
                print()
        
        # Check if format is compatible with GPT Researcher
        print("🔧 Checking GPT Researcher compatibility...")
        required_fields = ['title', 'url']
        
        for result in results[:5]:  # Check first 5 results
            missing_fields = [field for field in required_fields if field not in result]
            if missing_fields:
                print(f"⚠️ Result missing fields: {missing_fields}")
                print(f"   Available fields: {list(result.keys())}")
            else:
                print("✅ Result format compatible with GPT Researcher")
                break
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Search request failed: {e}")
        return False

def test_searxng_engines():
    """Test which search engines are available in SearXNG"""
    searx_url = os.getenv("SEARX_URL")
    
    if not searx_url:
        return False
    
    print(f"\n🔧 Testing available search engines...")
    
    # Try to get engines list (if available)
    engines_endpoint = f"{searx_url.rstrip('/')}/engines"
    
    try:
        response = requests.get(engines_endpoint, timeout=10)
        if response.status_code == 200:
            try:
                engines_data = response.json()
                print(f"✅ Found {len(engines_data)} available engines")
                
                # Show some popular engines
                popular_engines = ['google', 'bing', 'duckduckgo', 'startpage', 'yahoo']
                available_popular = []
                
                for engine_name in popular_engines:
                    if any(engine.get('name', '').lower() == engine_name for engine in engines_data):
                        available_popular.append(engine_name)
                
                if available_popular:
                    print(f"📊 Popular engines available: {', '.join(available_popular)}")
                
            except json.JSONDecodeError:
                print("⚠️ Engines endpoint doesn't return JSON (this is normal for some SearXNG instances)")
        else:
            print("⚠️ Engines endpoint not available (this is normal for some SearXNG instances)")
            
    except requests.exceptions.RequestException:
        print("⚠️ Could not fetch engines list (this is normal for some SearXNG instances)")
    
    return True

def main():
    print("🚀 SearXNG Connectivity Test")
    print("=" * 40)
    
    # Test basic connectivity
    if not test_searxng_connectivity():
        print("\n❌ Basic connectivity test failed")
        return
    
    # Test search API
    if not test_searxng_search_api():
        print("\n❌ Search API test failed")
        return
    
    # Test engines (optional)
    test_searxng_engines()
    
    print("\n✅ All SearXNG tests passed!")
    print("🎯 Your SearXNG instance is ready for GPT Researcher")
    print("\n📝 Next steps:")
    print("   1. Run: python switch_search.py searx,mcp")
    print("   2. Test with: pipenv run python test.py")

if __name__ == "__main__":
    main()