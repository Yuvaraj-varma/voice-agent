from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import base64
import httpx
import os

from services.rag_service import RAGService
from utils.logger import logger

router = APIRouter(tags=["📚 DS Tutor (RAG)"])


# ------------------------------------------
# REQUEST / RESPONSE MODELS
# ------------------------------------------
class DSRagRequest(BaseModel):
    question: str
    voiceId: Optional[str] = "EXAVITQu4vr4xnSDxMaL"  # Sarah voice
    includeAudio: Optional[bool] = False


class RAGResponse(BaseModel):
    answer: str
    sources: List[str]
    provider: Optional[str] = None
    audio: Optional[str] = None  # Base64 encoded audio


# ------------------------------------------
# TTS FOR DS TUTOR
# ------------------------------------------
async def synthesize_ds_tutor_speech(text: str, voice_id: str) -> Optional[str]:
    ds_elevenlabs_key = os.getenv("DS_TUTOR_ELEVENLABS_API_KEY") or os.getenv("ELEVENLABS_API_KEY")

    if not text:
        return None

    # Try ElevenLabs first
    if ds_elevenlabs_key:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                    headers={"xi-api-key": ds_elevenlabs_key, "Content-Type": "application/json"},
                    json={"text": text[:5000], "model_id": "eleven_turbo_v2", "voice_settings": {"stability": 0.7, "similarity_boost": 0.8}},
                )
            if res.status_code == 200:
                audio_b64 = base64.b64encode(res.content).decode()
                return f"data:audio/mpeg;base64,{audio_b64}"
            logger.error(f"DS Tutor ElevenLabs error {res.status_code}, falling back to gTTS")
        except Exception as e:
            logger.error(f"DS Tutor ElevenLabs failed: {e}, falling back to gTTS")

    # Fallback to gTTS
    try:
        from gtts import gTTS
        import io
        tts = gTTS(text=text[:5000], lang='en', slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        audio_b64 = base64.b64encode(buf.read()).decode()
        return f"data:audio/mpeg;base64,{audio_b64}"
    except Exception as e:
        logger.error(f"gTTS error: {e}")
        return None


# ------------------------------------------
# SERVICE ACCESS (FROM APP STATE)
# ------------------------------------------
def get_service(request: Request) -> RAGService:
    return request.app.state.rag_service


# ------------------------------------------
# ENDPOINT
# ------------------------------------------
@router.post("/ds-rag-agent", response_model=RAGResponse, summary="📚 Ask DS Tutor", description="Ask a Data Science question → Pinecone finds relevant docs → Gemini answers from your PDFs")
async def ds_rag_query(
    body: DSRagRequest,
    service: RAGService = Depends(get_service),
):
    start = time.perf_counter()

    answer, sources, provider = await service.process_question(body.question)
    
    # Generate audio if requested
    audio = None
    if body.includeAudio and body.voiceId:
        audio = await synthesize_ds_tutor_speech(answer, body.voiceId)

    elapsed = round(time.perf_counter() - start, 3)
    logger.info(f"RAG response generated in {elapsed}s (audio: {audio is not None})")

    return RAGResponse(
        answer=answer,
        sources=sources,
        provider=provider,
        audio=audio,
    )
