import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
FB_AUTH_TOKEN = os.getenv('FB_AUTH_TOKEN')
FB_VERIFY_TOKEN = os.getenv('FB_VERIFY_TOKEN')
FB_PAGE_ID = os.getenv('FB_PAGE_ID')

cwd = os.getcwd()

DB_DIR = os.path.join(
    cwd,
    'data',
    'db'
)
INPUT_DIR = os.path.join(
    cwd,
    'data',
    'input'
)
OUTPUT_DIR = os.path.join(
    cwd,
    'data',
    'output'
)

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
