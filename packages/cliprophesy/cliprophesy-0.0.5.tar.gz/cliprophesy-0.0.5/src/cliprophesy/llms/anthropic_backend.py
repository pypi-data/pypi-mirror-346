# after pip install alembic

import os
import requests
import time

from typing import List

from cliprophesy.llms import prompts

DEBUG = True

class AnthropicBackend:
    """LLM backend using Anthropic's Claude models."""

    def __init__(self, model="claude-3-haiku-20240307"):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.model = os.environ.get("ANTHROPIC_MODEL", model)

    def get_suggestions(self, current_line: str, history: List[str], extended_history: List[str], stdin="", pwd="", status="", env="", test_request: bool = False, debug: bool = False) -> List[str]:
        """Get command suggestions based on current line and history."""
        prompt = self._build_prompt(current_line, history, extended_history, stdin, pwd, status, env)

        if debug:
            print(prompt)
        try:
            start_time = time.perf_counter()
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
            end_time = time.perf_counter()
            latency = end_time - start_time
            print(f"Latency: {latency:.6f} seconds")
            data = response.json()
            text = data["content"][0]["text"].strip()
            # Parse the raw suggestions
            raw_suggestions = [line.strip("1234567890.:- ").strip()
                             for line in text.splitlines() if line.strip()]

            # Convert to CommandSuggestion objects
            return raw_suggestions

        except Exception as e:
            if DEBUG:
                print(e)
            return []

    def _build_prompt(self, current_line: str, history, extended_history=[], stdin="", pwd="", status="", env="") -> str:
        """Build the prompt for the LLM."""
        recent_history = history[-20:] if len(history) > 20 else history
        recent_history = '\n'.join(recent_history)

        return prompts.PROMPT.format(current_line=current_line, history=recent_history, stdin=stdin, pwd=pwd, status=status, env=env)
