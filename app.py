import streamlit as st

st.title("My First Streamlit App")
st.write("Welcome to this simple learning app!")

name = st.text_input("What is your name?")
if name:
    st.write(f"Hello, {name}! upload file you want to convert into markdown file")
