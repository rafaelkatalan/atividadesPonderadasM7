import psycopg2
from flask import Flask, render_template, request, jsonify, redirect
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sqlalchemy import create_engine
import datetime

app = Flask(__name__)
jwt = JWTManager(app)
# Set your Flask app's secret key
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Set your JWT secret key
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_here'

@jwt.expired_token_loader
def handle_expired_token():
    return redirect(('/loginPage'))

@jwt.invalid_token_loader
def handle_invalid_token():
    return redirect(('/loginPage'))

@app.errorhandler(401)
def unauthorized(error):
    # Redirect the user to the login page
    return redirect(('/loginPage'))

def connect_to_db():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="senha",
        host="localhost",
        port="5432"
    )
    return connection


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
        access_token = create_access_token(identity=users[0])
        return redirect('/getnotes', code = 303)
    else:
        print('Login falhou')
        return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401

@app.route('/newnotePage')
@jwt_required()
def newnotePage():
    return render_template('newNote.html')

@app.route('/newnote', methods=['POST'])
@jwt_required()
def newnote():

    connection = connect_to_db()
    cursor = connection.cursor()
    title = request.form.get('title')
    content = request.form.get('content')
    to_do_date = request.form.get('date')  # Replace this with the actual timestamp
    print(title, content, to_do_date)
    # Use parameterized query to prevent SQL injection
    cursor.execute("INSERT INTO notes (title, content, to_do_date, user_id) VALUES (%s, %s, %s, %s)", (title, content, to_do_date, get_jwt_identity()))

    connection.commit()
    connection.close()

    return redirect('/getnotes')

@app.route('/getnotes', methods=['GET'])
@jwt_required()
def getnotes():
    
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM notes WHERE user_id = '{get_jwt_identity()}'")
    notes = cursor.fetchall()
    print(notes)
    connection.close()
    return render_template('notes.html', notes=notes)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

# Cria a instância da engine do banco de dados
#alchemyEngine = create_engine('postgresql+psycopg2://postgres:senha@127.0.0.1:5432', pool_recycle=3600);

#dbConnection = alchemyEngine.connect()

