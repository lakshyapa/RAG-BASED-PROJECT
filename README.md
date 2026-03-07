Overview

This project implements a Retrieval-Augmented Generation (RAG) chatbot that answers user queries using information retrieved from a document knowledge base. Instead of relying only on a language model, the system retrieves relevant document chunks and uses them as context to generate more accurate and reliable responses.

The application integrates LangChain for the RAG pipeline, FastAPI for backend APIs, and Streamlit for the interactive user interface.

Architecture

The chatbot follows the RAG pipeline:

Document Loading – Upload and process documents (PDF, text, etc.).

Text Chunking – Split documents into smaller chunks for better retrieval.

Embedding Generation – Convert text chunks into vector embeddings.

Vector Database Storage – Store embeddings in a vector database.

Similarity Search – Retrieve relevant chunks based on user query.

LLM Response Generation – Pass retrieved context to the language model to generate a response.

Frontend Interaction – Users interact with the chatbot via Streamlit UI.

Features

Document-based question answering

Retrieval-Augmented Generation (RAG) architecture

FastAPI REST API backend

Interactive chatbot interface using Streamlit

Vector similarity search using FAISS / Chroma

Context-aware responses from LLMs

Tech Stack

Python

LangChain

FastAPI

Streamlit

FAISS / Chroma Vector Database

OpenAI / HuggingFace Embeddings

Project Structure
rag-chatbot
│
├── app
│   ├── main.py            # FastAPI backend
│   ├── rag_pipeline.py    # RAG implementation
│   ├── embeddings.py      # Embedding generation
│
├── frontend
│   └── streamlit_app.py   # Streamlit UI
│
├── data                   # Uploaded documents
├── requirements.txt
└── README.md

pip install -r requirements.txt
Run FastAPI backend
uvicorn main
