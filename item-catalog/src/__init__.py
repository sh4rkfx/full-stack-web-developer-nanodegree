"""Main File."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
import sqlite3


# pylint: disable=invalid-name

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
oauth = OAuth(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


from src.auth.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


# Import Blueprint from view at the bottom of the init file
from src.products.views import prods_blueprint
from src.auth.views import auth_blueprint

# BluePrints Listing
app.register_blueprint(prods_blueprint)
app.register_blueprint(auth_blueprint)
