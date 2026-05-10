from fastapi import APIRouter, Depends, Request, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import time
import base64
import httpx
import os

from services.rag_service import RAGService
from utils.logger import logger

router = APIRouter(tags=["🧾 Invoice System (RAG)"])


# ------------------------------------------
# MODELS
# ------------------------------------------
class InvoiceQueryRequest(BaseModel):
    question: str
    voiceId: Optional[str] = "EXAVITQu4vr4xnSDxMaL"
    includeAudio: Optional[bool] = False
    session_id: Optional[str] = None


class InvoiceQueryResponse(BaseModel):
    answer: str
    sources: List[str]
    provider: Optional[str] = None
    audio: Optional[str] = None


class UploadResponse(BaseModel):
    message: str
    chunks: int


# ------------------------------------------
# TTS
# ------------------------------------------
async def synthesize_speech(text: str, voice_id: str) -> Optional[str]:
    key = os.getenv("DS_TUTOR_ELEVENLABS_API_KEY") or os.getenv("ELEVENLABS_API_KEY")
    if not text:
        return None

    if key:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                    headers={"xi-api-key": key, "Content-Type": "application/json"},
                    json={"text": text[:5000], "model_id": "eleven_turbo_v2"},
                )
            if res.status_code == 200:
                return f"data:audio/mpeg;base64,{base64.b64encode(res.content).decode()}"
        except Exception as e:
            logger.error(f"ElevenLabs failed: {e}")

    try:
        from gtts import gTTS
        import io
        tts = gTTS(text=text[:5000], lang="en", slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return f"data:audio/mpeg;base64,{base64.b64encode(buf.read()).decode()}"
    except Exception as e:
        logger.error(f"gTTS error: {e}")
        return None


# ------------------------------------------
# DEPENDENCY
# ------------------------------------------
def get_service(request: Request) -> RAGService:
    return request.app.state.rag_service


# ------------------------------------------
# UPLOAD INVOICE PDF → PINECONE
# ------------------------------------------
@router.post("/upload-invoice", response_model=UploadResponse, summary="📤 Upload Invoice PDF")
async def upload_invoice(
    file: UploadFile = File(...),
    session_id: str = Form("default"),
    service: RAGService = Depends(get_service),
):
    if not file.filename.endswith(".pdf"):
        from fastapi import HTTPException
        raise HTTPException(400, "Only PDF files are supported")

    content = await file.read()
    chunks = await service.ingest_invoice(content, file.filename, session_id)

    return UploadResponse(
        message=f"Invoice '{file.filename}' uploaded and indexed successfully",
        chunks=chunks,
    )


# ------------------------------------------
# QUERY INVOICES
# ------------------------------------------
@router.post("/invoice-query", response_model=InvoiceQueryResponse, summary="🔍 Query Invoices")
async def invoice_query(
    body: InvoiceQueryRequest,
    service: RAGService = Depends(get_service),
):
    start = time.perf_counter()

    answer, sources, provider = await service.process_question(body.question, body.session_id or "default")

    audio = None
    if body.includeAudio and body.voiceId:
        audio = await synthesize_speech(answer, body.voiceId)

    elapsed = round(time.perf_counter() - start, 3)
    logger.info(f"Invoice query answered in {elapsed}s")

    return InvoiceQueryResponse(answer=answer, sources=sources, provider=provider, audio=audio)


# ------------------------------------------
# KEEP OLD ROUTES AS ALIASES (backward compat)
# ------------------------------------------
@router.post("/upload-pdf", response_model=UploadResponse, include_in_schema=False)
async def upload_pdf_alias(file: UploadFile = File(...), service: RAGService = Depends(get_service)):
    return await upload_invoice(file, service)


@router.post("/ds-rag-agent", response_model=InvoiceQueryResponse, include_in_schema=False)
async def ds_rag_alias(body: InvoiceQueryRequest, service: RAGService = Depends(get_service)):
    return await invoice_query(body, service)
