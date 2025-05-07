import os
import requests
from typing import List
from cliprophesy.llms import base

class OpenAIBackend(base.BaseBackend):
    def __init__(self, model="gpt-4o"):
        self.api_key = os.environ.get("OPENAI_API_KEY", False)
        self.model = os.environ.get("OPENAI_MODEL", model)

    def get_suggestions_internal(self, prompt:str) -> List[str]:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 250,
                "temperature": 0.7,
                "n": 1,
            },
            timeout=10
        )
        data = response.json()
        text = data["choices"][0]["message"]["content"].strip()
        return [line.strip("1234567890.:- ").strip()
                for line in text.splitlines() if line.strip()]
