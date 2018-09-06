# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_oauthlib.provider import OAuth2Provider

from servers.oauth2.config import configure
from servers.oauth2.routes import setup_routes

oauth2_server = Blueprint(__name__, 'oauth2_server', template_folder='templates')

configure(oauth2_server)

oauth = OAuth2Provider()
oauth.init_app(oauth2_server)

setup_routes(oauth2_server, oauth)
# setup_handlers(app, oauth)


#
# @app.route('/oauth/token', methods=['GET', 'POST'])
# @oauth.token_handler
# def access_token():
#     return None
#
#
# @app.route('/oauth/authorize', methods=['GET', 'POST'])
# @oauth.authorize_handler
# def authorize(*args, **kwargs):
#     user = current_user()
#     if not user:
#         return redirect('/')
#     if request.method == 'GET':
#         client_id = kwargs.get('client_id')
#         client = Client.query.filter_by(client_id=client_id).first()
#         kwargs['client'] = client
#         kwargs['user'] = user
#         return render_template('authorize.html', **kwargs)
#
#     confirm = request.form.get('confirm', 'no')
#     return confirm == 'yes'
#
#


