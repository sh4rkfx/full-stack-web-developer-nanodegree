"""Product Related Forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    """Form to handle category details."""

    category_slug = HiddenField(label='slug')
    category_name = StringField('Category', validators=[DataRequired()],
                                render_kw={'class': 'form-control'})
    category_description = StringField(u'Description', widget=TextArea(),
                                       validators=[DataRequired()],
                                       render_kw={'class': 'form-control'})
    upload_submit = SubmitField('Save Details',
                                render_kw={'class': 'btn btn-primary mybtn'})


class ItemForm(FlaskForm):
    """Form to handle category details."""

    item_slug = HiddenField(label='slug')
    item_name = StringField('Item Name', validators=[DataRequired()],
                            render_kw={'class': 'form-control'})
    item_description = StringField(u'Description', widget=TextArea(),
                                   validators=[DataRequired()],
                                   render_kw={'class': 'form-control'})
    category = QuerySelectField(label=u"Category", allow_blank=False,
                                validators=[DataRequired()],
                                render_kw={'class': 'form-control'})

    upload_submit = SubmitField('Save Details',
                                render_kw={'class': 'btn btn-primary mybtn'})
