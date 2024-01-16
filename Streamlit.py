# Streamlit.py
import streamlit as st
from OpenAI_key import OpenAIKey, update_openai_key
from File_loading import FileLoader, display_uploaded_files
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from Vector_Embedding import TextEmbedder

class StreamlitApp:
    def __init__(self):
        self.openai_key = OpenAIKey.key
        self.file_loader = FileLoader()
        self.character_text_splitter = CharacterTextSplitter(separator=' ', chunk_size=100, chunk_overlap=20, length_function=len)
        self.recursive_text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20, length_function=len)
        self.text_embedder = TextEmbedder()

    def main_bar(self, uploaded_files, text_content, text_splitter_name, chunk_size, chunk_overlap, model_names):
        st.title("Advanced Document Interpreter Bot")
        st.write("Streamlit App is running!")
        st.write("Uploaded Files:", ", ".join(display_uploaded_files(uploaded_files)))
        st.write(f"OpenAI API Key: {self.openai_key}")
        st.write("Text Content:", text_content)
        st.write(f"Text Splitter: {text_splitter_name}")
        st.write("Chunk Size:", chunk_size)
        st.write("Chunk Overlap:", chunk_overlap)

        # Display splitted text
        text_splitter = self.character_text_splitter if text_splitter_name == 'Character Text Splitter' else self.recursive_text_splitter
        text_splitter.chunk_size = chunk_size
        text_splitter.chunk_overlap = chunk_overlap

        splitted_text = self.create_documents(text_splitter, [text_content], chunk_size, chunk_overlap)

        if splitted_text:
            st.write("Splitted Text:")
            for chunk in splitted_text:
                st.write(chunk)

        # Commented out the code for embeddings
        # for model_name in model_names:
        #     embeddings = self.text_embedder.embed_text(splitted_text, model_name)
        #     st.write(f"Embeddings for Model {model_name}:")
        #     for index, vector in enumerate(embeddings):
        #         st.write(f"Vector {index + 1}: {vector}")

    def create_documents(self, text_splitter, texts, chunk_size, chunk_overlap):
        text_splitter.chunk_size = chunk_size
        text_splitter.chunk_overlap = chunk_overlap
        return text_splitter.create_documents(texts)

    def sidebar(self):
        # Sidebar for OpenAI API Key update
        st.sidebar.title("Bot Settings")
        new_openai_key = st.sidebar.text_input("Enter New OpenAI API Key", value=self.openai_key, type="password")
        if st.sidebar.button("Update OpenAI Key"):
            update_openai_key(new_openai_key)
            st.sidebar.success("OpenAI Key updated successfully!")

        # Sidebar for file upload and other settings
        st.sidebar.header("File Settings")

        # File uploader for PDF, DOCX, and ZIP files
        uploaded_files = st.sidebar.file_uploader("Upload your files", type=['pdf', 'docx', 'zip'], accept_multiple_files=True, key="file_uploader")

        # Radio button for text splitting options
        text_splitter_name = st.sidebar.radio("Choose Text Splitter", ['Character Text Splitter', 'Recursive Text Splitter'], index=1)

        # Multi-select for choosing models
        model_names = st.sidebar.multiselect("Choose Embedding Models", ["BAAI/bge-small-en-v1.5", "intfloat/e5-large-v2"], default=["BAAI/bge-small-en-v1.5"])

        # Display user input settings at the end of the sidebar
        st.sidebar.header("Text Splitter Settings")
        chunk_size = st.sidebar.slider("Chunk Size", min_value=50, max_value=1000, value=250)
        chunk_overlap = st.sidebar.slider("Chunk Overlap", min_value=10, max_value=200, value=30)

        return uploaded_files, text_splitter_name, chunk_size, chunk_overlap, model_names

    def run(self):
        uploaded_files, text_splitter_name, chunk_size, chunk_overlap, model_names = self.sidebar()

        text_content = ""
        for file in uploaded_files:
            text_content += self.file_loader.extract_text_from_uploaded_file(file)

        text_splitter = self.character_text_splitter if text_splitter_name == 'Character Text Splitter' else self.recursive_text_splitter

        # Use st.session_state to store and retrieve dynamic values
        st.session_state.chunk_size = chunk_size
        st.session_state.chunk_overlap = chunk_overlap

        text_splitter.chunk_size = st.session_state.chunk_size
        text_splitter.chunk_overlap = st.session_state.chunk_overlap

        self.main_bar(uploaded_files, text_content, text_splitter_name, chunk_size, chunk_overlap, model_names)

# Run the Streamlit application
if __name__ == "__main__":
    app = StreamlitApp()
    app.run()
