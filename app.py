import streamlit as st
import tempfile
import os
from docling.document_converter import DocumentConverter

st.set_page_config(page_title="PDF/HTML to Markdown Converter")
st.title("📄 Document to Markdown Agent")

# File uploader for PDF and HTML
uploaded_file = st.file_uploader("Upload a PDF or HTML file", type=["pdf", "html"])

if uploaded_file is not None:
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    try:
        with st.spinner("Converting document to Markdown..."):
            # Initialize Docling for conversion
            converter = DocumentConverter()
            result = converter.convert(tmp_path)
            markdown_output = result.document.export_to_markdown()

            # Display Preview
            st.subheader("Markdown Preview")
            st.text_area("Content", markdown_output, height=300)

            # Download Button
            st.download_button(
                label="📥 Download Markdown File",
                data=markdown_output,
                file_name=f"{uploaded_file.name.rsplit('.', 1)[0]}.md",
                mime="text/markdown"
            )
            
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        os.remove(tmp_path)
