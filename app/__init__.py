from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

from app import views,models


@lm.user_loader

def load_user(user_id):
    return models.User.query.filter(models.User.id == int(user_id)).first()
