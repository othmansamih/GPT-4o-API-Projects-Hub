import os
import json
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utilities import configure_api_key, load_chatbot_model, image_captionning_model_response, text_embeddings_model_response, question_answering_model_response
from PIL import Image


# translating words in streamlit
def translate_role_for_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return "user"

# getting the api key
def save_api_key(api_key):
    working_dir = os.path.dirname(os.path.abspath(__file__))
    with open(f"{working_dir}/config.json", "w") as f:
        config = {"GOOGLE_API_KEY": api_key}
        json.dump(config, f)


# configuring the streamlit page
st.set_page_config(
    page_title="Gemini AI",
    page_icon="🧠",
    layout="centered"
)

# displaying the sidebar
with st.sidebar:
    api_key = st.text_input("Enter your API key", type="password")
    if api_key:
        if "saved_api_key" not in st.session_state or st.session_state.saved_api_key!= api_key:
            st.session_state.clear()
            st.session_state.saved_api_key = api_key
            save_api_key(api_key)
            configure_api_key()

    selected = option_menu(
        menu_title="Gemini AI",
        options=["Chatbot", "Image captionning", "Text embeddings", "Ask me anything"],
        menu_icon="robot",
        icons=["chat-dots-fill", "badge-cc-fill", "textarea-t", "question-circle-fill"],
        default_index=0
    )


if selected == "Chatbot":
    # loading the gemini-1.5-flash model
    model_name = "gemini-1.5-flash"
    model = load_chatbot_model(model_name)

    # intializing the streamlit history
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # setting the streamlit page title
    st.title("Chatbot")

    # displaying the messages contained in the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # allowing the user to enter the prompt
    user_prompt = st.chat_input(f"Ask {model_name}...")
    if user_prompt:
        # displaying the user's prompt
        st.chat_message("user").markdown(user_prompt)

        # getting the user's response
        response = st.session_state.chat_session.send_message(user_prompt)

        # diplaying the response
        st.chat_message("assistant").markdown(response.text)

elif selected == "Image captionning":
    # setting the streamlit page title
    st.title("Image captionning")

    # getting the caption of the uploaded image
    image = st.file_uploader("Upload your image here", type=["PNG", "JPEG", "WEBP", "HEIC", "HEIF"])
    if image:
        col1, col2 = st.columns(2)
        with col1:
            img = Image.open(image)
            st.image(img)
        with col2:
            model_name = "gemini-1.5-flash"
            response = image_captionning_model_response(model_name, img)
            if response:
                st.info(response)

elif selected == "Text embeddings":
    # setting the streamlit page title
    st.title("Text embeddings")

    # getting the embeddings of the entered text
    text = st.text_area("", placeholder="Enter the text to get the embeddings")
    if st.button("Embed text"):
        embeddings = text_embeddings_model_response(text)
        st.info(embeddings)

elif selected == "Ask me anything":
    # setting the streamlit page title
    st.title("Ask me anything")

    # getting an answer for the asked question
    model_name = "gemini-1.5-flash"
    prompt = st.text_area(label="", placeholder=f"Ask {model_name}...")
    if st.button("Get response"):
        response = question_answering_model_response(model_name, prompt)
        st.markdown(response)
