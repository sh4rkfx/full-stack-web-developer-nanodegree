"""Contains the products endpoints."""

from flask import Blueprint, render_template, request, flash, redirect, jsonify
from flask import url_for, abort
from flask_login import current_user, login_required
from src import db, app
from . import forms, models
import sqlite3

# pylint: disable=invalid-name
# Create a blueprint to contain all the products views and items
prods_blueprint = Blueprint('products', __name__, template_folder='templates')


@prods_blueprint.route('/items.json')
def item_listing():
    item_list = fetch_full_listing()
    return jsonify(json_list=[i.serialize for i in item_list])


@prods_blueprint.route('/items/category/<category_slug>.json')
@prods_blueprint.route('/items/category/<category_slug>')
@prods_blueprint.route('/')
def index(category_slug=None):
    """Home Page listing of products."""
    sort_order = models.Category.category_name.asc()
    category_list = (models.Category.query
                     .filter(models.Category.is_deleted == False)
                     .order_by(sort_order).all())
    if category_slug:
        item_list = fetch_category_items_list(category_slug)
    else:
        item_list = fetch_latest_items_list()
    if 'json' in request.path:
        return jsonify(json_list=[i.serialize for i in item_list])
    return render_template('items_list.html', category_list=category_list,
                           item_list=item_list, category_slug=category_slug)


@prods_blueprint.route('/categories/<category_slug>', methods=['GET', 'POST'])
@prods_blueprint.route('/categories/<category_slug>/<action_page>',
                       methods=['GET', 'POST'])
def category_details_action(category_slug, action_page=None):
    """View, Edit and Delete category details."""
    filter1 = models.Category.is_deleted == False
    filter2 = models.Category.category_slug == category_slug
    my_category = (models.Category.query
                   .filter(filter1)
                   .filter(filter2)
                   .first_or_404())
    category_form = forms.CategoryForm(obj=my_category)
    if request.method == 'POST':
        if category_form.validate_on_submit():
            category_slug = category_form.category_slug.data
            filter2 = models.Category.category_slug == category_slug
            my_category = (models.Category.query
                           .filter(filter2)
                           .first_or_404())
            if not my_category:
                abort(404)
            if action_page == 'edit':
                my_category.category_name = category_form.category_name.data
                my_category.category_description = (category_form.
                                                    category_description.data)
                db.session.commit()
                flash('Category details updated successfully', 'success')
            elif action_page == 'delete':
                my_category.is_deleted = True
                db.session.commit()
                flash('Category deleted', 'info')
                return jsonify(redirect_url=str(url_for('products.index')))
            return redirect(url_for('products.index'))
        else:
            flash_errors(category_form)
    if action_page is None:
        actionstate = 'readmode'
    else:
        actionstate = 'editmode'

    return render_template('category_details.html', actionstate=actionstate,
                           form=category_form, category_slug=category_slug)


@prods_blueprint.route('/categories/create', methods=['GET', 'POST'])
def category_details():
    """Capture new category details."""
    category_form = forms.CategoryForm()
    if request.method == 'POST':
        if category_form.validate_on_submit():
            new_category = models.Category(
                category_name=category_form.category_name.data,
                category_description=category_form.category_description.data)
            db.session.add(new_category)
            db.session.commit()

            flash('Category details submitted successfully', 'success')
            return redirect(url_for('products.index'))
            # return str(request.form)
        else:
            flash_errors(category_form)
            # flash('Error on category details.', 'error')
    return render_template('category_details.html', form=category_form,
                           actionstate='createmode')


@prods_blueprint.route('/items/create', methods=['GET', 'POST'])
@login_required
def new_items_details():
    """Capture new items details."""
    item_form = forms.ItemForm()
    category_count = count_category_list()
    if category_count < 1:
        new_category = models.Category(
            category_name='Default Category',
            category_description='Default Category')
        db.session.add(new_category)
        db.session.commit()
    item_form.category.query = fetch_category_list()

    if request.method == 'POST':
        if item_form.validate_on_submit():
            new_item = models.Item(
                item_name=item_form.item_name.data,
                item_description=item_form.item_description.data,
                category=item_form.category.data,
                created_by=current_user.id)
            db.session.add(new_item)
            db.session.commit()

            flash('Item details submitted successfully', 'success')
            return redirect(url_for('products.index'))
        else:
            flash_errors(item_form)
            # flash('Error on category details.', 'error')
    return render_template('item_details.html', form=item_form,
                           actionstate='createmode')


@prods_blueprint.route('/items/<item_slug>/<action_page>',
                       methods=['GET', 'POST'])
@login_required
def item_details_action(item_slug, action_page=None):
    """View, Edit and Delete item details."""
    filter1 = models.Item.is_deleted == False
    filter2 = models.Item.item_slug == item_slug
    my_item = (models.Item.query
               .filter(filter1)
               .filter(filter2)
               .first_or_404())
    item_form = forms.ItemForm(obj=my_item)
    item_form.category.query = fetch_category_list()
    if request.method == 'POST':
        if item_form.validate_on_submit():
            item_slug = item_form.item_slug.data
            filter2 = models.Item.item_slug == item_slug
            my_item = (models.Item.query
                             .filter(filter2)
                             .first_or_404())
            if not my_item:
                abort(404)
            if action_page == 'edit':
                if current_user.id == my_item.created_by:
                    my_item.item_name = item_form.item_name.data
                    my_item.item_description = item_form.item_description.data
                    my_item.category = item_form.category.data
                    db.session.commit()
                    flash('Item details updated successfully', 'success')
                else:
                    flash('Details not updated, user not authorized', 'error')
            elif action_page == 'delete':
                if current_user.id == my_item.created_by:
                    my_item.is_deleted = True
                    db.session.commit()
                    flash('Item deleted', 'info')
                    return jsonify(redirect_url=str(url_for('products.index')),
                                   error_state=0)
                else:
                    flash('Item not deleted, user not authorized', 'error')
                    return jsonify(redirect_url=str(url_for('products.index')),
                                   error_state=1,
                                   error_msg=('Item not deleted, \
                                              user not authorized'))
            return redirect(url_for('products.index'))
        else:
            flash_errors(item_form)
    if action_page is None:
        actionstate = 'readmode'
    else:
        actionstate = 'editmode'

    return render_template('item_details.html', actionstate=actionstate,
                           form=item_form, item_slug=item_slug)


@prods_blueprint.route('/items/<item_slug>.json')
@prods_blueprint.route('/items/<item_slug>', methods=['GET', 'POST'])
def item_details_view(item_slug):
    """View item details."""
    filter1 = models.Item.is_deleted == False
    filter2 = models.Item.item_slug == item_slug
    my_item = (models.Item.query
               .filter(filter1)
               .filter(filter2)
               .first_or_404())
    if 'json' in request.path:
        return jsonify(my_item.serialize)
    return render_template('item_read_page.html', my_item=my_item)


# Helper Functions
def flash_errors(form):
    """Process the flash message."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                u"Error in the %s field - %s" %
                (getattr(form, field).label.text, error),
                'error')


def fetch_category_list():
    """Build up the category list."""
    categories = models.Category
    filter_clause = categories.is_deleted == False
    return (categories.query
            .filter(filter_clause)
            .order_by(categories.category_name)
            .all())

def count_category_list():
    """Build up the category list."""
    categories = models.Category
    filter_clause = categories.is_deleted == False
    return (categories.query
            .filter(filter_clause)
            .count())

def fetch_base_items_list():
    """Build up the items list."""
    items = models.Item
    filter_clause = items.is_deleted == False
    return (items.query
            .filter(filter_clause))


def fetch_latest_items_list():
    """Build up the items list."""
    base_items = fetch_base_items_list()
    sort_order = models.Item.created_datetime.desc()
    return (base_items
            .order_by(sort_order)
            .limit(5)
            .all())


def fetch_category_items_list(category_slug):
    """Build up the items list per category."""
    not_deleted = models.Item.is_deleted == False
    extra_filter_clause = models.Category.category_slug == category_slug
    sort_order = models.Item.item_name.asc()
    listing = (db.session.query(models.Item)
                 .join(models.Item.category)
                 .filter(not_deleted)
                 .filter(extra_filter_clause)
                 .order_by(sort_order)
                 .all())
    return (listing)


def fetch_full_listing():
    """Build up the items listing."""
    not_deleted = models.Item.is_deleted == False
    sort_order = models.Item.item_name.asc()
    listing = (db.session.query(models.Item)
                 .filter(not_deleted)
                 .order_by(sort_order)
                 .all())
    return (listing)
