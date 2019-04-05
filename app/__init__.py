from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'login'

facebook_blueprint = make_facebook_blueprint(client_id='433391737423638', client_secret = '19ecf5a071d73202cb10701c94dfe5de', redirect_url = 'https://cs4398-final-project.herokuapp.com/facebook_login')
google_blueprint = make_google_blueprint(client_id='535013055834-9jk2rccnrb4cr2a4equ3st7ov7fkbqur.apps.googleusercontent.com', client_secret='cKhV7gREwZ7S_MnoPjZeiuD2', redirect_url='https://cs4398-final-project.herokuapp.com/google_login/')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models