from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import base64
import httpx
import os

from services.rag_service import RAGService
from utils.logger import logger

router = APIRouter()


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
    """Generate speech for DS Tutor using separate API key"""
    ds_elevenlabs_key = os.getenv("DS_TUTOR_ELEVENLABS_API_KEY") or os.getenv("ELEVENLABS_API_KEY")
    
    if not ds_elevenlabs_key or not text:
        return None
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                headers={
                    "xi-api-key": ds_elevenlabs_key,
                    "Content-Type": "application/json",
                },
                json={
                    "text": text[:5000],  # Limit text length
                    "model_id": "eleven_turbo_v2",
                    "voice_settings": {
                        "stability": 0.7,
                        "similarity_boost": 0.8,
                    },
                },
            )
        
        if res.status_code == 200:
            audio_b64 = base64.b64encode(res.content).decode()
            return f"data:audio/mpeg;base64,{audio_b64}"
        
        logger.error(f"DS Tutor TTS error {res.status_code}: {res.text[:200]}")
        return None
        
    except Exception as e:
        logger.error(f"DS Tutor TTS error: {e}")
        return None


# ------------------------------------------
# SERVICE ACCESS (FROM APP STATE)
# ------------------------------------------
def get_service(request: Request) -> RAGService:
    return request.app.state.rag_service


# ------------------------------------------
# ENDPOINT
# ------------------------------------------
@router.post("/ds-rag-agent", response_model=RAGResponse)
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
