from datetime import datetime

from flask import Blueprint, request

from document_gpt.helper.conversation import create_conversation, get_consent, get_email, get_mobile, get_name, get_general_response
from document_gpt.helper.messenger_api import send_message
from document_gpt.helper.database import get_user, create_user, update_messages, update_user
from document_gpt.helper.utils import get_chat_history_from_mongodb, create_airtable_user
from config import config

facebook = Blueprint(
    'facebook',
    __name__
)


@facebook.route('/facebook', methods=['GET'])
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


@facebook.route('/facebook', methods=['POST'])
def facebook_messenger():
    try:
        body = request.get_json()
        sender_id = body['entry'][0]['messaging'][0]['sender']['id']
        query = body['entry'][0]['messaging'][0]['message']['text']
        user = get_user(sender_id)
        if user:
            if user['status'] == 'active':
                chat_history = get_chat_history_from_mongodb(user['messages'][-2:])
                response = create_conversation(query, chat_history)
                update_messages(sender_id, query,
                                response, user['messageCount'])
                send_message(sender_id, response)
            else:
                properties = user['properties']
                property = ''
                for p in properties:
                    if not p['isFilled']:
                        property += p['name']
                        break

                if property == 'name':
                    response = get_name(query)
                    if response['status'] == -1:
                        send_message(sender_id, config.ERROR_MESSAGE)
                    elif response['status'] == 0:
                        send_message(sender_id, response['output'])
                    else:
                        properties[0]['isFilled'] = True
                        properties[0]['value'] = response['output']
                        update_user(
                            sender_id,
                            {
                                'userName': response['output'],
                                'properties': properties
                            }
                        )
                        response = get_general_response(
                            'Politely ask just the mobile number of the user.')
                        update_messages(sender_id, query,
                                        response, user['messageCount'])
                        send_message(
                            sender_id,
                            response)

                elif property == 'mobile':
                    response = get_mobile(query)
                    if response['status'] == -1:
                        send_message(sender_id, config.ERROR_MESSAGE)
                    elif response['status'] == 0:
                        send_message(sender_id, response['output'])
                    else:
                        properties[2]['isFilled'] = True
                        properties[2]['value'] = response['output']
                        update_user(
                            sender_id,
                            {
                                'mobile': response['output'],
                                'properties': properties
                            }
                        )
                        response = get_general_response(
                            'Politely ask just the eamil address of the user.')
                        update_messages(sender_id, query,
                                        response, user['messageCount'])
                        send_message(
                            sender_id,
                            response)

                elif property == 'email':
                    response = get_email(query)
                    if response['status'] == -1:
                        send_message(sender_id, config.ERROR_MESSAGE)
                    elif response['status'] == 0:
                        send_message(sender_id, response['output'])
                    else:
                        properties[1]['isFilled'] = True
                        properties[1]['value'] = response['output']
                        update_user(
                            sender_id,
                            {
                                'email': response['output'],
                                'properties': properties
                            }
                        )
                        update_messages(sender_id, query,
                                        config.CONSENT_MESSAGE, user['messageCount'])
                        send_message(
                            sender_id,
                            config.CONSENT_MESSAGE)

                elif property == 'consent':
                    response = get_consent(query)
                    if response['status'] == -1:
                        send_message(sender_id, config.ERROR_MESSAGE)
                    elif response['status'] == 0:
                        send_message(sender_id, response['output'])
                    else:
                        properties[3]['isFilled'] = True
                        properties[3]['value'] = response['output']
                        update_user(
                            sender_id,
                            {
                                'consent': response['output'],
                                'properties': properties
                            }
                        )
                        send_message(
                            sender_id, 'You are now ask any query regarding Nutri Hydro and its products.')

                else:
                    update_user(
                        sender_id,
                        {
                            'status': 'active'
                        }
                    )
                    airtable_user = {
                        'fb_id': str(sender_id),
                        'name': properties[0]['value'],
                        'email': properties[1]['value'],
                        'mobile': properties[2]['value'],
                        'consent': properties[3]['value']
                    }
                    create_airtable_user(airtable_user)
                    chat_history = get_chat_history_from_mongodb(user['messages'][-2:])
                    response = create_conversation(query, chat_history)
                    update_messages(sender_id, query,
                                    response, user['messageCount'])
                    send_message(sender_id, response)

        else:
            response = get_general_response(
                'Politely ask just the name of the user.')
            message = {
                'query': query,
                'response': response,
                'createdAt': datetime.now().strftime('%d/%m/%Y, %H:%M')
            }
            user = {
                'userName': '',
                'senderId': sender_id,
                'messages': [message],
                'messageCount': 1,
                'mobile': '',
                'email': '',
                'consent': '',
                'channel': 'Facebook',
                'is_paid': False,
                'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M'),
                'status': 'inactive',
                'properties': [
                    {
                        'name': 'name',
                        'isFilled': False,
                        'value': ''
                    },
                    {
                        'name': 'email',
                        'isFilled': False,
                        'value': ''
                    },
                    {
                        'name': 'mobile',
                        'isFilled': False,
                        'value': ''
                    },
                    {
                        'name': 'consent',
                        'isFilled': False,
                        'value': ''
                    }
                ]
            }
            create_user(user)
            send_message(sender_id, response)
    except:
        pass

    return 'OK', 200
