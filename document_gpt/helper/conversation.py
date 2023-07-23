from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from config import config

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
import pinecone


def create_conversation(query: str, chat_history: list) -> str:
    try:
        pinecone.init(
            api_key=config.PINECONE_API_KEY,
            environment=config.PINECONE_ENVIRONMENT,
        )
        embeddings = OpenAIEmbeddings(
            openai_api_key=config.OPENAI_API_KEY
        )
        db = Pinecone.from_existing_index(
            index_name=config.PINECONE_INDEX_NAME,
            embedding=embeddings
        )
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=False
        )
        cqa = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(temperature=0.0,
                           openai_api_key=config.OPENAI_API_KEY),
            retriever=db.as_retriever(),
            memory=memory,
            get_chat_history=lambda h: h,
        )
        result = cqa({'question': query, 'chat_history': chat_history})
        return result['answer']
    except Exception as e:
        print(e)
        return config.ERROR_MESSAGE


def create_conversation_gradio(query: str, chat_history: list) -> tuple:
    try:
        pinecone.init(
            api_key=config.PINECONE_API_KEY,
            environment=config.PINECONE_ENVIRONMENT,
        )
        embeddings = OpenAIEmbeddings(
            openai_api_key=config.OPENAI_API_KEY
        )
        db = Pinecone.from_existing_index(
            index_name=config.PINECONE_INDEX_NAME,
            embedding=embeddings
        )
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=False
        )
        cqa = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(temperature=0.0,
                           openai_api_key=config.OPENAI_API_KEY),
            retriever=db.as_retriever(),
            memory=memory,
            get_chat_history=lambda h: h,
        )
        result = cqa({'question': query, 'chat_history': chat_history})
        chat_history.append((query, result['answer']))
        return '', chat_history
    except Exception as e:
        chat_history.append((query, e))
        return '', chat_history


def get_mobile(query: str) -> dict:
    response_schemas = [
        ResponseSchema(name="mobile", description="it is a mobile number")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(
                "try to extract a mobile number from the question, if not found output -1.\n{format_instructions}\n{question}")
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )
    try:
        chat = ChatOpenAI(temperature=0, openai_api_key=config.OPENAI_API_KEY)
        _input = prompt.format_prompt(question=query)
        output = chat(_input.to_messages())
        output = output_parser.parse(output.content)
        if output['mobile'] == -1:
            response = chat.predict('Politely ask mobile number of the user.')
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
    response_schemas = [
        ResponseSchema(
            name="email", description="it is an email address of a user")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(
                "try to extract an email address from the question, if not found output -1.\n{format_instructions}\n{question}")
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )
    try:
        chat = ChatOpenAI(temperature=0, openai_api_key=config.OPENAI_API_KEY)
        _input = prompt.format_prompt(question=query)
        output = chat(_input.to_messages())
        output = output_parser.parse(output.content)
        if output['email'] == -1:
            response = chat.predict('Politely ask email of a person.')
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
    response_schemas = [
        ResponseSchema(name="consent", description="it is a consent of a user")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(
                "try to extract a consent of user from the question, if found then return either Yes or No, if not found output -1.\n{format_instructions}\n{question}")
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )
    try:
        chat = ChatOpenAI(temperature=0, openai_api_key=config.OPENAI_API_KEY)
        _input = prompt.format_prompt(question=query)
        output = chat(_input.to_messages())
        output = output_parser.parse(output.content)
        if output['consent'] == -1:
            return {
                'status': 0,
                'output': config.CONSENT_MESSAGE
            }
        return {
            'status': 1,
            'output': output['consent']
        }
    except:
        return {
            'status': -1,
            'output': -1
        }


def get_name(query: str) -> dict:
    response_schemas = [
        ResponseSchema(name="name", description="it is a name of a person")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template(
                "try to extract name of a person from the question, if found then capitalize the name, if not found output -1.\n{format_instructions}\n{question}")
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )
    try:
        chat = ChatOpenAI(temperature=0, openai_api_key=config.OPENAI_API_KEY)
        _input = prompt.format_prompt(question=query)
        output = chat(_input.to_messages())
        output = output_parser.parse(output.content)
        if output['name'] == -1:
            response = chat.predict('Politely ask name of a person.')
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
        chat = ChatOpenAI(temperature=0, openai_api_key=config.OPENAI_API_KEY)
        response = chat.predict(query)
        return response
    except:
        return config.ERROR_MESSAGE
