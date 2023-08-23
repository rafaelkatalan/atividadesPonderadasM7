import psycopg2
from flask import Flask, render_template, request, jsonify, redirect
from sqlalchemy import create_engine
import datetime

app = Flask(__name__)

def connect_to_db():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="senha",
        host="localhost",
        port="5432"
    )
    return connection

def checkUser():
    connection = connect_to_db()
    cursor = connection.cursor()
    user = 'userTeste'
    cursor.execute(f"SELECT * FROM users WHERE username = '{user}'")
    user = cursor.fetchone()
    if user[2] == 'teste123':
        return [True, user[0]]

#@app.route('/')
#def index():
#    return render_template('index.html')

@app.route('/loginPage')
def loginPage():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    #read user and password from db
    connection = connect_to_db()
    cursor = connection.cursor()
    username = request.form.get('username')
    password = request.form.get('password')
    print(username, password)
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    users = cursor.fetchone()
    print(users)
    connection.close()
    if password == users[2]:
        print('Login realizado com sucesso')
        return jsonify({'status': 'success'})
    else:
        print('Login falhou')
        return jsonify({'status': 'fail'})

@app.route('/newnotePage')
def newnotePage():
    return render_template('newNote.html')

@app.route('/newnote', methods=['POST'])
def newnote():
    user = checkUser()
    if user[0]:
        
        connection = connect_to_db()
        cursor = connection.cursor()
        title = request.form.get('title')
        content = request.form.get('content')
        to_do_date = request.form.get('date')  # Replace this with the actual timestamp
        print(title, content, to_do_date)
        # Use parameterized query to prevent SQL injection
        cursor.execute("INSERT INTO notes (title, content, to_do_date, user_id) VALUES (%s, %s, %s, %s)", (title, content, to_do_date, user[1]))

        connection.commit()
        connection.close()

        return redirect('/getnotes')
    else:
        return jsonify({'status': 'fail'})

@app.route('/getnotes', methods=['GET'])
def getnotes():
    user = checkUser()
    if user[0]:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM notes WHERE user_id = '{user[1]}'")
        notes = cursor.fetchall()
        print(notes)
        connection.close()
        return render_template('notes.html', notes=notes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

# Cria a instância da engine do banco de dados
#alchemyEngine = create_engine('postgresql+psycopg2://postgres:senha@127.0.0.1:5432', pool_recycle=3600);

#dbConnection = alchemyEngine.connect()

