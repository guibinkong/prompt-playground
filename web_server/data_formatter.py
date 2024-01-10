from data import TemplateInstance, RetrievalConfig


def format_template(tmpl: TemplateInstance, new_input=None):
    prompt = f'{tmpl.instruction}\n\nContext: {tmpl.context}\n\n'
    if tmpl.examples:
        prompt += '\n\nHere are some examples:\n\n'
        for e in tmpl.examples:
            prompt += f'User: {e.input}\n\nAI: {e.output}\n\n\n'
    if new_input:
        prompt += f'User: {new_input}\n\nAI:\n'
    else:
        prompt += 'User: {input}\n\nAI:\n'
    return prompt


def format_retrieval(retrieval: RetrievalConfig):
    msg = ''
    for i, e in enumerate(retrieval.urls):
        msg += f'{i+1}: {e}\n\n'
    return msg
