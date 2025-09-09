#!/usr/bin/env python3
"""
Quick verification script to check if temperature settings are being loaded correctly.
"""
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    print("🔧 Temperature Configuration Verification")
    print("=" * 50)
    
    # Check environment variables directly
    print("\n📁 Environment Variables:")
    print(f"   TEMPERATURE: {os.getenv('TEMPERATURE', 'not set')}")
    print(f"   FAST_TEMPERATURE: {os.getenv('FAST_TEMPERATURE', 'not set')}")
    print(f"   SMART_TEMPERATURE: {os.getenv('SMART_TEMPERATURE', 'not set')}")
    print(f"   STRATEGIC_TEMPERATURE: {os.getenv('STRATEGIC_TEMPERATURE', 'not set')}")
    
    # Try to load GPT Researcher config
    try:
        from gpt_researcher.config.config import Config
        cfg = Config()
        print("\n⚙️ GPT Researcher Config Object:")
        
        # Check different possible attribute names for temperature
        temp_attrs = [
            'temperature',
            'fast_llm_temperature', 
            'smart_llm_temperature',
            'strategic_llm_temperature',
            'llm_temperature',
            'default_temperature'
        ]
        
        found_attrs = []
        for attr in temp_attrs:
            if hasattr(cfg, attr):
                value = getattr(cfg, attr)
                print(f"   {attr}: {value}")
                found_attrs.append(attr)
        
        if not found_attrs:
            print("   ⚠️ No temperature attributes found in Config object")
            print("   Available attributes:")
            attrs = [attr for attr in dir(cfg) if not attr.startswith('_')]
            for attr in sorted(attrs)[:10]:  # Show first 10 to avoid clutter
                print(f"     - {attr}")
            print("     ... (and more)")
            
    except ImportError as e:
        print(f"\n❌ Could not import GPT Researcher Config: {e}")
    except Exception as e:
        print(f"\n❌ Error checking Config: {e}")
    
    print("\n✅ Verification complete!")

if __name__ == "__main__":
    main()