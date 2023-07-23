import tempfile
import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.vectorstores import Pinecone
from PyPDF2 import PdfReader
import pinecone

from config import config

def create_indexes(file: tempfile) -> str:
    try:
        file_path = file.name
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        output_file_path = os.path.join(
            config.OUTPUT_DIR,
            'output.txt'
        )
        with open(output_file_path, 'w') as file:
            file.write(text)
        loader = DirectoryLoader(
            f'{config.OUTPUT_DIR}',
            glob='**/*.txt',
            loader_cls=TextLoader
        )
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=0
        )
        texts = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings(
            openai_api_key=config.OPENAI_API_KEY
        )
        pinecone.init(
            api_key=config.PINECONE_API_KEY,
            environment=config.PINECONE_ENVIRONMENT
        )
        indexes_list = pinecone.list_indexes()
        if config.PINECONE_INDEX_NAME not in indexes_list:
            pinecone.create_index(
                name=config.PINECONE_INDEX_NAME,
                dimension=1536
            )
        Pinecone.from_documents(
            documents=texts,
            embedding=embeddings,
            index_name=config.PINECONE_INDEX_NAME
        )
        os.unlink(output_file_path)
        return 'Document uploaded and index created successfully. You can chat now.'
    except Exception as e:
        return e

def clear_indexes() -> str:
    try:
        pinecone.init(
            api_key=config.PINECONE_API_KEY,
            environment=config.PINECONE_ENVIRONMENT
        )
        indexes_list = pinecone.list_indexes()
        if config.PINECONE_INDEX_NAME in indexes_list:
            pinecone.delete_index(name=config.PINECONE_INDEX_NAME)
        return 'Indexes cleared.'
    except Exception as e:
        return e
    