from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = 'login'

facebook_blueprint = make_facebook_blueprint(client_id='433391737423638', client_secret = '19ecf5a071d73202cb10701c94dfe5de', redirect_url = 'https://cs4398-final-project.herokuapp.com/facebook_login')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models