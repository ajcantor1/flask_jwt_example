from flask import Flask
import os
from dotenv import load_dotenv

from api.routes import api
from auth.routes import auth

from extensions import jwt, db

def createApp():
    load_dotenv()

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')

    db_username = os.getenv('POSTGRES_USERNAME')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_name = os.getenv('POSTGRES_DB')
    db_url = os.getenv('POSTGRES_URL')
    db_port = os.getenv('POSTGRES_PORT')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@{db_url}:{db_port}/{db_name}'

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(api, url_prefix='/api')

    return app