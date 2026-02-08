import streamlit as st

st.title("My First Streamlit App")
st.write("Welcome to this simple learning app!")

name = st.text_input("What is your name?")
if name:
    st.write(f"Hello, {name}! upload file you want to convert into markdown file")

import os
from langchain_openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader, BSHTMLLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Set your API key in environment variables
# os.environ["OPENAI_API_KEY"] = "your-api-key"

def convert_to_markdown(file_path: str, file_type: str) -> str:
    """
    Loads a file and uses an LLM to convert its content to Markdown.
    """
    
    # 1. Load the document
    if file_type == 'pdf':
        loader = PyPDFLoader(file_path)
    elif file_type == 'html':
        loader = BSHTMLLoader(file_path)
    else:
        raise ValueError("Unsupported file type")

    docs = loader.load()
    
    # Combine documents into a single string if multiple pages
    full_text = "\n\n".join([doc.page_content for doc in docs])

    # 2. Define the LLM agent/chain for conversion
    llm = OpenAI(temperature=0.1)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert document formatter. Convert the following text into clean, well-structured GitHub Flavored Markdown (GFM). Preserve all headers, lists, links, and bold text correctly."),
        ("user", "{text}")
    ])
    
    output_parser = StrOutputParser()
    
    chain = prompt | llm | output_parser
    
    # 3. Run the conversion
    markdown_output = chain.invoke({"text": full_text})
    
    return markdown_output

# Example Usage:
# assuming you have a file named "sample.pdf" or "sample.html"
# md_content = convert_to_markdown(file_path="sample.pdf", file_type="pdf")
# print(md_content)
