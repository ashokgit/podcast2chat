import gradio as gr
from index_bot import IndexBot

# Load the index
index_bot = IndexBot('transcriptions/AndrewHuberMan/avatar.json')


def predict(query, person, state):
    index_bot = IndexBot(person)
    response = index_bot.ask_bot(query, state)
    state = state + [(query, response)]
    return state, state


# Define the Gradio interface


title = "Q&A with Your Favorite Podcast Host / Philishoper"
description = "Ask any question with: Andrew Huberman/LexFridman/Terence Mckenna"

with gr.Blocks() as app:
    markdown_text = "# {}\n{}".format(title, description)
    gr.Markdown(markdown_text)
    chatbot = gr.Chatbot(elem_id="chatbot")
    state = gr.State([])

    with gr.Column():
        person = gr.Dropdown(["transcriptions/AndrewHuberMan/avatar.json",
                              "transcriptions/LexFridman/avatar.json",
                              "transcriptions/TerenceMckenna/avatar.json"], value="transcriptions/AndrewHuberMan/avatar.json")
        default = "I am a 36 years old male, in IT. I am also a diabetic. It's early in the morning in Nepal exactly 7:00 AM. I've just woken up. What suggestions do you have for me to increase my health and work productivity? Write me a personal plan for my morning, break it down in time also. and Suggestions thru out the day."
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter", value=default).style(
            container=False)
    txt.submit(predict, [txt, person, state], [chatbot, state])

app.launch()
