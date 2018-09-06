# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from flask import session, request, render_template
from flask.json import jsonify
from werkzeug.security import gen_salt
from werkzeug.utils import redirect

from servers.oauth2.lib import BaseViewHandler
from servers.oauth2.models import User, Client, Grant, Token
from servers.oauth2.respository import db_session


class HomeHandler(BaseViewHandler):
    """
    HomeHandler
    -----------

    """

    def get(self):
        user = self.current_user()
        return render_template('home.html', user=user)

    def post(self):
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db_session.add(user)
            db_session.commit()
        session['id'] = user.id
        return redirect('/')


class ClientHandler(BaseViewHandler):
    """
    ClientHandler
    -------------

    """

    def get(self):
        user = self.current_user()
        if not user:
            return redirect('/')
        item = Client(
            client_id=gen_salt(40),
            client_secret=gen_salt(50),
            _redirect_uris=' '.join([
                'http://localhost:8000/authorized',
                'http://127.0.0.1:8000/authorized',
                'http://127.0.1:8000/authorized',
                'http://127.1:8000/authorized',
            ]),
            _default_scopes='email',
            user_id=user.id,
        )
        db_session.add(item)
        db_session.commit()
        return jsonify(
            client_id=item.client_id,
            client_secret=item.client_secret,
        )


class MeHandler(BaseViewHandler):

    # @oauth.require_oauth()
    def get(self):
        user = request.oauth.user
        return jsonify(username=user.username)


class AuthorizeHandler(BaseViewHandler):
    # @app.route('/oauth/authorize', methods=['GET', 'POST'])
    # @oauth.authorize_handler
    def authorize(self, *args, **kwargs):
        user = self.current_user()
        if not user:
            return redirect('/')
        if request.method == 'GET':
            client_id = kwargs.get('client_id')
            client = Client.query.filter_by(client_id=client_id).first()
            kwargs['client'] = client
            kwargs['user'] = user
            return render_template('authorize.html', **kwargs)

        confirm = request.form.get('confirm', 'no')
        return confirm == 'yes'


class OAuth2Handler(BaseViewHandler):

    @staticmethod
    def load_client(client_id):
        return Client.query.filter_by(client_id=client_id).first()

    @staticmethod
    def load_grant(client_id, code):
        return Grant.query.filter_by(client_id=client_id, code=code).first()

    def save_grant(self, client_id, code, request, *args, **kwargs):
        # decide the expires time yourself
        expires = datetime.utcnow() + timedelta(seconds=100)
        grant = Grant(
            client_id=client_id,
            code=code['code'],
            redirect_uri=request.redirect_uri,
            _scopes=' '.join(request.scopes),
            user=self.current_user(),
            expires=expires
        )
        db_session.add(grant)
        db_session.commit()
        return grant

    @staticmethod
    def load_token(access_token=None, refresh_token=None):
        if access_token:
            return Token.query.filter_by(access_token=access_token).first()
        elif refresh_token:
            return Token.query.filter_by(refresh_token=refresh_token).first()

    @staticmethod
    def save_token(token, request, *args, **kwargs):
        toks = Token.query.filter_by(
            client_id=request.client.client_id,
            user_id=request.user.id
        )
        # make sure that every client has only one token connected to a user
        for t in toks:
            db_session.delete(t)

        expires_in = token.pop('expires_in')
        expires = datetime.utcnow() + timedelta(seconds=expires_in)

        tok = Token(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
            _scopes=token['scope'],
            expires=expires,
            client_id=request.client.client_id,
            user_id=request.user.id,
        )
        db_session.add(tok)
        db_session.commit()
        return tok
