from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain.prompts import SemanticSimilarityExampleSelector, FewShotPromptTemplate
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from langchain.chains.sql_database.prompt import SQLDatabaseChain
import os
from few_shots import few_shots

from dotenv import load_dotenv
load_dotenv()

def get_few_shot_db_chain():
    db_user = "root"
    db_password = "Aruboi2001!"
    db_host = "localhost"
    db_name = "tshirts"

    database = SQLDatabase.from_uri (f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
                              sample_rows_in_table_info=3)
    
    llm = GoogleGenerativeAI(model="models/text-bison-001",google_api_key = os.environ['GOOGLE_API_KEY'],temperature=0.1)

    embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')

    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize,embeddings,metadatas=few_shots)

    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2
    )
    
    mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".
    
    Use the following format:
    
    Question: Question here
    SQLQuery: Query to run with no pre-amble
    SQLResult: Result of the SQLQuery
    Answer: Final answer here
    
    No pre-amble.
    """
    example_prompt = PromptTemplate(
        input_variables= ["Question","SQLQuery","SQLResult","Answer"],
        template="\nQuestion: {Question}\n SQLQuery:{SQLQuery}\n SQLResult:{SQLResult}\n Answer:{Answer}",
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix = mysql_prompt,
        suffix = PROMPT_SUFFIX,
        input_variables=["input","table_info","top_k"],
    )

    chain = create_sql_query_chain(llm, database,prompt=few_shot_prompt)
    return chain






