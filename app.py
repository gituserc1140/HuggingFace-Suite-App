import streamlit as st
import requests
from transformers import pipeline

# Hugging Face API endpoint
API_URL = "https://api-inference.huggingface.co/models/"

st.title("Hugging Face Model Interaction App")

# Model selection
selected_model = st.selectbox("Choose a Hugging Face Model", [
    "distilbert-base-uncased-finetuned-sst-2-english", 
    "t5-small", 
    "facebook/bart-large-cnn"
])

# User input
user_input = st.text_area("Enter your text here:", "Hello, how are you?")

if st.button("Get Prediction"):
    if user_input:
        # Prepare headers for API request
        headers = {"Authorization": f"Bearer YOUR_HUGGINGFACE_API_KEY"}
        
        # Make API request
        response = requests.post(
            f"{API_URL}{selected_model}",
            headers=headers,
            json={"inputs": user_input}
        )
        
        if response.status_code == 200:
            prediction = response.json()
            st.write("Prediction:", prediction)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    else:
        st.warning("Please enter some text to get a prediction.")

# Local model inference (optional)
st.subheader("Local Model Inference")
local_model_name = st.selectbox("Choose a Local Model", [
    "distilbert-base-uncased-finetuned-sst-2-english", 
    "t5-small"
])

if st.button("Run Local Model"):
    if user_input:
        classifier = pipeline("sentiment-analysis", model=local_model_name)
        result = classifier(user_input)
        st.write("Local Model Prediction:", result)
    else:
        st.warning("Please enter some text to run the local model.")