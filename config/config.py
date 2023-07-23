import os
import tempfile

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
FB_AUTH_TOKEN = os.getenv('FB_AUTH_TOKEN')
FB_VERIFY_TOKEN = os.getenv('FB_VERIFY_TOKEN')
FB_PAGE_ID = os.getenv('FB_PAGE_ID')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_APP_ID = os.getenv('AIRTABLE_APP_ID')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')

ERROR_MESSAGE = 'We are facing a technical issue at this moment.'

CONSENT_MESSAGE = '''By engaging with us on our Facebook Chat feature, you hereby authorize NutriHydro Plant Nutrients to collect and store specific data related to you, namely your name, Facebook user ID, and the contents of your messages.We guarantee that your data will not be distributed to third parties, and its use will be strictly confined to the enhancement of our services and products to better suit your needs.\n\nYou maintain the right to request data deletion at any point by contacting us. For any inquiries concerning this agreement, kindly contact us at NutriHydro Plant Nutrients.\n\nKindly note, usage of Facebook is governed by its separate terms and privacy policy.\n\nBy utilizing our Facebook Chat, you are expressing your agreement with the aforementioned terms.'''

OUTPUT_DIR = os.path.join(
    tempfile.gettempdir(),
    'rkk-document-gpt',
    'output'
)

os.makedirs(OUTPUT_DIR, exist_ok=True)