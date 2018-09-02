# -*- coding: utf-8 -*-
from flask import session, request, render_template
from flask.json import jsonify
from werkzeug.security import gen_salt
from werkzeug.utils import redirect

from servers.oauth2.lib import BaseViewHandler
from servers.oauth2.models import User, Client
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
