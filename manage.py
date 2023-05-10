import os

from flask_cli import FlaskGroup
from flask_cors import CORS
from flask_migrate import Migrate

from app import blueprint
from app.main import create_app, db

app = create_app(os.getenv('FLASK_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()
CORS(app, resources={r"/*": {"origins": "*"}})
cli = FlaskGroup(app)

migrate = Migrate()
migrate.init_app(app, db)
FLASK_APP = "manage.py"


def run():
    db.create_all()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    cli()
