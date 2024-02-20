import os,pickle
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.vectorstores import VectorStoreRetriever


from dotenv import load_dotenv
load_dotenv()


llm = GoogleGenerativeAI(model="models/text-bison-001",google_api_key = os.environ['GOOGLE_API_KEY'],temperature=0.1)
file_path = "faiss.pkl"

def rag_query(question):
    if os.path.exists(file_path):
        with open(file_path,"rb") as f:
            vectorstore = pickle.load(f)

            # vectorretriever = VectorStoreRetriever(vectorstore=vectorstore)
            chain = RetrievalQA.from_llm(llm=llm,retriever=VectorStoreRetriever(vectorstore=vectorstore))
            result = chain.invoke({"query":question})
            return result
