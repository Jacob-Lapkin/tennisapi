from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow

ma = Marshmallow()
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    key = db.Column(db.String(255))

class Racquets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    brand = db.Column(db.String(255))
    name = db.Column(db.String(255))
    weight = db.Column(db.Integer)
    head_size = db.Column(db.Integer)
    release_year = db.Column(db.Integer, default = int(datetime.datetime.now().year))

# Schemas for serialization
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "key")

class RacquetsSchema(ma.Schema):
    class Meta:
        fields = ("id", "brand", "name", "weight", "head_size", "release_year")

User_schema = UserSchema()
Users_schema = UserSchema(many=True)

Racquet_schema = RacquetsSchema()
Racquets_schema = RacquetsSchema(many=True)
    
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