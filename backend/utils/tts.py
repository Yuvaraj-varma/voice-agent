import requests, base64, os
from dotenv import load_dotenv

load_dotenv()
ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY")

def text_to_speech(text, voice_id="Clyde"):
    """
    Convert AI text → speech using ElevenLabs API
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVEN_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }

    res = requests.post(url, headers=headers, json=data)
    if res.status_code != 200:
        print("❌ ElevenLabs error:", res.text)
        return None

    audio_base64 = base64.b64encode(res.content).decode("utf-8")
    return f"data:audio/mpeg;base64,{audio_base64}"
