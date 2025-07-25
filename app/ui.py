import streamlit as st

# It contains the Streamlit UI components for uploading PDF files. This module provides a file uploader for users to upload PDF documents.
def pdf_uploader():
    return st.file_uploader(
        'Upload PDF files',
        type='pdf',
        accept_multiple_files=True,
        help="Upload one or more PDF documents"
    )
