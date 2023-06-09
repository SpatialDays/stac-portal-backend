from flask.app import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name

db: SQLAlchemy = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app() -> Flask:
    global db
    app = Flask(__name__)
    app.config.from_object(config_by_name["prod"])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app
