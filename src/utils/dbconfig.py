import os

DATABASE_CONFIG = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'dbname': 'postgres',
    'port': '5432',
}
