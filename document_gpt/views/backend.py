from flask import Blueprint, request, jsonify

from document_gpt.helper.conversation import create_conversation
from document_gpt.helper.utils import get_chat_history
from config import config

backend = Blueprint(
    'backend',
    __name__
)

@backend.route('/api/qa', methods=['POST'])
def api_qa():
    try:
        body = request.get_json()
        query = body['query']
        data = query.split('\n')
        chat_history = get_chat_history(data)
        response = create_conversation(query, chat_history)
        return jsonify(
            {
                'status': 1,
                'response': response
            }
        )
    except:
        return jsonify(
            {
                'status': 0,
                'response': config.ERROR_MESSAGE
            }
        )
    