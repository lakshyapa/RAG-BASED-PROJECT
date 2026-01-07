#load splitter embedding vector store 
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
import langchain
from langchain_community.document_loaders import DirectoryLoader,PyMuPDFLoader,TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
data_path="../knowledge"
faiss_path="../faiss_index_store"
print("loading the directory...")
pdf_loader=DirectoryLoader(data_path,glob="**/*.pdf",loader_cls=PyMuPDFLoader)
pdf_doc=pdf_loader.load()
#now we do text splitting
text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=150)
docs=text_splitter.split_documents(pdf_doc)
print("creating embedding...")
#create embeddings
embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#do vector store
db=FAISS.from_documents(docs,embeddings)
db.save_local(faiss_path)
print("faiss stored success") 