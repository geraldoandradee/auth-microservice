# -*- coding: utf-8 -*-
import os

import click
from flask import Flask
from flask.cli import AppGroup
from servers.oauth2.config import configure as configure_oauth2

import constants

app = Flask(__name__)

if os.getenv('SERVER_OPERATION_MODE') == constants.SERVER_OAUTH_OPERATION_MODE:
    from servers.oauth2.server import oauth2_server

    configure_oauth2(app=app)
    app.register_blueprint(oauth2_server)

else:
    raise Exception("SERVER_OPERATION_MODE env var is not setted correctly.")

user_cli = AppGroup('db')


@user_cli.command('init')
@click.argument('dbname')
def init_db(dbname):
    if dbname == constants.SERVER_OAUTH_OPERATION_MODE:
        from servers.oauth2.respository import Base, engine
        from servers.oauth2.models import User, Token, Grant, Client
        Base.metadata.create_all(bind=engine)
    else:
        raise Exception("Server Operation Mode not known.")
