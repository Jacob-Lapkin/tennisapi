from xmlrpc.client import Marshaller
from flask import Flask, redirect, render_template, jsonify, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
import stripe
from dotenv import load_dotenv
import os
from models import Racquets_schema, Users_schema, User, Racquets, db, seed_racquets, ma, seed_tournamenttype
from views.atp import atp
from views.rackets import rackets
from views.auth import auth
from views.home import homes
from api_key import generate_key

# loading dotenv
load_dotenv()

app = Flask(__name__)
# app configs
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
app.config["SECRET_KEY"] = "Change this"
db.init_app(app)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
login_manager.login_message_category = "danger"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Flask Mail 
# fill in mail config here

# blueprints
app.register_blueprint(atp)
app.register_blueprint(rackets)
app.register_blueprint(auth)
app.register_blueprint(homes)
# init bcrypt
bcrypt = Bcrypt(app)
# init json web token manager
app.config["JWT_SECRET_KEY"] = "Change this"
jwt_manager = JWTManager(app)
# init marshmallow
ma.init_app(app)

# stripe api key
stripe.api_key = os.environ.get('stripe_key')


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
        seed_tournamenttype()
        seed_racquets()


@app.route("/", methods=["POST", "GET"])
def index():
    if "email" in request.form and request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        check_user = User.query.filter_by(email = email).first()
        if check_user == None:
            flash("Email does not exist", "danger")
            return redirect(url_for("index"))
        if bcrypt.check_password_hash(check_user.password, password): 
            flash("User logged in", "success")
            login_user(check_user)
            session['user_id'] = check_user.id
            return redirect(url_for("home.home"))
        else: 
            flash("Password is incorrect", 'danger')
            return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/registering", methods=["GET", "POST"])
def registering():
    if "reg-email" in request.form and request.method == "POST": 
        name = request.form['reg-name']
        email = request.form['reg-email']
        password = request.form['reg-password']
        hashed_password = bcrypt.generate_password_hash(password)
        check_user = User.query.filter_by(email = email).first()
        if check_user:
            flash("Email already exists", "danger")
            return redirect(url_for("registering"))
        new_user = User(name = name, email = email, password = hashed_password, key=generate_key())
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(email = email).first()
        login_user(user)
        flash("Successfully registered", "success")
        return redirect(url_for("checkout"))
    return render_template("registering.html")

@app.route('/checkout', methods=["POST", "GET"])
@login_required
def checkout():
    return render_template('checkout.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
  session = stripe.checkout.Session.create(
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'Tennis API',
        },
        'unit_amount': 500,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url="http://localhost:5000/success?session_id={CHECKOUT_SESSION_ID}",
    cancel_url='http://localhost:5000/',
  )


  return redirect(session.url, code=303)

@app.route("/success")
def success():
    user_id = current_user.id
    try:
        session_id  = request.args.get('session_id')
        check_status = stripe.checkout.Session.retrieve(
    session_id)   
        if check_status['payment_status'] == "paid":
            print("This is Paid")
            user = User.query.filter_by(id=user_id).first()
            user.paid = True
            db.session.commit()
            return redirect(url_for('home.home'))
        else:
            return redirect(url_for('index'))
    except stripe.error.InvalidRequestError:
        return redirect(url_for('index'))
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')