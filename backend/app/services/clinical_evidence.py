import re
import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceMatch:
    canonical_flag: str
    label: str
    detected: bool
    matched_text: str | None


CHEST_PAIN_FLAG_PATTERNS: dict[str, tuple[str, list[str]]] = {
    "exertional chest pressure": (
        "dolor torácico opresivo relacionado con el esfuerzo",
        [
            r"(?:dolor|presion|opresion|molestia).{0,35}(?:esfuerzo|ejercicio)",
            r"(?:esfuerzo|ejercicio).{0,35}(?:dolor|presion|opresion|molestia)",
            r"exertional.{0,20}(?:chest )?(?:pain|pressure|discomfort)",
        ],
    ),
    "radiation to left arm": (
        "irradiación al brazo izquierdo",
        [
            r"(?:irradia|irradiado|irradiacion).{0,25}(?:brazo|miembro superior) izquierdo",
            r"radiat(?:es|ing|ion|ed).{0,25}left arm",
        ],
    ),
    "diaphoresis": (
        "diaforesis o sudoración fría",
        [r"diaforesis", r"sudoracion(?: fria| profusa)?", r"sudor frio", r"diaphoresis", r"cold sweat"],
    ),
    "cardiovascular risk factors": (
        "factores de riesgo cardiovascular",
        [
            r"factores? de riesgo cardiovascular",
            r"cardiovascular risk factors?",
            r"(?:hipertension|hta|diabetes|tabaquismo|fumador|dislipidemia|obesidad|antecedente familiar)",
            r"(?:hypertension|diabetes|smoking|smoker|dyslipidemia|obesity|family history)",
        ],
    ),
}

NEGATION_PATTERN = re.compile(r"(?:\bno\b|\bsin\b|\bniega\b|\bnegativo para\b)\s+(?:\w+\s+){0,3}$")


def normalize_clinical_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.lower())
    without_accents = "".join(character for character in decomposed if not unicodedata.combining(character))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", without_accents)).strip()


class ClinicalEvidenceMatcher:
    """Transparent bilingual matcher for rubric-aligned clinical evidence."""

    def match_red_flags(self, response_text: str, red_flags: list[str]) -> list[EvidenceMatch]:
        normalized_response = normalize_clinical_text(response_text)
        return [self._match_flag(normalized_response, flag) for flag in red_flags]

    def _match_flag(self, normalized_response: str, canonical_flag: str) -> EvidenceMatch:
        normalized_flag = normalize_clinical_text(canonical_flag)
        label, patterns = CHEST_PAIN_FLAG_PATTERNS.get(
            normalized_flag,
            (canonical_flag, [re.escape(normalized_flag)]),
        )

        for pattern in patterns:
            match = re.search(pattern, normalized_response)
            if match and not self._is_negated(normalized_response, match.start()):
                return EvidenceMatch(
                    canonical_flag=canonical_flag,
                    label=label,
                    detected=True,
                    matched_text=match.group(0),
                )

        return EvidenceMatch(
            canonical_flag=canonical_flag,
            label=label,
            detected=False,
            matched_text=None,
        )

    def _is_negated(self, normalized_response: str, match_start: int) -> bool:
        prefix = normalized_response[max(0, match_start - 45) : match_start]
        return bool(NEGATION_PATTERN.search(prefix))
