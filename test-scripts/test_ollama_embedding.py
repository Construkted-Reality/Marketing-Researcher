#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ollama_embedding():
    """Test Ollama embedding server connectivity"""
    embedding_api_base = os.getenv("OPENAI_EMBEDDING_API_BASE")
    
    if not embedding_api_base:
        print("❌ OPENAI_EMBEDDING_API_BASE not found in environment variables")
        return False
    
    # Remove any trailing /v1 since Ollama doesn't use that
    base_url = embedding_api_base.rstrip('/v1').rstrip('/')
    
    print(f"🔍 Testing Ollama server at: {base_url}")
    
    try:
        # Test 1: Check if Ollama is running
        print("📡 Checking if Ollama server is responding...")
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"✅ Ollama server is running with {len(models)} models")
            for model in models:
                print(f"  📦 {model.get('name', 'unknown')}")
        else:
            print(f"❌ Ollama server check failed: {response.status_code}")
            return False
        
        # Test 2: Try embedding with a known model
        print("🧠 Testing embedding generation...")
        embed_models = ["nomic-embed-text", "all-minilm", "mxbai-embed-large"]
        
        for model_name in embed_models:
            try:
                embed_response = requests.post(
                    f"{base_url}/api/embeddings",
                    json={
                        "model": model_name,
                        "prompt": "Hello, this is a test"
                    },
                    timeout=10
                )
                
                if embed_response.status_code == 200:
                    data = embed_response.json()
                    embedding = data.get("embedding", [])
                    if embedding and len(embedding) > 0:
                        print(f"✅ Embedding test successful with model: {model_name}")
                        print(f"📏 Embedding dimension: {len(embedding)}")
                        return True
                else:
                    print(f"⚠️ Model {model_name} failed: {embed_response.status_code}")
                    
            except Exception as e:
                print(f"⚠️ Model {model_name} error: {e}")
                
        print("❌ No working embedding models found")
        print("💡 Try running: ollama pull nomic-embed-text")
        return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Ollama server at {base_url}")
        print("💡 Make sure Ollama is running: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Ollama server error: {e}")
        return False

if __name__ == "__main__":
    test_ollama_embedding()