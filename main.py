import streamlit as st
from database_query import get_few_shot_db_chain
from internet_query import rag_query
import pickle
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS

col1,col2 = st.columns(2)

col1.title ("Database Q&A")

question = st.text_input("Query Question:")

if question != None:
    chain = get_few_shot_db_chain()
    answer = chain.run(question)
    col1.header("Output:")
    col1.write(answer)


col2.title ("Internet Q&A")

c1,c2 = col2.columns(2)

file_path = "faiss.pkl"
c1.sidebar.title("Fashion Article URLs")

urls=[]
for i in range(2):
    url = c1.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url  = c1.sidebar.button("Process URLs")
if process_url!= None:
    # load data
    loader = UnstructuredURLLoader(urls=urls)
    c2.text("Loading of data✅...")
    data = loader.load()
    # split data
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000,
    )
    c2.text("Splitting data into chunks✅...")
    docs = text_splitter.split_documents(data)
    # create embeddings and save it to FAISS index
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    c2.text("Creating vector embedding✅...")
    time.sleep(2)

    # Save the FAISS index to a pickle file
    with open(file_path, "wb") as f:
        pickle.dump(vectorstore, f)


question = c2.text_input("Question:")

if question!=None:
    result = rag_query(question)
    c2.header("Answer:")
    c2.write(result['answer'])

    #displaying of the sources
    sources = result.get("sources","")
    if sources is not None:
        c2.subheader("Source of answer:")
        sources_list = sources.split("\n")
        for source in sources_list:
            c2.write(source)








