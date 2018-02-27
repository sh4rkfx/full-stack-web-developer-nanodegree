"""Contains all raw data models and structures."""

from datetime import datetime
from src import db


class Category(db.Model):
    """Contain the Category details."""

    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.Text, nullable=False, unique=True)
    category_description = db.Column(db.Text, nullable=False)
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False,
                           server_default='f')
    category_slug = db.Column(db.String, nullable=False, unique=True)
    created_by = db.Column(db.Integer, default=1, server_default='1')
    created_datetime = db.Column(db.DateTime, default=datetime.now())
    last_modified_datetime = db.Column(db.DateTime, nullable=True)

    def __init__(self, category_name, category_description):
        """Receive data for new item."""
        self.category_name = category_name
        self.category_description = category_description
        self.is_deleted = False
        self.created_by = 1
        self.created_datetime = datetime.now()
        self.category_slug = category_name.replace(" ", "-").lower()

    def __repr__(self):
        """Instance Representation."""
        return str(self.category_name)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'category_id'         : self.category_id,
            'category_name'       : self.category_name,
            'category_description': self.category_description,
            'category_slug'       : self.category_slug
        }

class Item(db.Model):
    """Contain the Item details."""

    __tablename__ = 'items'

    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text, nullable=False, unique=True)
    item_description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.category_id))
    category = db.relationship(Category, backref=db.backref(
                               'items', lazy='dynamic'))
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False,
                           server_default='f')
    item_slug = db.Column(db.String, nullable=False, unique=True)
    created_by = db.Column(db.Integer, default=1, server_default='1')
    created_datetime = db.Column(db.DateTime, default=datetime.now())
    last_modified_datetime = db.Column(db.DateTime, nullable=True)

    def __init__(self, item_name, item_description, category, created_by):
        """Receive data for new item."""
        self.item_name = item_name
        self.item_description = item_description
        self.category = category
        self.is_deleted = False
        self.created_by = created_by
        self.created_datetime = datetime.now()
        self.item_slug = item_name.replace(" ", "-").lower()
        self.item_category = self.build_item_category()

    def __repr__(self):
        """Instance Representation."""
        return str(self.item_name)

    def build_item_category(self):
        """Display the category for the item instance."""
        return str(self.item_name) + str(self.category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'item_id'         : self.item_id,
            'item_name'       : self.item_name,
            'item_description': self.item_description,
            'item_slug'       : self.item_slug
        }
