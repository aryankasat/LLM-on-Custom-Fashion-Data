import streamlit as st
from internet_query import rag_query
import pickle,time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.embeddings.huggingface import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores.faiss import FAISS

st.title ("Internet Q&A")

st.sidebar.title("Fashion Article URLs")

urls=[]
for i in range(2):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url  = st.sidebar.button("Process URLs")
file_path = "faiss.pkl"
left_page = st.empty()

if process_url:
    # load data
    loader = UnstructuredURLLoader(urls=urls)
    left_page.text("Loading of data✅...")
    data = loader.load()
    # split data
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000,
    )
    left_page.text("Splitting data into chunks✅...")
    docs = text_splitter.split_documents(data)
    # create embeddings and save it to FAISS index
    embeddings = HuggingFaceBgeEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
    vectorstore = FAISS.from_documents(docs, embeddings)
    left_page.text("Creating vector embedding✅...")
    # Save the FAISS index to a pickle file
    with open(file_path, "wb") as f:
        pickle.dump(vectorstore, f)


question = st.text_input("Question:")

if question:
    result = rag_query(question)
    st.header("Answer:")
    st.write(result['result'])