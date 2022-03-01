from flask import Flask, redirect, render_template, session, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from models import User, Racquet_schema, Racquets, Racquets_schema, Users_schema, User_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

db = SQLAlchemy()
atp = Blueprint('atp', __name__, url_prefix="")

@atp.route("/atp", methods=["GET", "POST"])
def atp_players():
    print("this is atp players")
    return jsonify(message = "this is a page for ATP players")