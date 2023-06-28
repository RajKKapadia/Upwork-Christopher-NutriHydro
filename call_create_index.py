import asyncio

from document_gpt.helper.index import create_index

loop = asyncio.get_event_loop()

loop.run_until_complete(create_index('data/input/commercial_hydroponics.pdf'))
