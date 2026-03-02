from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
import time

from services.rag_service import RAGService
from utils.logger import logger

router = APIRouter()


# ------------------------------------------
# REQUEST / RESPONSE MODELS
# ------------------------------------------
class DSRagRequest(BaseModel):
    question: str


class RAGResponse(BaseModel):
    answer: str
    sources: List[str]
    provider: Optional[str] = None


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

    elapsed = round(time.perf_counter() - start, 3)
    logger.info(f"RAG response generated in {elapsed}s")

    return RAGResponse(
        answer=answer,
        sources=sources,
        provider=provider,
    )
