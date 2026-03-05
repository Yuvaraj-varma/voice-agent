from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse, StreamingResponse
from pathlib import Path
import google.generativeai as genai
import httpx
import os
import tempfile

from utils.logger import log_error

router = APIRouter(tags=["Voice Transform"])

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def get_gemini_key():
    return os.getenv("GEMINI_API_KEY")

def get_eleven_key():
    return os.getenv("ELEVENLABS_API_KEY")


# ---------------------------------------------------------
# ElevenLabs TTS
# ---------------------------------------------------------
async def eleven_tts(text: str, voice_id: str):
    api_key = get_eleven_key()
    if not api_key or not text:
        return None

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    payload = {
        "text": text[:5000],
        "model_id": "eleven_turbo_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8,
        },
    }

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(url, headers=headers, json=payload)

        if res.status_code != 200:
            log_error(Exception(res.text), "Voice Transform TTS")
            return None

        return res.content

    except Exception as e:
        log_error(e, "Voice Transform ElevenLabs")
        return None


# ---------------------------------------------------------
# VOICE TRANSFORM ENDPOINT
# ---------------------------------------------------------
@router.post("/voice-transform")
async def voice_transform(
    file: UploadFile = File(...),
    voiceId: str = Form(...),
):
    tmp_path = None

    try:
        gemini_key = get_gemini_key()
        if not gemini_key:
            return JSONResponse(
                {"error": "Gemini not configured"},
                status_code=500,
            )
        
        genai.configure(api_key=gemini_key)

        if not file.filename:
            return JSONResponse(
                {"error": "Invalid file"},
                status_code=400,
            )

        ext = Path(file.filename).suffix.lower()
        if ext not in {".wav", ".webm", ".mp3"}:
            return JSONResponse(
                {"error": "Unsupported audio format"},
                status_code=400,
            )

        content = await file.read()
        if not content:
            return JSONResponse(
                {"error": "Empty file"},
                status_code=400,
            )

        if len(content) > MAX_FILE_SIZE:
            return JSONResponse(
                {"error": "File too large"},
                status_code=413,
            )

        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp:
            temp.write(content)
            tmp_path = temp.name

        # -------------------------
        # Gemini Speech-to-Text
        # -------------------------
        model = genai.GenerativeModel("gemini-1.5-flash")

        with open(tmp_path, "rb") as audio_file:
            audio_data = audio_file.read()

        stt_response = model.generate_content(
            [
                "Transcribe this audio accurately. Output ONLY the text:",
                {
                    "mime_type": f"audio/{ext.replace('.', '')}",
                    "data": audio_data,
                },
            ]
        )

        text = (stt_response.text or "").strip()

        if not text:
            return JSONResponse(
                {"error": "Could not transcribe audio"},
                status_code=400,
            )

        # -------------------------
        # ElevenLabs TTS
        # -------------------------
        audio_bytes = await eleven_tts(text, voiceId)

        if not audio_bytes:
            return JSONResponse(
                {"error": "Failed to generate audio"},
                status_code=500,
            )

        return StreamingResponse(
            iter([audio_bytes]),
            media_type="audio/mpeg",
        )

    except Exception as e:
        log_error(e, "Voice Transform")
        return JSONResponse(
            {"error": "Processing failed"},
            status_code=500,
        )

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
