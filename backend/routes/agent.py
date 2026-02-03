from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse
import tempfile, os, requests, base64, google.generativeai as genai
from dotenv import load_dotenv
import re
from datetime import datetime
import pytz
# test git change
# Agent API main route handler
# This file handles agent-related endpoints
# Validates incoming request data
# Checks required fields before processing
# Handles agent creation logic
# Handles agent update logic
# Handles agent delete logic
# Sends standardized success responses
# Sends standardized error responses
# Logs agent-related actions
# Catches unexpected exceptions
# Uses service layer for business logic
# Keeps routing logic minimal
# Ensures proper HTTP status codes
# Prevents invalid agent data insertion
# Supports future agent enhancements
# Improves code readability
# Added for git commit practice
# Temporary comments for learning git
# End of agent route comments

load_dotenv()

router = APIRouter()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SPORTS_API_KEY = os.getenv("SPORTS_API_KEY")

ELEVEN_URL = "https://api.elevenlabs.io/v1/text-to-speech"
SPORTS_API_BASE = "https://v1.cricket.api-sports.io"

genai.configure(api_key=GEMINI_API_KEY)


# ----------------------------------------------------
# Helper: Clean text (remove markdown)
# ----------------------------------------------------
def clean_text(text: str):
    if not text:
        return ""
    text = re.sub(r"[*_~`]+", "", text)         # remove markdown (*, _, ~)
    text = re.sub(r"\b\d{1,2}:\d{2}\b", "", text)  # remove timestamps
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ----------------------------------------------------
# Helper: Get today's date in India
# ----------------------------------------------------
def get_india_date():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    return now.strftime("%A, %d %B %Y")  # Example: Friday, 21 November 2025


# ----------------------------------------------------
# Helper: Real-time sports data
# ----------------------------------------------------
def get_live_cricket_score():
    try:
        headers = {
            "x-rapidapi-key": SPORTS_API_KEY,
            "x-rapidapi-host": "v1.cricket.api-sports.io"
        }

        url = f"{SPORTS_API_BASE}/fixtures?live=all"
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            return "I could not fetch live cricket scores right now."

        data = res.json()

        if "response" not in data or len(data["response"]) == 0:
            return "There are no live cricket matches at the moment."

        match = data["response"][0]

        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        status = match["status"]
        venue = match["venue"]["name"]

        return f"Live cricket update: {home} vs {away}. Status: {status}. Venue: {venue}."

    except Exception as e:
        print("Sports API error:", e)
        return "Sports data is temporarily unavailable."


# ----------------------------------------------------
# Convert text → ElevenLabs audio
# ----------------------------------------------------
def generate_speech(text: str, voice="Clyde"):
    if not text:
        return None
    try:
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "text": text,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
        }
        url = f"{ELEVEN_URL}/{voice}"
        res = requests.post(url, headers=headers, json=payload)

        if res.status_code != 200:
            print("ElevenLabs Error:", res.text)
            return None

        return f"data:audio/mpeg;base64,{base64.b64encode(res.content).decode()}"

    except Exception as e:
        print("TTS Error:", e)
        return None


# ----------------------------------------------------
# 🎙 Voice Agent
# ----------------------------------------------------
@router.post("/agent")
async def process_voice(request: Request, file: UploadFile = File(...)):
    try:
        form = await request.form()
        voice = form.get("voiceId", "Clyde")

        # Save temp audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(await file.read())
            tmp.flush()
            audio_path = tmp.name

        model = genai.GenerativeModel("gemini-2.5-flash")

        # India date
        today_india = get_india_date()

        response = model.generate_content([
            {
                "role": "user",
                "parts": [
                    {"mime_type": "audio/webm", "data": open(audio_path, "rb").read()},
                    {
                        "text": (
                            f"Today's date in India is {today_india}. "
                            "If the question is about sports, answer using real-time live score API results. "
                            "Otherwise, answer normally in simple clean English with no markdown."
                        )
                    },
                ],
            }
        ])

        os.remove(audio_path)

        ai_text = clean_text(response.text)

        # Sports auto-detection
        if any(word in ai_text.lower() for word in ["cricket", "score", "match", "ipl"]):
            ai_text = get_live_cricket_score()

        audio_data = generate_speech(ai_text, voice)

        return {
            "userText": "Your voice message",
            "text": ai_text,
            "audio": audio_data,
        }

    except Exception as e:
        print("Voice agent error:", e)
        return JSONResponse({"error": str(e)}, status_code=500)


# ----------------------------------------------------
# 💬 Text Agent
# ----------------------------------------------------
@router.post("/text-agent")
async def process_text(request: Request):
    try:
        data = await request.json()
        user_text = data.get("text", "")
        voice = data.get("voiceId", "Clyde")

        today_india = get_india_date()

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            f"Today's date in India is {today_india}. "
            f"Respond to this query in clean English: {user_text}"
        )

        ai_text = clean_text(response.text)

        # If user asked about sports → use live API
        if any(word in user_text.lower() for word in ["cricket", "score", "match", "ipl"]):
            ai_text = get_live_cricket_score()

        audio_data = generate_speech(ai_text, voice)

        return {
            "userText": user_text,
            "text": ai_text,
            "audio": audio_data,
        }

    except Exception as e:
        print("Text agent error:", e)
        return JSONResponse({"error": str(e)}, status_code=500)


# ----------------------------------------------------
# 🔊 Voices list
# ----------------------------------------------------
@router.get("/voices")
def list_voices():
    try:
        url = "https://api.elevenlabs.io/v1/voices"
        headers = {"xi-api-key": ELEVENLABS_API_KEY}

        response = requests.get(url, headers=headers)
        return response.json()

    except Exception as e:
        print("Voice fetch error:", e)
        return {"error": str(e)}
