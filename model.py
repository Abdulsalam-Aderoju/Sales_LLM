import streamlit as st
import ollama
import pandas as pd
import time


def stream_data(text, delay = 0.02):
    for word in text.split():
        yield word + " "
        time.sleep(delay)



# Web App title
st.title("Sales Insights Generator")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages upon rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# Prompt and File Inputs
prompt_text = st.chat_input("Ask any question regarding your data")
uploaded_file = st.file_uploader("Upload your csv file", type=['csv', "excel"])


# Run this where there is prompt and file is uploaded
if uploaded_file is not None and prompt_text:

    # Read file and convert to json
    data = pd.read_csv(uploaded_file)
    data = data.to_json(orient='records')

    # Add latest message to history
    st.session_state["messages"].append({"role": "user", "content": prompt_text})

    # Create a prompt container for user
    with st.chat_message("user"):
        st.write(prompt_text)


    # Behind the scenes processing

    # Create a prompt container for assistant (AI)
    with st.chat_message("assistant"):
        with st.spinner("Thinking hard..."):

            # Content that will be sent to ollama
            content = f"Data: {data}\nPrompt: {prompt_text}"

            # Result being provided by model based on content recieved
            result = ollama.chat(model = "llama3", messages = [{
                "role": "assistant",
                "content": content
            }])

            # Content of model response and final output
            response = result["message"]["content"]
            st.session_state["messages"].append({"role": "assistant", "content": response})
            st.write_stream(stream_data(response))

else:
    st.write("Please provide a prompt or upload a file")

