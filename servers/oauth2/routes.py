# -*- coding: utf-8 -*-
from servers.oauth2.handlers import HomeHandler, ClientHandler


def setup_routes(app):
    app.add_url_rule('/', view_func=HomeHandler.as_view('home'))
    app.add_url_rule('/client', view_func=ClientHandler.as_view('client'))

