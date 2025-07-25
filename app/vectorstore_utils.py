from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List

## This function creates a FAISS (facebook ai similarity search) index from a list of texts using HuggingFace embeddings.
## It uses the "sentence-transformers/all-mpnet-base-v2" model to convert texts into embeddings.
## The resulting FAISS index can be used for efficient similarity search and retrieval of relevant documents based on a query.
def create_faiss_index(texts: List[str]):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    return FAISS.from_texts(texts, embeddings)

# This function retrieves relevant documents from a FAISS vector store based on a query.
# It performs a similarity search using the provided query and returns the top k most relevant documents.
def retrieve_relevant_docs(vectorstore, query: str, k: int = 3):
    docs = vectorstore.similarity_search(query, k=k)
    return docs
