from enum import StrEnum, auto


class DocumentStatus(StrEnum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()


class DocumentFileType(StrEnum):
    PDF = auto()
    MARKDOWN = "md"
