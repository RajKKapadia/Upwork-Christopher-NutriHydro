from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
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

def get_mobile(query: str) -> dict:
    response_schemas = [
        ResponseSchema(name="mobile", description="it is a mobile number")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template("try to extract a mobile number from the question, if not found output -1.\n{format_instructions}\n{question}")  
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )
    try:
        chat = ChatOpenAI(temperature=0,openai_api_key=config.OPENAI_API_KEY)
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
        ResponseSchema(name="email", description="it is an email address of a user")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template("try to extract an email address from the question, if not found output -1.\n{format_instructions}\n{question}")  
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )
    try:
        chat = ChatOpenAI(temperature=0,openai_api_key=config.OPENAI_API_KEY)
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
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template("try to extract a consent of user from the question, if found then return either Yes or No, if not found output -1.\n{format_instructions}\n{question}")  
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )
    try:
        chat = ChatOpenAI(temperature=0,openai_api_key=config.OPENAI_API_KEY)
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
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    prompt = ChatPromptTemplate(
        messages=[
            HumanMessagePromptTemplate.from_template("try to extract name of a person from the question, if found then capitalize the name, if not found output -1.\n{format_instructions}\n{question}")  
        ],
        input_variables=["question"],
        partial_variables={"format_instructions": format_instructions}
    )
    try:
        chat = ChatOpenAI(temperature=0,openai_api_key=config.OPENAI_API_KEY)
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
        chat = ChatOpenAI(temperature=0,openai_api_key=config.OPENAI_API_KEY)
        response = chat.predict(query)
        return response
    except:
        return config.ERROR_MESSAGE
    