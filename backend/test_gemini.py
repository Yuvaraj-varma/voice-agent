import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

# Get Gemini API key from .env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY missing in .env")
    exit()

# Configure Gemini
genai.configure(api_key=api_key)

# ✅ Use the working model name from your list
model = genai.GenerativeModel("gemini-2.5-flash")

# Send a simple test prompt
response = model.generate_content("Hi Gemini! Say hello to Yuvaraj in a friendly way.")

print("\n✅ Gemini response:")
print(response.text)
