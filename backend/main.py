from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from routes.ds_rag_agent import router as ds_rag_router
from routes.text_speech_routes import router as text_speech_router
from routes.voice_transform import router as voice_transform_router
from routes.voice_agent import router as voice_agent_router

from utils.logger import setup_logging, logger
from dotenv import load_dotenv
from pathlib import Path

from exceptions.base import AppException
from exceptions.handlers import app_exception_handler
from middleware.request_id import RequestIDMiddleware
from services.rag_service import RAGService

import logging
import warnings

# ENV
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# LOGGING
setup_logging()

logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("transformers").setLevel(logging.WARNING)
logging.getLogger("chromadb").setLevel(logging.WARNING)

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Voice Agent Backend",
    version="1.0.0",
)

# -----------------------------------------------------
# LIFECYCLE (IMPORTANT)
# -----------------------------------------------------
@app.on_event("startup")
async def startup():
    logger.info("Starting backend services...")

    app.state.rag_service = RAGService()
    await app.state.rag_service.startup()

    logger.info("All services ready")


@app.on_event("shutdown")
async def shutdown():
    if hasattr(app.state, "rag_service"):
        await app.state.rag_service.shutdown()
        logger.info("RAG service shutdown complete")


# MIDDLEWARE
app.add_middleware(RequestIDMiddleware)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # Allow all hosts for deployment
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",  # Vercel frontend
        "https://*.onrender.com",  # Render backend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ROUTES
app.include_router(ds_rag_router, prefix="/api")
app.include_router(text_speech_router, prefix="/api")
app.include_router(voice_transform_router, prefix="/api")
app.include_router(voice_agent_router, prefix="/api")

@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    return {"status": "healthy"}

@app.get("/health")
async def health():
    rag_ok = app.state.rag_service.health_check()
    return {"status": "ok", "vector_db": rag_ok}
