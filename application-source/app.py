import streamlit as st
from llama_index.llms.openai_like import OpenAILike
import os
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    Numeric,
    select,
    inspect,
    insert,
)
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine

model_uri = os.getenv("inference_endpoint")

model_uri = 'https://llama-31-8b-instruct-redhat-ahead.apps.ai-dev01.kni.syseng.devcluster.openshift.com/v1'
api_key = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkE1V0NJeW84VUJBSWRYcW5ZSG1uZmRLejRYV1BYemVMb0E4ZTk4UUhmR2cifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJyZWRoYXQtYWhlYWQiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlY3JldC5uYW1lIjoiZGVmYXVsdC1uYW1lLWxsYW1hLTMxLThiLWluc3RydWN0LXNhIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImxsYW1hLTMxLThiLWluc3RydWN0LXNhIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiNmM1OGE4MGYtN2JhZS00OTBlLTliYTItYzJhZDUwNmU4N2JlIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OnJlZGhhdC1haGVhZDpsbGFtYS0zMS04Yi1pbnN0cnVjdC1zYSJ9.uZxVPPbqFt5iqorisFLSmJt9SkYkuoRkUJSaQP4ngknbp45YF44eQFEJa9NNoGq0LdAzAmYeS0XHNsogUZmKJua1WcQfJZdXB82BG29lYPDZkYFh4esWvU7AWTraBHhLQiJMR2z4u6RBV2ghPm_BlR3t-qSVsl4qiv1ciYvlpNwjUo1hTaPhxY7Ik-een66iYOYazBPLJ1dNfJjoO1nf4HpCkQHp-rsS3q4TsxtbP8kZjouQ5QvaS2kZR1N77a0CYQq_ae70LAz1LbeeocD1Hb9y7-Im9Cnu5l33aC01mBbtDWBv5IoMSnnorZeUebNGsu533LAgL5uSfzopl3hhKfYX6CAcb1zkwg_r-bwNBOmHzcdoHTUdZs037B7UuBVlcND1j9HwL0f2dwGAoCmGxPSK5TLvuFgGRkPL9MuCWZ9jZwAahsXT5PXfEy5s4w0VHoUsmTNsTxueRof6do5BvhrqPs6iicuOBrzW1TDOtX0zIm7xry2uUb5L1ZGnTCduteQPXoZiW4MUhm6a5pi-QG2AIU1nk0gWTVGd5eELW-F9EMQgufHFoPrkN23d7OsXfxeWv1ilesRueeh_3fekG5Zij01dpQIxDlHQ7g4_FUhhs_mu6oKc8ZpFj85GxumpU5pjR9Bxe6lRoXkk5KknrZ9pok-1tijWyr7qyajjPC0"

def get_db_connection_uri():

    #uri = os.getenv("URI")
    uri = "postgresql://postgres:postgres@pgvector-postgres-service.redhat-ahead.svc.cluster.local:5432/postgres"

    return uri

def submitQuery(query: str) -> str:

    os.environ["OPENAI_API_KEY"] = api_key

    llm = OpenAILike(
        model="llama-31-8b-instruct",
        api_base=f"{model_uri}",
        api_key=api_key,
        context_window=8096,
        is_chat_model=True,
        is_function_calling_model=False,
    )

    sql_database = SQLDatabase(engine, include_tables=["products"])

    uri = get_db_connection_uri()
    engine = create_engine(uri)
    metadata_obj = MetaData()

    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database, tables=["products"], llm=llm
    )
    response = query_engine.query(query)

    return f"Echo: {response}"

# Streamlit UI
st.set_page_config(page_title="Minimal Chatbot", layout="centered")

st.markdown(
    """
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .stTextArea > div > textarea {
        font-size: 16px;
        color: #333;
        background-color: #f8f8f8;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("💬 Minimal Chatbot")

query = st.text_input("Type your message:")

if query:
    response = submitQuery(query)
    st.text_area("Response:", value=response, height=100, max_chars=None, key=None)
