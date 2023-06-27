import os

from flask_cli import FlaskGroup
from flask_cors import CORS
from flask_migrate import Migrate
from gevent.threadpool import ThreadPool
import multiprocessing
import logging
logging.basicConfig(level=logging.INFO)

from app import blueprint
from app.main import create_app, db

app = create_app()
_num_workers = multiprocessing.cpu_count() * 100
if _num_workers > 1000:
    _num_workers = 1000
logging.info(f"Set number of gevent greenlets to {_num_workers}")
_pool = ThreadPool(_num_workers)
app.register_blueprint(blueprint)
app.pool = _pool
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
