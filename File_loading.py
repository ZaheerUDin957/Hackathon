import zipfile
import os
import fitz  # PyMuPDF for handling PDF files
import docx2txt
import streamlit as st
import tempfile

class FileLoader:
    @staticmethod
    def load_file(file_path):
        return "File loaded successfully!"

    @staticmethod
    def extract_text_from_pdf(pdf_file):
        try:
            # Ensure pdf_file is bytes
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text()
            return text
        except Exception as e:
            st.warning(f"Error extracting text from PDF: {e}")
            return ""
        finally:
            # Close the PyMuPDF document (release resources)
            if 'pdf_document' in locals() and pdf_document:
                pdf_document.close()

    @staticmethod
    def extract_text_from_docx(docx_file):
        return docx2txt.process(docx_file)

    @staticmethod
    def extract_text_from_zip(zip_file):
        text = ""
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.filename.lower().endswith(('.pdf', '.docx')):
                    with zip_ref.open(file_info) as file:
                        if file_info.filename.lower().endswith('.pdf'):
                            text += FileLoader.extract_text_from_pdf(file)
                        elif file_info.filename.lower().endswith('.docx'):
                            text += FileLoader.extract_text_from_docx(file)
        return text

    @staticmethod
    def extract_text_from_uploaded_file(uploaded_file):
        _, file_extension = os.path.splitext(uploaded_file.name.lower())
        if file_extension == '.pdf':
            return FileLoader.extract_text_from_pdf(uploaded_file)
        elif file_extension == '.docx':
            return FileLoader.extract_text_from_docx(uploaded_file)
        elif file_extension == '.zip':
            return FileLoader.extract_text_from_zip(uploaded_file)
        else:
            st.warning(f"Unsupported file format: {file_extension}")
            return ""

def display_uploaded_files(file_uploader):
    return [file.name for file in file_uploader if file is not None]
