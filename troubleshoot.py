"""
Detailed Google Gemini API Troubleshooting
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ GOOGLE_API_KEY environment variable not set")
    print("   Make sure .env file exists with: GOOGLE_API_KEY=YOUR_KEY")
    exit()

print("✅ API Key found")
print(f"   Key starts with: {api_key[:20]}...")
print()

# Configure the client
genai.configure(api_key=api_key)

print("=" * 60)
print("Testing Google Gemini API Access")
print("=" * 60)

# Test 1: List models (should work)
print("\n📋 Test 1: Listing available models...")
try:
    models = list(genai.list_models())
    print(f"✅ SUCCESS: Found {len(models)} models")
except Exception as e:
    print(f"❌ FAILED: {e}")
    exit()

# Test 2: Try to use gemini-2.5-flash
print("\n🤖 Test 2: Testing gemini-2.5-flash model...")
try:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Say hello!")
    print(f"✅ SUCCESS: Model responded with: {response.text[:50]}...")
except Exception as e:
    print(f"❌ FAILED: {e}")
    print(f"   Error type: {type(e).__name__}")

    # Try alternative models
    print("\n🔄 Trying alternative models...")
    alternatives = [
        "gemini-2.0-flash",
        "gemini-flash-latest",
        "gemini-pro-latest"
    ]

    for alt_model in alternatives:
        try:
            print(f"   Trying {alt_model}...", end=" ")
            model = genai.GenerativeModel(alt_model)
            response = model.generate_content("Say hello!")
            print(f"✅ WORKS!")
            print(f"   Use this in the app: {alt_model}")
            break
        except Exception as alt_e:
            print(f"❌ Failed")

print("\n" + "=" * 60)
print("Troubleshooting complete!")
print("=" * 60)
