import requests
import base64
import os
from dotenv import load_dotenv
from utils.logger import log_error

load_dotenv()
ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVEN_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable not set")

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

    try:
        res = requests.post(url, headers=headers, json=data, timeout=30)
        if res.status_code != 200:
            log_error(Exception(f"ElevenLabs API error: {res.text}"), "TTS Generation")
            return None
        audio_base64 = base64.b64encode(res.content).decode("utf-8")
        return f"data:audio/mpeg;base64,{audio_base64}"
    except Exception as e:
        log_error(e, "TTS Generation")
        return None
