from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from utils.dataframe import load_df
from utils.db import db_connect, read_query_config

queries = read_query_config()
all_shipper_query = queries['all_shipper']

connection = db_connect()
df_B = load_df(connection, all_shipper_query)

booking_number_with_shipper_query = queries['booking_number_with_shipper']
connection = db_connect()
df_A = load_df(connection, booking_number_with_shipper_query)


# Convert names into tokenized representations
vectorizer = CountVectorizer()
X_a = vectorizer.fit_transform(df_A['name'])
X_b = vectorizer.transform(df_B['name'])

# Compute cosine similarity between datasets
similarity_matrix = cosine_similarity(X_a, X_b)

# Find closest name for each name in dataset A
closest_names = []
for i in range(len(df_A)):
    closest_index = np.argmax(similarity_matrix[i])
    closest_name = df_B.iloc[closest_index]['name']
    closest_names.append(closest_name)

df_A['closest_name'] = closest_names

print(df_A)
df_A.to_csv('sklearn_mapped_shipper_output.csv', index=False)