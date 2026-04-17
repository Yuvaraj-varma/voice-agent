import asyncio
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from pydantic import BaseModel
import httpx
import tempfile
import base64
import os
from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path
import google.generativeai as genai

from utils.logger import logger

router = APIRouter(tags=["🤖 Voice Agent"])

# --------------------------------------------
# MODELS
# --------------------------------------------

class TextAgentRequest(BaseModel):
    text: str
    voiceId: str = "21m00Tcm4TlvDq8ikWAM"


class AgentResponse(BaseModel):
    userText: str
    text: str
    audio: Optional[str] = None


# --------------------------------------------
# BASE AGENT
# --------------------------------------------

class BaseVoiceAgent(ABC):
    @abstractmethod
    async def transcribe(self, audio_path: str) -> str:
        pass

    @abstractmethod
    async def generate_response(self, text: str) -> str:
        pass

    @abstractmethod
    async def synthesize_speech(self, text: str, voice_id: str) -> Optional[str]:
        pass


# --------------------------------------------
# GEMINI VOICE AGENT
# --------------------------------------------

class GeminiVoiceAgent(BaseVoiceAgent):
    def __init__(self, http_client: httpx.AsyncClient):
        # Use ONLY the dedicated Voice Agent Gemini key
        voice_agent_key = os.getenv("VOICE_AGENT_GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=voice_agent_key)
        self.http = http_client

    def get_elevenlabs_key(self):
        return os.getenv("ELEVENLABS_API_KEY")

    async def transcribe(self, audio_path: str) -> str:
        try:
            with open(audio_path, "rb") as f:
                audio = f.read()

            if len(audio) < 1024:
                return ""

            audio_b64 = base64.b64encode(audio).decode()

            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            response = await asyncio.to_thread(model.generate_content, [
                "Transcribe this audio accurately. Output ONLY the text:",
                {"mime_type": "audio/webm", "data": audio_b64},
            ])

            return response.text.strip() if response.text else ""

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return ""

    async def generate_response(self, text: str) -> str:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain.agents import AgentExecutor, create_tool_calling_agent
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_core.tools import tool

            @tool
            def web_search(query: str) -> str:
                """Search the web for real-time information, latest news, current events, prices."""
                try:
                    from ddgs import DDGS
                    results = DDGS().text(query, max_results=3)
                    if not results:
                        return "No results found."
                    return "\n".join([f"{r['title']}: {r['body']}" for r in results])
                except Exception as e:
                    return f"Search failed: {e}"

            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=os.getenv("VOICE_AGENT_GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY"),
                temperature=0.3
            )

            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful voice assistant. Answer briefly and clearly. Use web_search tool for real-time info like news, weather, prices, current events."),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ])

            agent = create_tool_calling_agent(llm, [web_search], prompt)
            executor = AgentExecutor(agent=agent, tools=[web_search], verbose=True, max_iterations=3)
            result = await asyncio.to_thread(executor.invoke, {"input": text})
            logger.info(f"Agent result: {result}")
            return result.get("output", "I couldn't process that.")

        except Exception as e:
            logger.error(f"Response generation error: {e}")
            return "I encountered an error."

    async def synthesize_speech(self, text: str, voice_id: str) -> Optional[str]:
        if not text:
            return None

        # Try ElevenLabs first
        elevenlabs_key = self.get_elevenlabs_key()
        if elevenlabs_key:
            try:
                res = await self.http.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                    headers={"xi-api-key": elevenlabs_key, "Content-Type": "application/json"},
                    json={"text": text[:5000], "model_id": "eleven_turbo_v2"},
                )
                if res.status_code == 200:
                    audio_b64 = base64.b64encode(res.content).decode()
                    return f"data:audio/mpeg;base64,{audio_b64}"
                logger.error(f"ElevenLabs error {res.status_code}, falling back to gTTS")
            except Exception as e:
                logger.error(f"ElevenLabs failed: {e}, falling back to gTTS")

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


# --------------------------------------------
# ORCHESTRATOR
# --------------------------------------------

class VoiceAgentOrchestrator:
    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=30.0)
        self.agent = GeminiVoiceAgent(self.http_client)
        self.max_file_size = 50 * 1024 * 1024

    async def process_voice(self, file: UploadFile, voice_id: str) -> AgentResponse:
        tmp_path = None

        try:
            if not file.content_type.startswith("audio/"):
                raise HTTPException(400, "Invalid audio file")

            ext = Path(file.filename).suffix.lower()
            if ext not in {".webm", ".wav", ".mp3"}:
                raise HTTPException(400, "Unsupported audio format")

            content = await file.read()
            if len(content) > self.max_file_size:
                raise HTTPException(413, "File too large")

            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            user_text = await self.agent.transcribe(tmp_path)
            if not user_text:
                raise HTTPException(400, "No speech detected")

            ai_text = await self.agent.generate_response(user_text)
            audio = await self.agent.synthesize_speech(ai_text, voice_id)

            return AgentResponse(
                userText=user_text,
                text=ai_text,
                audio=audio,
            )

        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    async def process_text(self, text: str, voice_id: str) -> AgentResponse:
        if not text.strip():
            raise HTTPException(400, "Text is empty")

        text = text.strip()[:1000]

        ai_text = await self.agent.generate_response(text)
        audio = await self.agent.synthesize_speech(ai_text, voice_id)

        return AgentResponse(
            userText=text,
            text=ai_text,
            audio=audio,
        )


# --------------------------------------------
# DEPENDENCY
# --------------------------------------------

_orchestrator: Optional[VoiceAgentOrchestrator] = None


def get_orchestrator():
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = VoiceAgentOrchestrator()
    return _orchestrator


# --------------------------------------------
# ENDPOINTS
# --------------------------------------------

@router.post("/voice-agent", response_model=AgentResponse, summary="🎤 Speak to AI agent", description="Upload voice recording → Gemini transcribes + responds → ElevenLabs speaks back")
async def voice_agent(
    file: UploadFile = File(...),
    voiceId: str = Form("21m00Tcm4TlvDq8ikWAM"),
    orchestrator: VoiceAgentOrchestrator = Depends(get_orchestrator),
):
    return await orchestrator.process_voice(file, voiceId)


@router.post("/text-agent", response_model=AgentResponse, summary="⌨️ Type to AI agent", description="Type your question → Gemini responds → ElevenLabs speaks back")
async def text_agent(
    request: TextAgentRequest,
    orchestrator: VoiceAgentOrchestrator = Depends(get_orchestrator),
):
    return await orchestrator.process_text(request.text, request.voiceId)


@router.get("/voice-agent-health", summary="✅ Voice agent health check")
async def voice_agent_health():
    return {
        "status": "ok",
        "gemini": "ready",
        "elevenlabs": "configured" if os.getenv("ELEVENLABS_API_KEY") else "missing",
    }
