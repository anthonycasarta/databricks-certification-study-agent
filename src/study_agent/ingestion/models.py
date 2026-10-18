from dataclasses import dataclass
from datetime import datetime

from study_agent.ingestion.enums import DocumentFileType, DocumentStatus


@dataclass
class DocumentMetadata:
    document_id: str
    file_name: str
    file_path: str
    file_type: DocumentFileType
    file_size_bytes: int
    content_hash: str
    ingested_at: datetime
    status: DocumentStatus
