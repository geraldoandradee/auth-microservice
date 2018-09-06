# -*- coding: utf-8 -*-
from servers.oauth2.handlers import HomeHandler, ClientHandler, MeHandler, AuthorizeHandler, OAuth2Handler


def setup_routes(app, oauth):
    app.add_url_rule('/', view_func=HomeHandler.as_view('home'))
    app.add_url_rule('/client', view_func=ClientHandler.as_view('client'))
    app.add_url_rule('/api/me', view_func=MeHandler.as_view('me'))
    app.add_url_rule('/oauth/authorize', view_func=AuthorizeHandler.as_view('oauth.authorize'))
    handler = OAuth2Handler()
    oauth.clientgetter(handler.load_client)
    oauth.grantgetter(handler.load_grant)
    oauth.grantsetter(handler.save_grant)
    oauth.tokengetter(handler.load_token)
    oauth.tokensetter(handler.save_token)
