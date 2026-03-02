from abc import ABC, abstractmethod
from typing import Optional


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> Optional[str]:
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass
