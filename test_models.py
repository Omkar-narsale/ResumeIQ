"""
Test script to list available Gemini models
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not set")
    exit()

genai.configure(api_key=api_key)

print("📋 Available Models:")
print("-" * 50)

try:
    for model in genai.list_models():
        print(f"✅ {model.name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"   Methods: {model.supported_generation_methods}")
except Exception as e:
    print(f"❌ Error: {e}")
