from cliprophesy.llms import anthropic_backend


def get_backend(llm_backend):
    if llm_backend == 'anthropic':
        return anthropic_backend.AnthropicBackend()
    return anthropic_backend.AnthropicBackend()
