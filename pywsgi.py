from gevent import monkey
from gevent.pywsgi import WSGIServer

from manage import app
monkey.patch_all()


http_server = WSGIServer(('0.0.0.0', 5001), app)
http_server.serve_forever()