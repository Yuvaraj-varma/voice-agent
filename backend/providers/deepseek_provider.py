import os
from typing import Optional
import httpx

from providers.base_provider import BaseLLMProvider
from utils.logger import logger


class DeepSeekProvider(BaseLLMProvider):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.model = "deepseek-chat"

    @property
    def provider_name(self) -> str:
        return "deepseek"

    async def generate(self, prompt: str) -> Optional[str]:
        if not self.api_key:
            return None

        try:
            res = await self.client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 500,
                },
            )

            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"].strip()

        except Exception as e:
            logger.error(f"DeepSeek error: {e}")

        return None
