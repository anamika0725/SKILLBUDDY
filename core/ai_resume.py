import json
import os

from django.conf import settings

try:
    from google import genai
except ImportError:  # pragma: no cover - optional at runtime
    genai = None


def analyze_resume_with_gemini(resume_text: str, requirement_title: str, required_skills: list[str]) -> dict[str, object] | None:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or not genai or not resume_text.strip() or not required_skills:
        return None

    client = genai.Client(api_key=api_key)
    schema = {
        'type': 'object',
        'properties': {
            'summary': {
                'type': 'string',
                'description': 'Short summary of the candidate resume for this role.',
            },
            'improvement_suggestions': {
                'type': 'array',
                'items': {'type': 'string'},
                'description': 'Short concrete suggestions to improve the resume for this role.',
            },
            'matched_skills': {
                'type': 'array',
                'items': {'type': 'string'},
                'description': 'Required skills clearly present in the resume.',
            },
            'missing_skills': {
                'type': 'array',
                'items': {'type': 'string'},
                'description': 'Required skills that are missing or not clearly shown in the resume.',
            },
            'score': {
                'type': 'integer',
                'minimum': 0,
                'maximum': 100,
                'description': 'Readiness score for the role from 0 to 100.',
            },
            'is_ready': {
                'type': 'boolean',
                'description': 'Whether the candidate looks ready for this role right now.',
            },
        },
        'required': ['summary', 'improvement_suggestions', 'matched_skills', 'missing_skills', 'score', 'is_ready'],
        'additionalProperties': False,
    }
    prompt = (
        f"Analyze this resume for the role '{requirement_title}'. "
        "Use only evidence from the resume text. "
        "Do not invent skills that are not mentioned or strongly implied. "
        "Match against the required skills list and return structured JSON only.\n\n"
        f"Required skills: {', '.join(required_skills)}\n\n"
        f"Resume text:\n{resume_text[:15000]}"
    )
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_json_schema': schema,
            'temperature': 0.2,
        },
    )

    payload = json.loads(response.text)
    return {
        'summary': str(payload.get('summary', '')).strip(),
        'improvement_suggestions': _normalize_text_list(payload.get('improvement_suggestions', [])),
        'matched_skills': _normalize_skill_list(payload.get('matched_skills', []), required_skills),
        'missing_skills': _normalize_skill_list(payload.get('missing_skills', []), required_skills),
        'score': _normalize_score(payload.get('score', 0)),
        'is_ready': bool(payload.get('is_ready', False)),
    }


def _normalize_skill_list(values: object, allowed_skills: list[str]) -> list[str]:
    if not isinstance(values, list):
        return []
    allowed_lookup = {skill.lower(): skill for skill in allowed_skills}
    cleaned: list[str] = []
    for value in values:
        if not isinstance(value, str):
            continue
        match = allowed_lookup.get(value.strip().lower())
        if match and match not in cleaned:
            cleaned.append(match)
    return cleaned


def _normalize_score(value: object) -> int:
    try:
        score = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, min(score, 100))


def _normalize_text_list(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    cleaned: list[str] = []
    for value in values:
        if not isinstance(value, str):
            continue
        item = value.strip()
        if item and item not in cleaned:
            cleaned.append(item)
    return cleaned
