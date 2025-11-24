from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    app.config.setdefault('SECRET_KEY', 'dev-secret-change-this')
    app.config.setdefault('SESSION_PERMANENT', False)

    from .views import views

    app.register_blueprint(views, url_prefix='/') 

    from .models import Hotel, Booking, Guest

    with app.app_context():
        db.create_all()
    return app

def create_database(app):
    if not path.exists('EigenEntwicklung/website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')