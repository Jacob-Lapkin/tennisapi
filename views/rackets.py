from click import argument
from flask import Flask, Blueprint, session, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from models import User, Racquet_schema, Racquets, Racquets_schema, Users_schema, User_schema, db
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager


rackets = Blueprint("rackets", __name__, url_prefix="")

@rackets.route("/racquets", methods=["POST", "GET"])
def racquets():
    if request.method == "GET":
        all_arguments = request.args
        brand = request.args.get("brand")
        name = request.args.get("name")
        weight = request.args.get("weight")
        head_size = request.args.get("head_size")
        list_of_args = ["brand", "name", "weight", "head_size"]
        for key, value in all_arguments.items():
            if key not in list_of_args:
                return jsonify(message = "There was an invalid argument"), 400
        try:
            finished_filtering = Racquets.query.filter_by(**all_arguments).all()
            if len(finished_filtering) == 0:
                return jsonify(message = "No racquets exist with those arguments"), 400
            finished_serialized = Racquets_schema.dump(finished_filtering)
            return jsonify(Racquets = finished_serialized)
        except KeyError:
            return jsonify(message="invalid arguments"), 400
    if request.method == "POST":
        racquets = request.get_json()
        required_specs = ["brand", "name", "head_size", "weight", "release_year"]
        for i in racquets.keys():
            if i not in required_specs:
                return jsonify(message = "Invalid Arguments. you must post 'brand', 'name', 'head_size', 'weight', and 'release_year'"), 400
        if len(racquets) != 5:
            return jsonify(message = "You must include all required data. This API aims to be as descriptive as possible"), 400
        brand = racquets['brand']
        name = racquets['name']
        head_size = racquets['head_size']
        weight = racquets['weight']
        release_year = racquets['release_year']
        search_racquet = Racquets.query.filter_by(brand = brand, name=name, head_size=head_size, weight=weight, release_year=release_year).first()
        # check if integer or float
        print(type(weight))
        def check_type(argument):
            if type(argument) == int or type(argument) == float:
                return True
            else:
                return False
        for i in [weight, head_size, release_year]:
            if check_type(i) == False:
                return jsonify(message = f'you must provide an integer or float argument for weight, head_size, and release_year. you posted {i} not as an integer nor float')
        if search_racquet:
            return jsonify(message="Sorry, this racquet already exists in the database"), 400
        if search_racquet != True:
            new_racquet = Racquets(brand = brand, name=name, head_size=(head_size), weight=weight, release_year=release_year)
            db.session.add(new_racquet)
            db.session.commit()
            return jsonify(message = "Racquet added to database"), 201
        return jsonify(racquets)

        
