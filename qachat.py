from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
import json

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load gemini pro model and get response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize our Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# File uploader for JSON files
uploaded_file = st.file_uploader("Upload a JSON file", type="json")

# Function to summarize JSON content
def summarize_json_content(json_content):
    # Assuming the JSON content is a list of dictionaries
    text_to_summarize = json.dumps(json_content)
    response = get_gemini_response(f"Summarize this content: {text_to_summarize}")
    summary = ""
    for chunk in response:
        summary += chunk.text
    return summary

if uploaded_file is not None:
    json_content = json.load(uploaded_file)
    summary = summarize_json_content(json_content)
    st.subheader("The Summary is")
    st.write(summary)
    st.session_state['chat_history'].append(("You", "Uploaded JSON file"))
    st.session_state['chat_history'].append(("Bot", summary))

# Input field for user questions
input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
