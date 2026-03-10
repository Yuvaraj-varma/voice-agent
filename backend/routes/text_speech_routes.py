from fastapi import APIRouter, Form, Request
from fastapi.responses import StreamingResponse, JSONResponse
import httpx
import os

from utils.logger import log_error

router = APIRouter()

ELEVEN_URL = "https://api.elevenlabs.io/v1"

def get_api_key():
    return os.getenv("ELEVENLABS_API_KEY")


# ---------------------------------------------
# 🔊 TEXT → SPEECH
# ---------------------------------------------
# Fix default voiceId to use valid ElevenLabs voice
@router.post("/speech")
async def text_to_speech(
    request: Request,
    text: str = Form(None),
    voiceId: str = Form("EXAVITQu4vr4xnSDxMaL"),  # Use Sarah voice by default
):
    try:
        # Allow JSON body OR form-data
        if text is None:
            try:
                data = await request.json()
                text = data.get("text", "").strip()
                voiceId = data.get("voiceId", "EXAVITQu4vr4xnSDxMaL")
            except Exception as e:
                log_error(e, "JSON parsing")
                return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

        if not text:
            return JSONResponse({"error": "Text is empty"}, status_code=400)

        api_key = get_api_key()
        if not api_key:
            return JSONResponse(
                {"error": "ELEVENLABS_API_KEY missing"},
                status_code=500,
            )

        url = f"{ELEVEN_URL}/text-to-speech/{voiceId}"

        payload = {
            "text": text[:5000],
            "model_id": "eleven_turbo_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8,
            },
        }

        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(url, headers=headers, json=payload)

        if res.status_code != 200:
            log_error(Exception(res.text), "TTS failed")
            return JSONResponse(
                {"error": "TTS failed"},
                status_code=500,
            )

        return StreamingResponse(
            iter([res.content]),
            media_type="audio/mpeg",
        )

    except Exception as e:
        log_error(e, "TTS")
        return JSONResponse({"error": "Internal server error"}, status_code=500)


# ---------------------------------------------
# 🎵 GET VOICES
# ---------------------------------------------
@router.get("/voices")
async def get_voices():
    try:
        api_key = get_api_key()
        if not api_key:
            return JSONResponse(
                {"error": "API key not configured"},
                status_code=500,
            )

        url = f"{ELEVEN_URL}/voices"
        headers = {
            "xi-api-key": api_key,
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.get(url, headers=headers)

        if res.status_code != 200:
            log_error(Exception(res.text), "Get Voices")
            return JSONResponse(
                {"error": "Failed to fetch voices"},
                status_code=500,
            )

        voices = res.json().get("voices", [])

        clean = [
            {"id": v.get("voice_id"), "name": v.get("name")}
            for v in voices
            if v.get("voice_id") and v.get("name")
        ]

        return {"voices": clean}

    except Exception as e:
        log_error(e, "Get Voices")
        return JSONResponse(
            {"error": "Internal server error"},
            status_code=500,
        )
