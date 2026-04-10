import os
import base64
import time
import httpx
from typing import List, Optional, Tuple

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from pinecone import Pinecone

from utils.logger import logger


class RAGService:
    """
    LangChain-powered RAG service using Pinecone + Gemini.
    """

    def __init__(self):
        self.http_client: Optional[httpx.AsyncClient] = None
        self.qa_chain = None
        self.vectorstore = None
        self.cache = {}

    # --------------------------------------------------
    # LIFECYCLE
    # --------------------------------------------------
    async def startup(self):
        logger.info("Initializing LangChain RAG service")

        self.http_client = httpx.AsyncClient(timeout=30.0)

        api_key = os.getenv("RAG_GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        pc_api_key = os.getenv("PINECONE_API_KEY")

        if not pc_api_key:
            logger.warning("PINECONE_API_KEY not set. RAG disabled.")
            return

        try:
            # LangChain Embeddings
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                google_api_key=api_key
            )

            # LangChain Pinecone VectorStore
            self.vectorstore = PineconeVectorStore(
                index_name="ds-tutor",
                embedding=embeddings,
                pinecone_api_key=pc_api_key
            )

            # LangChain LLM
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash-lite",
                google_api_key=api_key,
                temperature=0.3
            )

            # LangChain Prompt Template
            prompt_template = PromptTemplate(
                input_variables=["context", "question"],
                template="""
You are a Data Science tutor helping students prepare for exams.

First check if the question is related to the material below.
- If YES → answer using ONLY the material with: definition, key concepts, examples, and why it matters in Data Science.
- If NO → respond exactly: "This topic is not covered in the material."

Context:
{context}

Question: {question}

Answer:"""
            )

            # LangChain RetrievalQA Chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
                chain_type_kwargs={"prompt": prompt_template},
                return_source_documents=True
            )

            logger.info("LangChain RAG service initialized successfully")

        except Exception as e:
            logger.error(f"RAG init failed: {e}")

    async def shutdown(self):
        if self.http_client:
            await self.http_client.aclose()
            logger.info("RAG HTTP client closed")

    # --------------------------------------------------
    # HEALTH CHECK
    # --------------------------------------------------
    def health_check(self) -> bool:
        return self.qa_chain is not None

    # --------------------------------------------------
    # MAIN RAG PIPELINE
    # --------------------------------------------------
    async def process_question(self, question: str) -> Tuple[str, List[str], str]:
        if question in self.cache:
            logger.info("RAG cache hit")
            return self.cache[question]

        if not self.qa_chain:
            return "RAG service is not available.", [], "none"

        try:
            import asyncio
            result = await asyncio.to_thread(self.qa_chain.invoke, {"query": question})

            answer = result.get("result", "Unable to generate response.")

            # Extract source pages from documents
            sources = []
            for doc in result.get("source_documents", []):
                page = doc.metadata.get("page")
                if isinstance(page, int):
                    sources.append(f"Page {page + 1}")
            sources = list(set(sources))

            logger.info(f"RAG answer generated | sources: {sources}")

            self.cache[question] = (answer, sources, "gemini")
            return answer, sources, "gemini"

        except Exception as e:
            logger.error(f"RAG pipeline error: {e}")
            return "Unable to generate response.", [], "none"

    # --------------------------------------------------
    # TTS
    # --------------------------------------------------
    async def synthesize_speech(self, text: str, voice_id: str = None) -> Optional[str]:
        try:
            from gtts import gTTS
            import io

            if not text:
                return None

            tts = gTTS(text=text[:5000], lang='en', slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            audio_data = audio_buffer.read()
            return f"data:audio/mpeg;base64,{base64.b64encode(audio_data).decode()}"

        except Exception as e:
            logger.error(f"TTS error: {e}")
            return None
