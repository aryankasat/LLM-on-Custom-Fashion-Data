import streamlit as st
from internet_query import rag_query
import pickle
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS

st.title ("Internet Q&A")

file_path = "faiss.pkl"
st.sidebar.title("Fashion Article URLs")

urls=[]
for i in range(2):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url  = st.sidebar.button("Process URLs")
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
    embeddings = HuggingFaceEmbeddings()
    text_embeddings = embeddings.embed_documents(docs)
    text_embedding_pairs = zip(docs, text_embeddings)
    text_embedding_pairs_list = list(text_embedding_pairs)
    vectorstore = FAISS.from_embeddings(text_embedding_pairs_list, embeddings)
    left_page.text("Creating vector embedding✅...")
    time.sleep(2)

    # Save the FAISS index to a pickle file
    with open(file_path, "wb") as f:
        pickle.dump(vectorstore, f)


    question = left_page.text_input("Question:")

    if question!=None:
        result = rag_query(question)
        left_page.header("Answer:")
        left_page.write(result['answer'])

        #displaying of the sources
        sources = result.get("sources","")
        if sources is not None:
            left_page.subheader("Source of answer:")
            sources_list = sources.split("\n")
            for source in sources_list:
                left_page.write(source)