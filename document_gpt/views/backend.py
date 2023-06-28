from flask import Blueprint, request, jsonify

from document_gpt.helper.conversation import create_conversation
from document_gpt.helper.utils import get_context

backend = Blueprint(
    'backend',
    __name__
)

@backend.route('/api/qa', methods=['POST'])
def api_qa():
    try:
        qa = create_conversation()
        body = request.get_json()
        query = body['query']
        data = query.split('\n')
        context = get_context(data)
        res = qa({
            'context': context,
            'query': data[-1]
        })
        print(res)
        return jsonify(
            {
                'status': 1,
                'response': res['result']
            }
        )
    except:
        return jsonify(
            {
                'status': 0,
                'response': 'We are facing technical issue at this point.'
            }
        )
    