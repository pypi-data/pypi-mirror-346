import argparse

from cliprophesy import common
from cliprophesy.inputs import ShellReader, formatting

def get_completions(command, backend, debug):
    backend = common.get_backend(backend)
    reader = ShellReader.FishShellReader()
    context = reader.get_context()
    return backend.get_suggestions(command, test_request=False, **context)

def format_suggestions(suggestions):
    return formatting.PrettySuggestionFormatter.format_suggestions(suggestions)

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("current_line")
    parser.add_argument("--shell", default="fish")
    parser.add_argument("--backend", default="anthropic")
    parser.add_argument("--debug", action='store_true')

    args = parser.parse_args()
    try:
        if args.debug:
            import time
            import logging
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            start = time.time()
        for suggestion in format_suggestions(get_completions(args.current_line, args.backend, args.debug)):
            if not args.debug and 'quick thoughts' in suggestion.lower():
                continue
            print(suggestion)
        if args.debug:
            latency = time.time() - start
            logging.info(f"Latency {latency}")
        return 0
    except Exception as e:
        if args.debug:
            print(e)
        return 1


if __name__ == '__main__':
    run()
