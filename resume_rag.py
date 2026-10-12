import os
from io import BytesIO
from typing import List

from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    try:
        import streamlit as st
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        GOOGLE_API_KEY = None

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. Configure it in your "
        "local .env file or Streamlit Cloud Secrets."
    )


# Initialize the embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
)


def extract_resume_text(
    pdf_file,
    filename: str
) -> List[Document]:
    """
    Extract text from an uploaded PDF resume.

    pdf_file can be a file path or an uploaded file object.
    """

    if isinstance(pdf_file, str):
        reader = PdfReader(pdf_file)
    else:
        reader = PdfReader(BytesIO(pdf_file.getvalue()))

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": filename,
                        "page": page_number
                    }
                )
            )

    if not documents:
        raise ValueError(
            f"No extractable text found in {filename}. "
            "The PDF may be scanned or image-based."
        )

    return documents


def split_resume_documents(
    documents: List[Document]
) -> List[Document]:
    """
    Split resume text into smaller chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    return chunks


def build_resume_vector_store(
    resume_documents: List[Document]
):
    """
    Create a FAISS vector store from resume chunks.
    """

    if not resume_documents:
        raise ValueError(
            "No resume text is available for indexing."
        )

    chunks = split_resume_documents(resume_documents)

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vector_store


def retrieve_relevant_resume_content(
    vector_store,
    job_description: str,
    k: int = 5
):
    """
    Retrieve resume passages relevant to a job description.
    """

    if not job_description.strip():
        raise ValueError(
            "Please provide a Job Description."
        )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": k}
    )

    relevant_documents = retriever.invoke(
        job_description
    )

    return relevant_documents