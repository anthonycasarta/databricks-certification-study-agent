from datetime import UTC, datetime

from study_agent.ingestion.enums import DocumentFileType, DocumentStatus
from study_agent.ingestion.models import DocumentMetadata


def test_document_metadata() -> None:
    ingestion_time = datetime.now(UTC)

    document = DocumentMetadata(
        document_id="doc_000",
        file_name="test_doc",
        file_path="Volumes/study_agent/bronze/source_documents/test_doc.pdf",
        file_size_bytes=1024,
        file_type=DocumentFileType.PDF,
        content_hash="1234",
        ingested_at=ingestion_time,
        status=DocumentStatus.PENDING,
    )

    assert document.document_id == "doc_000"
    assert document.file_name == "test_doc"
    assert (
        document.file_path == "Volumes/study_agent/bronze/source_documents/test_doc.pdf"
    )
    assert document.file_size_bytes == 1024
    assert document.file_type == DocumentFileType.PDF
    assert document.content_hash == "1234"
    assert document.ingested_at == ingestion_time
    assert document.ingested_at.tzinfo == UTC
    assert document.status == DocumentStatus.PENDING
