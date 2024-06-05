import streamlit as st
import pandas as pd

# Inject custom CSS
st.markdown("""
    <style>
    .stFileUpload label {
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2px solid #4CAF50;
        padding: 10px;
        border-radius: 10px;
        background-color: #f9f9f9;
        color: #333;
        cursor: pointer;
        font-weight: bold;
    }
    .stFileUpload label:hover {
        background-color: #e0e0e0;
        border-color: #45a049;
    }
    .stFileUpload input {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('Custom File Uploader Example')

# File uploader widget
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

# Process and display the uploaded file
if uploaded_file is not None:
    file_details = {
        "Filename": uploaded_file.name,
        "FileType": uploaded_file.type,
        "FileSize": uploaded_file.size
    }
    st.write(file_details)

    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    st.write(df)
