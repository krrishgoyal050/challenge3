import httpx

from app.core.config import get_settings
from app.services.recommendations import build_sustainability_plan


class SustainabilityAssistant:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.memory: dict[int, list[str]] = {}

    async def respond(self, user_id: int, message: str, context: dict[str, object]) -> str:
        self.memory.setdefault(user_id, []).append(message)
        prompt = (
            "You are a practical carbon reduction coach. Give concise, safe, personalized advice.\n"
            f"Recent context: {context}\nUser message: {message}"
        )
        if not self.settings.gemini_api_key:
            plan = build_sustainability_plan()
            path = " -> ".join(plan["best_reduction_path"])
            return f"Based on your profile, start with quick wins and follow this reduction path: {path}. Keep actions small, measurable, and weekly."

        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-1.5-flash:generateContent?key={self.settings.gemini_api_key}"
        )
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
            response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]


assistant = SustainabilityAssistant()
