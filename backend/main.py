from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.agent import router as agent_router
from routes.text_speech_routes import router as text_speech_router
from routes.voice_transform import router as voice_transform_router   # NEW ROUTE

import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="🎙 Voice Agent Backend",
    version="1.0.0",
    description="Backend for AI Agent, Text-to-Speech, and Voice Transformation (Speech → Text → Speech)"
)

# -----------------------------------------------------
# CORS
# -----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # your frontend uses localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------
# ROUTERS
# -----------------------------------------------------

# AI Agent (Gemini + ElevenLabs)
app.include_router(agent_router, prefix="/api", tags=["AI Agent"])

# Text → Speech (TTS) Routes + Voices
app.include_router(text_speech_router, prefix="/api", tags=["Text-to-Speech"])

# Voice Transform Route (Speech → Text using Gemini, then Text → Speech using ElevenLabs)
app.include_router(voice_transform_router, prefix="/api", tags=["Voice Transform"])

# -----------------------------------------------------
# ROOT
# -----------------------------------------------------
@app.get("/")
def home():
    return {"message": "✅ Voice Agent Backend Running — GPT + Voice Ready!"}
