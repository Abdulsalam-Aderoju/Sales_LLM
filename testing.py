import streamlit as st
import ollama
import pandas as pd
import time
import regex as re

def stream_data(text, delay=0.2):
    # Split text into parts while preserving sentence endings and bullet points
    parts = re.split(r'(\s*[\.\!\?]\s+|\n\s*|\s*[\-\*\d]+\s+)', text)
    for part in parts:
        if part.strip():
            yield part
        time.sleep(delay)


# Web App title
st.title("Sales Insights Generator")

# Prompt and File Inputs
prompt_text = st.chat_input("Ask any question regarding your data")
uploaded_file = st.file_uploader("Upload your csv or excel file", type=['csv'])




# Run this where there is prompt and file is uploaded
if uploaded_file is not None and prompt_text:
    data = pd.read_csv(uploaded_file)
    data = data.to_json(orient='records')

    with st.chat_message("user"):
        st.write(prompt_text)

    with st.spinner("Analysing the data..."):
        contents = f"Data: {data}\nPrompt: {prompt_text}"

        result = ollama.chat(model =  "llama3", 
                            messages= [{"role": "user", "content": prompt_text}])
        response = result["message"]["content"]
        st.write(stream_data(response))
