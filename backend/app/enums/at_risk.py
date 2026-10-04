from enum import StrEnum


class AtRiskReason(StrEnum):
    LOW_MPS = "low_mps"
    INACTIVE = "inactive"
    LOW_READINESS = "low_readiness"


class AtRiskFlagStatus(StrEnum):
    OPEN = "open"
    REVIEWED = "reviewed"
    DISMISSED = "dismissed"
    RESOLVED = "resolved"


# A flag still counts against the learner in these states.
ACTIVE_FLAG_STATUSES = (AtRiskFlagStatus.OPEN, AtRiskFlagStatus.REVIEWED)
