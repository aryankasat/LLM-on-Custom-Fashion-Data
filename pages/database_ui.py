import streamlit as st
from database_query import get_few_shot_db_chain

st.title ("Database Q&A")

question = st.text_input("Query Question:")

if question:
    chain = get_few_shot_db_chain()
    answer = chain.invoke({"question":question})
    st.header("Output:")
    st.write(answer)