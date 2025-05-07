import requests

from typing import List

REMOTE_URL = "https://www.shbuddy.com/v1/completion"

class CLIBuddyInterface:
    def __init__(self, url, allow_stdin=False):
        self._url = REMOTE_URL
        self._allow_stdin = allow_stdin

    def get_suggestions(self, prompt: str, current_line: str, history: List[str], extended_history: List[str]=[], stdin="", pwd="", debug: bool = Fbalse) -> List[str]:
        if not self._allow_stdin:
            stdin = ''
        data = {
            "history": history,
            "enriched_history": [],
            "stdin": str(stdin),
            "pwd": pwd,
            "buffer": current_line,
            "test_request": debug
        }
        response = requests.post(self._url, json=data, timeout=10)
        data = response.json()
        return data['completions']
