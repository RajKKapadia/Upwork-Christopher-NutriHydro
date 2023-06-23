import os
import asyncio

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

from document_gpt.helper.conversation import create_conversation
from document_gpt.helper.create_index import create_index
from config import config


app = Flask(__name__)
CORS(app)


loop = asyncio.get_event_loop()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf']

@app.route('/api/createKnowledge', methods=['POST'])
def api_create_knowldge():
    if 'file' not in request.files:
        return 'There is no file with the key file.', 200
    file = request.files['file']
    if file.filename == '':
        return 'There is no file in the request.', 200
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(config.INPUT_DIR, filename)
        file.save(file_path)
        loop.run_until_complete(create_index(file_path))
        return render_template('success.html', name=file.filename)
    return 'Unknown error at the server.', 200
