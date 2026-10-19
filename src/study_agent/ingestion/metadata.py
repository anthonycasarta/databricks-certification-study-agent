from datetime import UTC, datetime
from hashlib import sha256
from pathlib import PurePosixPath
from uuid import uuid4

from study_agent.ingestion.enums import DocumentFileType


def determine_file_type(file_name: str) -> DocumentFileType:
    extension = PurePosixPath(file_name).suffix.lstrip(".").lower()

    return DocumentFileType(extension)


def calculate_content_hash(content: bytes) -> str:
    hashed_content = sha256(content)

    return hashed_content.hexdigest()


def generate_document_id() -> str:
    generated_id = uuid4()
    return str(generated_id)


def extract_file_name(path: str) -> str:
    file_name = PurePosixPath(path).name
    return file_name


def generate_ingestion_timestamp() -> datetime:
    return datetime.now(UTC)
