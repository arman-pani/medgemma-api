import httpx
import json
import time
import base64
from typing import AsyncGenerator, List, Dict, Any, Optional
from ..config import settings
from ..utils.prompts import get_system_prompt

class OllamaService:
    def __init__(self):
        self.base_url = f"{settings.OLLAMA_BASE_URL}/api/chat"
        self.timeout = httpx.Timeout(settings.REQUEST_TIMEOUT)

    async def generate_response(
        self, 
        user_prompt: str, 
        images: Optional[List[str]] = None,
        stream: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Generic generator to talk to Ollama's /api/chat endpoint.
        """
        payload = {
            "model": settings.MODEL_NAME,
            "messages": [
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": user_prompt}
            ],
            "stream": stream
        }

        if images:
            # According to Ollama API for multimodal:
            # The 'images' field should be in the message with 'user' role
            payload["messages"][1]["images"] = images

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                async with client.stream("POST", self.base_url, json=payload) as response:
                    if response.status_code != 200:
                        error_text = await response.aread()
                        yield {"error": f"Ollama error {response.status_code}: {error_text.decode()}"}
                        return

                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        chunk = json.loads(line)
                        yield chunk
            except httpx.RequestError as exc:
                yield {"error": f"Request to Ollama failed: {str(exc)}"}

    async def list_models(self) -> List[str]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{settings.OLLAMA_BASE_URL}/api/tags")
            if resp.status_code == 200:
                data = resp.json()
                return [m["name"] for m in data.get("models", [])]
            return []
