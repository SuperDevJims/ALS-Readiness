from enum import StrEnum


class ContentType(StrEnum):
    VIDEO = "video"
    AUDIO = "audio"
    READING = "reading"


class StimulusLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ContentStatus(StrEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class ContentProgressStatus(StrEnum):
    NOT_OPENED = "not_opened"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ContentVisibility(StrEnum):
    PRIVATE = "private"
    PUBLIC = "public"
