from flask import Flask, redirect, render_template, url_for, session, jsonify, flash, Blueprint
from flask_login import current_user, login_required
from models import db, User_schema, Users_schema, Racquet_schema, Racquets_schema, Racquets

homes = Blueprint("home", __name__, url_prefix="")

@homes.route("/home", methods=["POST", "GET"])
@login_required
def home():
    
    if current_user.paid == False:
        flash("You must pay before accessing your API Key", "danger")
        return redirect(url_for('checkout'))
    return render_template("home.html")