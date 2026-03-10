import os
import asyncio
import logging
import google.generativeai as genai


class GeminiKeyRotator:
    def __init__(self, api_keys=None):
        if api_keys:
            # Use provided keys
            self.api_keys = [k for k in api_keys if k]
        else:
            # Try numbered keys first
            self.api_keys = [
                os.getenv(f"GEMINI_API_KEY_{i}")
                for i in range(1, 9)
                if os.getenv(f"GEMINI_API_KEY_{i}")
            ]
            
            # Fallback to single GEMINI_API_KEY
            if not self.api_keys:
                primary_key = os.getenv("GEMINI_API_KEY")
                if primary_key:
                    self.api_keys = [primary_key]

        if not self.api_keys:
            raise ValueError("No GEMINI_API_KEY or GEMINI_API_KEY_1 to GEMINI_API_KEY_8 found")

        self.current_index = 0
        genai.configure(api_key=self.api_keys[self.current_index])

        logging.info(f"Initialized with {len(self.api_keys)} API keys")

    async def generate_content(self, model, contents):

        max_attempts = 5
        wait_time = 2

        for attempt in range(max_attempts):
            try:

                logging.info(
                    f"Generating content with {model} (attempt {attempt+1}/{max_attempts})"
                )

                gemini_model = genai.GenerativeModel(model)
                response = await asyncio.to_thread(
                    gemini_model.generate_content,
                    contents,
                )

                return response.text

            except Exception as e:

                error_msg = str(e).lower()

                if "quota" in error_msg or "rate" in error_msg or "429" in error_msg:

                    logging.warning(
                        f"Rate limit hit. Rotating key and retrying in {wait_time}s"
                    )

                    self._rotate_key()

                    await asyncio.sleep(wait_time)

                    wait_time = min(wait_time * 2, 60)

                else:
                    logging.error(f"Gemini error: {e}")
                    raise

        raise Exception("Max retries exceeded for Gemini API")

    def _rotate_key(self):

        self.current_index = (self.current_index + 1) % len(self.api_keys)
        genai.configure(api_key=self.api_keys[self.current_index])

        logging.info(f"Rotated to API key #{self.current_index + 1}")