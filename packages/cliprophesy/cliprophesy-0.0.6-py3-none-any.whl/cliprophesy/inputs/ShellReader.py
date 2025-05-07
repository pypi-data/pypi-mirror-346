import platform
import os
import time

class BaseShellReader:

    def _get_last_status(self):
        pass

    def _get_pwd(self):
        return ""

    def _read_history(self, limit:int = 400):
        return ""

    def _get_env_context(self) -> str:
        return ""

    def _get_extended_stdin(self) -> str:
        return ""

    def get_context(self):
        return {
            'status': self._get_last_status(),
            'history': self._read_history(),
            'env': self._get_env_context(),
            'pwd': self._get_pwd(),
            'extended_history': {},
            'stdin': self._get_extended_stdin()
        }

class ZshShellReader(BaseShellReader):
    def _get_last_status(self):
        return os.environ.get("exit_status") or -1

    def _get_pwd(self):
        return os.environ.get("PWD") or ""

    def _read_history(self, limit:int = 20):
        user = os.environ.get("USER")
        history_file = os.environ.get("HISTFILE", f"/home/{user}/.zzh_history")
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
        shell = 'zsh' # os.environ.get("SHELL") or os.environ.get("COMSPEC")
        return f"OS: {os_name}\nSHELL: {shell}" if shell else f"OS: {os_name}"

    def _get_extended_stdin(self) -> str:
        return ''

class FishShellReader(BaseShellReader):
    def _get_last_status(self):
        return os.environ.get("exit_status") or -1

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
        shell = 'fish' # os.environ.get("SHELL") or os.environ.get("COMSPEC")
        return f"OS: {os_name}\nSHELL: {shell}" if shell else f"OS: {os_name}"

    def _get_extended_stdin(self) -> str:
        logging_path_env = os.environ.get("CLISEER_LOG_DIR")
        if not logging_path_env:
            return ""
        cur_seconds = int(time.time())
        path = os.path.join(logging_path_env, "stdout/")

        contents = []
        for entry in os.scandir(path):
            if not entry.is_file():
                continue
            file_seconds = parse_seconds_from_fname(entry.name)
            if not file_seconds or (cur_seconds - file_seconds) > 300:
                continue
            try:
                with open(entry.path, "r") as f:
                    contents.append(f.read())
            except Exception as e:
                raise e
        return "==================".join(contents)

def parse_seconds_from_fname(fname):
    # expected format is <s>.<ns>.<random>
    try:
        parts = fname.split('.')
        if len(parts) == 3:
            return int(parts[0])
    except:
        pass
    return False

if __name__ == '__main__':
    f = FishShellReader()
    print(f._get_extended_stdin())
