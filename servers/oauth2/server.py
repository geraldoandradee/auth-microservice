# -*- coding: utf-8 -*-
import os
from flask import Blueprint
from flask_oauthlib.provider import OAuth2Provider

from servers.oauth2.routes import setup_routes

oauth2_server = Blueprint(__name__, 'oauth2_server',
                          template_folder=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates'))

oauth = OAuth2Provider()
oauth.init_app(oauth2_server)

setup_routes(oauth2_server, oauth)
