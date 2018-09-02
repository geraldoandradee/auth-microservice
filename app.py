import os

from website.app import create_app

app = create_app()


@app.cli.command()
def initdb():
    from website.models import db
    db.create_all()


@app.cli.command()
def init_db():
    from servers.oauth2.respository import Base, engine
    from servers.oauth2.models import *
    Base.metadata.create_all(bind=engine)