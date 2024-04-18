from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from utils.dataframe import load_df
from utils.db import db_connect, read_query_config

queries = read_query_config()
booking_w_contract_query = queries['booking_with_contract'].format(
    carrier_id='e5f83d5a-414a-4b82-92fc-c9e0b88da376',
    from_shipped_on_board='2024-02-01')

connection = db_connect()
df_B = load_df(connection, booking_w_contract_query)

booking_wo_contract_query = queries['booking_without_contract'].format(
    contract_number='23-033TPC', from_shipped_on_board='2024-02-01')
connection = db_connect()
df_A = load_df(connection, booking_wo_contract_query)

festure_cols = [
    'booking_number', 'place_of_receipt', 'port_of_load', 'port_of_discharge',
    'place_of_delivery', 'voyage', 'vessel'
]

X = df_B[festure_cols]
y = df_B['contract_number']

X_train, X_test, y_train, y_test = train_test_split(df_B,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=42)

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')
     ),  # Replace with appropriate imputation strategy
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[('cat', categorical_transformer,
                   festure_cols)  # Replace with your string columns
                  ])

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_jobs=4)
     )  # You can replace RandomForestClassifier with any other model
])

model.fit(X_train, y_train)
predicted_contract_numbers = model.predict(df_A[festure_cols])

# print(predicted_contract_numbers)
df_A['predicted_contract_number'] = predicted_contract_numbers

print(df_A)
print(model.score(X_train, y_train))
df_A.to_csv('output.csv', index=False)
