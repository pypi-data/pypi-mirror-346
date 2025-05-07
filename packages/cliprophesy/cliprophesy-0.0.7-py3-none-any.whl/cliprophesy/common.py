from cliprophesy.llms import anthropic_backend, openai_backend, clibuddy
import configparser
from pathlib import Path

def get_backend_from_args(user_requested, config):
    parser = configparser.ConfigParser()
    if user_requested:
        return get_backend(user_requested)
    elif parser.read(Path("~/.config/cliseer/settings.cfg").expanduser()):
        return get_backend(parser['settings']['provider'])
    else:
        get_backend('anthropic')

def get_backend(llm_str):
    if llm_str == 'anthropic':
        return anthropic_backend.AnthropicBackend()
    elif llm_str == 'openai':
        return openai_backend.OpenAIBackend()
    elif llm_str == 'clibuddy':
        return clibuddy.CLIBuddyInterface(allow_stdin=False)
    return anthropic_backend.AnthropicBackend()
