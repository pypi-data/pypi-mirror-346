import codecs
import os
import platform


class BaseShellReader:
    def _get_last_status(self):
        pass

    def _get_pwd(self):
        pass

    def _read_history(self, limit:int = 400):
        pass

    def _get_env_context(self) -> str:
        pass

    def get_context(self):
        return {
            'status': self._get_last_status(),
            'history': self._read_history(),
            'env': self._get_env_context(),
            'pwd': self._get_pwd(),
            'extended_history': {},
            'stdin': {}
        }

class FishShellReader(BaseShellReader):
    def _get_last_status(self):
        return os.environ.get("status")

    def _get_pwd(self):
        return os.environ.get("PWD") or ""

    def _read_history(self, limit:int = 400):
        hist_name = os.environ.get("fish_history", "fish")
        history_file = os.path.expanduser(f"~/.local/share/fish/{hist_name}_history")
        lines = []

        try:
            with open(history_file, 'r') as f:
                for line in f:
                    if line.strip().startswith("- cmd: "):
                        lines.append(line.strip()[7:])
        except Exception as e:
            pass  # Fallback gracefully
        return lines[-limit:]  # Return only the most recent commands

    def _get_env_context(self) -> str:
        os_name = platform.platform(aliased=True)
        # Note shell is just the default of what the user did
        shell = 'fish' #os.environ.get("SHELL") or os.environ.get("COMSPEC")
        return f"OS: {os_name}\nSHELL: {shell}" if shell else f"OS: {os_name}"
