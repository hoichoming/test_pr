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
shipper_query = queries['booking_number_with_shipper']

connection = db_connect()
df_shipper = load_df(connection, shipper_query)
# print(df_shipper)

df_shipper["name_vector"] = df_shipper["name"].apply(generate_vector)

df_shipper.head().to_csv('sklearn_mapped_shipper_search_output.csv', index=False)



