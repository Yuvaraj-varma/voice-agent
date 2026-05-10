import os
import io
import base64
import asyncio
import httpx
from typing import List, Optional, Tuple

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils.logger import logger


class RAGService:

    def __init__(self):
        self.http_client: Optional[httpx.AsyncClient] = None
        self.qa_chain = None
        self.vectorstore = None
        self.embeddings = None
        self.cache = {}

    # --------------------------------------------------
    # LIFECYCLE
    # --------------------------------------------------
    async def startup(self):
        logger.info("Initializing Invoice RAG service")

        self.http_client = httpx.AsyncClient(timeout=30.0)

        api_key = os.getenv("RAG_GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        pc_api_key = os.getenv("PINECONE_API_KEY")

        if not pc_api_key:
            logger.warning("PINECONE_API_KEY not set. RAG disabled.")
            return

        try:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/gemini-embedding-001",
                google_api_key=api_key,
            )

            self.vectorstore = PineconeVectorStore(
                index_name="invoice-system",
                embedding=self.embeddings,
                pinecone_api_key=pc_api_key,
            )

            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash-lite",
                google_api_key=api_key,
                temperature=0.2,
            )

            prompt = PromptTemplate(
                input_variables=["context", "question"],
                template="""You are an intelligent invoice assistant. Use the invoice data below to answer the question accurately.

If the answer is in the context, provide: invoice number, vendor, date, amount, and any relevant details.
If the question requires calculation (totals, averages, differences, percentages), perform the calculation using the data in the context and provide the final result.
If the question is hypothetical (e.g. 'what if GST was X%'), use the data from context and perform the hypothetical calculation.
If the answer is NOT in the context, respond: "This information is not found in the uploaded invoices."

Invoice Data:
{context}

Question: {question}

Answer:""",
            )

            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 4}),
                chain_type_kwargs={"prompt": prompt},
                return_source_documents=True,
            )

            logger.info("Invoice RAG service initialized successfully")

        except Exception as e:
            logger.error(f"RAG init failed: {e}")

    async def shutdown(self):
        if self.http_client:
            await self.http_client.aclose()

    # --------------------------------------------------
    # HEALTH
    # --------------------------------------------------
    def health_check(self) -> bool:
        return self.qa_chain is not None

    # --------------------------------------------------
    # INGEST INVOICE PDF → PINECONE
    # --------------------------------------------------
    async def ingest_invoice(self, pdf_bytes: bytes, filename: str, session_id: str = "default") -> int:
        if not self.vectorstore or not self.embeddings:
            logger.error("Vectorstore not initialized")
            return 0

        try:
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(pdf_bytes))
            full_text = "\n".join(
                page.extract_text() or "" for page in reader.pages
            )

            splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
            chunks = splitter.create_documents(
                [full_text],
                metadatas=[{"source": filename, "type": "invoice", "session_id": session_id}],
            )

            await asyncio.to_thread(self.vectorstore.add_documents, chunks, namespace=session_id)

            self.cache.pop(session_id, None)

            logger.info(f"Ingested {len(chunks)} chunks from {filename} in namespace {session_id}")
            return len(chunks)

        except Exception as e:
            logger.error(f"Invoice ingestion failed: {e}")
            return 0

    # --------------------------------------------------
    # QUERY
    # --------------------------------------------------
    async def process_question(self, question: str, session_id: str = "default") -> Tuple[str, List[str], str]:
        cache_key = f"{session_id}:{question}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        if not self.qa_chain:
            return "Invoice RAG service is not available.", [], "none"

        try:
            retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": 4, "namespace": session_id}
            )

            from langchain.chains import RetrievalQA
            qa = RetrievalQA.from_chain_type(
                llm=self.qa_chain.combine_documents_chain.llm_chain.llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": self.qa_chain.combine_documents_chain.llm_chain.prompt},
                return_source_documents=True,
            )

            result = await asyncio.to_thread(qa.invoke, {"query": question})

            answer = result.get("result", "Unable to generate response.")
            sources = list({
                doc.metadata.get("source", "Invoice")
                for doc in result.get("source_documents", [])
            })

            self.cache[cache_key] = (answer, sources, "gemini")
            return answer, sources, "gemini"

        except Exception as e:
            logger.error(f"RAG query error: {e}")
            return "Unable to generate response.", [], "none"
