import psycopg2
from flask import Flask, render_template, request, jsonify, redirect, session
from flask_jwt_extended import JWTManager, create_access_token, decode_token
#import joblib
import subprocess
import random
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
#para usar o modelo real importe a biblioteca pycaret com o comando a baixo:
#from pycaret.classification import load_model, predict_model


#para usar o modelo real execute a linha a baixo
#modelo = joblib.load('lgbmregressor.pkl')


app = Flask(__name__)
app.secret_key = 'any random string'
jwt = JWTManager(app)

def connect_to_db():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="senha",
        host="db",
        port="5432"
    )
    return connection

def checkUser():
    connection = connect_to_db()
    cursor = connection.cursor()
    access_token = session['access_token']
    current_user = decode_token(access_token)['sub']
    cursor.execute(f"SELECT * FROM users WHERE username = '{current_user[1]}'")
    user = cursor.fetchone()
    try:
        if user[2] == current_user[2]:
            return True, user
        else:
            return False, user
    except:
        return False, user
    

    
@app.route('/loginPage')
def loginPage():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    connection = connect_to_db()
    cursor = connection.cursor()
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    users = cursor.fetchone()
    connection.close()
    if password == users[2]:
        access_token = create_access_token(identity=users)
        print(access_token)
        session['access_token'] = access_token
        print('Login realizado com sucesso')
        return redirect('/inputData')
    else:
        print('Login falhou')
        return jsonify({'status': 'fail, wrong password or username'})
    
@app.route('/inputData', methods=['GET','POST'])
def inputData():
    user = checkUser()
    if user[0]:
        if request.method == 'POST':
            # Obtém os dados do formulário
            km = request.form['km']
            automovel = request.form['automovel']
            bicicleta = request.form['bicicleta']
            caminhao = request.form['caminhao']
            moto = request.form['moto']
            onibus = request.form['onibus']
            outros = request.form['outros']
            tracao_animal = request.form['tracao_animal']
            transporte_de_cargas_especiais = request.form['transporte_de_cargas_especiais']
            trator_maquinas = request.form['trator_maquinas']
            utilitarios = request.form['utilitarios']
            hora = request.form['hora']

            #para usar o modelo real descomente as linhas a baixo e comente a linha 98
            #dados = [[km, automovel, bicicleta, caminhao, moto, onibus, outros, tracao_animal, transporte_de_cargas_especiais, trator_maquinas, utilitarios, prediction_mortos, hora]]
            #resultado = modelo.predict(dados)
            # O resultado é a previsão para 'prediction_mortos'
            #resultado = resultado[0]

            resultado = random.randint(0, 10)



            # Conecta-se ao banco de dados PostgreSQL
            connection = connect_to_db()
            cursor = connection.cursor()

            # Insere os dados na tabela
            cursor.execute("INSERT INTO predictions (km, automovel, bicicleta, caminhao, moto, onibus, outros, tracao_animal, transporte_de_cargas_especiais, trator_maquinas, utilitarios, prediction_mortos, hora) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (km, automovel, bicicleta, caminhao, moto, onibus, outros, tracao_animal, transporte_de_cargas_especiais, trator_maquinas, utilitarios, resultado, hora))
            
            # Commit e fecha a conexão
            connection.commit()
            connection.close()

            return redirect('/dashboards')
        else:
            try:
                return render_template('input.html')
            except:
                return redirect('/loginPage')
    else:
        return redirect('/loginPage')

@app.route('/dashboards')
def dashboards():
    user = checkUser()
    if user[0]:
        connection = connect_to_db()
        cursor = connection.cursor()

        # SQL query to obtain the required data by joining 'rawdata' and 'predictions' tables
        cursor.execute('''
            SELECT
                r.hora,
                r.mortos AS mortos_rawdata,
                r.km AS km_rawdata
            FROM
                rawdata AS r
            ORDER BY r.hora DESC
        ''')

        data1 = cursor.fetchall()

        cursor.execute('''
            SELECT
                p.hora,
                p.prediction_mortos AS mortos_prediction,
                p.km AS km_prediction
            FROM
                predictions AS p
            ORDER BY p.hora DESC
            
        ''')

        data2 = cursor.fetchall()
                       

        # Close the database connection
        connection.close()
        column_names1 = ['hora', 'mortos_rawdata', 'km_rawdata']
        column_names2 = ['hora', 'prediction_mortos_predictions', 'km_predictions']
        
        df = pd.DataFrame(data1, columns=column_names1)
        df2 = pd.DataFrame(data2, columns=column_names2)
        print(df.columns)

        plt.plot(df['hora'], df['mortos_rawdata'], label='Mortos')
        plt.xlabel('hora')
        plt.ylabel('mortos_rawdata')

        buffer1 = io.BytesIO()
        plt.savefig(buffer1, format='png')
        buffer1.seek(0)

        plot_data1 = base64.b64encode(buffer1.read()).decode()
        plt.clf()
        plt.plot(df2['hora'], df2['prediction_mortos_predictions'], label='Prediction')
        plt.xlabel('hora')
        plt.ylabel('prediction_mortos_predictions')
 
        buffer2 = io.BytesIO()
        plt.savefig(buffer2, format='png')
        buffer2.seek(0)

        plot_data2 = base64.b64encode(buffer2.read()).decode()

        return render_template('dashboard.html', plot_data1=plot_data1, plot_data2=plot_data2)
    else:
        return redirect('/loginPage')
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)