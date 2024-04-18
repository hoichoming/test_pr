import psycopg2
from psycopg2 import OperationalError
from configparser import ConfigParser

from utils.dbconfig import DATABASE_CONFIG

def db_connect():
    try:
        connection = psycopg2.connect(**DATABASE_CONFIG)
        return connection

    except OperationalError as e:
        print(f"Error: {e}")

def read_query_config(filename='queries.ini', section='queries'):
    parser = ConfigParser()
    parser.read(filename)
    queries = dict(parser.items(section))
    return queries


def insert(df, table_name):
    try:
        connection = db_connect()

        df.to_sql(table_name, connection)

        connection.commit()
        connection.close()
    
    except OperationalError as e:
        print(e)
        pass

    finally:
        # Close the connection in the finally block
        if connection:
            connection.close()