# Auth Microservice Documentation


This is a OAuth2 server implementation using Flask. Not production ready.

# How to setup a database?

Simple. Run follow command:

    $ flask db init oauth

# How to test it?

This project has only functional tests implemented.

    $ pip install -r requirements/dev.txt
    $ flask db init oauth
    $ docker-compose up --build
    $ py.test -v 
    
    
# How to run

    $ cp .env.example .env
    $ docker-compose up --build
