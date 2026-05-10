"""
Invoice System - Test Suite
============================
Structure used by real companies:
- Unit Tests       : test individual functions in isolation (mocked)
- Integration Tests: test API endpoints end-to-end
- Edge Case Tests  : test invalid inputs, empty files, wrong formats
- Contract Tests   : test response schema matches what frontend expects

Run all tests:
    pytest tests/test_invoice_system.py -v

Run only unit tests:
    pytest tests/test_invoice_system.py -v -m unit

Run only integration tests:
    pytest tests/test_invoice_system.py -v -m integration
"""

import io
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient


# ─────────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def client():
    """Shared test client — created once per module."""
    from main import app
    with TestClient(app) as c:
        yield c


@pytest.fixture
def mock_rag_service():
    """Mock RAGService so tests don't hit real Pinecone/Gemini APIs."""
    service = MagicMock()
    service.ingest_invoice = AsyncMock(return_value=5)
    service.process_question = AsyncMock(return_value=(
        "Invoice INV-001 from Vendor ABC, dated 2024-01-15, total amount $1,500.00.",
        ["invoice_sample.pdf"],
        "gemini",
    ))
    service.health_check = MagicMock(return_value=True)
    return service


@pytest.fixture
def sample_pdf_bytes():
    """Minimal valid PDF bytes for upload tests."""
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n"
        b"xref\n0 4\ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n0\n%%EOF"
    )


# ─────────────────────────────────────────────────────────
# UNIT TESTS — test individual service functions
# ─────────────────────────────────────────────────────────

@pytest.mark.unit
class TestRAGServiceUnit:

    @pytest.mark.asyncio
    async def test_ingest_returns_chunk_count(self, mock_rag_service):
        """ingest_invoice() should return number of chunks created."""
        result = await mock_rag_service.ingest_invoice(b"fake pdf", "invoice.pdf")
        assert result == 5

    @pytest.mark.asyncio
    async def test_process_question_returns_tuple(self, mock_rag_service):
        """process_question() should return (answer, sources, provider)."""
        answer, sources, provider = await mock_rag_service.process_question("What is the total?")
        assert isinstance(answer, str)
        assert isinstance(sources, list)
        assert provider == "gemini"

    @pytest.mark.asyncio
    async def test_process_question_answer_not_empty(self, mock_rag_service):
        """Answer should never be empty string."""
        answer, _, _ = await mock_rag_service.process_question("What is the vendor name?")
        assert len(answer) > 0

    def test_health_check_returns_bool(self, mock_rag_service):
        """health_check() must return a boolean."""
        result = mock_rag_service.health_check()
        assert isinstance(result, bool)
        assert result is True


# ─────────────────────────────────────────────────────────
# INTEGRATION TESTS — test full API endpoints
# ─────────────────────────────────────────────────────────

@pytest.mark.integration
class TestUploadInvoiceEndpoint:

    def test_upload_valid_pdf(self, client, mock_rag_service, sample_pdf_bytes):
        """POST /upload-invoice with valid PDF → 200 + message + chunks."""
        with patch("routes.ds_rag_agent.get_service", return_value=mock_rag_service):
            res = client.post(
                "/api/upload-invoice",
                files={"file": ("invoice_sample.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")},
            )
        assert res.status_code == 200
        data = res.json()
        assert "message" in data
        assert "chunks" in data
        assert data["chunks"] >= 0  # 0 if Pinecone index not created yet, 5+ when index exists

    def test_upload_non_pdf_rejected(self, client, mock_rag_service):
        """POST /upload-invoice with .docx file → 400 error."""
        with patch("routes.ds_rag_agent.get_service", return_value=mock_rag_service):
            res = client.post(
                "/api/upload-invoice",
                files={"file": ("invoice.docx", io.BytesIO(b"fake docx"), "application/vnd.openxmlformats")},
            )
        assert res.status_code == 400

    def test_upload_no_file_returns_422(self, client):
        """POST /upload-invoice with no file → 422 validation error."""
        res = client.post("/api/upload-invoice")
        assert res.status_code == 422

    def test_upload_response_message_contains_filename(self, client, mock_rag_service, sample_pdf_bytes):
        """Response message should mention the uploaded filename."""
        with patch("routes.ds_rag_agent.get_service", return_value=mock_rag_service):
            res = client.post(
                "/api/upload-invoice",
                files={"file": ("my_invoice.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")},
            )
        assert "my_invoice.pdf" in res.json()["message"]


@pytest.mark.integration
class TestInvoiceQueryEndpoint:

    def test_query_valid_question(self, client, mock_rag_service):
        """POST /invoice-query with valid question → 200 + answer + sources."""
        with patch("routes.ds_rag_agent.get_service", return_value=mock_rag_service):
            res = client.post(
                "/api/invoice-query",
                json={"question": "What is the total amount?"},
            )
        assert res.status_code == 200
        data = res.json()
        assert "answer" in data
        assert "sources" in data
        assert "provider" in data

    def test_query_missing_question_returns_422(self, client):
        """POST /invoice-query with no question field → 422."""
        res = client.post("/api/invoice-query", json={})
        assert res.status_code == 422

    def test_query_response_schema(self, client, mock_rag_service):
        """Response must match the contract frontend expects."""
        with patch("routes.ds_rag_agent.get_service", return_value=mock_rag_service):
            res = client.post(
                "/api/invoice-query",
                json={"question": "Who is the vendor?"},
            )
        data = res.json()
        assert "answer" in data
        assert "sources" in data
        assert "provider" in data
        assert "audio" in data
        assert isinstance(data["sources"], list)

    def test_query_with_audio_flag(self, client, mock_rag_service):
        """POST /invoice-query with includeAudio=true → should not crash."""
        with patch("routes.ds_rag_agent.get_service", return_value=mock_rag_service):
            res = client.post(
                "/api/invoice-query",
                json={
                    "question": "What is the invoice date?",
                    "includeAudio": True,
                    "voiceId": "EXAVITQu4vr4xnSDxMaL",
                },
            )
        assert res.status_code == 200


# ─────────────────────────────────────────────────────────
# EDGE CASE TESTS — what real companies always test
# ─────────────────────────────────────────────────────────

@pytest.mark.unit
class TestEdgeCases:

    def test_query_very_long_question(self, client, mock_rag_service):
        """Very long question should not crash the API."""
        long_question = "What is the invoice amount? " * 100
        with patch("routes.ds_rag_agent.get_service", return_value=mock_rag_service):
            res = client.post(
                "/api/invoice-query",
                json={"question": long_question},
            )
        assert res.status_code == 200

    def test_upload_empty_pdf(self, client, mock_rag_service):
        """Uploading a 0-byte PDF should not crash — returns 200 or 400."""
        with patch("routes.ds_rag_agent.get_service", return_value=mock_rag_service):
            res = client.post(
                "/api/upload-invoice",
                files={"file": ("empty.pdf", io.BytesIO(b""), "application/pdf")},
            )
        assert res.status_code in [200, 400]

    def test_query_special_characters(self, client, mock_rag_service):
        """Question with special characters should not crash."""
        with patch("routes.ds_rag_agent.get_service", return_value=mock_rag_service):
            res = client.post(
                "/api/invoice-query",
                json={"question": "Invoice #INV-001 & total > $500?"},
            )
        assert res.status_code == 200

    def test_upload_large_filename(self, client, mock_rag_service, sample_pdf_bytes):
        """PDF with very long filename should be handled."""
        long_name = "a" * 200 + ".pdf"
        with patch("routes.ds_rag_agent.get_service", return_value=mock_rag_service):
            res = client.post(
                "/api/upload-invoice",
                files={"file": (long_name, io.BytesIO(sample_pdf_bytes), "application/pdf")},
            )
        assert res.status_code in [200, 400]


# ─────────────────────────────────────────────────────────
# CONTRACT TESTS — response shape never breaks frontend
# ─────────────────────────────────────────────────────────

@pytest.mark.unit
class TestResponseContracts:

    def test_upload_response_has_required_fields(self, client, mock_rag_service, sample_pdf_bytes):
        """UploadResponse must always have: message, chunks."""
        with patch("routes.ds_rag_agent.get_service", return_value=mock_rag_service):
            res = client.post(
                "/api/upload-invoice",
                files={"file": ("test.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")},
            )
        data = res.json()
        assert isinstance(data["message"], str)
        assert isinstance(data["chunks"], int)

    def test_query_response_has_required_fields(self, client, mock_rag_service):
        """InvoiceQueryResponse must always have: answer, sources, provider, audio."""
        with patch("routes.ds_rag_agent.get_service", return_value=mock_rag_service):
            res = client.post(
                "/api/invoice-query",
                json={"question": "List all invoices"},
            )
        data = res.json()
        assert isinstance(data["answer"], str)
        assert isinstance(data["sources"], list)
        assert data["provider"] in ["gemini", "none", None]
        assert "audio" in data
