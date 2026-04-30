"""
LLM Handler Module
Manages all interactions with Ollama API (running locally)
"""

import requests
import json


class LLMHandler:
    """Handles communication with Ollama API"""

    def __init__(self):
        """Initialize Ollama client"""
        self.model = "orca-mini"
        self.base_url = "http://localhost:11434/api/generate"

        # Test connection
        try:
            response = requests.post(
                self.base_url,
                json={"model": self.model, "prompt": "test", "stream": False},
                timeout=180
            )
            if response.status_code != 200:
                raise Exception("Ollama server not responding. Make sure to run: ollama serve")
        except requests.exceptions.ConnectionError:
            raise Exception("❌ Ollama server is not running!\n\nPlease start it with: ollama serve")

    def ask_claude(self, prompt: str, system_prompt: str = None) -> str:
        """
        Send a prompt to Ollama and get a response

        Args:
            prompt: The user prompt
            system_prompt: Optional system context

        Returns:
            Ollama's response as a string

        Raises:
            Exception: If API call fails
        """
        try:
            # Combine system prompt with user prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            else:
                full_prompt = prompt

            response = requests.post(
                self.base_url,
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "temperature": 0.7,
                },
                timeout=180
            )

            if response.status_code != 200:
                raise Exception(f"Ollama error: {response.text}")

            result = response.json()
            return result.get("response", "").strip()

        except requests.exceptions.ConnectionError:
            raise Exception("❌ Ollama server is not running!\n\nPlease start it with: ollama serve")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")


def get_llm_handler() -> LLMHandler:
    """Factory function to get LLM handler instance"""
    return LLMHandler()
