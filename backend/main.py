import os 
from fastapi import  FastAPI,UploadFile,File
from fastapi.responses import FileResponse 
from dotenv import load_dotenv  
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel 
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate 
load_dotenv()
faiss_path="../faiss_index_store"

embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db=FAISS.load_local(faiss_path,embeddings,allow_dangerous_deserialization=True)

orignal=["*"]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

retriever = db.as_retriever(search_kwargs={"k": 3})

SYSTEM_PROMPT = '''
You are a helpful assistant.
Use the context to answer the question in max three sentences.
If you don't know , just say i don't know.
Context: {context}
'''

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}")
])

qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Query(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "RAG API is running!"}

@app.post("/query")
def query_rag(query: Query):
    response = rag_chain.invoke({"input": query.text})
    return {"answer": response.get("answer", "No answer found")}
UPLOAD_DIR = "../knowledge"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"upload": f"File '{file.filename}' uploaded successfully!"}

@app.get("/fetch/{filename}")
async def fetch_document(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}
