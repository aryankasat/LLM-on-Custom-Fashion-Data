import streamlit as st
from database_query import get_few_shot_db_chain

st.title ("Database Q&A")

question = st.text_input("Query Question:")

if question:
    chain = get_few_shot_db_chain()
    answer = chain.invoke({"question":question})
    st.header("Output:")
    index = answer.find("Answer")
    index1 = answer.find("SQLResult")
    final_ans = answer[index+len("Answer")+1:]
    sql_query = answer[0:index1]
    st.subheader("SQL Query-")
    st.write(sql_query)
    st.subheader("Answer-")
    st.write(final_ans)