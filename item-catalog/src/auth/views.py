"""User Auth Routes."""

from flask import redirect, url_for, session, request, jsonify, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
import requests
from src import db, app, oauth
from . import models

# pylint: disable=invalid-name
# Create a blueprint to contain all the products views and items
auth_blueprint = Blueprint('auth', __name__, template_folder='templates')


@auth_blueprint.route('/nav/list_urls', methods=['GET', 'POST'])
def list_urls():
    """Create a list of urls in the app eg for a site map.
       Pending: Create a set comprehension for prepending the base
       domain to each of the urls.
    """
    routes = []
    for rule in app.url_map.iter_rules():
        url = rule.rule
        routes.append(url)
    return 'urls in this app are:' + str(set(routes))


google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@auth_blueprint.route('/userinfo')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/login')
def login():
    return google.authorize(callback=url_for('auth.authorized', _external=True))


@auth_blueprint.route('/logout')
@login_required
def logout():
    revoke_google_token()
    user = current_user
    user.is_authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    session.pop('google_token', None)
    return redirect(url_for('products.index'))


@auth_blueprint.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    # local_user_id = get_local_user_id('google', me.data['email'])
    local_user = get_local_user('google', me.data['email'])
    if local_user is not None:
        local_user.is_authenticated = True
        db.session.add(local_user)
        db.session.commit()
        login_user(local_user)
    return redirect(url_for('products.index'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


def revoke_google_token():
    if session.get('google_pgtoken'):
        token = session.get('google_token')
        requests.post('https://accounts.google.com/o/oauth2/revoke',
                      params={'token': token},
                      headers={'content-type':
                               'application/x-www-form-urlencoded'})


def get_local_user_id(network, site_id):
    """Get the local user_id from the social details."""
    network_check = models.User.oauth_site == network
    id_check = models.User.social_id == site_id
    existing_id = (models.User.query
                   .filter(network_check)
                   .filter(id_check)
                   .first())
    if existing_id:
        return existing_id.id
    new_id = models.User(
        oauth_site='google',
        social_id=site_id)
    db.session.add(new_id)
    db.session.commit()
    return new_id.id


def get_local_user(network, site_id):
    """Get the local user_instance from the social details."""
    network_check = models.User.oauth_site == network
    id_check = models.User.social_id == site_id
    existing_user = (models.User.query
                     .filter(network_check)
                     .filter(id_check)
                     .first())
    if existing_user:
        return existing_user
    me = google.get('userinfo')
    username = str(me.data['given_name']) + ' ' + str(me.data['family_name'])
    new_user = models.User(
        oauth_site='google',
        social_id=site_id,
        user_name=username)
    db.session.add(new_user)
    db.session.commit()
    return new_user
