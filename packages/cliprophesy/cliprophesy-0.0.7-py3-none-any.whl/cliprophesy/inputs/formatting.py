import shutil

from typing import List, Optional

class CommandSuggestion:
    """Represents a command suggestion with command text and explanation."""

    def __init__(self, command: str, explanation: Optional[str] = None):
        self.command = command.strip()
        self.explanation = explanation.strip() if explanation else None

    def __str__(self) -> str:
        return f"{self.command} # {self.explanation}" if self.explanation else self.command

class PrettySuggestionFormatter:
    """Formats command suggestions with pretty aligned comments."""

    @staticmethod
    def parse_suggestions(raw_suggestions: List[str]) -> List[CommandSuggestion]:
        """Parse raw suggestions into CommandSuggestion objects."""
        result = []

        for line in raw_suggestions:
            if line.startswith('Quick thoughts'):
                pass
            elif '#' in line:
                parts = line.split('#', 1)
                result.append(CommandSuggestion(parts[0], parts[1]))
            else:
                result.append(CommandSuggestion(line))

        return result

    @staticmethod
    def format_suggestions(raw_suggestions: List[str]) -> List[str]:
        suggestions = PrettySuggestionFormatter.parse_suggestions(raw_suggestions)
        """Format suggestions with aligned comments."""
        if not suggestions:
            return []

        # Find the longest command to determine alignment
        try:
            terminal_width = shutil.get_terminal_size().columns
        except:
            terminal_width = 80  # Fallback to reasonable default

        max_cmd_length = max(len(suggestion.command) for suggestion in suggestions)

        # Ensure we leave room for the comment
        max_cmd_length = min(max_cmd_length, terminal_width - 30)

        # Format each suggestion with aligned comments
        formatted = []
        for suggestion in suggestions:
            # Apply syntax highlighting to the command

            if suggestion.explanation:
                # Create padding between command and comment
                padding = ' ' * (max_cmd_length - len(suggestion.command) + 2)

                # Add comment with a different color
                comment_part = f"# {suggestion.explanation}"

                formatted_line = f"{suggestion.command}{padding}{comment_part}"

                formatted.append(formatted_line)
            else:
                formatted.append(suggestion.command)

        return formatted
