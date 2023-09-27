import psycopg2
import pandas as pd

def connect_to_db():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="senha",
        host="db",
        port="5432"
    )
    return connection

query = ''' DROP TABLE IF EXISTS rawdata;
            DROP TABLE IF EXISTS predictions;
            DROP TABLE IF EXISTS users;
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL);
            CREATE TABLE rawdata (
                km REAL,
                automovel REAL,
                bicicleta REAL,
                caminhao REAL,
                moto REAL,
                onibus REAL,
                outros REAL,
                tracao_animal REAL,
                transporte_de_cargas_especiais REAL,
                trator_maquinas REAL,
                utilitarios REAL,
                mortos REAL,
                hora INTERVAL);
            CREATE TABLE predictions (
                id SERIAL PRIMARY KEY,
                km REAL,
                automovel REAL,
                bicicleta REAL,
                caminhao REAL,
                moto REAL,
                onibus REAL,
                outros REAL,
                tracao_animal REAL,
                transporte_de_cargas_especiais REAL,
                trator_maquinas REAL,
                utilitarios REAL,
                prediction_mortos REAL,
                hora INTERVAL);
        '''

connection = connect_to_db()
cursor = connection.cursor()
cursor.execute(query)

# Load data from the Parquet file into a pandas DataFrame
parquet_file_path = './df_to_model.parquet'  # Replace with your Parquet file path
data_df = pd.read_parquet(parquet_file_path)


# Iterate over the DataFrame rows and insert data into the table
for index, row in data_df.iterrows():
    columns = ', '.join([ column_name for column_name in data_df.columns])
    placeholders = ', '.join(['%s' for _ in range(len(row))])
    insert_sql = f"INSERT INTO rawdata ({columns}) VALUES ({placeholders})"
    cursor.execute(insert_sql, tuple(row))

queryAdminUser = "INSERT INTO users (username, password) VALUES ('admin', 'admin')"

cursor.execute(queryAdminUser)
# Commit the changes
connection.commit()
connection.close()

print(f"Done")
