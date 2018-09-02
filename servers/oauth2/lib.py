# -*- coding: utf-8 -*-
from flask import session
from flask.views import MethodView

from servers.oauth2.models import User


class BaseViewHandler(MethodView):

    def current_user(self):
        if 'id' in session:
            uid = session['id']
            return User.query.get(uid)
        return None
