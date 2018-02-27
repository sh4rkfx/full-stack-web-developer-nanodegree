"""User Authentication Models."""

from flask_login import UserMixin
from src import db


class User(UserMixin, db.Model):
    """Simple User Details."""

    id = db.Column(db.Integer, primary_key=True)
    oauth_site = db.Column(db.String(250), nullable=False)
    social_id = db.Column(db.String(250), nullable=False)
    user_name = db.Column(db.String(250))
    is_authenticated = db.Column(db.Boolean(), nullable=False, default=False,
                                 server_default='f')
