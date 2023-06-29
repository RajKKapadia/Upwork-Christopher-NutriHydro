from pyairtable import Table

from config import config

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
    for d in data:
        context += f'User: {d["query"]}\n'
        context += f'AI: {d["response"]}\n'
    return context

table = Table(config.AIRTABLE_API_KEY, config.AIRTABLE_APP_ID, 'users')

def create_airtable_user(user: dict) -> None:
    table.create(user)