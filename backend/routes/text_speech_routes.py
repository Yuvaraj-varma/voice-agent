# backend/routes/text_speech_routes.py
from fastapi import APIRouter, Form, Request
from fastapi.responses import StreamingResponse, JSONResponse
import requests, os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_URL = "https://api.elevenlabs.io/v1"

HEADERS_JSON = {
    "xi-api-key": ELEVENLABS_API_KEY,
    "Content-Type": "application/json",
}

# ---------------------------------------------
# 🔊 1. TEXT → SPEECH (TTS)
# ---------------------------------------------
@router.post("/speech")
async def text_to_speech(
    request: Request,
    text: str = Form(None),
    voiceId: str = Form("Clyde"),
):
    try:
        # Allow JSON body also
        if text is None:
            data = await request.json()
            text = data.get("text", "")
            voiceId = data.get("voiceId", "Clyde")

        if not text.strip():
            return JSONResponse({"error": "Text is empty"}, status_code=400)

        url = f"{ELEVEN_URL}/text-to-speech/{voiceId}"

        payload = {
            "text": text,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
        }

        res = requests.post(url, headers=HEADERS_JSON, json=payload)

        if res.status_code != 200:
            return JSONResponse(
                {"error": "TTS failed", "details": res.text},
                status_code=500,
            )

        return StreamingResponse(iter([res.content]), media_type="audio/mpeg")

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ---------------------------------------------
# 🎵 2. GET VOICES (used by both pages)
# ---------------------------------------------
@router.get("/voices")
async def get_voices():
    try:
        url = f"{ELEVEN_URL}/voices"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Accept": "application/json",
        }

        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            return JSONResponse(
                {"error": "Failed to fetch voices", "details": res.text},
                status_code=500,
            )

        data = res.json()
        voices = data.get("voices", [])

        clean = [
            {"id": v.get("voice_id"), "name": v.get("name")}
            for v in voices
        ]

        return {"voices": clean}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
