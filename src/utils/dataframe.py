import pandas as pd


def load_df(connection, query):
    try:
        cur = connection.cursor()
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        # print(columns)
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=columns)
        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # Close the connection in the finally block
        if cur:
            cur.close()
        if connection:
            connection.close()
