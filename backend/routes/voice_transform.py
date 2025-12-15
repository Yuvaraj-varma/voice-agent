# backend/routes/voice_transform.py

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse, StreamingResponse
from dotenv import load_dotenv
import google.generativeai as genai
import requests, os, tempfile

load_dotenv()

router = APIRouter(tags=["Voice Transform"])

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY")

genai.configure(api_key=GEMINI_KEY)


# ---------------------------------------------------------
#  Helper → ElevenLabs (Text → Speech)
# ---------------------------------------------------------
def eleven_tts(text: str, voice_id: str):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": ELEVEN_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "model_id": "eleven_turbo_v2",
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.8},
    }

    res = requests.post(url, headers=headers, json=payload)

    if res.status_code != 200:
        print("❌ ElevenLabs error:", res.text)
        return None

    return res.content  # raw audio bytes


# ---------------------------------------------------------
#  MAIN ROUTE → Speech → Text (Gemini) → Speech (ElevenLabs)
# ---------------------------------------------------------
@router.post("/voice-transform")
async def voice_transform(
    file: UploadFile = File(...),
    voiceId: str = Form(...)   # ← get voiceId from frontend
):
    try:
        # Save uploaded audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            temp.write(await file.read())
            temp.flush()
            audio_path = temp.name

        # --- 1) Gemini Speech-to-Text ---
        model = genai.GenerativeModel("gemini-2.5-flash")
        stt_response = model.generate_content(
            {"mime_type": "audio/wav", "data": open(audio_path, "rb").read()}
        )

        text = (stt_response.text or "").strip()
        print("📝 Transcription:", text)

        if not text:
            return JSONResponse({"error": "Could not transcribe audio"}, status_code=400)

        # --- 2) ElevenLabs Text-to-Speech with SELECTED voiceId ---
        audio_bytes = eleven_tts(text, voiceId)

        if audio_bytes is None:
            return JSONResponse(
                {"error": "Failed to generate audio from ElevenLabs"},
                status_code=500,
            )

        return StreamingResponse(
            iter([audio_bytes]),
            media_type="audio/mpeg"
        )

    except Exception as e:
        print("❌ Voice Transform error:", e)
        return JSONResponse({"error": str(e)}, status_code=500)
