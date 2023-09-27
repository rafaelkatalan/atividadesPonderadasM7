import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to connect to the PostgreSQL database and obtain the data
def get_data():
    # Database connection settings
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="senha",
        host="db",
        port="5432"
    )

    cursor = connection.cursor()

    # SQL query to obtain the required data by joining 'rawdata' and 'predictions' tables
    cursor.execute('''
        SELECT
            r.hora,
            r.mortos AS mortos_rawdata,
            r.km AS km_rawdata,
            p.prediction_mortos AS prediction_mortos_predictions,
            p.km AS km_predictions
        FROM
            rawdata AS r
        JOIN
            predictions AS p
        ON
            r.hora = p.hora
    ''')

    data = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Convert the results into a pandas DataFrame
    df = pd.DataFrame(columns=['hora', 'mortos_rawdata', 'km_rawdata', 'prediction_mortos_predictions', 'km_predictions'])
    i = 0
    for row in df.iterrows():
        row['hora']  = data[0][i]
        row['mortos_rawdata'] = data[1][i]
        row['km_rawdata'] = data[2][i]
        row['prediction_mortos_predictions'] = data[3][i]
        row['km_predictions'] = data[4][i]
        i+=1

    return df

# Load the data
data = get_data()

# Title of the Dashboard
st.title('Dashboard de Relacionamento de Dados')

# Table with the data
st.write(data)

# Scatterplot: hora vs. mortos_rawdata
st.subheader('Gráfico de Dispersão: Hora vs. Mortos (rawdata)')
sns.scatterplot(data=data, x='hora', y='mortos_rawdata')
plt.xlabel('Hora')
plt.ylabel('Mortos (rawdata)')
st.pyplot()

# Scatterplot: km_rawdata vs. mortos_rawdata
st.subheader('Gráfico de Dispersão: KM vs. Mortos (rawdata)')
sns.scatterplot(data=data, x='km_rawdata', y='mortos_rawdata')
plt.xlabel('KM (rawdata)')
plt.ylabel('Mortos (rawdata)')
st.pyplot()

# Scatterplot: hora vs. prediction_mortos_predictions
st.subheader('Gráfico de Dispersão: Hora vs. Mortos (predictions)')
sns.scatterplot(data=data, x='hora', y='prediction_mortos_predictions')
plt.xlabel('Hora')
plt.ylabel('Mortos (predictions)')
st.pyplot()

# Scatterplot: km_predictions vs. prediction_mortos_predictions
st.subheader('Gráfico de Dispersão: KM vs. Mortos (predictions)')
sns.scatterplot(data=data, x='km_predictions', y='prediction_mortos_predictions')
plt.xlabel('KM (predictions)')
plt.ylabel('Mortos (predictions)')
st.pyplot()
