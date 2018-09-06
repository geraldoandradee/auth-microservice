# -*- coding: utf-8 -*-
import os
from flask_oauthlib.provider import OAuth2Provider


def configure(app):
    """

    :param app: Flask This is reference of a flask application.
    :return: None
    """
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': os.getenv('SQLALCHEMY_DATABASE_URI'),
        'DEBUG': bool(os.getenv('DEBUG', False)),
        'SECRET_KEY': os.getenv('SECRET_KEY'),
    })

