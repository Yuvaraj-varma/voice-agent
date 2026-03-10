import requests

api_key = "sk_86e3c14e7a5a99c63e0aa7e5bee0529ecda672c5b760dcd9"

# Test 1: Get voices
print("Testing ElevenLabs API key...")
print(f"Key: {api_key[:20]}...")

response = requests.get(
    "https://api.elevenlabs.io/v1/voices",
    headers={"xi-api-key": api_key}
)

if response.status_code == 200:
    voices = response.json().get("voices", [])
    print(f"✅ API key is VALID - Found {len(voices)} voices")
    if voices:
        print(f"   Sample voice: {voices[0]['name']} (ID: {voices[0]['voice_id']})")
else:
    print(f"❌ API key is INVALID - Status: {response.status_code}")
    print(f"   Error: {response.text}")

# Test 2: Try TTS
print("\nTesting Text-to-Speech...")
tts_response = requests.post(
    "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL",
    headers={
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    },
    json={
        "text": "Hello, this is a test.",
        "model_id": "eleven_turbo_v2"
    }
)

if tts_response.status_code == 200:
    print(f"✅ TTS works - Generated {len(tts_response.content)} bytes of audio")
else:
    print(f"❌ TTS failed - Status: {tts_response.status_code}")
    print(f"   Error: {tts_response.text}")