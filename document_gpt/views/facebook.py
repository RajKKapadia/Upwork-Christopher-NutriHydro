from flask import Blueprint, request

from document_gpt.helper.conversation import create_conversation
from document_gpt.helper.messenger_api import send_message
from config import config

facebook = Blueprint(
    'facebook',
    __name__
)

@facebook.route('/', methods=['GET'])
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


@facebook.route('/', methods=['POST'])
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
