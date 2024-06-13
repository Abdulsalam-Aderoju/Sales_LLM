import streamlit as st
import ollama
import pandas as pd
import time

def stream_data(text, delay=0.02):
    for word in text.split():
        yield word + " "
        time.sleep(delay)

# Web App title
st.title("Sales Insights Generator")

# Prompt and File Inputs
prompt_text = st.chat_input("Ask any question regarding your data")
uploaded_file = st.file_uploader("Upload your csv or excel file", type=['csv', 'xlsx', 'xls'])

# Run this where there is prompt and file is uploaded
if uploaded_file is not None and prompt_text:
    try:
        # Read file and convert to json
        try:
            if uploaded_file.type == 'text/csv':
                data = pd.read_csv(uploaded_file)
            elif uploaded_file.type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
                data = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file type.")
                data = None

        except Exception as e:
            st.error(f"Error reading the file: {e}")
            data = None

        if data is not None:
            data = data.to_json(orient='records')

            # Create a prompt container for user
            with st.chat_message("user"):
                st.write(prompt_text)

            # Behind the scenes processing
            # Create a prompt container for assistant (AI)

            with st.spinner("Thinking hard..."):
                try:
                    # Content that will be sent to ollama
                    content = f"Data: {data}\nPrompt: {prompt_text}"

                    # Result being provided by model based on content received
                    result = ollama.chat(model="llama3", messages=[{
                        "role": "user",
                        "content": content
                    }])

                    # Ensure response has the expected structure
                    if "message" in result and "content" in result["message"]:
                        response = result["message"]["content"]
                        st.write(stream_data(response))
                    else:
                        st.error("Unexpected response structure from the model.")

                except Exception as e:
                    st.error(f"Error processing the request: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

else:
    st.write("Please provide a prompt or upload a file")
