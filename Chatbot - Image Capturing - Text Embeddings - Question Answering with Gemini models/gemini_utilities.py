import os
import json
import google.generativeai as genai

def get_google_api_key():
    working_dir = os.path.dirname(os.path.abspath(__file__))
    config_data = json.load(open(f"{working_dir}/config.json"))
    return config_data["GOOGLE_API_KEY"]

def configure_api_key():
    api_key = get_google_api_key()
    genai.configure(api_key=api_key)

def load_chatbot_model(model_name):
    model = genai.GenerativeModel(model_name)
    return model

def image_captionning_model_response(model_name, image):
    model = genai.GenerativeModel(model_name)
    text = "Give me a short description of this image"
    response = model.generate_content([text, image])
    return response.text

def text_embeddings_model_response(text):
    model_name = "models/embedding-001"
    results = genai.embed_content(
        model=model_name,
        content=text,
        task_type="retrieval_document",
        title="Embedding of a text"
    )
    return results['embedding']

def question_answering_model_response(model_name, prompt):
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text
