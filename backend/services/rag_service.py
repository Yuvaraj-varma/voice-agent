import os
import base64
import time
import httpx
import shutil
import chromadb
from pathlib import Path
from typing import List, Optional, Tuple

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

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
        self.vectorstore: Optional[Chroma] = None
        self.embeddings = None
        self.providers = []
        self.cache = {}
        self.max_chunks = 3
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")

    # --------------------------------------------------
    # LIFECYCLE
    # --------------------------------------------------
    async def startup(self):
        logger.info("Initializing RAG service")

        self.http_client = httpx.AsyncClient(timeout=30.0)

        # Initialize lightweight ONNX embeddings (no PyTorch!)
        logger.info("Loading ONNX embeddings (lightweight)...")
        self.embeddings = ONNXMiniLM_L6_V2()

        # Load or build vector DB
        persist_path = str(Path(os.getenv("CHROMA_PATH", "chroma_db")).resolve())
        logger.info(f"Loading Chroma DB from: {persist_path}")

        try:
            if Path(persist_path).exists():
                self.vectorstore = Chroma(
                    persist_directory=persist_path,
                    embedding_function=self.embeddings
                )
                # Test if it works
                self.vectorstore.similarity_search("test", k=1)
                logger.info("Chroma DB loaded successfully")
            else:
                raise Exception("Path not found")
        except Exception as e:
            logger.error(f"Failed to load Chroma DB: {e}. Rebuilding...")
            # Delete corrupted DB
            shutil.rmtree(persist_path, ignore_errors=True)
            self.vectorstore = await self._build_vectorstore()

        gemini_rotator = GeminiKeyRotator()

        self.providers = [
            GeminiProvider(gemini_rotator),
            DeepSeekProvider(self.http_client),
        ]

        logger.info("RAG service initialized successfully")

    async def _build_vectorstore(self) -> Optional[Chroma]:
        """Build vector store from PDF documents using ChromaDB directly"""
        try:
            pdf_path = os.getenv("PDF_PATH", "data/ds_notes")
            pdf_dir = Path(pdf_path).resolve()
            
            if not pdf_dir.exists():
                logger.error(f"PDF directory not found: {pdf_dir}")
                return None

            logger.info(f"Loading PDFs from: {pdf_dir}")
            loader = PyPDFDirectoryLoader(str(pdf_dir))
            documents = loader.load()
            
            if not documents:
                logger.error("No PDF documents found")
                return None

            logger.info(f"Loaded {len(documents)} pages from PDFs")
            
            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(documents)
            logger.info(f"Split into {len(splits)} chunks")

            # Use ChromaDB directly with ONNX embeddings
            persist_path = str(Path(os.getenv("CHROMA_PATH", "chroma_db")).resolve())
            
            # Create ChromaDB client
            client = chromadb.PersistentClient(path=persist_path)
            
            # Delete existing collection if any
            try:
                client.delete_collection(name="langchain")
            except:
                pass
            
            # Create collection with ONNX embeddings
            collection = client.create_collection(
                name="langchain",
                embedding_function=self.embeddings
            )
            
            # Add documents to collection (no embedding_function param here!)
            texts = [doc.page_content for doc in splits]
            metadatas = [doc.metadata for doc in splits]
            ids = [f"doc_{i}" for i in range(len(splits))]
            
            collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(splits)} chunks to ChromaDB")
            
            # Wrap with LangChain Chroma for similarity_search
            vectorstore = Chroma(
                client=client,
                collection_name="langchain",
                embedding_function=self.embeddings
            )
            
            logger.info(f"Vector store built and saved to: {persist_path}")
            return vectorstore
            
        except Exception as e:
            logger.error(f"Failed to build vector store: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None

    async def shutdown(self):
        if self.http_client:
            await self.http_client.aclose()
            logger.info("RAG HTTP client closed")

    # --------------------------------------------------
    # HEALTH CHECK
    # --------------------------------------------------
    def health_check(self) -> bool:
        try:
            if not self.vectorstore:
                return False
            self.vectorstore.similarity_search("health check", k=1)
            return True
        except Exception as e:
            logger.error(f"Vector DB health check failed: {e}")
            return False

    # --------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------
    async def retrieve_context(
        self, question: str
    ) -> Tuple[List[Document], str]:
        if not self.vectorstore:
            raise RuntimeError("RAGService not initialized. Call startup() first.")

        docs = self.vectorstore.similarity_search(question, k=self.max_chunks)
        logger.info(f"Retrieved {len(docs)} documents from Chroma")

        context = "\n\n".join([d.page_content for d in docs]) if docs else ""
        return docs, context

    def extract_sources(self, docs: List[Document]) -> List[str]:
        sources = []
        for d in docs:
            page = d.metadata.get("page")
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
Answer ONLY from the material.

Material:
{context}

Question: {question}
Answer:
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
    # TTS
    # --------------------------------------------------
    async def synthesize_speech(
        self, text: str, voice_id: str
    ) -> Optional[str]:
        if not self.elevenlabs_key or not text:
            return None

        res = await self.http_client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "xi-api-key": self.elevenlabs_key,
                "Content-Type": "application/json",
            },
            json={"text": text[:5000], "model_id": "eleven_turbo_v2"},
        )

        if res.status_code == 200:
            return f"data:audio/mpeg;base64,{base64.b64encode(res.content).decode()}"

        return None
