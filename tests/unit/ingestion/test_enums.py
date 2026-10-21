from study_agent.ingestion.enums import DocumentFileType, DocumentStatus


def test_document_status() -> None:
    assert DocumentStatus.PROCESSING.value == "processing"
    assert DocumentStatus.PENDING.value == "pending"
    assert DocumentStatus.COMPLETED.value == "completed"
    assert DocumentStatus.FAILED.value == "failed"


def test_document_file_type() -> None:
    assert DocumentFileType.PDF.value == "pdf"
    assert DocumentFileType.MARKDOWN.value == "md"
