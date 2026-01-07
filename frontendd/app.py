import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/query"

st.title("Document Chatbot")
st.write("Ask questions about your documents ")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:=st.chat_input("Ask me anything ..."):
    st.session_state.messages.append({"role": "human", "content": prompt})
    with st.chat_message("human"):
        st.markdown(prompt)
    
    with st.chat_message("ai"):
        with st.spinner("Thinking ..."):
            
            try:
                res=requests.post(API_URL, json={"text": prompt})
                res.raise_for_status()
                answer=res.json()["answer"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "ai", "content": answer})
            except Exception as e:
                st.error(f"api error {e}")
UPAPI_URL = "http://127.0.0.1:8000"
uploaded_file = st.sidebar.file_uploader("Upload a document", type=["txt", "pdf", "docx"])
if uploaded_file is not None:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(f"{UPAPI_URL}/upload/", files={"file": (uploaded_file.name, uploaded_file.getvalue())})
    st.sidebar.success(response.json()["upload"])

# Fetch section
filename = st.sidebar.text_input("Enter filename to fetch")
if st.sidebar.button("Fetch Document"):
    response = requests.get(f"{UPAPI_URL}/fetch/{filename}")
    if response.status_code == 200:
        st.sidebar.download_button("Download File", response.content, file_name=filename)
    else:
        st.sidebar.error(response.json().get("error", "Unknown error"))
