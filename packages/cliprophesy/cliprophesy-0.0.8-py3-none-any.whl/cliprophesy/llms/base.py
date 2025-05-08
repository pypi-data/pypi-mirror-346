import time
from abc import ABC, abstractmethod
from typing import List

from cliprophesy.llms import prompts

class BaseBackend:
    MODE = 'default'

    def get_suggestions(self, current_line: str, history: List[str], extended_history: List[str], stdin="", pwd="", status="", env="", test_request: bool = False, debug: bool = False) -> List[str]:
        try:
            start_time = time.perf_counter()
            if self.__class__.MODE == 'default':
                prompt = self._build_prompt(current_line, history, extended_history, stdin, pwd, status, env)
                if debug:
                    print(prompt)
                suggestions = self.get_suggestions_internal(prompt)
            else:
                suggestions = self.get_suggestions_internal_extended(current_line, history, extended_history, stdin, pwd, status, env, test_request, debug)
            if debug:
                end_time = time.perf_counter()
                print("backend call latency", end_time - start_time)
            return suggestions
        except Exception as e:
            if debug:
                print(e)
            return []

    @abstractmethod
    def get_suggestions_internal(self, prompt: str) -> List[str]:
        raise Exception("Not implemented")

    @abstractmethod
    def get_suggestions_internal_extended(self, current_line: str, history: List[str], extended_history: List[str], stdin="", pwd="", status="", env="", test_request: bool = False, debug: bool = False) -> List[str]:
        raise Exception("Not implemented")

    def _build_prompt(self, current_line: str, history, extended_history=[], stdin="", pwd="", status="", env="") -> str:
        """Build the prompt for the LLM."""
        recent_history = history[-20:] if len(history) > 20 else history
        recent_history = '\n'.join(recent_history)

        return prompts.PROMPT.format(current_line=current_line, history=recent_history, stdin=stdin, pwd=pwd, status=status, env=env)
