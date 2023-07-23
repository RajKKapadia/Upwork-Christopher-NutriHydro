from pyairtable import Table

from config import config


def get_chat_history(data: list) -> str:
    chat_history = []
    if len(data) == 2:
        return chat_history
    for i in range(1, len(data)-1, 2):
        chat_history.append(
            (
                data[i],
                data[i+1]
            )
        )
    return chat_history


def get_chat_history_from_mongodb(data: list) -> str:
    chat_history = []
    for d in data:
        chat_history.append(
            (
                d['query'],
                d['response']
            )
        )
    return chat_history


table = Table(config.AIRTABLE_API_KEY, config.AIRTABLE_APP_ID, 'users')


def create_airtable_user(user: dict) -> None:
    table.create(user)
