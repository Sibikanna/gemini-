from dotenv import load_dotenv
load_dotenv()  # loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")

def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

def get_sentiment_analysis(question):
    sentiment_prompt = f"Analyze the sentiment of the following text and classify it as Positive, Negative, or Neutral: {question}"
    sentiment_response = model.generate_content(sentiment_prompt)
    return sentiment_response.text

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")
input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# When submit is clicked
if submit:
    response = get_gemini_response(input)
    sentiment = get_sentiment_analysis(response)
    st.subheader("The Response is")
    st.write(response)
    st.subheader("Sentiment Analysis")
    st.write(f"The sentiment of the response is: {sentiment}")
