# How to run the app
There are two parts of the application...

* Gradio interface
* Python backend for Facebook Messenger and React frontend

# Gradio interface
run the Gradio interface using `uvicorn gradio_ui:app --reload`, this will run the application on `http://127.0.0.1:8000`, bind this to a domain...

# Python backend
run this application using `gunicorn run:app --bind 127.0.0.1:5000`, this application is already connected to `bknd/`...
