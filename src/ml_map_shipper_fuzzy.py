from fuzzywuzzy import process
import pandas as pd

from utils.dataframe import load_df
from utils.db import db_connect, read_query_config

queries = read_query_config()
all_shipper_query = queries['all_shipper']

connection = db_connect()
df_B = load_df(connection, all_shipper_query)

booking_number_with_shipper_query = queries['booking_number_with_shipper']
connection = db_connect()
df_A = load_df(connection, booking_number_with_shipper_query)


# Function to perform fuzzy matching
def fuzzy_match(name_a, options):
    matched_name = process.extractOne(name_a, options)[0]
    return matched_name

# Map names from dataset A to dataset B using fuzzy search
df_A['mapped_name'] = df_A['name'].apply(fuzzy_match, options=df_B['name'])


# Merge dataset A with dataset B based on mapped name
merged_data = pd.merge(df_A, df_B, left_on='mapped_name', right_on='name', how='left')

print(merged_data)
merged_data.to_csv('fuzzy_mapped_shipper_output.csv', index=False)