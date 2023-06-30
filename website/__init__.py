from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Monday Mfon'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
db.init_app(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(int(user_id))

from website.user import user
from auth import auth
from website.product import product
from website.cart import cart
from website.models import User, Product, Cart

app.register_blueprint(user, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(product, url_prefix='/')
app.register_blueprint(cart, url_prefix='/')

def create_database(app):
    if not path.exist('website/' + "database.db"):
        db.create_all(app=app)
        print("Database Created")