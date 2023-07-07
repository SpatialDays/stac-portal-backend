# DO NOT OPTIMISE IMPORTS IN THIS FILE

from gevent import monkey
from gevent.pywsgi import WSGIServer

monkey.patch_all()

from manage import app

http_server = WSGIServer(('0.0.0.0', 5001), app)
http_server.serve_forever()