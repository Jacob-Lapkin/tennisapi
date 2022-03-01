from flask import Flask, Blueprint, session, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from models import User, Racquets, User_schema, Users_schema, Racquet_schema, Racquets_schema, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user, login_required, logout_user

# login manager
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# bcrypt
bcrypt = Bcrypt()

auth = Blueprint("auth", __name__, url_prefix="")

@auth.route("/register", methods=["GET", "POST"])
def register():
    try: 
        user_info = request.get_json()
        name = user_info["name"]
        email =  user_info["email"]
        password = user_info['password']
        hashed_password = bcrypt.generate_password_hash(password)
        check_user = User.query.filter_by(email = email).first()
        if check_user:
            return jsonify(message = "Email already exists")
        new_user = User(name = name, email = email, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message = "Successfully registered"), 201

    except KeyError:
        return jsonify(message = "argumnet missing or incorrect"), 400

@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        try:
            user_info = request.get_json()
            email = user_info['email']
            password = user_info['password']
            check_user = User.query.filter_by(email = email).first()
            if check_user == False:
                return jsonify(message = "email does not exist")
            if bcrypt.check_password_hash(check_user.password, password):
                access_token = create_access_token(identity=email)
                return jsonify(message = "User logged in successfully", token = access_token), 200
            else: 
                return jsonify(message = "password is incorrect"), 401
        except KeyError:
            return jsonify(message = "argumnet missing or incorrect"), 400

@auth.route("/check", methods=["POST", "GET"])
def check_user():
    if request.method == "GET":
        email = request.args.get("email")
        name = request.args.get("name")
        print(email)
        print(name)
        user = User.query.filter(and_(User.email == email, User.name == name)).first()
        return jsonify(User = user.email, name = user.name)
        print("returned user")