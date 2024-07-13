import streamlit as st
from translator_app_utils import translator

# configuring the the Streamlit page
st.set_page_config(
    page_title="Translator app with GPT-4o using Streamlit & Langchain",
    page_icon="🌐",
    layout="centered"
)

# setting the title of the Streamlit app
st.title("Translator app with GPT-4o using Streamlit & Langchain")

col1, col2 = st.columns(2)
with col1:
    input_languages_list = ["English", "Mandarin", "Spanish", "French", "Hindi", "Arabic", "Bengali", "Portuguese", "Russian", "Japanese", "Lahnda"]
    input_language = st.selectbox(label="Input language", options=input_languages_list)
with col2:
    output_languages_list = [x for x in input_languages_list if x!= input_language]
    output_language = st.selectbox(label="Output language", options=output_languages_list)

input_text = st.text_area("Type the text to be translated")
translated_text = translator(input_language, output_language, input_text)
if st.button("Translate"):
    st.success(translated_text)