import os,pickle
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import RetrievalQAWithSourcesChain


from dotenv import load_dotenv
load_dotenv()


llm = GoogleGenerativeAI(model="models/text-bison-001",google_api_key = os.environ['GOOGLE_API_KEY'],temperature=0.1)
file_path = "vectorstore.pkl"

def rag_query(question):
    if os.path.exists(file_path):
        with open(file_path,"rb") as f:
            vectorstore = pickle.load(f)

            chain = RetrievalQAWithSourcesChain.from_llm(llm,retriver = vectorstore.as_retriver())
            result = chain ({"question":question},return_only_outputs = True)
            return result
