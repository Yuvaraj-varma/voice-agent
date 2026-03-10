import os
import time
from typing import Optional
import google.generativeai as genai

from providers.base_provider import BaseLLMProvider
from utils.logger import logger


class GeminiProvider(BaseLLMProvider):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = "gemini-2.5-flash"

    @property
    def provider_name(self) -> str:
        return "gemini"

    async def generate(self, prompt: str) -> Optional[str]:
        try:
            start = time.perf_counter()

            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)

            latency = round(time.perf_counter() - start, 3)
            logger.info(f"Gemini latency={latency}s")

            return response.text.strip() if response.text else None

        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return None
