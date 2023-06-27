from flask import Flask, request, jsonify
from flask_cors import CORS

from document_gpt.helper.conversation import create_conversation
from document_gpt.helper.messenger_api import send_message
from config import config

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200


def get_context(data: list) -> list:
    context = ''
    for i in range(0, len(data), 2):
        if len(data[:-2]) == i:
            context += f'AI - {data[i]}'
        else:
            context += f'AI - {data[i]}\n'
            context += f'User - {data[i+1]}\n'
    return context


@app.route('/api/qa', methods=['POST'])
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


@app.route('/facebook', methods=['GET'])
def facebook_verify():
    args = request.args.to_dict()
    mode = args['hub.mode']
    verify_token = args['hub.verify_token']
    challenge = args['hub.challenge']
    if mode == 'subscribe' and verify_token == config.FB_VERIFY_TOKEN:
        print('Webhook verified.')
        return challenge, 200
    else:
        return 'BAD_REQUEST', 403


@app.route('/facebook', methods=['POST'])
def facebook_messenger():
    try:
        # TODO
        # Get the sender id and query from the request
        body = request.get_json()
        sender_id = body['entry'][0]['messaging'][0]['sender']['id']
        query = body['entry'][0]['messaging'][0]['message']['text']
        print(sender_id, query)
        # TODO
        # get the user
        # if not create
        # create chat_history from the previous conversations
        qa = create_conversation()
        res = qa({
            'context': '',
            'query': query
        })
        print(res)
        # TODO
        # send message
        send_message(sender_id, res['result'])
    except:
        pass

    return 'OK', 200
