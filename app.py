from xmlrpc.client import Marshaller
from flask import Flask, redirect, render_template, jsonify, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from models import Racquets_schema, Users_schema, User, Racquets, db, seed_racquets, ma
from views.atp import atp
from views.rackets import rackets
from views.auth import auth, login_manager

app = Flask(__name__)
# app configs
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
app.config["SECRET_KEY"] = "Change this"
db.init_app(app)

# login manager
login_manager.init_app(app)

# blueprints
app.register_blueprint(atp)
app.register_blueprint(rackets)
app.register_blueprint(auth)
# init bcrypt
bcrypt = Bcrypt(app)
# init json web token manager
app.config["JWT_SECRET_KEY"] = "Change this"
jwt_manager = JWTManager(app)
# init marshmallow
ma.init_app(app)

#################################
######### database functions #########
#################################
def db_create():
    with app.app_context():
        db.create_all()
        print("created database")
def db_drop():
    with app.app_context():
        db.drop_all()
        print("dropped database")
def db_seed():
    with app.app_context():
        seed_racquets()


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')