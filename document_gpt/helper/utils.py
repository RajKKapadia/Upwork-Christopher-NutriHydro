def get_context(data: list) -> str:
    context = ''
    for i in range(0, len(data), 2):
        if len(data[:-2]) == i:
            context += f'AI - {data[i]}'
        else:
            context += f'AI - {data[i]}\n'
            context += f'User - {data[i+1]}\n'
    return context

def get_context_from_mongodb(data: list) -> str:
    context = ''
    for i in range(len(data)):
        context += f'User: {data[i]["query"]}\n'
        context += f'System: {data[i]["response"]}\n'
    return context