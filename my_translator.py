import fitz  # PyMuPDF
from docx import Document
from googletrans import Translator
import streamlit as st
import os
import tempfile

# Load the Google Translator
@st.cache_resource
def load_translator():
    return Translator()

translator = load_translator()

def extract_text_from_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    text = ""
    with fitz.open(temp_file_path) as doc:
        for page in doc:
            text += page.get_text("text")

    os.remove(temp_file_path)
    return text.strip()

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])

def translate_text(text):
    # Process the translation in batches for better performance
    translated = translator.translate(text, dest='te')
    return translated.text

def main():
    st.title("Telugu Translator (Organized Output)")
    st.write("Upload a PDF or DOCX file to translate its text into well-structured Telugu.")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"])

    if uploaded_file is not None:
        # Extract text based on file type
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file_path = temp_file.name
            try:
                text = extract_text_from_docx(temp_file_path)
            finally:
                os.remove(temp_file_path)
        else:
            st.error("Unsupported file format.")
            return

        st.subheader("Extracted Text")
        st.text_area("", text, height=300)

        if st.button("Translate to Telugu"):
            with st.spinner("Translating quickly with organized formatting..."):
                translated_text = translate_text(text)
            st.subheader("Translated Text (Organized Telugu)")
            st.text_area("", translated_text, height=300)

            # Download option
            st.download_button(
                label="Download as .txt",
                data=translated_text.encode('utf-8'),
                file_name="translated_text.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
