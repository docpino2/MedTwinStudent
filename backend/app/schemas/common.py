from enum import StrEnum


class LearningCycle(StrEnum):
    BASIC_SCIENCES = "basic_sciences"
    CLINICAL_SCIENCES = "clinical_sciences"
    INTERNSHIP = "internship"


class MasteryLevel(StrEnum):
    NOVICE = "novice"
    DEVELOPING = "developing"
    COMPETENT = "competent"
    ADVANCED = "advanced"

