# Vector_Database.py
from langchain.vectorstores import Qdrant, ElasticSearch
from langchain.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
import toml
import streamlit as st
class VectorDatabase:
    vectors_qdrant = {}
    vectors_elastic = {}

    # Load Qdrant configuration from secrets.toml
    secrets = toml.load("secrets.toml")
    qdrant_url = secrets.get("qdrant", {}).get("url", "")
    qdrant_api_key = secrets.get("qdrant", {}).get("api_key", "")

    @classmethod
    def save_vector_qdrant(cls, index, vector):
        cls.vectors_qdrant[index] = vector

    @classmethod
    def retrieve_vector_qdrant(cls, index):
        return cls.vectors_qdrant.get(index)

    @classmethod
    def save_vector_elastic(cls, index, vector):
        cls.vectors_elastic[index] = vector

    @classmethod
    def retrieve_vector_elastic(cls, index):
        return cls.vectors_elastic.get(index)

    @classmethod
    def get_vectorstore_qdrant(cls, text_chunks, COLLECTION_NAME):
        try:
            # Creating the Vector Store using Qdrant
            knowledge_base = Qdrant.from_documents(
                documents=text_chunks,
                embedding=HuggingFaceEmbeddings("facebook/dpr-question_encoder-single-nq-base"),
                url=cls.qdrant_url,
                prefer_grpc=True,
                api_key=cls.qdrant_api_key,
                collection_name=COLLECTION_NAME,
            )
        except Exception as e:
            st.write(f"Error with Qdrant: {e}")
            knowledge_base = None

        return knowledge_base

    @classmethod
    def get_vectorstore_elastic(cls, text_chunks, INDEX_NAME):
        try:
            # Creating the Vector Store using Elastic Search
            knowledge_base = ElasticSearch.from_documents(
                documents=text_chunks,
                embedding=HuggingFaceEmbeddings("facebook/dpr-question_encoder-single-nq-base"),
                index_name=INDEX_NAME,
                es_host="localhost",  # Update with your Elastic Search host
                es_port=9200,  # Update with your Elastic Search port
            )
        except Exception as e:
            st.write(f"Error with Elastic Search: {e}")
            knowledge_base = None

        return knowledge_base
