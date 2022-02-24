import os.path

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

import acronym
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'king'
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'acronym.db')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    db.init_app(app)

    from . import view
    from . import auth

    app.register_blueprint(view.view)
    app.register_blueprint(auth.auth)

    from .model import Users, Create
    # create_database(app)

    # Define flask_login LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'view.index'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))

    return app


# def create_database(app):
#     if not os.path.exists(basedir + 'acronym.db'):
#         db.create_all(app=app)
#         print('Database created successfully')
