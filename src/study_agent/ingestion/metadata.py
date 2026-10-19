from hashlib import sha256
from pathlib import Path

from study_agent.ingestion.enums import DocumentFileType


def determine_file_type(file_name: str) -> DocumentFileType:
    extension = Path(file_name).suffix.lstrip(".").lower()

    return DocumentFileType(extension)


def calculate_content_hash(content: bytes) -> str:
    hashed_content = sha256(content)

    return hashed_content.hexdigest()
