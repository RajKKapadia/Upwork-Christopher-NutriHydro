from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from config import config


def create_conversation() -> RetrievalQA:
    prompt_template = '''Followings are the conversation between AI and User.\
    Use the conversation as context and try to give accurate answer to the Question in the end.\
    If you don't know the answer, just say that I am sorry, I don't have a answer to your question..
    Context: {context}
    Question: {question}'''
    persist_directory = config.DB_DIR
    embeddings = OpenAIEmbeddings(
        openai_api_key=config.OPENAI_API_KEY
    )
    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=['context', 'question']
    )
    chain_type_kwargs = {'prompt': PROMPT}
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0.0),
        chain_type="stuff",
        retriever=db.as_retriever(),
        verbose=True,
        chain_type_kwargs=chain_type_kwargs
    )
    return qa


chat = ChatOpenAI(temperature=0.0, openai_api_key=config.OPENAI_API_KEY)


def get_mobile(query: str) -> str:
    mobile_schema = ResponseSchema(
        name='mobile',
        description='Was a mobile number of the user. If not found, output -1.'
    )
    template = '''For the following text, extract the following information: \
    mobile: Was a mobile number of the user. If not found, output -1. \
    text: {text} \
    {format_instructions}'''
    response_schemas = [mobile_schema]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_template(template=template)
    messages = prompt.format_messages(text=query,
                                      format_instructions=format_instructions)
    try:
        response = chat(messages)
        output = output_parser.parse(response.content)
        if output['mobile'] == -1:
            response = chat.predict('Politely ask just the mobile number of the user.')
            return {
                'status': 0,
                'output': response
            }
        return {
            'status': 1,
            'output': output['mobile']
        }
    except:
        return {
            'status': -1,
            'output': -1
        }


def get_email(query: str) -> str:
    email_schema = ResponseSchema(
        name='email',
        description='Was an email address fo the user. If not found, output -1.'
    )
    template = '''For the following text, extract the following information: \
    email: Was an email address fo the user. If not found, output -1. \
    text: {text} \
    {format_instructions}'''
    response_schemas = [email_schema]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_template(template=template)
    messages = prompt.format_messages(text=query,
                                      format_instructions=format_instructions)
    try:
        response = chat(messages)
        output = output_parser.parse(response.content)
        if output['email'] == -1:
            response = chat.predict('Politely ask just the email of the user.')
            return {
                'status': 0,
                'output': response
            }
        return {
            'status': 1,
            'output': output['email']
        }
    except:
        return {
            'status': -1,
            'output': -1
        }


def get_consent(query: str) -> str:
    consent_schema = ResponseSchema(
        name='consent',
        description='Was a consent of a person, either Yes or No. If not found, output -1.'
    )
    template = '''For the following text, extract the following information: \
    consent: Was a consent of a person, either Yes or No. If not found, output -1. \
    text: {text} \
    {format_instructions}'''
    response_schemas = [consent_schema]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_template(template=template)
    messages = prompt.format_messages(text=query,
                                      format_instructions=format_instructions)
    try:
        response = chat(messages)
        output = output_parser.parse(response.content)
        if output['consent'] == -1:
            response = config.CONSENT_MESSAGE
            return {
                'status': 0,
                'output': response
            }
        return {
            'status': 1,
            'output': output
        }
    except:
        return {
            'status': -1,
            'output': -1
        }

def get_name(query: str) -> str:
    name_schema = ResponseSchema(
        name='name',
        description='Was a name of the person. If not found, output -1.'
    )
    template = '''For the following text, extract the following information: \
    name: Was a name of the person. If found then capitalize the name and if not found, output -1. \
    text: {text} \
    {format_instructions}'''
    response_schemas = [name_schema]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_template(template=template)
    messages = prompt.format_messages(text=query,
                                      format_instructions=format_instructions)
    try:
        response = chat(messages)
        output = output_parser.parse(response.content)
        if output['name'] == -1:
            response = chat.predict('Politely ask just the name of the user.')
            return {
                'status': 0,
                'output': response
            }
        return {
            'status': 1,
            'output': output['name']
        }
    except:
        return {
            'status': -1,
            'output': -1
        }

def get_general_response(query: str) -> str:
    try:
        response = chat.predict(query)
        return response
    except:
        return config.ERROR_MESSAGE
    