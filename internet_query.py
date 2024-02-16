import os,pickle
from langchain.llms.google_palm import GooglePalm
from langchain.chains import RetrievalQAWithSourcesChain


from dotenv import load_dotenv
load_dotenv()

file_path = "vectorstore.pkl"
llm = GooglePalm(google_api_key = os.environ['GOOGLE_API_KEY'],temperature=0.1)

def rag_query(question):
    if os.path.exists(file_path):
        with open(file_path,"rb") as f:
            vectorstore = pickle.load(f)

            chain = RetrievalQAWithSourcesChain.from_llm(llm,retriver = vectorstore.as_retriver())
            result = chain ({"question":question},return_only_outputs = True)
            return result
