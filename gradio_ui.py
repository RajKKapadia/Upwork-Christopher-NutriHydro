import gradio as gr
from fastapi import FastAPI

from document_gpt.helper.conversation import create_conversation_gradio
from document_gpt.helper.index import create_indexes

def clear_indexes() -> tuple:
    return 'Document cleared.', None

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            file = gr.components.File(
                label='Upload your pdf file',
                file_count='single',
                file_types=['.pdf'])
            with gr.Row():
                upload = gr.components.Button(
                    value='Upload', variant='primary')
                index_clear_btn = gr.components.Button(
                    value='Clear', variant='stop')
        label = gr.components.Textbox()

    chatbot = gr.Chatbot(label='Talk to the Doument')
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    upload.click(create_indexes, [file], [label])
    index_clear_btn.click(clear_indexes, [], [label, file])
    msg.submit(create_conversation_gradio, [msg, chatbot], [msg, chatbot])

app = FastAPI()

@app.get('/')
async def root():
    return 'Gradio app is running at /gradio', 200

app = gr.mount_gradio_app(app, demo, path='/gradio')
