from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.agent import router as agent_router
from routes.crops import router as crops_router
from routes.speech_routes import router as speech_router




import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="🎙 Voice Agent Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router, prefix="/api", tags=["AI Agent"])
app.include_router(crops_router, prefix="/api", tags=["Crops"])
app.include_router(speech_router, prefix="/api", tags=["Speech Tools"])



@app.get("/")
def home():
    return {"message": "✅ Voice Agent Backend Running — ready for GPT + Voice!"}
