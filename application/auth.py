from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from pymongo import MongoClient
from flask import current_app
import json
from application.models import MongoDB
from application.models import User

auth = Blueprint('auth', __name__)

db = MongoDB() #Instancio a classe MongoDB
user = User()
@auth.route('/')
def conexao_teste():
    print('entrou conexao teste')
    return jsonify({'mensagem': 'Conexão bem-sucedida ao MongoDB Atlas!'})


@auth.route('/home')
def home():
    print(jsonify({'mensagem': 'Conexão bem-sucedida ao MongoDB Atlas!'}))
    return render_template("home.html")


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST':
        userName = request.form.get('userName').upper()
        passWord = request.form.get('passWord')
        print(userName,passWord)
        validation = user.userLogin(userName,passWord)
        if validation == True:
            return redirect(url_for('views.user_managemant'))
        else:
            flash('Falha na autenticação do usuário',category='error')   
    else:
        print('Error ao executar função login')
    return render_template("login.html")

@auth.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        firstName = request.form.get('firstName').upper()
        lastName = request.form.get('lastName').upper()
        userName = request.form.get('userName').upper()
        userEmail = request.form.get('userEmail').upper()
        passWord = request.form.get('passWord')
        if not firstName or not lastName or not userName or not userEmail or not passWord:
            flash('Existe campos no formulário não preenchidos', category='error')
            return render_template("register.html")
        else:
            validation = user.userRegister(firstName,lastName,userName,userEmail,passWord)
            if validation == True:
                flash('Cadastro efetuado com sucesso!', category='success')
                return redirect(url_for('views.login'))
            else:
                print('Falha no registro do usuário')
                flash('Nome de usuário ou email já utilizados', category='error')
                return render_template("register.html")

    return render_template("register.html")

@auth.route('/user_management', methods=['GET','POST'])
def user_management():
    if request.method == 'GET':
        print('entrou no get user_management')
        users = user.listUsers()
        decoded_result = json.loads(users)
    return render_template("user_management.html",decoded_result=decoded_result)