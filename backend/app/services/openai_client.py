import httpx

from app.core.config import settings


class OpenAICompatibleClient:
    """Thin adapter for OpenAI-compatible chat completion APIs."""

    def __init__(self) -> None:
        self.enabled = bool(settings.openai_api_key)

    async def chat(self, system: str, user: str) -> str | None:
        if not self.enabled:
            return None

        payload = {
            "model": settings.openai_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        }
        headers = {"Authorization": f"Bearer {settings.openai_api_key}"}

        async with httpx.AsyncClient(base_url=settings.openai_base_url, timeout=30) as client:
            response = await client.post("/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

