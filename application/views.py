from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")

@views.route('/user_management')
def user_management():
    return render_template("user_management.html")

@views.route('/register')
def user_register():
    return render_template("register.html")

@views.route('/login')
def login():
    return render_template("login.html")