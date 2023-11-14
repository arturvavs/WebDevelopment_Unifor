from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for,jsonify
#from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ='@root123'

    from .views import views
    from .auth import auth
    from .models import models
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
