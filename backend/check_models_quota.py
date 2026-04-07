import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

KEYS = {
    "TTS_GEMINI_API_KEY":         os.getenv("TTS_GEMINI_API_KEY"),
    "SPEECH_GEMINI_API_KEY":      os.getenv("SPEECH_GEMINI_API_KEY"),
    "VOICE_AGENT_GEMINI_API_KEY": os.getenv("VOICE_AGENT_GEMINI_API_KEY"),
    "RAG_GEMINI_API_KEY":         os.getenv("RAG_GEMINI_API_KEY"),
}

TEST_PROMPT = "Say OK"

async def test_model(client, model_name):
    try:
        await asyncio.to_thread(
            client.models.generate_content,
            model=model_name,
            contents=TEST_PROMPT
        )
        return model_name, "✅ FREE"
    except ClientError as e:
        err = str(e)
        if "429" in err or "RESOURCE_EXHAUSTED" in err:
            return model_name, "❌ QUOTA"
        elif "400" in err:
            return model_name, None  # skip non-text
        return model_name, f"⚠️ ERROR"
    except Exception:
        return model_name, f"⚠️ ERROR"

async def check_key(key_name, api_key, models):
    print(f"\n{'='*60}")
    print(f"🔑 {key_name}: {api_key[:20]}...")
    print(f"{'='*60}")

    client = genai.Client(api_key=api_key)
    tasks = [test_model(client, m) for m in models]
    results = await asyncio.gather(*tasks)

    free = []
    for model_name, status in sorted(results):
        if status is None:
            continue
        print(f"  {status}  {model_name}")
        if "FREE" in status:
            free.append(model_name)

    print(f"\n  → {len(free)} free model(s): {', '.join(free) if free else 'None'}")

async def main():
    first_key = next(v for v in KEYS.values() if v)
    client = genai.Client(api_key=first_key)
    all_models = sorted([
        m.name.replace("models/", "") for m in client.models.list()
        if "generateContent" in (m.supported_actions or [])
    ])
    print(f"Total models: {len(all_models)} | Checking all 4 keys in parallel...\n")

    await asyncio.gather(*[
        check_key(name, key, all_models)
        for name, key in KEYS.items() if key
    ])

asyncio.run(main())
