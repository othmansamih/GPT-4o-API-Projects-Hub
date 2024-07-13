import os
import json
import openai
import streamlit as st

# configuring the openai api key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data =json.load(open(f"{working_dir}/config.json"))
OPENAI_API_KEY = config_data["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# configuring the Streamlit page
st.set_page_config(
    page_title="GPT-4o Chatbot in Streamlit",
    page_icon= "🤖",
    layout="centered"
)

# setting the title
st.title("🤖 GPT-4o Chatbot in Streamlit")

# initializing the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# displaying chat messages from history on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# getting user's prompt
prompt = st.chat_input("Ask GPT-4o...")
if prompt:
    # displaying the user's prompt
    st.chat_message("user").markdown(prompt)

    # adding user's prompt to the chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # getting gpt-4o response
    response = openai.chat.completions.create(
        model = "gpt-4o",
        messages = [
            {"role": "system", "content": "you are a helpful assistant"},
            *st.session_state.messages
        ]
    )
    chatbot_response = response.choices[0].message.content

    with st.chat_message("assistant"):
        # displaying the gpt-4o's response
        st.markdown(chatbot_response)

        # adding GPT-4o's response to the chat history
        st.session_state.messages.append({"role": "assistant", "content": chatbot_response})
