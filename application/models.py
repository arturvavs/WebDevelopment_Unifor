
from flask import Blueprint, render_template, request, flash, redirect, url_for,jsonify
from pymongo import MongoClient
import json

models = Blueprint('models',__name__)

class MongoDB():
    def __init__(self):
        self.username = 'root'
        self.password = 'root123'
        self.cluster_name = 'cluster0'
        self.database_name = 'webDevelopement'
        self.mongoURL = f"mongodb+srv://{self.username}:{self.password}@{self.cluster_name}.o64y1wi.mongodb.net/?retryWrites=true&w=majority"
        self.client = None
        self.db = None
    
    def dbConnect(self):
        try:
            # Conecta ao cluster MongoDB Atlas
            self.client = MongoClient(self.mongoURL)

            # Acessa o banco de dados
            self.db = self.client[self.database_name]

            print("Conexão ao MongoDB Atlas estabelecida com sucesso!")

        except Exception as error:
            print(f"Erro ao conectar ao MongoDB Atlas: {error}")

    def dbDisconnect(self):
        if self.client:
            self.client.close()
            print("Conexão ao MongoDB Atlas encerrada.")

    #def userLogin(self):
    #    self.dbConnect
        
'''uri = "mongodb+srv://root:root123@cluster0.o64y1wi.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.webDevelopement
firstName = 'admin2'
userName = 'admin'
atributos = {"_id":0,"NM_PRIMEIRO_NOME":1,"NM_ULTIMO_NOME":1,"NM_USUARIO":1,"DS_EMAIL":1}
usuarios = list(db.user.find({},atributos))
for usuario in usuarios:
    print(usuario)'''


    
class User(MongoDB):
    def __init__(self):
        super().__init__()
        self.userId = None
        self.userName = None
        self.firstName = None
        self.lastName = None
        self.passWord = None
        self.email = None
        

    def userLogin(self,userName,passWord):
        validation = False
        self.dbConnect()
        try:
            user = self.db.user.find_one({"NM_USUARIO": userName}, {"NM_USUARIO": 1})
            password = self.db.user.find_one({"NM_USUARIO": userName}, {"DS_SENHA": 1})
            if user:
                select_user = user.get('NM_USUARIO')
                select_senha = password.get('DS_SENHA')
                if (select_senha == passWord) and (userName == select_user):
                    validation = True
                else:
                    validation = False
        except Exception as error:
            return "Falha ao executar função:", {error}
        return validation


    def userRegister(self,firstName,lastName,userName,userEmail,passWord):
        self.dbConnect()
        validation = False
        try:
            user = self.db.user.find_one({"NM_USUARIO": userName}, {"NM_USUARIO": 1})
            email = self.db.user.find_one({"DS_EMAIL": userEmail}, {"DS_EMAIL": 1})
            if user:
                return 'Usuário já cadastrado'
            else:
                if email:
                    return 'Email já está em uso'
                else:
                    self.db.user.insert_one({"NM_USUARIO":userName,
                                        "NM_PRIMEIRO_NOME":firstName,
                                        "NM_ULTIMO_NOME":lastName,
                                        "DS_EMAIL":userEmail,
                                        "DS_SENHA":passWord}
                                        )
                    validation = True
        except Exception as error:
            return "Falha ao executar função:", {error}
        return validation
            
    def listUsers(self):
        self.dbConnect()
        atributos = {"_id":0,"NM_PRIMEIRO_NOME":1,"NM_ULTIMO_NOME":1,"NM_USUARIO":1,"DS_EMAIL":1}
        usuarios = list(self.db.user.find({},atributos))
        json_result = json.dumps(usuarios)
        return json_result
   
        