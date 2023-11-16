from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
import json
from application.models import MongoDB
from application.models import User

auth = Blueprint('auth', __name__)

db = MongoDB() #Instancio a classe MongoDB
user = User()

@auth.route('/home')
def home():
    return render_template("home.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('userName').upper()
        password = request.form.get('passWord')
        validation = user.userLogin(username, password)
        if validation:
            return redirect(url_for('views.user_management'))
        flash('Falha na autenticação do usuário', category='error')
    return render_template("login.html")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('firstName').upper()
        last_name = request.form.get('lastName').upper()
        username = request.form.get('userName').upper()
        user_email = request.form.get('userEmail').upper()
        password = request.form.get('passWord')
        if not all([first_name, last_name, username, user_email, password]):
            flash('Existem campos no formulário não preenchidos', category='error')
            return render_template("register.html")
        validation = user.userRegister(first_name, last_name, username, user_email, password)
        if validation:
            flash('Cadastro efetuado com sucesso!', category='success')
            return redirect(url_for('views.login'))
        flash('Nome de usuário ou email já utilizados', category='error')
    return render_template("register.html")


@auth.route('/user_management', methods=['GET', 'POST'])
def user_management():
    if request.method == 'POST':
        search_type = request.form.get('searchType')
        search_input = request.form.get('searchInput').upper()
    else:
        search_type = request.args.get('searchType')
        search_input = request.args.get('searchInput').upper()
    users = user.listUser(search_type, search_input)
    decoded_result = json.loads(users)
    return render_template("user_management.html", decoded_result=decoded_result)


@auth.route('/user_management/<string:username>', methods=['DELETE'])
def delete_user(username):
    if request.method == 'DELETE':
        user.deleteUser(username)
        return jsonify({'mensagem': f'Usuário {username} excluído com sucesso'})