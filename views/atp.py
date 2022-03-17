import json
from click import argument
from flask import Flask, redirect, render_template, session, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from models import User, Racquet_schema, Racquets, Racquets_schema, Users_schema, User_schema, Tournamenttype, TournamentTypes_schema, Tournamentype_schema, Tournament, Tournament_schema, Tournaments_schema, db
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests
import pandas as pd
from api_key import check_key

atp = Blueprint('atp', __name__, url_prefix="")

@atp.route("/atp/greats/<key>", methods=["GET", "POST"])
def atp_players(key:int):
    greats = {
        "1" : {"Name": "Rafael Nadal", "Grand Slams": 21},
        "2" : {"Name": "Roger Federer", 'Grand Slams':20},
        "3" : {"Name": "Novak Djokovic", 'Grand Slams':20},
        "4" : {"Name": "Pete Sampras", 'Grand Slams':14}, 
        "5" : {"Name": "Bjorn Borg", 'Grand Slams':11}, 
        "6" : {"Name": "Rodney Laver", 'Grand Slams':11}, 
        "7" : {"Name": "Andre Agassi", 'Grand Slams':8}, 
        "8" : {"Name": "James Connor", 'Grand Slams':8}, 
        "9" : {"Name": "Andrew Murray", 'Grand Slams':3}, 
        "10" : {"Name": "John McEnroe", 'Grand Slams':7}, 
    }
    if not check_key(key):
        return jsonify(message = "this API key does not exist in our record"), 400
    else:
        return jsonify(All_Time_Greats = greats)

@atp.route("/atp/rankings/<key>", methods=["POST", "GET"])
def atp_rankings(key:int):
    if not check_key(key):
        return jsonify(message = "this API key does not exist in our record"), 400
    else: 
        url = requests.get("https://www.atptour.com/en/rankings/singles")
        rankings_tables = pd.read_html(url.text)
        rankings = rankings_tables[0]
        rankings_w_drop = rankings.drop(['+/-Rank','Unnamed: 2'], axis=1)
        ranking_dict = rankings_w_drop.to_dict("records")
        return jsonify(ATP_Rankings = ranking_dict)

@atp.route("/atp/stats/<stat>/<key>", methods=["POST", "GET"])
def scores(stat, key:int):
    if not check_key(key):
        return jsonify(message = "this API key does not exist in our record"), 400
    else: 
        try: 
            url = ""
            if stat == "service-games-won":
                url = requests.get("https://www.atptour.com/en/stats/service-games-won")
            if stat == "aces":
                url = requests.get("https://www.atptour.com/en/stats/aces/all/all/all/")
            if stat == "return-games-won":
                url = requests.get("https://www.atptour.com/en/stats/return-games-won/all/all/all/")
            if stat == "break-points-converted":
                url = requests.get("https://www.atptour.com/en/stats/break-points-converted/all/all/all/")
            stats = pd.read_html(url.text)
            stats_table = stats[0]
            stats_dict = stats_table.to_dict("records")
        except AttributeError:
            return jsonify(message = "Incorrect statistic inputted"), 400
        return jsonify({stat : stats_dict})
        # return jsonify(Todays_scores = scores_dict)

@atp.route('/atp/tournaments', methods=["GET","POST"])
def tournament():
    try:
        tournament_data = request.get_json()
        arguments = ["name", "location", "points", "key"]
        post_arguments = tournament_data.keys()
        for i in post_arguments:
            if i not in arguments:
                return jsonify(message = "You are missing arguments"), 400
        key = tournament_data['key']
        if not check_key(key):
            return jsonify(message = "This API key does not exist in our record"), 400
        name = tournament_data['name']
        location = tournament_data['location']
        points = tournament_data['points']
        
        find_tourn_type = Tournamenttype.query.filter_by(points = int(points)).first()
        if not find_tourn_type:
            return jsonify("No tournament exists with that point level"), 400
        check_exists = Tournament.query.filter_by(name=name).first()
        if check_exists:
            return jsonify(message="This tournament name seems to already exists"), 400
        new_tournament = Tournament(name = name, location = location, touramenttype_id = find_tourn_type.id)
        db.session.add(new_tournament)
        db.session.commit()
        return jsonify(message = "Successfully added tournament"), 200
    except KeyError:
        return jsonify(message = "There is a missing argument"), 400