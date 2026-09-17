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
    PENDING = "pending"    
    ACTIVE = "active"     
    INACTIVE = "inactive"  
    REJECTED = "rejected" 
