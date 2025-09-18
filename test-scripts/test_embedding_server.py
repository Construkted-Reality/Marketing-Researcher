#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_embedding_server():
    """Test embedding server connectivity"""
    embedding_api_base = os.getenv("OPENAI_EMBEDDING_API_BASE")
    embedding_api_key = os.getenv("OPENAI_EMBEDDING_API_KEY", "dummy-key")
    
    if not embedding_api_base:
        print("❌ OPENAI_EMBEDDING_API_BASE not found in environment variables")
        return False
    
    print(f"🔍 Testing embedding server at: {embedding_api_base}")
    
    # Test with a simple embedding request
    try:
        response = requests.post(
            f"{embedding_api_base}/embeddings",
            headers={
                "Authorization": f"Bearer {embedding_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "input": "Hello, this is a test",
                "model": "text-embedding-ada-002"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            embeddings = data.get("data", [])
            if embeddings and len(embeddings[0].get("embedding", [])) > 0:
                embedding_dim = len(embeddings[0]["embedding"])
                print(f"✅ Embedding server is working!")
                print(f"📏 Embedding dimension: {embedding_dim}")
                print(f"🔢 Model: {data.get('model', 'unknown')}")
                return True
            else:
                print("❌ Invalid response format from embedding server")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to embedding server at {embedding_api_base}")
        print("💡 Make sure your embedding server is running and accessible")
        return False
    except Exception as e:
        print(f"❌ Embedding server error: {e}")
        return False

if __name__ == "__main__":
    test_embedding_server()