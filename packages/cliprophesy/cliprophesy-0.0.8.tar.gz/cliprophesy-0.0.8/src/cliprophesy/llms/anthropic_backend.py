import os
import requests
from typing import List

from cliprophesy.llms import base

DEBUG = True

class AnthropicBackend(base.BaseBackend):
    def __init__(self, model="claude-3-haiku-20240307"):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY", False)
        self.model = os.environ.get("ANTHROPIC_MODEL", model)

    def get_suggestions_internal(self, prompt:str) -> List[str]:
        """Get command suggestions based on current line and history."""
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": self.model,
                "max_tokens": 250,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=10
        )
        data = response.json()
        text = data["content"][0]["text"].strip()
        # Parse the raw suggestions
        raw_suggestions = [line.strip("1234567890.:- ").strip()
                           for line in text.splitlines() if line.strip()]

        # Convert to CommandSuggestion objects
        return raw_suggestions
