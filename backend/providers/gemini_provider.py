import time
from typing import Optional

from providers.base_provider import BaseLLMProvider
from utils.gemini_rotator import GeminiKeyRotator
from utils.logger import logger


class GeminiProvider(BaseLLMProvider):
    def __init__(self, rotator: GeminiKeyRotator):
        self.rotator = rotator
        # FIX PROBLEM 2: Use gemini-1.5-flash-8b (higher free tier limits)
        self.model = "gemini-1.5-flash-8b"

    @property
    def provider_name(self) -> str:
        return "gemini"

    async def generate(self, prompt: str) -> Optional[str]:
        try:
            start = time.perf_counter()

            response = await self.rotator.generate_content(
                model=self.model,
                contents=prompt,
            )

            latency = round(time.perf_counter() - start, 3)
            logger.info(f"Gemini latency={latency}s")

            return response.strip() if response else None

        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return None
