from flask import Flask
from flask_cors import CORS

from document_gpt.views.facebook import facebook
from document_gpt.views.home import home
from document_gpt.views.backend import backend

app = Flask(__name__)
CORS(app)

app.register_blueprint(home)
app.register_blueprint(backend)
app.register_blueprint(facebook)
