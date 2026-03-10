import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Test the voice agent key
key = os.getenv("VOICE_AGENT_GEMINI_API_KEY")
print(f"Testing key: {key[:20]}...")

genai.configure(api_key=key)

# List available models
print("\nAvailable models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")

# Test with gemini-2.5-flash
try:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Say hello")
    print(f"\n✅ Success with gemini-2.5-flash: {response.text}")
except Exception as e:
    print(f"\n❌ Error with gemini-2.5-flash: {e}")