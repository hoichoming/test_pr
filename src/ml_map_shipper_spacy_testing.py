# from fuzzywuzzy import process
# import pandas as pd
import numpy as np
import spacy
from psycopg2 import sql

from utils.dataframe import load_df
from utils.db import db_connect, read_query_config, insert

nlp = spacy.load("en_core_web_md")

def generate_vector(text):
    doc = nlp(text)
    return doc.vector

queries = read_query_config()
all_shipper_query = queries['booking_number_with_shipper']

connection = db_connect()
df_shipper = load_df(connection, all_shipper_query)

df_shipper["name_vector"] = df_shipper["name"].apply(generate_vector)

connection = db_connect()

df_shipper['name_vector'] = df_shipper['name_vector'].apply(lambda x: x.tolist())

insert_query = sql.SQL('''
    INSERT INTO booking_event_ms.shipper_vector_testing (booking_number,name,name_vector)
    VALUES ({}, {}, {})
''').format(
    sql.Placeholder(), sql.Placeholder(), sql.Placeholder()
)

cur = connection.cursor()
cur.executemany(insert_query, df_shipper.values)
connection.commit()

# Close cursor and connection
cur.close()
connection.close()

print(df_shipper)

