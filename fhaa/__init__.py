"""
fhaa app
Authors: jlee (junlee9834@gmail.com)
"""

from flask import Flask, render_template # pip install flask 
from flask_migrate import Migrate # pip install flask-migrate
from flask_sqlalchemy import SQLAlchemy # pip install flask-migrate
from sqlalchemy import MetaData

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    
    app.app_context().push()
    
    # initialize connection
    # with app.app_context():
    #     init_database()

    # # initialize connection
    # @app.before_first_request
    # def beforeFirstRequest():
    #     init_database()

    # close connection
    # @app.teardown_appcontext
    # def teardown(exception):
    #     db_session.remove()
        
    # ORM (DB)
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("mysql+pymysql"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models
    
    
    # Blueprint
    from .views import main_views, auth_views, log_views, change_views, request_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(log_views.bp)
    app.register_blueprint(change_views.bp)
    app.register_blueprint(request_views.bp)
    
    # filter
    from .filter import add_datetime
    app.jinja_env.filters['add_datetime'] = add_datetime
    
    
    
    return app