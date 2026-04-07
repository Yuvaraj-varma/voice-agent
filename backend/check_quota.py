import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

KEYS = {
    "TTS_GEMINI_API_KEY":         os.getenv("TTS_GEMINI_API_KEY"),
    "SPEECH_GEMINI_API_KEY":      os.getenv("SPEECH_GEMINI_API_KEY"),
    "VOICE_AGENT_GEMINI_API_KEY": os.getenv("VOICE_AGENT_GEMINI_API_KEY"),
    "RAG_GEMINI_API_KEY":         os.getenv("RAG_GEMINI_API_KEY"),
}

TEST_PROMPT = "Say OK"
MODELS = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]

print(f"{'Key':<30} {'Status':<12} {'Info'}")
print("-" * 70)
for name, key in KEYS.items():
    print(f"{name}: {key[:20] if key else 'MISSING'}...")

for name, key in KEYS.items():
    if not key:
        print(f"{name:<30} {'MISSING':<12} Not set in .env")
        continue
    for model in MODELS:
        try:
            client = genai.Client(api_key=key)
            client.models.generate_content(model=model, contents=TEST_PROMPT)
            print(f"{name:<30} {'✅ OK':<12} Working with {model}")
            break
        except ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print(f"{name:<30} {'❌ QUOTA':<12} {model} - rate limit")
            elif "401" in str(e) or "API_KEY_INVALID" in str(e):
                print(f"{name:<30} {'❌ INVALID':<12} Invalid API key")
                break
            else:
                print(f"{name:<30} {'❌ ERROR':<12} {model} - {str(e)[:40]}")
        except Exception as e:
            print(f"{name:<30} {'❌ ERROR':<12} {str(e)[:50]}")
            break
