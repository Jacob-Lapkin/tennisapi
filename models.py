from email.policy import default
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_login import UserMixin
from sqlalchemy import ForeignKey

ma = Marshmallow()
db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    key = db.Column(db.String(255))
    paid = db.Column(db.Boolean, default=False)

class Racquets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    brand = db.Column(db.String(255))
    name = db.Column(db.String(255))
    weight = db.Column(db.Integer)
    head_size = db.Column(db.Integer)
    release_year = db.Column(db.Integer, default = int(datetime.datetime.now().year))

class Tournamenttype(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    points = db.Column(db.Integer)
    draw_size = db.Column(db.Integer)
    purse = db.Column(db.Integer)
    tournament = db.relationship("Tournament", backref="tournamenttype")

class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    touramenttype_id = db.Column(db.Integer, db.ForeignKey('tournamenttype.id'))

# Schemas for serialization
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "key")

class RacquetsSchema(ma.Schema):
    class Meta:
        fields = ("id", "brand", "name", "weight", "head_size", "release_year")

class TournamenttypeSchema(ma.Schema):
    class Meta:
        fields = ("id", "points", "draw_size", "purse")

class TournamentSchema(ma.Schema):
    class Meta:
        fields= ("id", "name", "location", "tournamenttype_id")


User_schema = UserSchema()
Users_schema = UserSchema(many=True)

Racquet_schema = RacquetsSchema()
Racquets_schema = RacquetsSchema(many=True)

Tournamentype_schema = TournamenttypeSchema()
TournamentTypes_schema = TournamenttypeSchema(many = True)

Tournament_schema = TournamentSchema()
Tournaments_schema = TournamentSchema(many=True)
    
def seed_racquets():
    babolat_strike = Racquets(brand = "Babolat",
                                name = "Pure Strike",
                                weight = 323,
                                head_size = 98,
                                release_year = 2021)
        
    head_speed = Racquets(brand = "Head",
                            name = "Speed Pro",
                            weight = 326,
                            head_size = 100,
                            release_year = 2022)
    
    wilson_staff = Racquets(brand = "Wilson",
                            name = "Pro Staff",
                            weight = 332,
                            head_size = 97,
                            release_year = 2021)
    racquets = [babolat_strike, head_speed, wilson_staff]
    for i in racquets:
        db.session.add(i)
    db.session.commit()
    print("seeded database")

def seed_tournamenttype():
    slam = Tournamenttype(points=2000, draw_size= 128, purse=8000000)
    one_thousand = Tournamenttype(points=1000, draw_size=128, purse=4000000)
    five_hundred = Tournamenttype(points=500, draw_size=64, purse=1000000)
    db.session.add_all([slam, one_thousand, five_hundred])
    db.session.commit()
