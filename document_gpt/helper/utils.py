def get_context(data: list) -> list:
    context = ''
    for i in range(0, len(data), 2):
        if len(data[:-2]) == i:
            context += f'AI - {data[i]}'
        else:
            context += f'AI - {data[i]}\n'
            context += f'User - {data[i+1]}\n'
    return context
