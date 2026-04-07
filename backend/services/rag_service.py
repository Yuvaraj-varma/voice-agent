import os
import base64
import time
import httpx
from typing import List, Optional, Tuple
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai

from utils.gemini_rotator import GeminiKeyRotator
from utils.logger import logger

from providers.gemini_provider import GeminiProvider
from providers.deepseek_provider import DeepSeekProvider


class RAGService:
    """
    Lifecycle-managed RAG service.
    Created once at FastAPI startup.
    """

    def __init__(self):
        self.http_client: Optional[httpx.AsyncClient] = None
        self.pc_index = None
        self.embeddings = None
        self.providers = []
        self.cache = {}
        self.max_chunks = 3

    # --------------------------------------------------
    # LIFECYCLE
    # --------------------------------------------------
    async def startup(self):
        logger.info("Initializing RAG service (Pinecone)")

        self.http_client = httpx.AsyncClient(timeout=30.0)
        self.embedding_model = None

        rag_gemini_key = os.getenv("RAG_GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=rag_gemini_key)

        pc_api_key = os.getenv("PINECONE_API_KEY")
        if pc_api_key:
            try:
                pc = Pinecone(api_key=pc_api_key)
                index_name = "ds-tutor"
                if index_name not in pc.list_indexes().names():
                    logger.warning(f"Pinecone index '{index_name}' not found. Create it manually.")
                else:
                    self.pc_index = pc.Index(index_name)
                    logger.info("Pinecone connected successfully")
            except Exception as e:
                logger.error(f"Pinecone init failed: {e}")
        else:
            logger.warning("PINECONE_API_KEY not set. RAG disabled.")

        self.providers = [
            GeminiProvider(rag_gemini_key),
        ]

        logger.info("RAG service initialized")

    def _encode(self, text: str) -> list:
        try:
            from google import genai as google_genai
            client = google_genai.Client(api_key=os.getenv("RAG_GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY"))
            result = client.models.embed_content(
                model="gemini-embedding-001",
                contents=text
            )
            return result.embeddings[0].values
        except Exception as e:
            logger.error(f"Encoding error: {e}")
            return []



    async def shutdown(self):
        if self.http_client:
            await self.http_client.aclose()
            logger.info("RAG HTTP client closed")

    # --------------------------------------------------
    # HEALTH CHECK
    # --------------------------------------------------
    def health_check(self) -> bool:
        return self.pc_index is not None

    # --------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------
    async def retrieve_context(
        self, question: str
    ) -> Tuple[List[dict], str]:
        if not self.pc_index:
            return [], ""

        try:
            embedding = self._encode(question)
            if not embedding:
                return [], ""
            
            results = self.pc_index.query(
                vector=embedding,
                top_k=self.max_chunks,
                include_metadata=True
            )
            
            docs = []
            for match in results.matches:
                docs.append({
                    "content": match.metadata.get("text", ""),
                    "page": match.metadata.get("page", 0)
                })
            
            context = "\n\n".join([d["content"] for d in docs])
            logger.info(f"Retrieved {len(docs)} docs from Pinecone")
            return docs, context
            
        except Exception as e:
            logger.error(f"Retrieval error: {e}")
            return [], ""

    def extract_sources(self, docs: List[dict]) -> List[str]:
        sources = []
        for d in docs:
            page = d.get("page")
            if isinstance(page, int):
                sources.append(f"Page {page + 1}")
        return list(set(sources))

    # --------------------------------------------------
    # GENERATION
    # --------------------------------------------------
    async def generate_answer(
        self, question: str, context: str
    ) -> Tuple[str, str]:
        if not context:
            return "This topic is not covered in the material.", "none"

        prompt = f"""
You are a Data Science tutor helping students prepare for exams.

Using ONLY the material below, provide a comprehensive explanation that includes:
1. Clear definition
2. Key concepts and types
3. Important examples
4. Why it matters in Data Science

Write in a way that helps students understand deeply for their exams.

Material:
{context}

Question: {question}

Detailed Answer:
"""

        for provider in self.providers:
            start = time.perf_counter()

            result = await provider.generate(prompt)

            latency = round(time.perf_counter() - start, 3)
            logger.info(
                f"provider={provider.provider_name} latency={latency}s"
            )

            if result:
                return result, provider.provider_name

        return "Unable to generate response.", "none"

    # --------------------------------------------------
    # MAIN RAG PIPELINE
    # --------------------------------------------------
    async def process_question(self, question: str):
        if question in self.cache:
            logger.info("RAG cache hit")
            return self.cache[question]

        docs, context = await self.retrieve_context(question)
        answer, provider = await self.generate_answer(question, context)

        result = (answer, self.extract_sources(docs), provider)
        self.cache[question] = result

        return result

    # --------------------------------------------------
    # TTS - FIX PROBLEM 3: Use gTTS (free, works on server IPs)
    # --------------------------------------------------
    async def synthesize_speech(
        self, text: str, voice_id: str = None
    ) -> Optional[str]:
        try:
            from gtts import gTTS
            import io
            
            if not text:
                return None
            
            # Generate speech with gTTS
            tts = gTTS(text=text[:5000], lang='en', slow=False)
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Return base64 encoded audio
            audio_data = audio_buffer.read()
            return f"data:audio/mpeg;base64,{base64.b64encode(audio_data).decode()}"
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return None
