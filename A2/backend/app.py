import psycopg2
from flask import Flask, render_template, request, jsonify, redirect, session
from flask_jwt_extended import JWTManager, create_access_token, decode_token

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
        return redirect('/getnotes')
    else:
        print('Login falhou')
        return jsonify({'status': 'fail, wrong password or username'})

@app.route('/newnotePage')
def newnotePage():
    return render_template('newNote.html')

@app.route('/newnote', methods=['POST'])
def newnote():
    user = checkUser()
    if user[0]:
        access_token = session['access_token']
        current_user = decode_token(access_token)['sub']
        connection = connect_to_db()
        cursor = connection.cursor()
        title = request.form.get('title')
        content = request.form.get('content')
        to_do_date = request.form.get('date')
        cursor.execute("INSERT INTO notes (title, content, to_do_date, user_id) VALUES (%s, %s, %s, %s)", (title, content, to_do_date, current_user[0]))

        connection.commit()
        connection.close()

        return redirect('/getnotes')
    else:
        return redirect('/loginPage')

@app.route('/getnotes', methods=['GET'])
def getnotes():
    user = checkUser()
    if user[0]:
        access_token = session['access_token']
        current_user = decode_token(access_token)['sub']
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM notes WHERE user_id = {current_user[0]}")
        notes = cursor.fetchall()
        connection.close()
        return render_template('notes.html', notes=notes)
    else:
        return redirect('/loginPage')
    
@app.route('/removenote', methods=['POST'])
def removenote():
    user = checkUser()
    if user[0]:
        connection = connect_to_db()
        cursor = connection.cursor()
        id = request.form.get('id')
        cursor.execute(f"DELETE FROM notes WHERE id = {id}")
        connection.commit()
        connection.close()
        return redirect('/getnotes')
    else:
        return redirect('/loginPage')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)