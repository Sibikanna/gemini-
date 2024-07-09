import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    try:
        # Define the path where you want to save the FAISS index
        index_path = "fiass_index"
        
        # Ensure the directory exists
        os.makedirs(index_path, exist_ok=True)
        
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        
        # Save the FAISS index to the specified path
        vector_store.save_local(index_path)
        
        # Check if the index file was created successfully
        index_file_path = os.path.join(index_path, "index.faiss")
        if not os.path.exists(index_file_path):
            st.error("Failed to create FAISS index file.")
        else:
            st.info("FAISS index created successfully.")
    except Exception as e:
        st.error(f"Error while creating FAISS index: {e}")


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n
    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    try:
        new_db = FAISS.load_local("faiss_index", embeddings)
    except Exception as e:
        st.error(f"Failed to load FAISS index: {e}")
        return

    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

    st.write("Reply: ", response["output_text"])

def main():
    st.set_page_config(page_title="Chat PDF")
    st.header("Chat with PDF using Gemini")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF file.")
                return

            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                if os.path.exists("faiss_index/index.faiss"):
                    st.success("Processing completed successfully.")
                else:
                    st.error("Failed to create the FAISS index. Please try again.")

if __name__ == "__main__":
    main()
