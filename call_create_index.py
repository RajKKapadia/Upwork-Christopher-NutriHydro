import asyncio

from document_gpt.helper.create_index import create_index

loop = asyncio.get_event_loop()

loop.run_until_complete(create_index('data/input/nutri_hydro_intro.pdf'))
