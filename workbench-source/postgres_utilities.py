import psycopg2
import os
import logging


def get_db_connection_uri():

    uri = os.getenv("URI")

    return uri


def create_db_connection():

    postgres_uri = get_db_connection_uri()
    
    conn = psycopg2.connect(postgres_uri)

    return conn